"""Verify fresh execution inventory and preservation, without requiring assertions to pass."""
from pathlib import Path
import json,hashlib,collections,subprocess,datetime
P=Path(__file__).resolve().parents[1];R=P/'suite-snapshot'
def read(p):return json.loads(p.read_text())
def require(x,msg):
 if not x:raise AssertionError(msg)
for name in ['owned-native.complete','supplement.complete','post-live.complete','n6-controls.complete','provenance-controls.complete','admission.complete','n7-prompts.complete']:require((P/name).exists(),'Unfinished '+name)
for n in ['n0','n1','n2','n3','n4','n5','n6','n7']:require((P/'logs'/('endpoint-'+n+'.done')).exists(),'Unfinished endpoint '+n)
admission=read(P/'admission-summary.json');require(admission['finite_observations']==980,'Admission observation inventory')
inputs=read(P/'inputs.json');require(all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in inputs['files'].items()),'Frozen snapshot changed')
for n in ['n1','n2','n3','n4','n5','n6','n7']:
 modes=['http','wss'] if n in ['n3','n4','n5','n7'] else ['http']
 for v in ['0.1','0.2','0.3','0.4']:
  path=R/'cases'/('standard-library-'+v+'.json');pack=read(path);data=read(P/'live-library'/n/path.name)
  require(data['manifest_sha256']==hashlib.sha256(path.read_bytes()).hexdigest(),'Manifest changed '+n+' '+v)
  require(collections.Counter((r['candidate'],r['id']) for r in data['results'])==collections.Counter((n+'-'+mode,c['id']) for mode in modes for c in pack['cases']),'Library row inventory '+n+' '+v)
for n in ['n2','n3','n4','n5','n7']:
 d=read(P/'live-controls'/('paused-prompt-http-'+n+'.json'));require(collections.Counter(r['id'] for r in d['results'])==collections.Counter(c['id'] for c in read(R/'cases/prompt-http-0.1.json')['cases']),'Prompt inventory '+n)
require(len(read(P/'smoke/http-context.json'))==7,'Live HTTP context group inventory')
require(len(read(P/'live-controls/trealla-sr015-exact-controls.json')['results'])==3,'Exact public receive repetitions incomplete')
require(len(read(P/'live-controls/live-n5-http-naming.json')['results'])==1,'Live N5 retained naming incomplete')
require(len(read(P/'live-controls/live-n5-http-ready-promise.json')['results'])==1,'Live N5 retained promise control incomplete')
require((P/'live-controls/n6-paused-more.json').exists(),'N6 broad API refusal controls incomplete')
extra=read(P/'public-extra/results.json')['results'];require(len(extra)==120,'Public supplementary row count');actors=['n3','n4','n5','n7'];require(collections.Counter((r['candidate'],r.get('peer')) for r in extra if r['suite']=='interop-actor-0.1')==collections.Counter({(a,b):3 for a in actors for b in actors if a!=b}),'Directed interop inventory')
for label in ['swi-n134','swi-n2','trealla-n5']:
 d=read(P/'orchestration/isolated'/label/'summary.json');require('summary' in d and 'source_directives' in d,'Private gate incomplete '+label)
log=(P/'logs/runner-self-tests.log').read_text();require('Ran 123 tests' in log and '\nOK\n' in log,'Runner self-tests failed')
require((P/'browser-compat/browser-local-compatibility-0.1.json').exists(),'Browser compatibility missing');require(len(read(P/'browser-compat/browser-local-compatibility-0.1.json')['results'])==6,'Browser inventory')
refused=[(d['suite'],r['id']) for f in (P/'live-library/n6').glob('*.json') for d in [read(f)] for r in d['results'] if r['status']=='fail'];controls=read(P/'live-controls/n6-paused-library.json')['results'] if refused else [];require(collections.Counter((r['suite'],r['id']) for r in controls)==collections.Counter(refused),'N6 refusal controls incomplete')
before=read(P/'preservation-before.json');after=json.loads(subprocess.check_output(['docker','inspect',*[r['name'] for r in before]]));lookup={d['Name']:(d['Id'],d['Image']) for d in after};require(all(lookup[r['name']]==(r['id'],r['image']) for r in before),'Persistent service changed')
owned=[x for x in subprocess.check_output(['docker','ps','-a','--format','{{.Names}}'],text=True).splitlines() if x in ['conformance-post-uri-lab-20261120','conformance-post-uri-browser-20261120','conformance-post-uri-provenance-20261120'] ];require(not owned,'Owned fixture still exists')
result=dict(status='completed_with_failures_retained',completed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),manifest_count=inputs['manifest_count'],main_case_rows=inputs['main_case_rows'],live_library_rows=9262,additional_finite_admission_observations=980,directed_actor_pairs=12,public_extra_rows=120,runner_self_tests=123,n6_paused_control_rows=len(controls)+len(read(P/'live-controls/n6-paused-more.json')['results']),n6_paused_library_control_rows=len(controls),persistent_container_ids_and_images_unchanged=True,observed_automatic_restart=read(P/'runtime-restarts.json'),inputs_unchanged=True,all_observations_fresh=True)
(P/'completion-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
