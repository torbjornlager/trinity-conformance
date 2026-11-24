from pathlib import Path
import json,sys,time,hashlib
P=Path(__file__).resolve().parents[1];R=P/'suite-snapshot';sys.path[:0]=[str(R/'runner'),str(R/'adapters')]
import run as actor,baseline
from library_prefix import http_prefix,session_prefix
node=sys.argv[1];url='https://'+node+'.elfenbenstornet.se';F=P/'live-library'/node;F.mkdir(parents=True,exist_ok=True)
time.sleep(303 if node=='n6' else 61)
http_interval=.8
last_http=0;old_request=baseline.http_request
def request(*args,**kwargs):
 global last_http
 delay=http_interval-(time.monotonic()-last_http)
 if delay>0:time.sleep(delay)
 last_http=time.monotonic();return old_request(*args,**kwargs)
baseline.http_request=request
class Paced(actor.Harness):
 last_send=0
 def send(self,command):
  delay=(.3 if node=='n7' else .2)-(time.monotonic()-self.last_send)
  if delay>0:time.sleep(delay)
  self.last_send=time.monotonic();return super().send(command)
for ver in ['0.1','0.2','0.3','0.4']:
 path=R/'cases'/('standard-library-'+ver+'.json');pack=json.loads(path.read_text());rows=[]
 def save():
  (F/(pack['suite']+'.json')).write_text(json.dumps(dict(suite=pack['suite'],endpoint=url,manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),scope='Authorized public live HTTP and retained-session standard library; original source/goals and bounded paging assertions',http_min_interval_seconds=http_interval,results=rows,counts={s:sum(x['status']==s for x in rows) for s in ['pass','fail','blocked']}),indent=2)+'\n')
 # Session path uses the same maintained per-pack lifetime as local_standard_library.py.
 if node in ['n3','n4','n5','n7']:
  done=set()
  try:
   with Paced(actor.Candidate(url.replace('https:','wss:')+'/ws','actor',10,None,url,False,())) as h:
    h.spawn_shell('[session(true),src_text('+actor.prolog_quote_atom(pack['source'])+')]')
    for c in pack['cases']:
     row=dict(candidate=node+'-wss',id=c['id'],title=c['title'])
     try:
      if c.get('bounded_prefix'):observed=session_prefix(c,h)
      else:
       h.call('('+c['goal']+'),LibraryCheck=passed','[limit(1)]');observed=h.recv_type('success',limit=64)
       actor.require(observed.get('more') is False and actor.row_value(observed,'LibraryCheck')=='passed',repr(observed))
      row.update(status='pass',observation=observed)
     except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
     rows.append(row);done.add(c['id']);save()
    h.halt()
  except Exception as e:
   for c in pack['cases']:
    if c['id'] not in done:rows.append(dict(candidate=node+'-wss',id=c['id'],status='blocked',detail='retained session unavailable: '+type(e).__name__+': '+str(e)))
   save()
  print(node,pack['suite'],'WSS complete',flush=True)
 for c in pack['cases']:
  if node=='n6' and c.get('bounded_prefix'):
   print('N6 quiet period before bounded generator:303 seconds',flush=True);time.sleep(303)
  row=dict(candidate=node+'-http',id=c['id'],title=c['title'])
  try:
   wire=dict(requests=[dict(params=dict(goal='('+c['goal']+'),LibraryCheck=passed',template='LibraryCheck',format='prolog',limit=1,src_text=pack['source']),expect_prolog='success([passed],false).')])
   observed=http_prefix(c,pack['source'],url) if c.get('bounded_prefix') else baseline.http_case(wire,url,10,None,False)
   row.update(status='pass',observation=observed)
  except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
  rows.append(row);save()
 print(node,pack['suite'],'HTTP complete',flush=True)
(P/'logs'/('library-'+node+'.done')).write_text('complete\n')
