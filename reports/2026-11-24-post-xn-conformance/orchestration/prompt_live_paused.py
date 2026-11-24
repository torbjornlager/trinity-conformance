from pathlib import Path
import sys,time,threading,json,urllib.request,urllib.error,http.cookiejar,urllib.parse
P=Path(__file__).resolve().parents[1];R=P/'suite-snapshot';sys.path[:0]=[str(R/'runner')];import prompt_http as prompt
node=sys.argv[1];F=P/'live-controls';F.mkdir(exist_ok=True)
while not (P/'logs'/('library-'+node+'.done')).exists():time.sleep(2)
time.sleep(61)
if node=='n5':
 opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()));base='https://n5.elfenbenstornet.se';pid=None;status=None
 try:
  req=urllib.request.Request(base+'/toplevel_spawn',data=b'{"options":"[session(true)]"}',headers={'Content-Type':'application/json'})
  try:
   with opener.open(req,timeout=10) as f:d=json.load(f);status=f.status;pid=d.get('pid')
  except urllib.error.HTTPError as e:status=e.code
 finally:
  if pid:
   req=urllib.request.Request(base+'/toplevel_halt',data=urllib.parse.urlencode(dict(pid=pid,format='json')).encode())
   with opener.open(req,timeout=10) as f:f.read()
 if status==404:
  pack=json.loads(prompt.MANIFEST.read_text());rows=[dict(id=c['id'],engine='trealla',status='unsupported',detail='Live optional retained HTTP session routes return HTTP 404; enabled exact-runtime fixture observations are separate') for c in pack['cases']]
  (F/('paused-prompt-http-'+node+'.json')).write_text(json.dumps(dict(suite=pack['suite'],endpoint=base,results=rows,route_probe_http_status=404),indent=2)+'\n');(P/'logs'/('paused-prompt-'+node+'.done')).write_text('complete\n');raise SystemExit(0)
# Rate-limit session CREATION only; reply/abort/halt race submissions are unchanged.
lock=threading.Lock();original=prompt.post_response;last_spawn=0

def paced(base,command,fields,**kwargs):
 global last_spawn
 if command!='spawn':return original(base,command,fields,**kwargs)
 with lock:
  delay=4-(time.monotonic()-last_spawn)
  if delay>0:time.sleep(delay)
  try:return original(base,command,fields,**kwargs)
  finally:last_spawn=time.monotonic()
prompt.post_response=paced
sys.argv=['prompt_http.py','--'+('trealla' if node=='n5' else 'swi'),'https://'+node+'.elfenbenstornet.se','--output',str(F/('paused-prompt-http-'+node+'.json'))]
code=prompt.main();(P/'logs'/('paused-prompt-'+node+'.done')).write_text('complete\n');(P/('paused-prompt-'+node+'-job.json')).write_text(json.dumps(dict(exit_code=code,minimum_pause_between_session_spawns_seconds=4,race_submissions_unchanged=True),indent=2)+'\n');raise SystemExit(code)
