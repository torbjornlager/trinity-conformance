from pathlib import Path
import time,subprocess,json,concurrent.futures,sys
P=Path(__file__).resolve().parent;R=P/'suite-snapshot'
while not ((P/'post-live.complete').exists() and (P/'n6-controls.complete').exists()):time.sleep(3)
print('Final finite admission phase:61-second quiet period',flush=True);time.sleep(61)
F=P/'live-controls/admission';F.mkdir(parents=True)
def one(n):
 with (P/'logs'/('admission-'+n+'.log')).open('w') as log:r=subprocess.run([sys.executable,str(R/'runner/admission.py'),'--url','https://'+n+'.elfenbenstornet.se','--count','140','--interval','.6','--output',str(F/(n+'.json'))],stdout=log,stderr=subprocess.STDOUT)
 d=json.loads((F/(n+'.json')).read_text());return dict(node=n,status=d['status'],count=d['count'],admission=d['node_info'].get('admission'),completed_requests_per_minute=d['completed_requests_per_minute'],exit_code=r.returncode)
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:rows=list(pool.map(one,['n1','n2','n3','n4','n5','n6','n7']))
for row in rows:
 limits=row['admission'];expected='requests_per_minute' if row['node']=='n6' else 'max_engine_starts_per_window' if row['node']=='n7' else 'max_call_requests_per_window'
 row['metadata_matches_selected_rate']=limits.get(expected)==120 and limits.get('rate_window_seconds')==60
 row['admission_policy_matches_before']=limits==json.loads((P/'metadata'/(row['node']+'.json')).read_text()).get('admission')
summary=dict(status='pass' if all(r['status']=='pass' and r['metadata_matches_selected_rate'] and r['admission_policy_matches_before'] for r in rows) else 'fail',finite_observations=980,quiet_period_seconds=61,scope='Fresh finite HTTP service and admission metadata only; outside81manifestrowcounts',nodes=rows)
(P/'admission-summary.json').write_text(json.dumps(summary,indent=2)+'\n');(P/'admission.complete').write_text('complete\n');print(json.dumps(summary),flush=True)
