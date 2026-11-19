from pathlib import Path
import json,hashlib,collections,subprocess,datetime
P=Path(__file__).resolve().parents[1];R=Path('/Users/lager/trinity-conformance')
def read(p):return json.loads(p.read_text())
def require(ok,reason):
 if not ok:raise AssertionError(reason)
inputs=read(P/'inputs.json');require(all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in inputs['files'].items()),'frozen input changed')
for n in ['n1','n2','n3','n4','n5','n6']:require((P/'logs'/('more-'+n+'.done')).exists(),n+' extended API incomplete')
for n in ['n1','n2','n3','n4','n5','n6','n7']:
 require((P/'logs'/('library-'+n+'.done')).exists(),n+' library incomplete')
 modes=['http','wss'] if n in ['n3','n4','n5','n7'] else ['http']
 for v in ['0.1','0.2','0.3','0.4']:
  suite='standard-library-'+v;manifest=read(R/'cases'/(suite+'.json'));data=read(P/'live-library'/n/(suite+'.json'));require(data['manifest_sha256']==hashlib.sha256((R/'cases'/(suite+'.json')).read_bytes()).hexdigest(),suite+' hash mismatch')
  expected=collections.Counter((n+'-'+mode,c['id']) for mode in modes for c in manifest['cases']);actual=collections.Counter((r['candidate'],r['id']) for r in data['results']);require(actual==expected,n+' '+suite+' missing/duplicate/unexpected rows')
for n in ['n2','n3','n4','n5']:
 require((P/'logs'/('paused-prompt-'+n+'.done')).exists(),n+' prompts incomplete');data=read(P/'live-controls'/('paused-prompt-http-'+n+'.json'));wanted={c['id'] for c in read(R/'cases/prompt-http-0.1.json')['cases']};require({r['id'] for r in data['results']}==wanted and len(data['results'])==len(wanted),n+' prompt inventory')
require((P/'logs/public-extra.done').exists(),'public extras incomplete');data=read(P/'public-extra/results.json');require(len(data['results'])==120,'public extras expected120 rows')
supplementary=['supervisor-diagnostics-0.1','worker-diagnostics-0.1','native-terminal-newline-0.1','portable-text-0.1','wire-capabilities-0.1']
for node in ['n3','n4','n5','n7']:
 expected=collections.Counter((suite,c['id']) for suite in supplementary for c in read(R/'cases'/(suite+'.json'))['cases'])
 actual=collections.Counter((r['suite'],r['id']) for r in data['results'] if r['candidate']==node and r['suite'] in supplementary)
 require(actual==expected,node+' supplementary inventory')
naming=read(R/'cases/client-naming-0.1.json');require(collections.Counter(r['id'] for r in data['results'] if r['candidate']=='n7' and r['suite']==naming['suite'])==collections.Counter(c['id'] for c in naming['cases']),'N7 naming inventory')
actors=['n3','n4','n5','n7'];pairs=collections.Counter((r['candidate'],r.get('peer')) for r in data['results'] if r['suite']=='interop-actor-0.1');require(pairs==collections.Counter({(a,b):3 for a in actors for b in actors if a!=b}),'directed interoperation inventory')
require(read(P/'live-http-context-job.json')['exit_code']==0,'live context controls failed/incomplete');require(len(read(P/'smoke/http-context.json'))==7,'expected seven live HTTP context groups')
require((P/'logs/post-n5-controls.done').exists(),'N5 source/namespace controls incomplete')
require((P/'logs/n6-paused-library.done').exists(),'N6 paused library controls/recovery incomplete')
n6=read(P/'live-controls/n6-paused-library.json');require(collections.Counter((r['id'],r['status']) for r in n6['results'])==collections.Counter({('STDLIB-'+str(i),'pass'):1 for i in range(292,296)}),'N6 paused bounded prefixes')
require(read(P/'n6-library-recovery.json')['status']=='pass','N6 post-expiry recovery')
controls=read(P/'n7-paced-controls.json');require(len(controls['results'])==5 and all(r['status']=='pass' for r in controls['results']),'N7 primary paced controls')
for label in ['swi-n134','swi-n2','trealla-n5']:
 d=read(P/'orchestration/isolated'/label/'summary.json');require(d['summary']['passed'] and d['source_directives']=={'pass':7,'fail':0},'private image gate '+label)
require('Ran 114 tests' in (P/'logs/runner-self-tests.log').read_text() and '\nOK\n' in (P/'logs/runner-self-tests.log').read_text(),'runner self tests')
before=read(P/'preservation-before.json');now=json.loads(subprocess.check_output(['docker','inspect',*[r['name'] for r in before]]));lookup={d['Name']:(d['Id'],d['Image']) for d in now};require(all(lookup[r['name']]==(r['id'],r['image']) for r in before),'persistent service changed')
result=dict(status='completed_with_failures_retained',completed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),all_selected_jobs_have_terminal_evidence=True,live_library_executions=9262,n6_paused_library_controls=4,directed_actor_pairs=12,public_extra_rows=120,runner_self_tests=114,persistent_container_ids_and_images_unchanged=True,inputs_unchanged=True)
(P/'completion-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
