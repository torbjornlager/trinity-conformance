from pathlib import Path
import sys,json,time,subprocess,collections
P=Path(__file__).resolve().parents[1];R=P/'suite-snapshot';sys.path[:0]=[str(R/'runner')]
import run as actor,baseline
rows=[];actor.set_session_interval(15);url='wss://n7.elfenbenstornet.se/ws';candidate=actor.Candidate(url,'actor',10,None,'https://n7.elfenbenstornet.se',False,())
print('N7 quiet period: 61 seconds',flush=True);time.sleep(61)
for path in sorted((P/'public-initial/n7-before-enforced-pause').glob('*.json')):
 data=json.loads(path.read_text());pack=json.loads((R/'cases'/(data['suite']+'.json')).read_text());by_id={c['id']:c for c in pack['cases']}
 for original in data.get('results',[]):
  if original['status']!='fail' or '429' not in original.get('detail',''):continue
  case=by_id[original['id']];row=dict(id=case['id'],suite=pack['suite'],candidate='n7-paced-control',original_status=original['status'],original_detail=original.get('detail',''))
  time.sleep(15)
  try:row.update(status='pass',observation=baseline.query_case(case,url,10,None) if 'goal' in case else actor.CASE_FUNCTIONS[case['id']](candidate))
  except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
  rows.append(row);(P/'n7-paced-controls.json').write_text(json.dumps(dict(scope='User-requested rerun of original N7 429 admission refusals',quiet_seconds=61,minimum_session_start_interval_seconds=15,minimum_pause_between_cases_seconds=15,original_failures_preserved=True,results=rows,counts=dict(collections.Counter(r['status'] for r in rows))),indent=2)+'\n');print(case['id'],row['status'],flush=True)
print('Resuming unexecuted N7 primary cases with 15-second pauses',flush=True)
with (P/'logs/public-n7.log').open('a') as out:r=subprocess.run(['python3',str(P/'orchestration/public_resume_n7.py'),'n7'],stdout=out,stderr=subprocess.STDOUT)
(P/'n7-resume-job.json').write_text(json.dumps(dict(exit_code=r.returncode,session_start_interval_seconds=15,pause_between_cases_seconds=15),indent=2)+'\n')
print('N7 resumed primary exit',r.returncode,flush=True)
with (P/'logs/library-n7.log').open('w') as out:r=subprocess.run(['python3',str(P/'orchestration/live_library.py'),'n7'],stdout=out,stderr=subprocess.STDOUT)
(P/'n7-library-job.json').write_text(json.dumps(dict(exit_code=r.returncode),indent=2)+'\n');print('N7 library exit',r.returncode,flush=True)
