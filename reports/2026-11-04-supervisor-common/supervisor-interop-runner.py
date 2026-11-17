import subprocess,os,time,socket
from pathlib import Path
root=Path('/Users/lager/trealla-port');tpl='/Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl';swi='/usr/local/bin/swipl';env=dict(os.environ,TPL_LIBRARY_PATH=str(Path(tpl).parent/'library'))
node='/Users/lager/swi-prolog-node/prolog/web_prolog.pl'
logs=[];processes=[];failed=[]
def start(args):
 p=subprocess.Popen(args,cwd=root,env=env);processes.append(p);return p
def run(label,args):
 print(label,flush=True)
 try:subprocess.run(args,cwd=root,env=env,timeout=60,check=True)
 except subprocess.CalledProcessError:failed.append(label)
try:
 start([tpl,'-g',"consult('distribution.pl'),web_prolog:web_prolog_node(27965,[profile(actor),sandbox(blacklist)]),thread_get_message(stop)"])
 start([swi,'-q','-g',f"use_module('{node}'),node:node(27969,[profile(actor),auth(open)]),thread_get_message(stop)"])
 for port in [27965,27969]:
  for i in range(100):
   try:
    with socket.create_connection(('127.0.0.1',port),timeout=.2):break
   except OSError:time.sleep(.1)
  else:raise RuntimeError('fixture did not start')
 for port in [27965,27969]:
  tests=f'remote_supervisor_tests:remote_supervisor_live_test({port})'
  if port==27965:tests+=f',remote_supervisor_tests:remote_supervisor_source_test({port}),remote_supervisor_tests:remote_supervisor_extended_test({port})'
  run(f'Trealla supervisor -> {port}',[tpl,'-g',f"(catch((consult('remote_supervisor_tests.pl'),{tests}),E,(writeq(E),nl,fail))->halt;halt(1))"])
 run('Native SWI supervisor -> Trealla',[swi,'-q','-s','swi_supervisor_compat.pl','-g',f"swi_supervisor_compat:run(27970,27965,'{node}'),halt"])
 print('TARGETED SUPERVISOR INTEROP FAILURES: '+repr(failed),flush=True)
 if failed:raise RuntimeError(failed)
finally:
 for p in processes:p.terminate()
 for p in processes:
  try:p.wait(timeout=5)
  except subprocess.TimeoutExpired:p.kill();p.wait()
