from pathlib import Path
import sys,json,time,hashlib,collections,copy
P=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-conformance');sys.path[:0]=[str(R/'runner')];import baseline
url='https://n6.elfenbenstornet.se';targets=json.loads((P/'n6-targets.json').read_text());rows=[];old=baseline.http_request;last=0

def request(*a,**kw):
 global last
 delay=.8-(time.monotonic()-last)
 if delay>0:time.sleep(delay)
 last=time.monotonic();return old(*a,**kw)
baseline.http_request=request

def save():
 (P/'n6/results.json').write_text(json.dumps(dict(scope='Unchanged matchedpass-to-fail supporting assertions; initial303squiet,PE017separate303squiet; originalfullsweepunchanged',results=rows,counts=dict(collections.Counter(r['status'] for r in rows if r['trial']==1))),indent=2)+'\n')
def run(t,trial=1):
 suite=Path(t['file']).stem;path=R/'cases'/(suite+'.json');pack=json.loads(path.read_text());c=copy.deepcopy(next(c for c in pack['cases'] if c['id']==t['id']));row=dict(suite=suite,id=c['id'],trial=trial,original_file=t['file'],manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),started_utc=__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat())
 try:
  if c.get('transport')=='http':observed=baseline.http_case(c,url,10,None,False)
  else:
   params=dict(goal='('+c['goal']+'),BaselineResult=passed',template='BaselineResult',format='prolog',limit=1)
   if c.get('source'):params['src_text']=c['source']
   observed=baseline.http_case(dict(requests=[dict(params=params,expect_prolog='success([passed],false).')]),url,10,None,False)
  row.update(status='pass',observation=observed)
 except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
 rows.append(row);save();print(suite,c['id'],'trial',trial,row['status'],flush=True)
print('Initial N6 quiet period303seconds; no requests from this replay until expiry',flush=True);time.sleep(303)
finite=[t for t in targets if t['id'] not in ['LOCAL-001','PE-017']];assert len(finite)==54
for t in finite:run(t)
local=next(t for t in targets if t['id']=='LOCAL-001')
for trial in range(1,4):run(local,trial)
print('Separate303second quiet period before PE017 paged-error assertion',flush=True);time.sleep(303)
run(next(t for t in targets if t['id']=='PE-017'))
assert len([r for r in rows if r['trial']==1])==56
print('Final303second expiry before recovery check',flush=True);time.sleep(303)
recovery=baseline.http_case(dict(requests=[dict(params=dict(goal='Recovery=passed',template='Recovery',format='prolog',limit=1),expect_prolog='success([passed],false).')]),url,10,None,False)
(P/'n6/recovery.json').write_text(json.dumps(dict(status='pass',observed=recovery,query_retention_expired=True),indent=2)+'\n');(P/'n6.complete').write_text('complete\n');print('N6 replay and post-expiry recovery complete',flush=True)
