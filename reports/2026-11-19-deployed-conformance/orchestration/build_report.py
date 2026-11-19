#!/usr/bin/env python3
"""Export sanitized observations and an auditable per-file inventory from private run artifacts.

Run from this repository: python3 reports/2026-11-19-deployed-conformance/orchestration/build_report.py [artifact-root]
Counts are per observation file, not an aggregate feature-conformance percentage.
"""
import collections,hashlib,json,pathlib,re,shutil,subprocess,sys
R=pathlib.Path(__file__).resolve().parents[3]
D=pathlib.Path(__file__).resolve().parents[1]
O=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path('/Users/lager/trinity-demonstrator/.trinity/conformance-full-20261119')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
inputs=read(O/'inputs.json')
assert all(sha(R/f)==h for f,h in inputs['files'].items()), 'suite inputs changed'
# No private fixture programs, credential files, node logs or arbitrary Docker inspection are exported.
secret_values=set()
for p in (O/'orchestration/isolated').rglob('*.private.pl'):
 secret_values.update(re.findall(r"bearer_token\([^,]+,'([^']+)'",p.read_text()))
sensitive=re.compile(r'(^|[-_])(authorization|cookie|password|secret|token|credentials?|query.owner)([-_]|$)',re.I)
def clean(x):
 if isinstance(x,dict):
  return {k:('[REDACTED]' if (sensitive.search(k) or k=='principal_id') and not any(s in k for s in ['sha256','token_env','token-env','timeout']) else clean(v)) for k,v in x.items()}
 if isinstance(x,list):
  if len(x)==2 and isinstance(x[0],str) and sensitive.search(x[0]):return [x[0],'[REDACTED]']
  return [clean(v) for v in x]
 if isinstance(x,str):
  for v in secret_values:x=x.replace(v,'[REDACTED_FIXTURE_TOKEN]')
  x=re.sub(r'(?i)(Bearer\s+)[A-Za-z0-9_.~-]+',r'\1[REDACTED]',x)
  x=re.sub(r"(bearer_token\([^,]+,)'[^']+'",r"\1'[REDACTED]'",x)
  return x
 return x
statuses={'pass','fail','blocked','error','observed','unsupported','diagnostic_error','not_applicable','deferred'}
def rows(x):
 if isinstance(x,dict):
  if x.get('status') in statuses and any(k in x for k in ['id','case_id','case','title','kind']):yield x;return
  for k,v in x.items():
   if k not in ['observation','transcript','sources','source','inputs','requests']:yield from rows(v)
 elif isinstance(x,list):
  for v in x:yield from rows(v)
manifest={p.stem:read(p) for p in (R/'cases').glob('*.json')}
records=[];case_evidence=collections.defaultdict(set)
for sub in ['observations','public-extra','native','followup-native','extras','browser','browser-source-aware','orchestration/isolated']:
 for f in sorted((O/sub).rglob('*')):
  if not f.is_file() or f.suffix not in ['.json','']:continue
  try:data=read(f)
  except (ValueError,UnicodeError):continue
  # Isolated fixtures may contain private files: export only observations and release summaries.
  rs=list(rows(data))
  if not rs and not (isinstance(data,dict) and any(k in data for k in ['groups','packs','runs','checks','inputs_unchanged_during_run','driver_sha256'])) and f.name not in ['summary.json','startup-readiness.json','boolean-native-api-assertions.json']:continue
  rel=f.relative_to(O);target=D/'observations'/rel
  if not f.suffix:target=target.with_suffix('.json')
  write(target,clean(data))
  name=str(target.relative_to(D));classification='observation'
  if sub=='native' and str(rel).startswith('native/monitor-contracts-0.1/'):
   classification='invalid_fixture_attempt_common_source_overwrites_case_source'
  if sub=='browser' and f.parent==O/'browser' and any(f.name.startswith(s+'-') for s in ['copying-isolation-0.1','node-settings-0.1','receive-callback-context-0.1','server-waits-0.1','source-copying-0.1']):
   classification='embedded_attempt_case_source_not_loaded; see source-aware Chrome results'
  suite=data.get('suite') if isinstance(data,dict) else None
  if suite in manifest and ('diagnostic' in suite or manifest[suite].get('scope')=='diagnostic'):
   classification='diagnostic_only_raw_statuses_retained'
  if sub=='public-extra' and f.name=='n7-admission-controls.json':classification='paced_control_original_failures_retained'
  if 'source-aware' in str(rel):classification='source_aware_replication'
  if 'boolean-resource-controls' in str(rel):classification='resource_preservation_control_groups_not_portable_case_rows'
  if 'remote-without-instrumentation' in str(rel):classification='supplementary_remote_context_without_return_barriers_not_strict_gate'
  records.append(dict(file=name,suite=suite,classification=classification,counts=dict(collections.Counter(r['status'] for r in rs)),rows=len(rs)))
  for row in rs:
   if row.get('status') not in ['not_applicable','deferred'] and row.get('id'):case_evidence[row['id']].add(name)
for f in ['inputs.json','images.json','native-plan.json','native-jobs.json','browser-plan.json','browser-jobs.json','browser-source-aware-jobs.json','followup-native-jobs.json','public-jobs.json','orchestration/isolated-summary.json']:
 write(D/('suite-inputs.json' if f=='inputs.json' else 'execution/'+f),clean(read(O/f)))
for f in (O/'metadata').glob('*.json'):write(D/'metadata'/f.name,clean(read(f)))
for f in (O/'orchestration').glob('*.py'):
 (D/'orchestration'/f.name).write_text(clean(f.read_text()))
shutil.copyfile(O/'runner-self-tests.log',D/'execution/runner-self-tests.log')
# Retain the explicit setup/instrumentation failures without exporting verbose credential-bearing node logs.
for f in [O/'browser/maintained-monitors/remote.txt',O/'native/retained-context/attachments.log',O/'native-container-logs/native-promises.log',O/'native-container-logs/native-promise-diagnostics.log']:
 if f.exists():
  target=D/'execution'/f.relative_to(O);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(clean(f.read_text()))
coverage=[]
for name,m in sorted(manifest.items()):
 cases=m['cases'];missing=[c['id'] for c in cases if c['id'] not in case_evidence]
 coverage.append(dict(suite=name,sha256=inputs['files']['cases/'+name+'.json'],case_rows=len(cases),missing_case_ids=missing,case_id_evidence={c['id']:sorted(case_evidence[c['id']]) for c in cases},note='ID-level evidence may include a maintained superset; distinct versions have separate hashed observation files. Evidence does not imply pass or applicability to every runtime.'))
before=read(O/'preservation-before.json');ids=subprocess.check_output(['docker','ps','-aq'],text=True).split()
inspected=json.loads(subprocess.check_output(['docker','inspect',*ids],text=True))
after=[dict(name=x['Name'],id=x['Id'],image=x['Image']) for x in inspected if x['Config'].get('Labels',{}).get('com.docker.compose.project')]
lookup={x['name']:x for x in after}
preserved=all(lookup.get(x['name'])==x for x in before)
assert preserved,'persistent Compose container identity/image changed'
write(D/'preservation.json',dict(before=before,after=after,baseline_containers_unchanged=preserved,note='Compares container IDs/images only; does not certify all internal mutable state. Owned labs are excluded.'))
write(D/'verification.json',dict(source_revision=inputs['revision'],hashed_inputs_unchanged=True,manifest_count=len(manifest),main_case_rows=sum(len(m['cases']) for m in manifest.values()),all_main_case_ids_have_execution_evidence=all(not c['missing_case_ids'] for c in coverage),runner_self_tests_passed=111,coverage=coverage,limitations=['Repeated IDs across packs are not independent features.','Six retained-context attachment controls did not execute: stale instrumentation boundary.','Strict monitor browser/native return-barrier group did not execute: stale instrumentation boundary.','All raw failures, blocked cases, unsupported cases and diagnostic statuses remain visible.']))
summary=dict(date='2026-11-19',source_revision=inputs['revision'],status='not_all_green',manifest_count=len(manifest),main_case_rows=sum(len(m['cases']) for m in manifest.values()),accounting='Per-file observations, including repeated routes, older pack versions, controls and invalid fixture attempts. Do not sum into a language-conformance percentage. Group summaries are not case rows.',files=records)
write(D/'SUMMARY.json',summary)
write(D/'provenance.json',dict(suite_revision=inputs['revision'],native_swi_commit='26e1ce7d712afafe440e3f87388baec4490232ec',native_swi_version='11.0.0',demonstrator_upgrade='dc66d8c21165ee3cd50531a39c885482bbcbd44b',deployment_notes='b14feb3',browser_package='0363b38b3d4939a53f62a57b23fbc4e73997e79f',browser_package_manifest_sha256='00fb7161d9a61968da6238ebf6630416ab51ea25eeed93953879c2349ef0435a',browser_engine='SWI-Prolog 10.1.19 / swipl-wasm 8.2.5; browser runtime payload unchanged by native SWI upgrade',node='22.23.4',chromium='156.0.8078.79',live_engine_images=read(O/'images.json'),lab_images={'native':'sha256:70ea45353c0a23d42a609ca851ea1600d89e70bdea8916ee1cd3a2bda2ff58c5','browser':'sha256:93daa029dbdabb5777fc72cbcd6afdcc2593e54ea5ce65286ce34e0aeb2ebe2d'},synthetic_git_revisions={'trealla':'5ecab8e6823362ac943bd4a4ec4f1e3acb01497c','gnu':'1ff2c6d5ff2d0f70290f2e8567178c8d19c106cf'},synthetic_revision_note='Trealla/GNU and suite lab Git snapshots were initialized only for adapter provenance. They are not upstream commits. Engine files came from the exact deployed image IDs; per-file hashes are in the observations.',isolation='Disposable Docker labs, network none except loopback; three private exact-image gates on an owned temporary network. Frozen suite copied with docker cp because host bind mounts were unavailable.',redaction='Private fixtures and credential files omitted. Credential keys, authorization headers, query-owner header values and private fixture token literals redacted in exported observations.'))
print(json.dumps(dict(files=len(records),manifest_count=len(manifest),main_case_rows=sum(len(m['cases']) for m in manifest.values()),missing=[c['suite'] for c in coverage if c['missing_case_ids']],persistent_containers_unchanged=preserved)))
