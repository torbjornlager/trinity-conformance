from pathlib import Path
import subprocess,json,time,os
O=Path(__file__).resolve().parent
started=time.monotonic()
while True:
 if not (O/'public-library.json').exists():
  assert time.monotonic()-started<180
  time.sleep(1);continue
 data=json.loads((O/'public-library.json').read_text())
 assert data['counts']['fail']==0,'public library assertion failed'
 if data['counts']['pass']==672:break
 assert time.monotonic()-started<180,'public library qualification did not finish'
 time.sleep(1)
env=dict(os.environ,NODE_PATH='/tmp/promise-context-browser-tools/node_modules')
plans=[('verification',['python3',str(O/'verify-public.py')]),('localhost',['python3',str(O/'check-localhost-public.py')]),('pingpong',['python3',str(O/'check-pingpong-public.py')]),('browser',['/Users/lager/.nvm/versions/node/v22.23.4/bin/node',str(O/'check-browser.cjs')])]
for label,cmd in plans:
 print('START',label,flush=True)
 with (O/('public-'+label+'.txt')).open('w') as log:code=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,env=env).returncode
 print('DONE',label,code,flush=True)
 assert code==0,label+' regression failed'
