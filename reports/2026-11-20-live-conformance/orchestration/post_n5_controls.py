from pathlib import Path
import sys,json,time,hashlib,collections,http.cookiejar,urllib.request,urllib.parse,secrets
P=Path(__file__).resolve().parents[1];R=P/'suite-snapshot';sys.path[:0]=[str(R/'runner')];import run as actor,baseline
# Wait until N5's existing extra selection has completed its three explicit-empty-source trials.
while True:
 try:
  data=json.loads((P/'public-extra/results.json').read_text());done=any(r.get('candidate')=='n5' and r.get('id')=='SR-015' and r.get('trial')==3 for r in data['results'])
 except (OSError,ValueError):done=False
 if done:break
 time.sleep(2)
F=P/'live-controls';rows=[];path=R/'cases/selective-receive-0.2.json';pack=json.loads(path.read_text());case=next(c for c in pack['cases'] if c['id']=='SR-015')
if pack.get('source'):case=dict(case,source=pack['source']+'\n'+case.get('source',''))
actor.set_session_interval(2.1)
for trial in range(1,4):
 row=dict(candidate='n5',id=case['id'],trial=trial,source_options_identical_to_original_case=True)
 try:row.update(status='pass',observation=baseline.query_case(case,'wss://n5.elfenbenstornet.se/ws',10,None))
 except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
 rows.append(row)
(F/'trealla-sr015-exact-controls.json').write_text(json.dumps(dict(suite=pack['suite'],manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),results=rows,counts=dict(collections.Counter(r['status'] for r in rows))),indent=2)+'\n')
# Live HTTP namespace controls use the now-observed available N5 session route.
url='https://n5.elfenbenstornet.se';clients={};sessions=[];observed={}
def post(route,params,opener=None):
 data=json.dumps(params).encode() if route=='toplevel_spawn' else urllib.parse.urlencode(dict(params,format='json')).encode()
 req=urllib.request.Request(url+'/'+route,data=data,headers={'Content-Type':'application/json' if route=='toplevel_spawn' else 'application/x-www-form-urlencoded'})
 with (opener or clients[params['pid']]).open(req,timeout=10) as f:return json.load(f)
def call(pid,goal):return post('toplevel_call',dict(pid=pid,goal='('+goal+'),AuditCheck=passed',limit=1))
try:
 for _ in range(2):
  opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()));pid=post('toplevel_spawn',dict(options='[session(true)]'),opener)['pid'];sessions.append(pid);clients[pid]=opener
 name='hctx_live_'+secrets.token_hex(8)
 goals=[('first_register',sessions[0],f'self(S),register({name},S)'),('other_hidden_and_duplicate',sessions[1],f'whereis({name},undefined),self(S),register({name},S)'),('owner_lookup',sessions[0],f'self(S),whereis({name},S)'),('other_withdraw',sessions[1],f'unregister({name})'),('owner_preserved',sessions[0],f'self(S),whereis({name},S)'),('other_removed',sessions[1],f'whereis({name},undefined)')]
 for label,pid,goal in goals:observed[label]=call(pid,goal)
 ok=all(e.get('type')=='success' and e.get('more') is False for e in observed.values());row=dict(candidate='trealla',id='HCTX-002',status='pass' if ok else 'fail',observation=observed)
 (F/'live-n5-http-naming.json').write_text(json.dumps(dict(suite='http-session-context-0.1',endpoint=url,scope='Live anonymous retained HTTP ordinary-name namespace assertions; no node setting or credentials changed',manifest_sha256=hashlib.sha256((R/'cases/http-session-context-0.1.json').read_bytes()).hexdigest(),results=[row]),indent=2)+'\n')
 # Supplementary ready-producer controls, not the canonical pending-producer barrier test.
 trace={};trace['created']=call(sessions[0],"promise('https://n1.elfenbenstornet.se',true,R,[template(mark)])");ref=str(trace['created']['data'][0]['R']);assert ref.isdigit()
 trace['foreign_yield']=call(sessions[1],f'catch(yield({ref},_,[timeout(0)]),error(existence_error(promise,{ref}),_),Missing=true),Missing==true')
 trace['foreign_cleanup']=call(sessions[1],f'promise_cleanup({ref})');trace['owner_collect']=call(sessions[0],f'yield({ref},success([mark],false),[timeout(5)])')
 ok=all(e.get('type')=='success' and e.get('more') is False for e in trace.values())
 (F/'live-n5-http-ready-promise.json').write_text(json.dumps(dict(scope='Supplementary live promise isolation and owner collection; producer-pending/release barrier is measured separately in owned fixtures',results=[dict(id='HCTX-LIVE-READY',candidate='trealla',status='pass' if ok else 'fail',observation=trace)]),indent=2)+'\n')
finally:
 for pid in sessions:post('toplevel_halt',dict(pid=pid))
(P/'logs/post-n5-controls.done').write_text('complete\n')
print('N5 exact receive repeats and live HTTP namespace controls complete',flush=True)
