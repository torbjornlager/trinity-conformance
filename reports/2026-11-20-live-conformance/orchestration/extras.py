import json,sys,subprocess,socket,time,os,threading,http.server,functools,hashlib
from pathlib import Path
R=Path('/Users/lager/trinity-demonstrator/.trinity/conformance-live-20261120/suite-snapshot');O=Path('/Users/lager/trinity-demonstrator/.trinity/conformance-live-20261120');F=O/'extras';F.mkdir(exist_ok=True);sys.path.insert(0,str(R/'runner'));import run as actor,baseline,admission_probe
records=[];processes=[];logs=[]
def port():
 with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]
def atom(s):return actor.prolog_quote_atom(str(s))
def save():
 (F/'results.json').write_text(json.dumps(dict(format='full-manifest-extra-observations-v1',results=records),indent=2)+'\n')
def case_record(candidate,suite,case,fn,diagnostic=False,route=None):
 row=dict(candidate=candidate,suite=suite,id=case['id'],title=case['title']);started=time.monotonic()
 if route:row['route']=route
 try:
  row.update(status='observed' if diagnostic else 'pass',observation=fn())
  if diagnostic and isinstance(row['observation'],dict) and row['observation'].get('complete') is False:row['status']='diagnostic_error'
 except Exception as e:row.update(status='diagnostic_error' if diagnostic else 'fail',detail=type(e).__name__+': '+str(e))
 row['duration_ms']=round((time.monotonic()-started)*1000);records.append(row);save();print(candidate,suite,case['id'],row['status'],flush=True)
def start(name,cmd,cwd,p):
 log=(F/(name+'-node.log')).open('w');logs.append(log);proc=subprocess.Popen(cmd,cwd=cwd,env=dict(os.environ,TPL_LIBRARY_PATH='/opt/trealla/library'),stdout=log,stderr=subprocess.STDOUT);processes.append(proc)
 for _ in range(200):
  if proc.poll() is not None:raise RuntimeError(name+' startup exited')
  try:
   with socket.create_connection(('127.0.0.1',p),timeout=.1):return proc
  except OSError:time.sleep(.05)
 raise TimeoutError(name+' readiness')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R/'fixtures/portable-text')));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
ports={n:port() for n in ['swi','trealla','gnu']};urls={n:'http://127.0.0.1:'+str(p) for n,p in ports.items()};source='http://127.0.0.1:'+str(server.server_port)
try:
 for n in ['swi','trealla']:
  peer=urls['trealla' if n=='swi' else 'swi'];pairs='['+','.join(atom(u)+"-'conformance-isolated-peer-only'" for u in urls.values())+']'
  opts='profile(actor),sandbox(blacklist),auth(open),max_ws_commands_per_window(100000),max_call_requests_per_window(100000),max_session_spawns_per_window(100000),peer_transport_tokens('+pairs+'),load_uri_allowed_origins(['+','.join(map(atom,[*urls.values(),source]))+"]),load_uri_allowed_ip_ranges(['127.0.0.0/8'])"
  if n=='swi':
   goal="use_module('/opt/swi-prolog-node/prolog/web_prolog.pl'),set_setting(http:public_host,'127.0.0.1'),set_setting(http:public_port,"+str(ports[n])+"),set_setting(http:public_scheme,http),node("+str(ports[n])+",["+opts+"]),thread_get_message(stop)";cmd=['/usr/bin/swipl','-f','none','-q','-g',goal];cwd='/opt/swi-prolog-node'
  else:
   opts+=",node_url("+atom(urls[n])+"),bind_address('127.0.0.1'),bearer_token(peer,'[REDACTED]',[execute,internal_transport])"
   cmd=['/opt/trealla/tpl','-g','use_module(distribution),web_prolog:web_prolog_node('+str(ports[n])+',['+opts+'])'];cwd='/work/trealla'
  start(n,cmd,cwd,ports[n])
 for n in ['swi','trealla']:
  ws=urls[n].replace('http:','ws:')+'/ws'
  for suite in ['admission-marker-controls-0.1','admission-paths-0.1']:
   pack=json.loads((R/'cases'/(suite+'.json')).read_text())
   for c in pack['cases']:case_record(n,suite,c,lambda c=c:admission_probe.observe(c,ws,8,None),True)
 for n in ['swi','trealla']:
  for peer in ['swi','trealla']:
   for suite in ['interop-http-0.1','interop-actor-0.1','interop-successor-0.1']:
    pack=json.loads((R/'cases'/(suite+'.json')).read_text().replace('__PEER__',urls[peer]))
    for c in pack['cases']:
     fn=(lambda c=c:baseline.http_case(c,urls[n],8,None,False)) if c['transport']=='http' else (lambda c=c:baseline.query_case(c,urls[n].replace('http:','ws:')+'/ws',8,None))
     case_record(n+'-to-'+peer,suite,c,fn)
 with (F/'prompt-http.log').open('w') as log:r=subprocess.run([sys.executable,str(R/'runner/prompt_http.py'),'--swi',urls['swi'],'--trealla',urls['trealla'],'--output',str(F/'prompt-http.json')],stdout=log,stderr=subprocess.STDOUT,timeout=600)
 print('prompt-http exit',r.returncode,flush=True)
 # Direct GNU API checks use the same versioned goals, with the GNU worker's own envelope.
 worker='/work/gnu/isobase/query-worker'
 for manifest in sorted((R/'cases').glob('*.json')):
  pack=json.loads(manifest.read_text());suite=pack['suite']
  if pack.get('minimum_profile')!='isobase' or pack.get('source') or suite.startswith('standard-library-'):continue
  for c in pack['cases']:
   if c.get('transport')!='query' or c.get('source'):continue
   def check(c=c):
    r=subprocess.run([worker,'query(('+c['goal']+'),ok)','100'],cwd='/work/gnu/isobase',capture_output=True,text=True,timeout=30)
    parsed=[json.loads(line) for line in r.stdout.splitlines()];actor.require(r.returncode==0 and parsed==[dict(type='success',answers=['ok'],more=False)],str(parsed));return parsed
   case_record('gnu-direct-api',suite,c,check)
finally:
 for p in reversed(processes):
  p.terminate()
  try:p.wait(timeout=3)
  except subprocess.TimeoutExpired:p.kill();p.wait()
 for log in logs:log.close()
 server.shutdown();server.server_close();thread.join()
