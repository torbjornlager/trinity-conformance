#!/usr/bin/env python3
"""Run identical URI identity and copied-I/O cases in both native directions."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runner'))
from run import Candidate, Harness, require, row_value, prolog_quote_atom

def fingerprint(root):
    revision=subprocess.run(['git','rev-parse','HEAD'],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    diff=subprocess.run(['git','diff','HEAD','--'],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    scope=root/'prolog' if (root/'prolog').is_dir() else root
    files=scope.rglob('*.pl') if scope!=root else scope.glob('*.pl')
    return dict(revision=revision.stdout.strip() if revision.returncode==0 else None,
                diff_sha256=hashlib.sha256(diff.stdout).hexdigest() if diff.returncode==0 else None,
                files_sha256={str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(files)})

def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]

def query(url, source, goal, case, timeout):
    with Harness(Candidate(url, 'actor', timeout, None, None, False, ())) as h:
        h.spawn_shell('[session(true),src_text(' + prolog_quote_atom(source) + ')]')
        h.call('(' + goal + '),ContractResult=passed', '[limit(1)]')
        outputs=[];raw_outputs=[]
        for _ in range(96):
            event=h.recv()
            if event.get('type')=='success':
                require(row_value(event,'ContractResult')=='passed',repr(event))
                require(event.get('more') is False, 'case left a continuation')
                break
            require(event.get('type') not in ('failure','error'),repr(event))
            body=event.get('event',event)
            if body.get('type')=='output':
                raw_outputs.append(body.get('data'))
                outputs.append(str(body.get('data','')).rstrip('\n'))
            h.acknowledge_output(event)
        else:raise AssertionError('no final success')
        if 'outputs' in case:require(outputs==case['outputs'],repr(outputs))
        if 'output_count' in case:require(len(outputs)==case['output_count'],repr(outputs))
        for text,count in case.get('output_counts',{}).items():
            require(outputs.count(text)==count,repr(outputs))
        h.call('AfterContract=ready','[limit(1)]')
        fresh=h.recv_type('success',limit=32)
        require(row_value(fresh,'AfterContract')=='ready',repr(fresh))
        h.halt()
        return dict(outputs=outputs,raw_output_data=raw_outputs,fresh_query=True)

def alias_client_contexts(url, source, peer, timeout, token=None):
    """Two fresh client roots address one canonical peer, with separate scopes."""
    candidate=Candidate(url,'actor',timeout,token,None,False,())
    def step(h,goal):
        h.call('('+goal+'),ContractResult=passed','[limit(1)]')
        result=h.recv_type('success',limit=64)
        require(row_value(result,'ContractResult')=='passed' and result.get('more') is False,repr(result))
        return result
    with Harness(candidate) as first, Harness(candidate) as second:
        roots=[]
        for marker,(h,node) in enumerate([(first,peer),(second,peer+'/')],1):
            h.spawn_shell('[session(true),src_text('+prolog_quote_atom(source)+')]')
            child=('self(Child),register(uri_client_alias,Child),whereis(uri_client_alias,Child),'
                   'send(Owner,alias_ready),'
                   f'receive({{probe(From)->send(From,alias_alive({marker}))}}),'
                   f'receive({{probe(Again)->send(Again,alias_alive({marker}))}}),receive({{stop->true}})' )
            result=step(h,'actors(Before),self(Owner),spawn(('+child+'),P,[node('
                        +prolog_quote_atom(node)+'),monitor(true)]),'
                        'receive({alias_ready->true},[timeout(4),on_timeout(throw(alias_client_not_ready))])')
            roots.append((h,str(row_value(result,'P')),str(row_value(result,'Before')),marker))
        require(roots[0][1]!=roots[1][1],'two clients returned the same actor')
        def probe(h,pid,marker):
            step(h,'self(Owner),send('+pid+',probe(Owner)),receive({alias_alive('+str(marker)+') -> true},'
                   '[timeout(4),on_timeout(throw(alias_client_misrouted))])')
        for h,pid,_,marker in roots:probe(h,pid,marker)
        step(first,'catch((exit('+roots[1][1]+',forbidden),Verdict=allowed),'
                   'error(permission_error(exit,actor,_),_),Verdict=denied),Verdict==denied')
        for h,pid,before,marker in roots:
            probe(h,pid,marker)
            step(h,'send('+pid+',stop),nu_done('+pid+'),nu_baseline('+before+')')
            h.halt()
        return dict(distinct_client_actors=True,ordinary_names_isolated=True,
                    foreign_exit_denied=True,both_targets_survived=True,baselines_restored=True)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--swi-root',type=Path,default=ROOT.parent/'swi-prolog-node')
    p.add_argument('--trealla-root',type=Path,default=ROOT.parent/'trealla-port')
    p.add_argument('--swipl',default='/usr/local/bin/swipl')
    p.add_argument('--tpl',required=True)
    p.add_argument('--literal-peer-credentials',action='store_true',help='compatibility fixture: authorize both literal root-URL spellings')
    p.add_argument('--manifest',type=Path,default=ROOT/'cases/node-uri-io-0.2.json')
    p.add_argument('--case',action='append',default=[])
    p.add_argument('--timeout',type=float,default=8)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    manifest=a.manifest.resolve();pack=json.loads(manifest.read_text())
    source=(ROOT/pack['source_file']).read_text()
    known={c['id'] for c in pack['cases']};require(set(a.case)<=known,'unknown case')
    ports={n:free_port() for n in ('swi','trealla')}
    urls={n:f'http://127.0.0.1:{v}' for n,v in ports.items()}
    urls['swi']=f'http://localhost:{ports["swi"]}'
    credential_urls=[url for base in urls.values() for url in ((base,base+'/') if a.literal_peer_credentials else (base,))]
    credentials=tempfile.TemporaryDirectory(prefix='node-uri-peer-')
    credential_file=Path(credentials.name)/'peers.pl'
    token='node-uri-fixture-credential-00000000'
    pairs='['+','.join(prolog_quote_atom(url)+'-'+prolog_quote_atom(token) for url in credential_urls)+']'
    credential_file.write_text(pairs+'.\n');credential_file.chmod(0o600)
    nodes=[];logs=[];rows=[];sources={}
    try:
        for name in ('swi','trealla'):
            root=a.swi_root if name=='swi' else a.trealla_root
            peer='trealla' if name=='swi' else 'swi'
            # Configure canonical logical nodes once. The compatibility option
            # retains the earlier exact-spelling fixture for historical controls.
            options=f'profile(actor),auth(open),max_session_spawns_per_window(1000),bearer_token(peer,{prolog_quote_atom(token)},[execute,internal_transport])'
            if name=='swi':
                options+=f',peer_transport_tokens({pairs})'
                goal=f'use_module({prolog_quote_atom(str(root/"prolog/web_prolog.pl"))}),node({ports[name]},[{options}]),thread_get_message(stop)'
                cmd=[a.swipl,'-f','none','-q','-g',goal]
            else:
                goal=f'use_module(distribution),use_module(peer_topology),peer_topology:configure_credentials({prolog_quote_atom(str(credential_file))}),web_prolog:web_prolog_node({ports[name]},[{options}])'
                cmd=[a.tpl,'-g',goal]
            env=os.environ.copy()
            for key in ('WP_CONFIG_FILE','WP_NATIVE_STATE','WP_NATIVE_MODE','SWI_HOME_DIR','SWIPL_HOME_DIR'):
                env.pop(key,None)
            if name=='trealla':env['TPL_LIBRARY_PATH']=str(Path(a.tpl).parent/'library')
            log=(a.output/(name+'.log')).open('w');logs.append(log)
            proc=subprocess.Popen(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT);nodes.append(proc)
            for _ in range(180):
                require(proc.poll() is None,name+' startup failed; see log')
                try:
                    with socket.create_connection(('127.0.0.1',ports[name]),timeout=.1):break
                except OSError:time.sleep(.03)
            else:raise TimeoutError(name+' startup')
            require('syntax error' not in (a.output/(name+'.log')).read_text().lower(),
                    name+' runtime parse error during startup; see node log')
            query(urls[name].replace('http:','ws:')+'/ws',source,'true',{},a.timeout)
            sources[name]=fingerprint(root)
        for name in ('swi','trealla'):
            peer='trealla' if name=='swi' else 'swi'
            for case in pack['cases']:
                if a.case and case['id'] not in a.case:continue
                row=dict(candidate=name,peer=peer,id=case['id'],title=case['title'])
                goal=case.get('goal','').replace('$SELF_SLASH',prolog_quote_atom(urls[name]+'/')).replace('$PEER_SLASH',prolog_quote_atom(urls[peer]+'/')).replace('$SELF',prolog_quote_atom(urls[name])).replace('$PEER',prolog_quote_atom(urls[peer]))
                try:
                    observation=(alias_client_contexts(urls[name].replace('http:','ws:')+'/ws',source,urls[peer],a.timeout,
                                                      token if case.get('authenticated') else None)
                                 if case.get('execution')=='alias_client_contexts'
                                 else query(urls[name].replace('http:','ws:')+'/ws',source,goal,case,a.timeout))
                    row.update(status='pass',observation=observation)
                except Exception as e:row.update(status='fail',detail=str(e))
                rows.append(row);print(name,case['id'],row['status'],flush=True)
    finally:
        for node in reversed(nodes):
            node.terminate()
            try:node.wait(timeout=3)
            except subprocess.TimeoutExpired:node.kill();node.wait(timeout=2)
        for log in logs:log.close()
        credentials.cleanup()
    report=dict(suite=pack['suite'],fixture_authorized_node_urls=credential_urls,adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),source_sha256=hashlib.sha256(source.encode()).hexdigest(),sources=sources,results=rows,counts={s:sum(r['status']==s for r in rows) for s in ('pass','fail')})
    (a.output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    return int(report['counts']['fail']>0)
if __name__=='__main__':raise SystemExit(main())
