import subprocess,os,time,json,socket,sys
from pathlib import Path
P=Path('/Users/lager/trinity-demonstrator/.trinity/conformance-post-uri-20261120' );R=P/'suite-snapshot';F=P/'prompt-enabled';F.mkdir();procs=[]
for name,port in [('swi',19790),('trealla',19791)]:
 opts='profile(actor),sandbox(blacklist),auth(open),max_call_requests_per_window(10000),max_ws_commands_per_window(10000),max_session_spawns_per_window(10000)'
 if name=='swi':
  cmd=['/usr/bin/swipl','-q','-f','none','-g',"use_module('/opt/swi-prolog-node/prolog/web_prolog.pl'),set_setting(http:public_host,'127.0.0.1'),set_setting(http:public_port,19790),set_setting(http:public_scheme,http),node(19790,["+opts+"]),thread_get_message(stop)"]
  cwd='/opt/swi-prolog-node'
 else:
  cmd=['/opt/trealla/tpl','-g',"use_module(distribution),web_prolog:web_prolog_node(19791,[bind_address('127.0.0.1'),node_url('http://127.0.0.1:19791'),http_sessions(true),"+opts+"])"];cwd='/work/trealla'
 log=(F/(name+'-node.log')).open('w');proc=subprocess.Popen(cmd,cwd=cwd,env=dict(os.environ,TPL_LIBRARY_PATH='/opt/trealla/library'),stdout=log,stderr=log);procs.append((proc,log))
 for _ in range(200):
  if proc.poll() is not None:raise RuntimeError(name+' startup failed')
  try:
   with socket.create_connection(('127.0.0.1',port),timeout=.1):break
  except OSError:time.sleep(.05)
try:
 subprocess.run([sys.executable,str(R/'runner/prompt_http.py'),'--swi','http://127.0.0.1:19790','--trealla','http://127.0.0.1:19791','--output',str(F/'prompt-http-enabled.json')],stdout=(F/'runner.log').open('w'),stderr=subprocess.STDOUT,timeout=600)
finally:
 for proc,log in procs:
  proc.terminate()
  try:proc.wait(timeout=5)
  except subprocess.TimeoutExpired:proc.kill();proc.wait()
  log.close()
