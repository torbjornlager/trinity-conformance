#!/usr/bin/env python3
"""Run the separate promise pack on disposable pinned-SWI/Trealla fixtures."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args],text=True).strip()
def quote(p):return "'"+str(p).replace('\\','\\\\').replace("'","''")+"'"
def free_port():
    with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]
def tree(p):
    return {str(f.relative_to(p)):sha(f) for f in sorted(p.rglob('*')) if f.is_file() and f.suffix not in ['.pyc','.log'] and '__pycache__' not in f.parts and '.git' not in f.parts}
def preservation(native,trealla,swipl,tpl):
    processes=subprocess.check_output(['ps','-axo','pid,lstart,command'],text=True)
    live=[s for s in processes.splitlines() if 'start_local_node.pl -- n3' in s or 'n5_frontend.py' in s or ('trealla-current/tpl -g' in s and '306' in s)]
    return dict(native_prolog=tree(native/'prolog'),trealla_sources={p.name:sha(p) for p in trealla.glob('*.pl')},
                engines={str(p):sha(p) for p in [swipl,tpl]},library=tree(tpl.parent/'library'),live=live)

def validate_swi_source(native,demonstrator,candidate=False,candidate_revision=None):
    pin_path=demonstrator/'dependencies/swi-prolog-node.json'
    pin=json.loads(pin_path.read_text())
    if candidate_revision and not candidate:
        raise ValueError('candidate revision requires explicit candidate mode')
    if candidate:
        actual=git(native,'rev-parse','HEAD')
        expected=candidate_revision or pin['revision']
        if candidate_revision and not re.fullmatch(r'[0-9a-f]{40}',candidate_revision):
            raise ValueError('candidate revision must be a full immutable commit id')
        if actual!=expected:
            raise ValueError('SWI candidate must start at the unchanged pinned revision or explicitly selected revision')
        if actual!=pin['revision']:
            try:git(native,'merge-base','--is-ancestor',pin['revision'],actual)
            except subprocess.CalledProcessError as error:
                raise ValueError('explicit SWI candidate must descend from the unchanged pin') from error
        for name in ['load.pl','pack.pl','prolog/web_prolog/node.pl']:
            if not (native/name).is_file():raise ValueError('missing native candidate file: '+name)
    else:
        subprocess.run([sys.executable,str(demonstrator/'tools/pinned_swi.py'),'--native-root',str(native),'--check'],check=True)
    return dict(mode='explicit working-tree candidate' if candidate else 'strict pinned dependency',
                pin_path=str(pin_path),pin_sha256=sha(pin_path),pin_revision=pin['revision'],
                candidate_base_revision=actual if candidate else pin['revision'])

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['swipl','tpl','swi-root','trealla-root','demonstrator-root','output']:parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--swi-source-candidate',action='store_true',help='explicitly test a source patch over the unchanged pinned SWI revision; never changes the pin')
    parser.add_argument('--swi-candidate-revision',help='full explicitly selected candidate base commit; must descend from unchanged pin')
    parser.add_argument('--diagnostics-only',action='store_true')
    parser.add_argument('--local-manifest',type=Path,help='run one local ACTOR pack per candidate, without a peer')
    a=parser.parse_args()
    if a.local_manifest and a.diagnostics_only:parser.error('choose local manifest or promise diagnostics')
    if a.local_manifest:a.local_manifest=a.local_manifest.resolve(strict=True)
    for key in ['swipl','tpl','swi_root','trealla_root','demonstrator_root']:setattr(a,key,getattr(a,key).resolve(strict=True))
    swi_input=validate_swi_source(a.swi_root,a.demonstrator_root,a.swi_source_candidate,a.swi_candidate_revision)
    a.output=a.output.resolve();a.output.mkdir(parents=True,exist_ok=False)
    before=preservation(a.swi_root,a.trealla_root,a.swipl,a.tpl)
    before['dependency_pin']=swi_input['pin_sha256']
    env=dict(os.environ,TPL_LIBRARY_PATH=str(a.tpl.parent/'library'))
    for key in ['SWI_HOME_DIR','SWIPL_HOME_DIR','WP_CONFIG_FILE','WP_ASSET_ROOT','WP_WASM_SOURCE_DIR','WP_NATIVE_STATE','WP_NATIVE_MODE']:env.pop(key,None)
    runs=[];procs=[];logs=[];nodes={}
    provenance=dict(runs=runs,sources={name:dict(path=str(p),revision=git(p,'rev-parse','HEAD'),status=git(p,'status','--short')) for name,p in [('conformance',ROOT),('swi',a.swi_root),('trealla',a.trealla_root),('demonstrator',a.demonstrator_root)]},
        inputs={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'cases/promise-yield-0.1.json',ROOT/'cases/promise-diagnostics-0.1.json',ROOT/'profiles/promise-yield-0.1.md',ROOT/'cases/interop-http-0.1.json',ROOT/'runner/baseline.py',ROOT/'runner/run.py',Path(__file__),*([a.local_manifest] if a.local_manifest else [])]},
        versions={},nodes=nodes,swi_source_input=swi_input)
    if a.local_manifest and any(c.get('transport')=='admission' for c in json.loads(a.local_manifest.read_text())['cases']):
        provenance['inputs']['runner/admission_probe.py']=sha(ROOT/'runner/admission_probe.py')
    for name,cmd in [('swi',[str(a.swipl),'--version']),('trealla',[str(a.tpl),'-g','current_prolog_flag(version_data,V),writeq(V),nl,halt'])]:
        r=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=10);provenance['versions'][name]=(r.stdout+r.stderr).strip()
    try:
        for name in ['swi','trealla']:
            port=free_port();url=f'http://127.0.0.1:{port}'
            if name=='swi':
                goal=f"use_module(library(sgml)),use_module(library(option)),consult({quote(a.swi_root/'load.pl')}),set_setting(http:public_host,'127.0.0.1'),set_setting(http:public_port,{port}),set_setting(http:public_scheme,http),use_module(library(socket)),tcp_socket(S),tcp_bind(S,ip(127,0,0,1):{port}),tcp_listen(S,128),node:node({port},[tcp_socket(S),profile(actor),sandbox(blacklist),auth(open)]),thread_get_message(stop)"
                cmd=[str(a.swipl),'-f','none','-q','-g',goal];cwd=a.swi_root
            else:
                goal=f"use_module(web_prolog),use_module(distribution),web_prolog:web_prolog_node({port},[bind_address('127.0.0.1'),node_url({quote(url)}),profile(actor),sandbox(blacklist),auth(open)]),thread_get_message(stop)"
                cmd=[str(a.tpl),'-g',goal];cwd=a.trealla_root
            log=(a.output/(name+'-node.log')).open('w');logs.append(log)
            proc=subprocess.Popen(cmd,cwd=cwd,env=env,stdout=log,stderr=log,start_new_session=True);procs.append(proc)
            nodes[name]=dict(url=url,pid=proc.pid,command=cmd,profile='actor',sandbox='blacklist',auth='open, disposable loopback fixture')
            for _ in range(150):
                if proc.poll() is not None:raise RuntimeError(name+' exited during startup')
                try:
                    with socket.create_connection(('127.0.0.1',port),timeout=.1):break
                except OSError:time.sleep(.05)
            else:raise TimeoutError(name+' startup')
        for caller in nodes:
            for peer in ([None] if a.local_manifest else nodes):
                for suite in ([json.loads(a.local_manifest.read_text())['suite'].removesuffix('-0.1')] if a.local_manifest else (['promise-diagnostics'] if a.diagnostics_only else ['promise-yield','interop-http'])):
                    label=f'{caller}-{suite}'+(f'-to-{peer}' if peer else '');report=a.output/(label+'.json')
                    endpoint=nodes[caller]['url']
                    if suite!='interop-http':endpoint=endpoint.replace('http:','ws:')+'/ws'
                    cmd=[sys.executable,'runner/baseline.py','--manifest',str(a.local_manifest) if a.local_manifest else f'cases/{suite}-0.1.json','--url',endpoint,'--candidate',caller,'--profile','actor','--timeout','8','--report',str(report)]
                    if peer:cmd+=['--peer',nodes[peer]['url']]
                    with (a.output/(label+'.log')).open('w') as log:
                        p=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=log,stderr=log,start_new_session=True)
                        try:code=p.wait(timeout=90)
                        except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait();code=124
                    runs.append(dict(label=label,exit_code=code,report=report.name if report.exists() else None,command=cmd))
                    print(label,code,flush=True)
    finally:
        for p in reversed(procs):
            if p.poll() is None:
                os.killpg(p.pid,signal.SIGTERM)
                try:p.wait(timeout=5)
                except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
        for log in logs:log.close()
        after=preservation(a.swi_root,a.trealla_root,a.swipl,a.tpl)
        after['dependency_pin']=sha(a.demonstrator_root/'dependencies/swi-prolog-node.json')
        checks={k:before[k]==after[k] for k in before}
        (a.output/'preservation.json').write_text(json.dumps(dict(checks=checks,before=before,after=after),indent=2)+'\n')
        provenance['temporary_nodes_stopped']=all(p.poll() is not None for p in procs)
        provenance['engine_hashes']=before['engines'];provenance['preservation']=checks
        (a.output/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    return int(len(runs)!=(2 if a.local_manifest else (4 if a.diagnostics_only else 8)) or any(r['exit_code']!=0 for r in runs) or not all(checks.values()))
if __name__=='__main__':raise SystemExit(main())
