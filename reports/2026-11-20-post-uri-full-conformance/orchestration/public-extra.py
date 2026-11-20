import json,sys,time,hashlib
from pathlib import Path
R=Path('/Users/lager/trinity-demonstrator/.trinity/conformance-post-uri-20261120/suite-snapshot');O=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'runner'));import run as actor,baseline
F=O/'public-extra';F.mkdir(exist_ok=True);rows=[]
while not all((O/'logs'/('endpoint-'+n+'.done')).exists() for n in ['n0','n1','n2','n3','n4','n5','n7']):time.sleep(2)
while not (O/'n7-prompts.complete').exists():time.sleep(2)
sys.path.insert(0,str(R/'adapters'));import client_naming
def naming_case(case,url):
 observed=client_naming.execute(case,lambda:client_naming.Session(url,None));actor.require(observed['status']=='pass',repr(observed));return observed
def save():
 (F/'results.json').write_text(json.dumps(dict(format='direct-runner-observations-v1',results=rows),indent=2)+'\n')
def check(node,suite,case,fn,peer=None):
 time.sleep(2.1)
 row=dict(candidate=node,suite=suite,id=case['id'],title=case['title']);t=time.monotonic()
 if peer:row['peer']=peer
 try:row.update(status='pass',observation=fn())
 except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
 row['duration_ms']=round((time.monotonic()-t)*1000);rows.append(row);save();print(node,suite,case['id'],row['status'],flush=True)
def wait_node(node):
 while not (O/'logs'/('library-'+node+'.done')).exists():time.sleep(2)
 while node in ['n3','n4','n5'] and not (O/'logs'/('paused-prompt-'+node+'.done')).exists():time.sleep(2)
for node in ['n3','n4','n5','n7']:
 wait_node(node)
 if node=='n7':time.sleep(61)
 actor.set_session_interval(2.1)
 url='wss://'+node+'.elfenbenstornet.se/ws';candidate=actor.Candidate(url,'actor',8,None,'https://'+node+'.elfenbenstornet.se',False,())
 for suite in ['supervisor-diagnostics-0.1','worker-diagnostics-0.1','native-terminal-newline-0.1','portable-text-0.1','wire-capabilities-0.1']:
  pack=json.loads((R/'cases'/(suite+'.json')).read_text())
  for case in pack['cases']:
   if case.get('transport')=='wire':fn=lambda c=case:baseline.wire_case(c,url,8,None)
   else:fn=lambda c=case:actor.CASE_FUNCTIONS[c['id']](candidate)
   check(node,suite,case,fn)
 if node=='n5':
  suite='selective-receive-0.2';pack=json.loads((R/'cases'/(suite+'.json')).read_text());case=next(c for c in pack['cases'] if c['id']=='SR-015');case=dict(case,source=pack.get('source','')+'\n'+case.get('source',''))
  for trial in range(1,4):
   check(node,suite,case,lambda c=case:baseline.query_case(c,url,10,None));rows[-1].update(trial=trial,selection='controlled unchanged repetition of initial public-only failure; private fixture passes');save()
 if node=='n7':
  suite='client-naming-0.1';pack=json.loads((R/'cases'/(suite+'.json')).read_text())
  for case in pack['cases']:check(node,suite,case,lambda c=case:naming_case(c,url))
 if node=='n3':
  suite='demonstrator-tutorials-0.1';pack=json.loads((R/'cases'/(suite+'.json')).read_text())
  for case in pack['cases']:check(node,suite,case,lambda c=case:actor.CASE_FUNCTIONS[c['id']](candidate))
pack=json.loads((R/'cases/interop-actor-0.1.json').read_text())
for source in ['n3','n4','n5','n7']:
 wait_node(source)
 if source=='n7':time.sleep(61)
 actor.set_session_interval(2.1)
 for target in [n for n in ['n3','n4','n5','n7'] if n!=source]:
  for original in pack['cases']:
   case=json.loads(json.dumps(original).replace('__PEER__','https://'+target+'.elfenbenstornet.se'))
   check(source,pack['suite'],case,lambda c=case:baseline.query_case(c,'wss://'+source+'.elfenbenstornet.se/ws',8,None),target)

(O/'logs/public-extra.done').write_text('complete\n')
