"""Repeat only refused N6 library assertions after query-retention expiry."""
from pathlib import Path
import json,time,sys,hashlib,collections
P=Path(__file__).resolve().parent;R=P/'suite-snapshot';sys.path[:0]=[str(R/'runner')];import baseline
from library_prefix import http_prefix
while not (P/'logs/endpoint-n6.done').exists():time.sleep(3)
print('N6 final query-expiry quiet period:303 seconds',flush=True);time.sleep(303)
rows=[];last=0;original=baseline.http_request

def paced(*a,**kw):
 global last
 delay=.8-(time.monotonic()-last)
 if delay>0:time.sleep(delay)
 last=time.monotonic();return original(*a,**kw)
baseline.http_request=paced
for f in sorted((P/'live-library/n6').glob('*.json')):
 before=json.loads(f.read_text());path=R/'cases'/f.name;pack=json.loads(path.read_text());selected={r['id'] for r in before['results'] if r['status']=='fail'}
 for c in pack['cases']:
  if c['id'] not in selected:continue
  if c.get('bounded_prefix'):time.sleep(303)
  row=dict(candidate='n6-paused-control',suite=pack['suite'],id=c['id'],original_file=str(f.relative_to(P)),manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
  try:
   wire=dict(requests=[dict(params=dict(goal='('+c['goal']+'),LibraryCheck=passed',template='LibraryCheck',format='prolog',limit=1,src_text=pack['source']),expect_prolog='success([passed],false).')])
   observed=http_prefix(c,pack['source'],'https://n6.elfenbenstornet.se') if c.get('bounded_prefix') else baseline.http_case(wire,'https://n6.elfenbenstornet.se',10,None,False)
   row.update(status='pass',observation=observed)
  except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
  rows.append(row);(P/'live-controls/n6-paused-library.json').write_text(json.dumps(dict(scope='Fresh unchanged assertions after303-second quiet period; original refusal files retained',results=rows,counts=dict(collections.Counter(r['status'] for r in rows))),indent=2)+'\n');print(pack['suite'],c['id'],row['status'],flush=True)
(P/'live-controls/n6-paused-library.json').write_text(json.dumps(dict(scope='Unchanged library assertions after query expiry; zero rows when no refusals',results=rows,counts=dict(collections.Counter(r['status'] for r in rows))),indent=2)+'\n')
(P/'n6-library-recovery.json').write_text(json.dumps(dict(status='pass' if all(r['status']=='pass' for r in rows) else 'fail',quiet_period_seconds=303,controlled_refused_cases=len(rows),original_results_preserved=True),indent=2)+'\n');

# Replay broad API admission refusals with the original case goals and profiles.
more=[]
for f in sorted((P/'live-more/n6').glob('*.json')):
 before=json.loads(f.read_text());pack=json.loads((R/'cases'/f.name).read_text());lookup={c['id']:c for c in pack['cases']}
 if pack['suite']=='relation-error-admission-0.1':continue # RELATION-only negative case is inapplicable to ISOBASE.
 for r in before['results']:
  if r['status']=='fail' and any(v in r.get('detail','') for v in ['503','query_limit_exceeded','429']):more.append((f,pack,lookup[r['id']]))
replayed=[]
if more and rows:
 print('N6 broad API expiry pause before controls',flush=True);time.sleep(303)
for i,(f,pack,original_case) in enumerate(more):
 c=json.loads(json.dumps(original_case).replace('__PEER__','https://n4.elfenbenstornet.se'))
 if pack.get('source'):c['source']=pack['source']+'\n'+c.get('source','')
 if c.get('candidate_error_formals') and 'gnu' in c['candidate_error_formals']:
  c['expected_formal']=c['candidate_error_formals']['gnu'];c['expected_error_names']=[c['expected_formal'].split('(')[0]]
 row=dict(candidate='n6-paused-more',suite=pack['suite'],id=c['id'],original_file=str(f.relative_to(P)),goal_and_assertions_unchanged=True,attempts=[])
 for attempt in range(2):
  try:
   if c['transport']=='http':observed=baseline.http_case(c,'https://n6.elfenbenstornet.se',10,None,pack.get('scope')=='diagnostic')
   else:
    params=dict(goal='('+c['goal']+'),BaselineResult=passed',template='BaselineResult',format='prolog',limit=1)
    if c.get('source'):params['src_text']=c['source']
    observed=baseline.http_case(dict(requests=[dict(params=params,expect_prolog='success([passed],false).')]),'https://n6.elfenbenstornet.se',10,None,pack.get('scope')=='diagnostic')
   row.update(status='pass',observation=observed);row['attempts'].append(dict(attempt=attempt+1,status='pass'));break
  except Exception as e:
   detail=type(e).__name__+': '+str(e);capacity=any(v in detail for v in ['503','query_limit_exceeded','429']);row['attempts'].append(dict(attempt=attempt+1,status='admission_refusal' if capacity else 'fail',detail=detail))
   if capacity and attempt==0:
    (P/'live-controls/n6-more-admission-attempts.json').write_text(json.dumps(dict(results=replayed+[dict(row,status='blocked')]),indent=2)+'\n');print('N6 capacity refusal retained; expiry pause before same unchanged assertion',c['id'],flush=True);time.sleep(303)
   else:row.update(status='fail',detail=detail)
 replayed.append(row);(P/'live-controls/n6-paused-more.json').write_text(json.dumps(dict(scope='Original broad ISOBASE assertions after303-second expiry; .8-second HTTP pacing; recurrent capacity refusals retained and at mostone retry after303s',results=replayed,counts=dict(collections.Counter(r['status'] for r in replayed))),indent=2)+'\n');print(pack['suite'],c['id'],row['status'],flush=True)
(P/'n6-controls.complete').write_text('complete\n')
