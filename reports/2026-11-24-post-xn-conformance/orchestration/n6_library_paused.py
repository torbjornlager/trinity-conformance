from pathlib import Path
import sys,json,time,hashlib,collections
P=Path(__file__).resolve().parents[1];R=P/'suite-snapshot';sys.path[:0]=[str(R/'runner')];import baseline
from library_prefix import http_prefix
path=R/'cases/standard-library-0.4.json';pack=json.loads(path.read_text());ids=['STDLIB-292','STDLIB-293','STDLIB-294','STDLIB-295'];rows=[];original=baseline.http_request;last=0
output=P/'live-controls/n6-paused-library.json'
if output.exists():
 rows=json.loads(output.read_text())['results']
 for row in rows:row.setdefault('quiet_seconds_before',61)

def paced(*a,**kw):
 global last
 delay=1.3-(time.monotonic()-last)
 if delay>0:time.sleep(delay)
 try:return original(*a,**kw)
 finally:last=time.monotonic()
baseline.http_request=paced
for id in ids:
 if any(r['id']==id and r['status']=='pass' for r in rows):continue
 print('N6 quiet period before',id,'303 seconds',flush=True);time.sleep(303);case=next(c for c in pack['cases'] if c['id']==id);row=dict(candidate='n6-http',id=id,title=case['title'],quiet_seconds_before=303)
 try:row.update(status='pass',observation=http_prefix(case,pack['source'],'https://n6.elfenbenstornet.se'))
 except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
 rows.append(row);(P/'live-controls/n6-paused-library.json').write_text(json.dumps(dict(suite=pack['suite'],manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),scope='Unchanged bounded-prefix assertions after query-capacity refusals; original HTTP503 results preserved',quiet_seconds_between_cases=303,prior_successes_retained_with_original_pause=True,results=rows,counts=dict(collections.Counter(r['status'] for r in rows))),indent=2)+'\n');print(id,row['status'],flush=True)
# Do not leave this run's bounded infinite continuations awaiting the idle expiry.
print('N6 final idle-expiry quiet period: 303 seconds',flush=True);time.sleep(303)
health=baseline.http_case(dict(requests=[dict(params=dict(goal='N6Recovered=passed',template='N6Recovered',format='prolog',limit=1),expect_prolog='success([passed],false).')]),'https://n6.elfenbenstornet.se',10,None,False)
(P/'n6-library-recovery.json').write_text(json.dumps(dict(status='pass',post_run_quiet_seconds=303,recovery=health),indent=2)+'\n');(P/'logs/n6-paused-library.done').write_text('complete\n')
