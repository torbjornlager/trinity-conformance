from pathlib import Path
import json,hashlib,subprocess
O=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-demonstrator')
def read(name):return json.loads((O/name).read_text())
assert len(read('rollout-results.json'))==12
assert len(read('running-runtime-pins.json'))==12
assert all(x['exit_code']==0 for x in read('build-results.json'))
assert read('public-contexts/results.json')['counts']=={'pass':42,'fail':0,'blocked':9,'error':0}
assert read('public-contexts-first-permitted-run/results.json')['counts']=={'pass':42,'fail':0,'blocked':9,'error':0}
assert all(x.get('policy_exclusion') for x in read('public-contexts/results.json')['results'] if x['status']=='blocked')
checks={}
for file,expected in [('public-library.json',672),('public-library-browser.json',1568),('public-verification.json',60),('public-localhost.json',34),('public-browser.json',42)]:
 d=read(file);assert d['counts']=={'pass':expected,'fail':0},(file,d['counts']);checks[file]=expected
assert read('public-pingpong.json')['counts']==dict(pass_count=3,fail_count=0);checks['public-pingpong.json']=3;checks['public-contexts/results.json']=42
assert sum(checks.values())==2421
assert all(x['revoked'] for x in read('ephemeral-credential-cleanup.json'))
assert all(x['revoked'] for x in read('ephemeral-credential-cleanup-first-permitted.json'))
assert read('n5-peer-configuration-verification.json')['persisted_across_restart']
record={'status':'deployed and verified','consumer_image_revision':(O/'consumer-revision.txt').read_text().strip(),'consumer_documentation_revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'public_pass_count':2421,'public_context_policy_exclusions':9,'services':12,'public_checks':checks,'pins':{p.stem:json.loads(p.read_text()) for p in (R/'dependencies').glob('*.json')},'scope':'Selected deployment checks, not complete Appendix B or ISO certification','evidence_sha256':{str(p.relative_to(O)):hashlib.sha256(p.read_bytes()).hexdigest() for p in O.rglob('*') if p.is_file() and p.name!='verification.json' and '__pycache__' not in p.parts}}
(O/'verification.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS release: 12 services, exact pins, 2421 public checks, 9 explicit policy exclusions')
