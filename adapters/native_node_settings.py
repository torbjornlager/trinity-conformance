#!/usr/bin/env python3
"""Public settings on disposable native profile/sandbox fixtures."""
import argparse,json,os,re,subprocess,sys,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runner'))
import baseline
from local_runtime_contracts import free_port
quote=baseline.actor.prolog_quote_atom

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--swi-root',type=Path,required=True)
    parser.add_argument('--trealla-root',type=Path,required=True)
    parser.add_argument('--swipl',default='swipl');parser.add_argument('--tpl',required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=False);rows=[]
    for name,root in [('swi',args.swi_root),('trealla',args.trealla_root)]:
      for profile in ['relation','isobase','isotope','actor']:
       for mode in ['blacklist','whitelist','off']:
        port=free_port();url=f'http://127.0.0.1:{port}';label=f'{name}-{profile}-{mode}'
        options=f'profile({profile}),sandbox({mode}),auth(open),rate_window_seconds(71),max_inflight_calls(13),max_term_text_bytes(70001),max_call_requests_per_window(1000)'
        if name=='swi':
            goal=f"use_module({quote(str(root/'prolog/web_prolog.pl'))}),use_module(library(socket)),tcp_socket(S),tcp_bind(S,ip(127,0,0,1):{port}),tcp_listen(S,128),node:node({port},[tcp_socket(S),{options}]),thread_get_message(stop)"
            cmd=[args.swipl,'-q','-g',goal]
        else:
            goal=f"use_module(distribution),web_prolog:web_prolog_node({port},[bind_address('127.0.0.1'),{options}])"
            cmd=[args.tpl,'-g',goal]
        env=dict(os.environ,TPL_LIBRARY_PATH=str(Path(args.tpl).resolve().parent/'library'))
        with (args.output/(label+'.log')).open('w') as log:
          proc=subprocess.Popen(cmd,cwd=root,env=env,stdout=log,stderr=log)
          try:
            deadline=time.monotonic()+12
            while True:
                try:
                    with urlopen(url+'/node_info',timeout=.3) as response:info=json.load(response)
                    break
                except OSError:
                    if proc.poll() is not None or time.monotonic()>deadline:raise RuntimeError(label+' startup failed')
                    time.sleep(.05)
            def check(case_id,goal,expected,host=False):
                row=dict(candidate=name,profile=profile,mode=mode,id=case_id)
                params=dict(goal=goal,template='V',format='prolog',limit=100)
                request=Request(url+'/call?'+urlencode(params),headers={'Host':'settings-spoof.invalid:65000'} if host else {})
                try:
                    with urlopen(request,timeout=8) as response:body=response.read().decode()
                    baseline.actor.require(baseline.variant_tokens(body)==baseline.variant_tokens(expected),repr(body))
                    row.update(status='pass',body=body)
                except Exception as error:row.update(status='fail',detail=str(error))
                rows.append(row);print(label,case_id,row['status'],flush=True)
            expected=dict(url=info['self_url'],profile=profile,sandbox=mode,auth='open',rate_window_seconds=71,max_inflight_calls=13,max_term_text_bytes=70001,max_call_requests_per_window=1000)
            for key,value in expected.items():
                term=str(value) if isinstance(value,int) else value if re.fullmatch('[a-z][A-Za-z_0-9]*',value) else quote(value)
                check('value-'+key,f'node_setting({key},V)','success(['+term+'],false).')
            check('host-identity','node_setting(url,V)','success(['+quote(info['self_url'])+'],false).',True)
            for key in ['bearer_token','peer_transport_tokens','shared_db_source','principal_policies','42','[]','setting(a)']:
                check('unavailable-'+key,f'node_setting({key},V)','failure.')
            check('wrong-value','node_setting(profile,ns_impossible_profile)','failure.')
            if profile=='relation':
                for key in ['max_load_text_bytes','max_session_spawns_per_window','max_ws_frame_bytes']:check('family-'+key,f'node_setting({key},V)','failure.')
            elif profile=='isobase':
                for key in ['max_session_spawns_per_window','max_ws_frame_bytes']:check('family-'+key,f'node_setting({key},V)','failure.')
            elif profile=='isotope':check('family-max_ws_frame_bytes','node_setting(max_ws_frame_bytes,V)','failure.')
          finally:
            proc.terminate()
            try:proc.wait(timeout=5)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
        (args.output/'results.json').write_text(json.dumps(dict(suite='native-node-settings-0.1',results=rows),indent=2)+'\n')
    return int(any(row['status']=='fail' for row in rows))
if __name__=='__main__':raise SystemExit(main())
