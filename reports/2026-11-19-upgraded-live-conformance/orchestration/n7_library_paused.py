from pathlib import Path
import sys,json,time,collections,hashlib
P=Path(__file__).resolve().parents[1];R=P/'suite-snapshot';sys.path[:0]=[str(R/'runner')]
import run as actor,baseline
from library_prefix import session_prefix,http_prefix
F=P/'live-library/n7';F.mkdir(exist_ok=True);url='https://n7.elfenbenstornet.se';original=P/'live-library/n7-http-allocation-attempt'
actor.set_session_interval(15);old_request=baseline.http_request;last_http=0
# Stateless calls each allocate a new public engine. Retain the route's 20/min limit.
def paced(*a,**kw):
 global last_http
 delay=4-(time.monotonic()-last_http)
 if delay>0:time.sleep(delay)
 try:return old_request(*a,**kw)
 finally:last_http=time.monotonic()
baseline.http_request=paced
class Paced(actor.Harness):
 last_send=0
 def send(self,command):
  delay=.3-(time.monotonic()-self.last_send)
  if delay>0:time.sleep(delay)
  self.last_send=time.monotonic();return super().send(command)
print('N7 HTTP library quiet period: 61 seconds',flush=True);time.sleep(61)
for version in ['0.1','0.2','0.3','0.4']:
 path=R/'cases'/('standard-library-'+version+'.json');pack=json.loads(path.read_text());rows=[]
 prior=original/(pack['suite']+'.json');data=json.loads(prior.read_text()) if prior.exists() else dict(results=[])
 prior_by={(r['candidate'],r['id']):r for r in data['results']}
 def usable(mode,case):
  r=prior_by.get(('n7-'+mode,case['id']))
  # Preserve completed predicates, including real failures; rerun admission refusals/unexecuted rows.
  return r if r and r['status'] in ['pass','fail'] and '429' not in r.get('detail','') else None
 def carry(r):return dict(r,carried_forward_from=str(prior.relative_to(P)))
 def save():
  (F/(pack['suite']+'.json')).write_text(json.dumps(dict(suite=pack['suite'],candidate='n7',endpoint=url,manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),scope='Paused live completion; valid first observations carried forward, original admission refusals preserved separately',http_pause_after_completed_request_seconds=4,minimum_ws_session_start_interval_seconds=15,results=rows,counts=dict(collections.Counter(r['status'] for r in rows))),indent=2)+'\n')
 todo=[c for c in pack['cases'] if not usable('wss',c)]
 for c in pack['cases']:
  if usable('wss',c):rows.append(carry(usable('wss',c)))
 if todo:
  time.sleep(15)
  try:
   with Paced(actor.Candidate(url.replace('https:','wss:')+'/ws','actor',12,None,url,False,())) as h:
    h.spawn_shell('[session(true),src_text('+actor.prolog_quote_atom(pack['source'])+')]')
    for c in todo:
     row=dict(candidate='n7-wss',id=c['id'],title=c['title'])
     try:
      if c.get('bounded_prefix'):observed=session_prefix(c,h)
      else:
       h.call('('+c['goal']+'),LibraryCheck=passed','[limit(1)]');observed=h.recv_type('success',limit=64);actor.require(observed.get('more') is False and actor.row_value(observed,'LibraryCheck')=='passed',repr(observed))
      row.update(status='pass',observation=observed)
     except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
     rows.append(row);save()
    h.halt()
  except Exception as e:
   done={r['id'] for r in rows if r['candidate']=='n7-wss'}
   for c in todo:
    if c['id'] not in done:rows.append(dict(candidate='n7-wss',id=c['id'],status='blocked',detail=type(e).__name__+': '+str(e)))
   save()
 print(version,'WSS complete',flush=True)
 for c in pack['cases']:
  if usable('http',c):rows.append(carry(usable('http',c)));save();continue
  row=dict(candidate='n7-http',id=c['id'],title=c['title'])
  try:
   wire=dict(requests=[dict(params=dict(goal='('+c['goal']+'),LibraryCheck=passed',template='LibraryCheck',format='prolog',limit=1,src_text=pack['source']),expect_prolog='success([passed],false).')])
   observed=http_prefix(c,pack['source'],url) if c.get('bounded_prefix') else baseline.http_case(wire,url,12,None,False)
   row.update(status='pass',observation=observed)
  except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
  rows.append(row);save()
 print(version,'HTTP complete',dict(collections.Counter(r['status'] for r in rows)),flush=True)
(P/'logs/library-n7.done').write_text('complete\n');(P/'n7-paced-library-job.json').write_text(json.dumps(dict(status='complete',http_pause_seconds=4,ws_session_start_interval_seconds=15,initial_refusals_retained=True),indent=2)+'\n')
