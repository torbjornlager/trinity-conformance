#!/usr/bin/env python3
"""Shared native discovery metadata and owner-controlled lifecycle checks."""
import argparse,json,os,subprocess,sys,time
from pathlib import Path
from urllib.request import urlopen
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runner'))
import baseline
from local_runtime_contracts import free_port
quote=baseline.actor.prolog_quote_atom

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--swi-root',type=Path,required=True);parser.add_argument('--trealla-root',type=Path,required=True)
    parser.add_argument('--tpl',required=True);parser.add_argument('--swipl',default='swipl')
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    rows=[];fixture=ROOT/'fixtures/discovery';expected=['last/2','review_empty/1','review_fact/1','review_grammar/3','review_rule/1']
    for name,root in [('swi',args.swi_root),('trealla',args.trealla_root)]:
      for mode in ['blacklist','whitelist','off']:
        label=name+'-'+mode;port=free_port();url=f'http://127.0.0.1:{port}';ack=args.output/(label+'.ack');token=0
        prepare=f"use_module({quote(str(fixture/'control.pl'))}),discovery_control:start({name},{port},{quote(str(ack.resolve()))},{quote(str(fixture/'updated.pl'))}),"
        opts=f'profile(actor),sandbox({mode}),auth(open),load_shared_db_file({quote(str(fixture/"shared.pl"))})'
        if name=='swi':
            # Start trusted actors after listener identity exists, within that node.
            launch=f"discovery_control:start(swi,{port},{quote(str(ack.resolve()))},{quote(str(fixture/'updated.pl'))})"
            goal=f"use_module({quote(str(root/'prolog/web_prolog.pl'))}),use_module({quote(str(fixture/'control.pl'))}),use_module(library(socket)),tcp_socket(S),tcp_bind(S,ip(127,0,0,1):{port}),tcp_listen(S,128),node:node({port},[tcp_socket(S),{opts}]),node_runtime_state:with_node_port_context({port},{launch}),thread_get_message(stop)"
            cmd=[args.swipl,'-q','-g',goal]
        else:
            goal='use_module(distribution),'+prepare+f"web_prolog:web_prolog_node({port},[bind_address('127.0.0.1'),{opts}])"
            cmd=[args.tpl,'-g',goal]
        env=dict(os.environ,TPL_LIBRARY_PATH=str(Path(args.tpl).resolve().parent/'library'))
        with (args.output/(label+'.log')).open('w') as log:
          proc=subprocess.Popen(cmd,cwd=root,env=env,stdin=subprocess.PIPE,text=True,stdout=log,stderr=log)
          try:
            def info():
                with urlopen(url+'/node_info',timeout=3) as response:return json.load(response)
            def wait_ack(want):
                deadline=time.monotonic()+8
                while time.monotonic()<deadline:
                    try:
                        parts=ack.read_text().split()
                        if len(parts)>=2 and int(parts[0])==want:
                            if parts[1]=='error':raise RuntimeError('owner control: '+' '.join(parts[2:]))
                            if len(parts)==2:return int(parts[1])
                    except (OSError,ValueError):pass
                    if proc.poll() is not None:raise RuntimeError(label+' exited; see node log')
                    time.sleep(.02)
                raise TimeoutError(label+' owner-control acknowledgement missing')
            def control(action):
                nonlocal token
                token+=1;proc.stdin.write(f'command({token},{action}).\n');proc.stdin.flush();return wait_ack(token)
            deadline=time.monotonic()+12
            while True:
                try:info();break
                except OSError:
                    if proc.poll() is not None or time.monotonic()>deadline:raise RuntimeError(label+' startup failed')
                    time.sleep(.04)
            wait_ack(0)
            def check(case_id,operation):
                row=dict(candidate=name,mode=mode,id=case_id)
                try:row.update(status='pass',observation=operation())
                except Exception as error:row.update(status='fail',detail=str(error))
                rows.append(row);print(label,case_id,row['status'],flush=True)
            def snapshot(provides,services):
                data=info()
                baseline.actor.require(data['provides']==provides,repr(data['provides']))
                baseline.actor.require(data['services']==services,repr(data['services']))
                return dict(provides=data['provides'],services=data['services'])
            check('ND-001',lambda:snapshot(expected,['discovery_public']))
            def stable_initialization():
                before=control('inspect');observations=[snapshot(expected,['discovery_public']) for _ in range(3)];after=control('inspect')
                baseline.actor.require(before==after,repr((before,after)));return dict(initializations=before,observations=observations)
            check('ND-002',stable_initialization)
            def private_shadow():
                control('prepare_private')
                candidate=baseline.actor.Candidate(url.replace('http:','ws:')+'/ws','actor',8,None,None,False,())
                with baseline.actor.Harness(candidate) as h:
                    h.spawn_shell('[session(true),src_text('+quote('review_fact(private). private_only(secret).')+')]')
                    observed=snapshot(expected,['discovery_public']);h.halt();return observed
            check('ND-003',private_shadow)
            def changed(action,provides,services):control(action);return snapshot(provides,services)
            check('ND-004',lambda:changed('unregister',expected,[]))
            check('ND-005',lambda:changed('publish',expected,['discovery_public']))
            check('ND-006',lambda:changed('stop',expected,[]))
            check('ND-007',lambda:changed('reconfigure',['review_changed/1'],[]))
            check('ND-008',lambda:changed('clear',[],[]))
          finally:
            proc.terminate()
            try:proc.wait(timeout=5)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
            if proc.stdin:proc.stdin.close()
        (args.output/'results.json').write_text(json.dumps(dict(suite='native-discovery-0.1',results=rows),indent=2)+'\n')
    return int(any(row['status']=='fail' for row in rows))
if __name__=='__main__':raise SystemExit(main())
