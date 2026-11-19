import json,sys,time,hashlib
from pathlib import Path
R=Path('/Users/lager/trinity-conformance');O=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'runner'));import run as actor,baseline
F=O/'public-extra';F.mkdir();rows=[]
def save():
 (F/'results.json').write_text(json.dumps(dict(format='direct-runner-observations-v1',results=rows),indent=2)+'\n')
def check(node,suite,case,fn,peer=None):
 row=dict(candidate=node,suite=suite,id=case['id'],title=case['title']);t=time.monotonic()
 if peer:row['peer']=peer
 try:row.update(status='pass',observation=fn())
 except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
 row['duration_ms']=round((time.monotonic()-t)*1000);rows.append(row);save();print(node,suite,case['id'],row['status'],flush=True)
for node in ['n3','n4','n5','n7']:
 if node=='n7':time.sleep(61)
 actor.set_session_interval(5 if node=='n7' else 2.1)
 url='wss://'+node+'.elfenbenstornet.se/ws';candidate=actor.Candidate(url,'actor',8,None,'https://'+node+'.elfenbenstornet.se',False,())
 for suite in ['supervisor-diagnostics-0.1','worker-diagnostics-0.1','native-terminal-newline-0.1','portable-text-0.1','wire-capabilities-0.1']:
  pack=json.loads((R/'cases'/(suite+'.json')).read_text())
  for case in pack['cases']:
   if case.get('transport')=='wire':fn=lambda c=case:baseline.wire_case(c,url,8,None)
   else:fn=lambda c=case:actor.CASE_FUNCTIONS[c['id']](candidate)
   check(node,suite,case,fn)
 if node=='n3':
  suite='demonstrator-tutorials-0.1';pack=json.loads((R/'cases'/(suite+'.json')).read_text())
  for case in pack['cases']:check(node,suite,case,lambda c=case:actor.CASE_FUNCTIONS[c['id']](candidate))
pack=json.loads((R/'cases/interop-actor-0.1.json').read_text())
for source in ['n3','n4','n5','n7']:
 if source=='n7':time.sleep(61)
 actor.set_session_interval(5 if source=='n7' else 2.1)
 for target in [n for n in ['n3','n4','n5','n7'] if n!=source]:
  for original in pack['cases']:
   case=json.loads(json.dumps(original).replace('__PEER__','https://'+target+'.elfenbenstornet.se'))
   check(source,pack['suite'],case,lambda c=case:baseline.query_case(c,'wss://'+source+'.elfenbenstornet.se/ws',8,None),target)
# Preserve first-run admission failures and rerun only those unchanged cases as controls.
time.sleep(61);actor.set_session_interval(5);node='n7';url='wss://n7.elfenbenstornet.se/ws';candidate=actor.Candidate(url,'actor',5,None,'https://n7.elfenbenstornet.se',False,());controls=[]
for p in sorted((O/'observations/n7').glob('*.json')):
 data=json.loads(p.read_text());pack=json.loads((R/'cases'/(data['suite']+'.json')).read_text());by_id={c['id']:c for c in pack['cases']}
 for original in data.get('results',[]):
  if original['status']!='fail' or '429' not in original.get('detail',''):continue
  c=by_id[original['id']];row=dict(candidate='n7-paced-control',suite=pack['suite'],id=c['id'])
  try:
   value=baseline.query_case(c,url,8,None) if 'goal' in c else actor.CASE_FUNCTIONS[c['id']](candidate)
   row.update(status='pass',observation=value)
  except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
  controls.append(row);(F/'n7-admission-controls.json').write_text(json.dumps(dict(results=controls,session_interval_seconds=5,original_failures_preserved=True),indent=2)+'\n');print('N7 CONTROL',c['id'],row['status'],flush=True)
