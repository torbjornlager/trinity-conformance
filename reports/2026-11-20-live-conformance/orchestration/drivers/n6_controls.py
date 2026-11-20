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
(P/'n6-library-recovery.json').write_text(json.dumps(dict(status='pass' if all(r['status']=='pass' for r in rows) else 'fail',quiet_period_seconds=303,controlled_refused_cases=len(rows),original_results_preserved=True),indent=2)+'\n');(P/'n6-controls.complete').write_text('complete\n')
