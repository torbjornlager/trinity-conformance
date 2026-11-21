from pathlib import Path
import time,subprocess,json,urllib.request,urllib.error,http.cookiejar,urllib.parse
P=Path(__file__).resolve().parents[1]
while not all((P/'logs'/('library-'+n+'.done')).exists() for n in ['n2','n3','n4','n5']):time.sleep(2)
while not all((P/'logs'/('paused-prompt-'+n+'.done')).exists() for n in ['n2','n3','n4','n5']):time.sleep(2)
time.sleep(61)
with (P/'logs/live-http-context.log').open('w') as out:r=subprocess.run(['python3',str(P/'orchestration/live_http_context.py')],stdout=out,stderr=subprocess.STDOUT)
(P/'live-http-context-job.json').write_text(json.dumps(dict(exit_code=r.returncode),indent=2)+'\n')
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()));url='https://n5.elfenbenstornet.se';pid=None;record={}
try:
 req=urllib.request.Request(url+'/toplevel_spawn',data=json.dumps(dict(options='[session(true)]')).encode(),headers={'Content-Type':'application/json'})
 try:
  with opener.open(req,timeout=10) as f:d=json.load(f);status=f.status
 except urllib.error.HTTPError as e:status=e.code;d=e.read().decode()
 if status==404:record=dict(status='unsupported',http_status=status,detail='Optional retained HTTP session routes are disabled in the preserved live N5 configuration; controlled exact-runtime fixture coverage is separate')
 elif status==200 and isinstance(d,dict) and d.get('type')=='spawned':pid=d['pid'];record=dict(status='observed',http_status=status,detail='Retained HTTP session spawn is available; this route probe is not full controlled context qualification')
 else:record=dict(status='fail',http_status=status,observation=d)
finally:
 if pid:
  req=urllib.request.Request(url+'/toplevel_halt',data=urllib.parse.urlencode(dict(pid=pid,format='json')).encode())
  with opener.open(req,timeout=10) as f:f.read()
 (P/'live-n5-http-route.json').write_text(json.dumps(record,indent=2)+'\n')
