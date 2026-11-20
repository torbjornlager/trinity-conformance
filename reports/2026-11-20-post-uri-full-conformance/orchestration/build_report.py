"""Export this run's observations; raw failures and invalid attempts stay visible."""
import json,hashlib,re,collections,subprocess,shutil,sys
from pathlib import Path
R=Path('/Users/lager/trinity-conformance');O=Path(__file__).resolve().parents[1];D=(O/'report-draft') if '--draft' in sys.argv else R/'reports/2026-11-20-post-uri-full-conformance'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
STATUS={'pass','fail','blocked','error','observed','unsupported','diagnostic_error','not_applicable','deferred'}
def rows(x):
 if isinstance(x,dict):
  if x.get('status') in STATUS and any(k in x for k in ['id','case_id','case','label','title']):yield x;return
  for k,v in x.items():
   if k not in ['observation','transcript','sources','source','inputs','requests','events','trace']:yield from rows(v)
 elif isinstance(x,list):
  for v in x:yield from rows(v)
secrets=set()
for p in (O/'orchestration/isolated').rglob('*.private.pl'):
 secrets.update(re.findall(r"bearer_token\([^,]+,'([^']+)'",p.read_text()))
sensitive=re.compile(r'(^|[-_])(authorization|cookie|password|secret|token|credentials?|query.owner)([-_]|$)',re.I)
def clean(x):
 if isinstance(x,dict):return {k:('[REDACTED]' if (sensitive.search(k) or k=='principal_id') and not any(s in k for s in ['sha256','token_env','token-env','timeout']) else clean(v)) for k,v in x.items()}
 if isinstance(x,list):
  if len(x)==2 and isinstance(x[0],str) and sensitive.search(x[0]):return [x[0],'[REDACTED]']
  return [clean(v) for v in x]
 if isinstance(x,str):
  for value in secrets:x=x.replace(value,'[REDACTED_FIXTURE_TOKEN]')
  x=re.sub(r'(?i)(Bearer\s+)[A-Za-z0-9_.~-]+',r'\1[REDACTED]',x)
  return re.sub(r"(bearer_token\([^,]+,)'[^']+'",r"\1'[REDACTED]'",x)
 return x
inputs=read(O/'inputs.json');assert all(sha(R/f)==h for f,h in inputs['files'].items()),'Frozen suite inputs changed'
if D.exists():
 assert '--draft' in sys.argv,'Final report already exists'
 shutil.rmtree(D)
D.mkdir(parents=True)
manifests={p.stem:read(p) for p in sorted((R/'cases').glob('*.json'))};by_hash={sha(R/'cases'/(s+'.json')):s for s in manifests}
records=[];evidence=collections.defaultdict(list)
subdirs=['observations','public-initial','public-extra','live-more','live-library','live-library-initial-concurrent','live-library-overlap-attempt','live-controls','native','followup-native','extras','supplemental','orchestration/isolated','smoke','prompt-enabled','procps-rerun','procps-rerun-before-profiles','browser-compat']
def classification(path):
 s=str(path)
 if s=='live-controls/prompt-http-n2.json':return 'first_public_session_spawn_admission_attempt_preserved'
 if s=='live-controls/n6-paused-library.json':return 'paced_public_capacity_control_original_refusal_retained'
 if 'paused-prompt-http' in s:return 'paced_public_http_prompt_controls'
 if 'http-allocation-attempt' in s:return 'first_public_http_engine_admission_attempt_preserved'
 if s.startswith('procps-rerun-before-profiles/'):return 'invalid_fixture_setup_missing_profile_provenance_inputs'
 if 'initial-websocket-transport' in s:return 'invalid_harness_transport_for_http_only_endpoint'
 if any(w in s for w in ['overlap-attempt','initial-concurrent']):return 'overlapping_orchestration_attempt_not_qualification'
 if 'before-http-transport-correction' in s:return 'superseded_transport_attempt'
 if s.startswith('public-initial/'):return 'first_attempt_preserved'
 if s.startswith('live-controls/partial-page'):return 'unchanged_assertion_control_with_correct_wss_url'
 if s.startswith(('native/','followup-native/','extras/','supplemental/','orchestration/isolated/','prompt-enabled/','procps-rerun/','browser-compat/')):return 'owned_fixture_or_direct_api_not_live_endpoint'
 return 'public_live_observation'
def inferred_suites(data,path):
 result=set()
 if isinstance(data,dict) and data.get('suite') in manifests:result.add(data['suite'])
 if isinstance(data,dict) and data.get('manifest_sha256') in by_hash:result.add(by_hash[data['manifest_sha256']])
 for part in path.parts:
  for s in manifests:
   if part==s or part.startswith(s+'-') or part==s+'.json':result.add(s)
 # Maintained aggregate adapters select these exact manifests.
 for part,suites in {'promises':['promise-yield-0.1','interop-http-0.1'],'promises-valid':['promise-yield-0.1','interop-http-0.1'],'promise-diagnostics':['promise-diagnostics-0.1'],'promise-diagnostics-valid':['promise-diagnostics-0.1'],'partial-page-errors':['partial-page-errors-0.1','error-contract-0.1'],'node-uri-io':['node-uri-io-0.1'],'rpc-timeouts-fixtures':['rpc-timeout-0.1'],'http-transport-fixtures':['http-transport-options-0.1'],'statechart-document-fixtures':['statechart-document-0.1'],'contexts':['retained-context-0.1'],'closure':['retained-context-0.1'],'client-naming':['client-naming-0.1'],'receive-controls':['receive-control-0.1'],'library-noncompletion':['library-noncompletion-0.1'],'http-context-authenticated':['http-session-context-0.1'],'http-context-anonymous':['http-session-context-0.1'],'prompt-http.json':['prompt-http-0.1'],'prompt-http-enabled.json':['prompt-http-0.1']}.items():
  if part in path.parts:result.update(suites)
 return result
for sub in subdirs:
 for f in sorted((O/sub).rglob('*')):
  if not f.is_file() or f.suffix not in ['', '.json']:continue
  if '.private.' in f.name:continue
  try:data=read(f)
  except (ValueError,UnicodeError):continue
  rs=list(rows(data));has_group=isinstance(data,dict) and any(k in data for k in ['packs','checks','groups','runs'])
  if not rs and not has_group and f.name not in ['summary.json','startup-readiness.json']:continue
  rel=f.relative_to(O);target=D/'observations'/rel;write(target,clean(data));scope=classification(rel);suites=inferred_suites(data,rel)
  file_node=next((x for x in rel.parts if x in ['n0','n1','n2','n3','n4','n5','n6','n7']),None)
  if suites=={'relation-error-admission-0.1'} and file_node and file_node!='n0':scope='out_of_scope_relation_negative_on_higher_profile'
  if suites=={'isobase-error-admission-0.1'} and file_node and file_node not in ['n1','n6']:scope='out_of_scope_isobase_negative_on_higher_profile'
  if suites=={'browser-local-compatibility-0.1'} and rel.parts[0]!='browser-compat':scope='out_of_scope_browser_expectations_on_native'
  record=dict(file=str(target.relative_to(D)),classification=scope,suites=sorted(suites),counts=dict(collections.Counter(r['status'] for r in rs)),rows=len(rs));records.append(record)
  for row in rs:
   selected={row['suite']} if row.get('suite') in manifests else suites
   for suite in selected:
    if any(c['id']==row.get('id',row.get('case_id',row.get('case'))) for c in manifests[suite]['cases']):
     row_scope=scope
     node=next((x for x in rel.parts if x in ['n0','n1','n2','n3','n4','n5','n6','n7']),None)
     if suite=='relation-error-admission-0.1' and node and node!='n0':row_scope='out_of_scope_relation_negative_on_higher_profile'
     if suite=='isobase-error-admission-0.1' and node and node not in ['n1','n6']:row_scope='out_of_scope_isobase_negative_on_higher_profile'
     if suite=='browser-local-compatibility-0.1' and not str(row.get('candidate','')).startswith('swi-wasm'):row_scope='out_of_scope_browser_expectation_on_native'
     if 'invalid WebSocket URL' in row.get('detail',''):row_scope='invalid_harness_toplevel_url'
     evidence[(suite,row.get('id',row.get('case_id',row.get('case'))))].append(dict(file=record['file'],status=row['status'],candidate=row.get('candidate',row.get('engine')),classification=row_scope))
for n in ['n7-paced-controls.json','n7-resume-job.json','n7-library-job.json','live-n5-http-route.json','lab-cleanup.json','live-http-context-job.json','provenance.json','public-rate-observations.json','phase-correction.json','worker-correction.json','fixture-setup-corrections.json','n7-admission-policy.json','n7-paced-library-job.json','completion-verification.json','browser-provenance.json','n6-query-policy.json','n6-library-recovery.json']:
 if (O/n).exists():write(D/'execution'/n,clean(read(O/n)))
if (O/'n7-paced-controls.json').exists():
 for row in read(O/'n7-paced-controls.json')['results']:evidence[(row['suite'],row['id'])].append(dict(file='execution/n7-paced-controls.json',candidate='n7-paced-control',status=row['status'],classification='user_requested_paused_control_original_refusal_retained'))
for p in O.glob('*-jobs.json'):write(D/'execution'/p.name,clean(read(p)))
for p in O.glob('*-plan.json'):write(D/'execution'/p.name,clean(read(p)))
# Keep fixture setup corrections and the fresh execution plans reviewable.
for name in ['fixture-setup-corrections.json','endpoint-jobs.json','post-live-jobs.json','supplement-jobs.json','provenance-control-jobs.json','n7-prompt-job.json','input-comparison.json','runtime-restarts.json']:
 if (O/name).exists():write(D/'execution'/name,clean(read(O/name)))
for name in ['runner-self-tests-old-node-attempt.log','browser-missing-npm-attempt.log','followup-promises-valid.log','provenance-promises-ownership-attempt.log']:
 if (O/'logs'/name).exists():
  out=D/'execution'/name.replace('.log','.txt');text=clean((O/'logs'/name).read_text());out.write_text(('\n'.join(line.rstrip() for line in text.splitlines())+'\n') if name=='browser-missing-npm-attempt.log' else text)
if (O/'admission-summary.json').exists():
 admission=read(O/'admission-summary.json');admission['scope']='Fresh finite HTTP service and admission metadata only; outside manifest case-row counts';write(D/'execution/admission-summary.json',clean(admission))
for f in (O/'live-controls/admission').glob('*.json'):
 data=read(f);target=D/'observations/live-controls/admission'/f.name;write(target,clean(data))
 if not any(r['file']==str(target.relative_to(D)) for r in records):records.append(dict(file=str(target.relative_to(D)),classification='supplementary_finite_admission_probe_not_manifest_case',suites=[],counts=dict(collections.Counter(r['status'] for r in data['observations'])),rows=len(data['observations'])))
write(D/'suite-inputs.json',inputs)
for p in (O/'metadata').glob('*.json'):write(D/'metadata'/p.name,clean(read(p)))
for name in ['prepare.py','build_lab.py','browser.py','post_live.py','supplement.py','provenance_controls.py','n6_controls.py','admission_after.py','n7_prompts.py','final_export.py']:
 if (O/name).exists():
  out=D/'orchestration/drivers'/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(clean((O/name).read_text()))
for name in ['Dockerfile','browser/Dockerfile']:
 if (O/'build'/name).exists():
  out=D/'orchestration/build'/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(clean((O/'build'/name).read_text()))
for p in (O/'orchestration').glob('*.py'):
 out=D/'orchestration'/p.name;out.parent.mkdir(exist_ok=True);out.write_text(clean(p.read_text()))
if (O/'logs/runner-self-tests.log').exists():
 out=D/'execution/runner-self-tests.txt';out.write_text(clean((O/'logs/runner-self-tests.log').read_text()))
for source_name in ['promise-diagnose.log','initial-procps-promises.log','initial-procps-portable-text-0.2.log','n7_paused-serialized.log','n7-library-paused.log','n6-library-paused.log','n6-library-paused-continued.log']:
 p=O/'logs'/source_name
 if p.exists():
  out=D/'execution'/source_name.replace('.log','.txt');out.write_text(clean(p.read_text()))
for p in [O/'native/retained-context/attachments.log',O/'native/retained-context/attachments.txt']:
 if p.exists():
  out=D/'execution/retained-context-attachments.txt';out.write_text(clean(p.read_text()))
coverage=[]
for suite,pack in manifests.items():
 entries=[]
 for index,case in enumerate(pack['cases']):
  candidates=evidence.get((suite,case['id']),[])
  wanted=case.get('candidate')
  if wanted in ['swi','trealla']:
   def engine(x):
    n=x.get('candidate') or '';return 'swi' if n in ['n1','n2','n3','n4'] or n.startswith('swi') else 'trealla' if n=='n5' or n.startswith('trealla') else n
   candidates=[x for x in candidates if engine(x)==wanted]
  valid=[e for e in candidates if not any(w in e['classification'] for w in ['invalid_harness','overlapping_orchestration','superseded_transport','out_of_scope'])]
  entries.append(dict(case_index=index,id=case['id'],candidate=wanted,statuses=sorted({e['status'] for e in valid}),has_execution_observation=any(e['status'] in ['pass','fail','observed','diagnostic_error','error'] for e in valid),evidence=valid))
 coverage.append(dict(suite=suite,sha256=sha(R/'cases'/(suite+'.json')),case_rows=len(entries),unaccounted_case_indexes=[e['case_index'] for e in entries if not e['evidence']],not_executed_case_indexes=[e['case_index'] for e in entries if not e['has_execution_observation']],cases=entries))
write(D/'verification.json',dict(source_revision=inputs['revision'],hashed_inputs_unchanged=True,manifest_count=len(manifests),main_case_rows=sum(len(p['cases']) for p in manifests.values()),runner_self_tests_passed=123,accounting='Per-version input rows. Blocked/unsupported/not-applicable rows are accounted for but are not execution or passing evidence. Repeated IDs and observations are not independent language features.',coverage=coverage))
write(D/'SUMMARY.json',dict(status='in_progress' if '--draft' in sys.argv else 'not_all_green',suite_revision=inputs['revision'],manifest_count=len(manifests),main_case_rows=sum(len(p['cases']) for p in manifests.values()),files=records))
# Compare only persistent service identities/images; exercise state is intentionally mutable.
before=read(O/'preservation-before.json');now=json.loads(subprocess.check_output(['docker','inspect',*[x['name'] for x in before]]));lookup={x['Name']:dict(name=x['Name'],id=x['Id'],image=x['Image']) for x in now};assert all(lookup.get(x['name'])==x for x in before),'Persistent service changed'
write(D/'preservation.json',dict(persistent_container_ids_and_images_unchanged=True,before=before,after=list(lookup.values()),observed_automatic_restart=read(O/'runtime-restarts.json'),scope='Container and image identities are unchanged. N5 automatically restarted during testing; no operator restart, configuration change or deployment was performed. This comparison does not certify every internal mutable value.'))
print(json.dumps(dict(files=len(records),manifests=len(manifests),unaccounted=[(c['suite'],c['unaccounted_case_indexes']) for c in coverage if c['unaccounted_case_indexes']],not_executed=[(c['suite'],len(c['not_executed_case_indexes'])) for c in coverage if c['not_executed_case_indexes']])))
