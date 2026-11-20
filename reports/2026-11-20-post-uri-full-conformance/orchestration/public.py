from pathlib import Path
import json,sys,time,subprocess,traceback
from urllib.request import urlopen
R=Path('/Users/lager/trinity-demonstrator/.trinity/conformance-post-uri-20261120/suite-snapshot');O=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'runner'));import run as actor,baseline
node=sys.argv[1];F=O/'observations'/node;F.mkdir(exist_ok=True);url='wss://'+node+'.elfenbenstornet.se/ws'
actor.set_session_interval(2.1)
profile='isobase' if node in ['n1','n6'] else 'isotope' if node=='n2' else 'relation' if node=='n0' else 'actor'
with urlopen('https://'+node+'.elfenbenstornet.se/node_info',timeout=12) as response:info=json.load(response)
(O/'metadata'/(node+'.json')).write_text(json.dumps(info,indent=2)+'\n')
if node=='n0':
 suites=['relation-error-admission-0.1']
else:suites=['isobase-http-0.1']
for suite in suites:
 cmd=[sys.executable,str(R/'runner/baseline.py'),'--manifest',str(R/'cases'/(suite+'.json')),'--url','https://'+node+'.elfenbenstornet.se','--profile',profile,'--candidate',node,'--report',str(F/(suite+'.json'))]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=180);(F/(suite+'.txt')).write_text(p.stdout+p.stderr);print(node,suite,p.returncode,flush=True)
if profile!='actor':sys.exit(0)
gate=json.loads((R/'profiles/actor-release-0.2.json').read_text());packs=[x['suite'] for x in gate['packs'] if x['suite']!='ownership-lifecycle-0.1']+['actor-behaviours-0.1','actor-supervisors-0.1','actor-workers-0.1','language-actor-0.1','server-waits-0.1','receive-callback-context-0.1','receive-wait-options-0.1','prompt-ws-0.1','source-directives-0.1']
candidate=actor.Candidate(url,'actor',5,None,'https://'+node+'.elfenbenstornet.se',False,())
for suite in packs:
 pack=json.loads((R/'cases'/(suite+'.json')).read_text());rows=[]
 for case in pack['cases']:
  started=time.monotonic();row=dict(id=case['id'],title=case['title'])
  try:
   observation=baseline.query_case(case,url,8,None) if 'goal' in case else actor.CASE_FUNCTIONS[case['id']](candidate)
   row.update(status='pass',observation=observation)
  except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
  row['duration_ms']=round((time.monotonic()-started)*1000);rows.append(row)
  report=dict(format='direct-runner-observations-v1',suite=suite,scope=pack.get('scope','required'),candidate=node,endpoint=url,manifest_sha256=__import__('hashlib').sha256((R/'cases'/(suite+'.json')).read_bytes()).hexdigest(),counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']},results=rows)
  (F/(suite+'.json')).write_text(json.dumps(report,indent=2)+'\n');print(node,suite,case['id'],row['status'],flush=True)
print(node,'complete',flush=True)
