"""Explicitly authorised live checks; each case owns its created sessions/actors."""
import argparse,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'conformance/runner'))
import run as actor,baseline,ownership_lifecycle as life
root=Path(__file__).resolve().parent

def check_node(url,output,token=None,observer_token=None):
 output.mkdir(parents=True,exist_ok=False)
 candidate=actor.Candidate(url,'actor',8,token,None,False,())
 profile=json.loads((root/'conformance/profiles/actor-release-0.2.json').read_text());rows=[];expected=[]
 for pack in profile['packs']:
  manifest=json.loads((root/'conformance/cases'/(pack['suite']+'.json')).read_text())
  for case in manifest['cases']:
   expected.append(case['id']);start=time.monotonic();row=dict(suite=pack['suite'],id=case['id'])
   try:
    if pack['suite']=='ownership-lifecycle-0.1':result=life.execute(candidate,case,observer_token)
    elif pack['runner']=='baseline.py':result=baseline.query_case(case,url,8,token)
    else:result=actor.CASE_FUNCTIONS[case['id']](candidate)
    row.update(status='pass',observation=result)
   except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
   row['seconds']=round(time.monotonic()-start,4);rows.append(row)
   (output/'results.json').write_text(json.dumps(rows,indent=2)+'\n');print(case['id'],row['status'],flush=True)
 summary=dict(profile=profile['profile'],endpoint=url,expected_cases=len(expected),passed_cases=sum(r['status']=='pass' for r in rows),passed=(len(rows)==44 and len(set(expected))==44 and all(r['status']=='pass' for r in rows)))
 (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');return summary['passed']

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--node',type=int,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.node not in [3,4]:p.error('public anonymous fixture is restricted to N3/N4')
 raise SystemExit(not check_node(f'wss://n{a.node}.elfenbenstornet.se/ws',a.output))
