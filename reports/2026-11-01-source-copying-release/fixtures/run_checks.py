#!/usr/bin/env python3
"""Disposable loopback nodes for the shared browser-client workflow checks."""
import argparse, hashlib, json, os, pathlib, signal, socket, subprocess, time, shutil
p=argparse.ArgumentParser(); p.add_argument('--sources',type=pathlib.Path,required=True); p.add_argument('--output',type=pathlib.Path,required=True); p.add_argument('--engine',choices=['swi','trealla','both'],default='both'); p.add_argument('--serve',action='store_true'); p.add_argument('--port',type=int,default=3060)
a=p.parse_args(); a.sources=a.sources.resolve(); a.output=a.output.resolve(); a.output.mkdir(parents=True,exist_ok=True)
base=pathlib.Path(__file__).resolve().parent
atom=lambda s: "'"+str(s).replace("'","''")+"'"
def sha(f): return hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
record={'date':time.strftime('%Y-%m-%d'),'method':'Shared browser JavaScript executed under Node; no GUI or usability evaluation','files':{f.name:sha(f) for f in base.iterdir() if f.is_file()},'engines':{}}
failed=False
for engine in (['swi','trealla'] if a.engine=='both' else [a.engine]):
 if a.serve:
  if a.engine=='both': raise ValueError('--serve requires one engine')
  port=a.port
 else:
  with socket.socket() as s: s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
 options="profile(actor),sandbox(blacklist),auth(open),ws_allowed_origins(['http://127.0.0.1:8000'])"
 if engine=='swi':
  exe=os.environ.get('SWIPL') or shutil.which('swipl') or '/usr/bin/swipl'
  text=f":- consult({atom(a.sources/'swi/load.pl')}).\nmain :- set_setting(http:public_host,'127.0.0.1'),set_setting(http:public_port,{port}),set_setting(http:public_scheme,http),use_module(library(socket)),tcp_socket(S),tcp_bind(S,ip(127,0,0,1):{port}),tcp_listen(S,128),node:node({port},[tcp_socket(S),{options}]),thread_get_message(stop).\n"
 else:
  exe=os.environ.get('TPL') or shutil.which('tpl') or '/opt/trealla/tpl'
  text=f":- asserta(user:file_search_path(library,{atom(a.sources/'trealla')})).\n:- use_module({atom(a.sources/'trealla/web_prolog.pl')}).\nmain :- web_prolog:web_prolog_node({port},[bind_address('127.0.0.1'),node_url('http://127.0.0.1:{port}'),{options}]),thread_get_message(stop).\n"
 script=a.output/f'{engine}-fixture.pl'; script.write_text(text)
 cmd=[exe,'-f','none','-q','-s',str(script),'-g','main','-t','halt'] if engine=='swi' else [exe,'-q','-f',str(script),'-g','main']
 env=dict(os.environ); env.setdefault('TPL_LIBRARY_PATH','/opt/trealla/library'); log=(a.output/f'{engine}-node.log').open('w')
 proc=subprocess.Popen(cmd,cwd=a.sources/engine,env=env,stdout=log,stderr=log,start_new_session=True)
 try:
  for _ in range(200):
   if proc.poll() is not None: raise RuntimeError(f'{engine} exited; see log')
   try:
    with socket.create_connection(('127.0.0.1',port),timeout=.1): pass
    break
   except OSError: time.sleep(.05)
  else: raise TimeoutError(engine)
  vcmd=[exe,'--version'] if engine=='swi' else [exe,'-g','current_prolog_flag(version_data,V),writeq(V),nl,halt']
  v=subprocess.run(vcmd,env=env,capture_output=True,text=True,timeout=10)
  record['engines'][engine]={'version':(v.stdout+v.stderr).strip(),'executable_sha256':sha(exe),'source_hashes':{str(f.relative_to(a.sources/engine)):sha(f) for f in (a.sources/engine).rglob('*.pl')}}
  if a.serve:
   print(f'Loopback demo: ws://127.0.0.1:{port}/ws; serve case-study/ at http://127.0.0.1:8000',flush=True); proc.wait()
  else:
   env.update(PLANNER_WS_URL=f'ws://127.0.0.1:{port}/ws',PLANNER_ENGINE=engine,PLANNER_REPORT=str(a.output/f'{engine}-results.json'))
   check=subprocess.run(['python3','/work/conformance/runner/baseline.py','--manifest','/work/conformance/cases/source-copying-0.1.json','--url',env['PLANNER_WS_URL'],'--candidate',engine,'--profile','actor','--report',str(a.output/f'{engine}-source-copying.json')],env=env,text=True,capture_output=True,timeout=180)
   (a.output/f'{engine}-checks.log').write_text(check.stdout+check.stderr); print(engine,check.stdout,check.stderr,flush=True); failed|=check.returncode!=0
 finally:
  if proc.poll() is None: os.killpg(proc.pid,signal.SIGTERM)
  try: proc.wait(timeout=5)
  except subprocess.TimeoutExpired: os.killpg(proc.pid,signal.SIGKILL); proc.wait()
  log.close(); (a.output/'environment.json').write_text(json.dumps(record,indent=2)+'\n')
raise SystemExit(1 if failed else 0)
