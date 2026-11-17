import subprocess,socket,time,urllib.request,urllib.parse,json,os
from pathlib import Path
root=Path('/Users/lager/trealla-port');out=Path('/Users/lager/trinity-conformance/reports/2026-11-05-library-finite-cases');tpl='/Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl'
with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
with (out/'succ-error-node.log').open('w') as log:
 p=subprocess.Popen([tpl,'-g',f'use_module(distribution),web_prolog:web_prolog_node({port},[max_call_requests_per_window(1000)])'],cwd=root,env=dict(os.environ,TPL_LIBRARY_PATH=str(Path(tpl).parent/'library')),stdout=log,stderr=log)
 try:
  for _ in range(150):
   if p.poll() is not None:raise RuntimeError('node startup failed')
   try:
    with socket.create_connection(('127.0.0.1',port),timeout=.1):break
   except OSError:time.sleep(.03)
  rows=[]
  for id,goal in [('STDLIB-134','succ(1.5,V)'),('STDLIB-137','succ(V,1.5)')]:
   q=urllib.parse.urlencode(dict(goal=f'catch({goal},E,true)',template='observed(E,V)',format='prolog',limit=1))
   with urllib.request.urlopen(f'http://127.0.0.1:{port}/call?'+q,timeout=8) as r:body=r.read().decode()
   rows.append(dict(id=id,goal=goal,expected_formal_error='type_error(integer,1.5)',actual_response=body))
  (out/'trealla-succ-error-observations.json').write_text(json.dumps(dict(scope='Raw error observations from disposable Trealla HTTP calls; not passing conformance assertions',results=rows),indent=2)+'\n')
  print(json.dumps(rows))
 finally:
  p.terminate()
  try:p.wait(timeout=5)
  except subprocess.TimeoutExpired:p.kill();p.wait()
