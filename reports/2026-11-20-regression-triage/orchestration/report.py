from pathlib import Path
import json,hashlib,subprocess,shutil,collections,re,datetime
P=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-conformance');S=Path('/Users/lager/swi-prolog-node');D=R/'reports/2026-11-20-regression-triage'
assert (P/'n6.complete').exists() and (P/'swi-raw.complete').exists() and (P/'swi-fixed.complete').exists();assert not D.exists()
inputs=json.loads((P/'inputs.json').read_text());assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in inputs['files'].items())
before=json.loads((P/'preservation-before.json').read_text());now=json.loads(subprocess.check_output(['docker','inspect',*[r['name'] for r in before]]));lookup={d['Name']:(d['Id'],d['Image']) for d in now};assert all(lookup[d['name']]==(d['id'],d['image']) for d in before)
source_commit=subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip();assert not subprocess.check_output(['git','-C',str(S),'status','--porcelain'],text=True).strip()
actor_hash=hashlib.sha256((S/'prolog/web_prolog/actors.pl').read_bytes()).hexdigest();candidate=json.loads((P/'swi/fixed/candidate.json').read_text());assert candidate['actor_file_sha256']==actor_hash
n6=json.loads((P/'n6/results.json').read_text());assert len([r for r in n6['results'] if r['trial']==1])==56;fixed=json.loads((P/'swi/fixed/results.json').read_text());assert fixed['completed']==1000
assert n6['counts']=={'pass':56} and fixed['counts']=={'pass':1000}
D.mkdir()
def clean(x):
 if isinstance(x,dict):return {k:('[REDACTED]' if re.search(r'(^|[-_])(authorization|cookie|password|secret|credentials?)([-_]|$)',k,re.I) or k=='principal_id' else clean(v)) for k,v in x.items()}
 if isinstance(x,list):return [clean(v) for v in x]
 if isinstance(x,str):return re.sub(r'(?i)(Bearer\s+)[A-Za-z0-9_.~-]+',r'\1[REDACTED]',x)
 return x
for folder in ['n6','swi']:
 for f in (P/folder).rglob('*.json'):
  dest=D/f.relative_to(P);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(clean(json.loads(f.read_text())),indent=2)+'\n')
for f in (P/'n6').rglob('*.log'):
 dest=D/f.relative_to(P).with_suffix('.txt');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(clean(f.read_text()).rstrip()+'\n')
for name in ['comparison.json','inputs.json','preservation-before.json']:(D/name).write_text(json.dumps(clean(json.loads((P/name).read_text())),indent=2)+'\n')
for name in ['prepare.py','n6_replay.py','nu_probe.py','swi_replay.py','retirement_probe.pl','fixed_replay.py','red_test.py','n6_capacity_probe.py','run_n6_capacity.py','report.py']:
 dest=D/'orchestration'/name;dest.parent.mkdir(exist_ok=True);dest.write_text(clean((P/name).read_text()).rstrip()+'\n')
for name in ['T0-fixed.log','native-fixed-all.log','retirement-regression-before.log','fixed-regression.log','swi-fixture-permission-attempt.log','n6-owned-capacity.log']:
 dest=D/'execution'/name.replace('.log','.txt');dest.parent.mkdir(exist_ok=True);dest.write_text(clean((P/'logs'/name).read_text()).rstrip()+'\n')
(D/'source').mkdir();shutil.copyfile(S/'tests/tiers/retirement_order_tests.pl',D/'source/retirement_order_tests.pl')
patch=subprocess.check_output(['git','-C',str(S),'show','--format=fuller','--no-ext-diff',source_commit],text=True);(D/'source/fix.patch').write_text(patch)
summary=dict(status='targeted_replays_completed_and_preexisting_race_fixed_in_candidate',completed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),matched_pass_to_fail_observations=124,capacity_refusals=121,library_paused_passes_in_full_run=66,supporting_capacity_replays=55,n6_target_replays=n6['counts'],n6_local_rpc_repetitions=[r['status'] for r in n6['results'] if r['id']=='LOCAL-001'],swi_previous=json.loads((P/'swi/previous/results.json').read_text())['counts'],swi_current=json.loads((P/'swi/current/results.json').read_text())['counts'],swi_fixed=fixed['counts'],source_fix_commit=source_commit,source_actor_file_sha256=actor_hash,native_tiers_passed=['LINT','TEXT','T0','T1_NATIVE','T2','T3_NATIVE','T4_NATIVE','T5'],native_test_processes_exit_code=0,native_tier_swipl_version=subprocess.check_output(['/usr/local/bin/swipl','--version'],text=True).strip(),production_container_ids_and_images_unchanged=True,fix_deployed=False,original_full_reports_unchanged=True,local_rpc_root_cause_proven=False)
(D/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
lines=['# Targeted regression triage — 20 November 2026','',
'**The N6 failures clear under correct resource preconditions. A pre-existing SWI actor-retirement race is reproduced and fixed in a tested source candidate.** The fix is committed and pushed; the live nodes still use the preceding runtime revision.','',
'[Comparison data](comparison.json) · [N6 replays](n6/results.json) · [source fix](source/fix.patch) · [summary](SUMMARY.json). The [full sweep](../2026-11-20-live-conformance/REPORT.md) and [preceding sweep](../2026-11-19-upgraded-live-conformance/REPORT.md) remain immutable.','',
'## Comparison method','',
'The comparison matches report path, case ID, candidate, route and peer in directly comparable files. It selects earlier passes that became failures; it excludes out-of-scope and superseded/invalid attempts. These are observation transitions, not124 distinct defects or language features. New extended N7 coverage is not classified as a regression without an earlier matching execution.','',
'| Matched transitions | Evidence and disposition |','|---|---|',
'|121 N6 query-capacity refusals|66 library cases already pass in paused controls in the full report; the remaining55 supporting cases all pass in this follow-up|',
'|2 SWI NU-003 failures, on N3/N4|One shared, pre-existing retirement race; reproduced in both source revisions and repaired in the candidate|',
'|1 N6 LOCAL-001 transport error|The original assertion passes on three consecutive replays after the initial expiry; the specific transport-error cause remains unproven|','',
'## N6 clean replay','',
'One sequential client waits303 seconds before starting. It runs54 finite supporting assertions, then LOCAL-001 three times. PE-017, whose first page deliberately retains a continuation, has a separate303-second quiet period before execution. A final303-second expiry and finite recovery check complete the run. No production quota, idle timeout or concurrency bound changes.','',
'All56 distinct target assertions pass. The two additional LOCAL-001 repetitions also pass:58 recorded observations in total. The four supporting groups that previously suffered cascading503s are ordinary timeout-option validation, introspection, successor and URI checks; their failures did not establish broken language assertions because admission refused execution.','',
'The earlier full sweep allowed retained queries from preceding API tests to consume N6 slots, then continued other cases and began its library phase after only61 seconds. N6 retains idle queries for300 seconds. This was a scheduling error in the test orchestration. Future runs must apply the retention-expiry precondition at relevant case/group boundaries, or use disposable fixtures for continuation-owning tests; pacing only by requests/minute is insufficient.','',
'LOCAL-001 returning a generic transport error is consistent with a refused nested localhost request, but this follow-up does not prove that mechanism. An additional uncontained-controller diagnostic could not establish a passing clean baseline. Its loopback/auth environment differs from the public presenter/broker. Those [unqualified diagnostics](n6/owned-capacity/results.json) are retained and excluded from causal conclusions and passing case counts.','',
'## SWI NU-003 reproduction and fix','',
'The old/current images use identical SWI11.0.0 engine inventories. Their actor implementation is unchanged between nativea2ff186 and e25b230. The original NU-003 case and helper source are unchanged. Fixtures have the same generous admission budgets and resource bounds so this comparison does not measure public quotas.','',
'| Runtime source | Original NU-003,1,000 repetitions |','|---|---|',
'| Previous a2ff186 | 997 pass, 3 cleanup failures |',
'| Current e25b230 | 998 pass, 2 cleanup failures |',
'| Fixed candidate '+source_commit[:7]+' | 1,000 pass, 0 failures |','',
'The small difference between3 and2 failures is not evidence of a changed failure rate. Both reproduce the same old bug. A controlled delivery barrier establishes the mechanism deterministically: through the existing send hook, deliver down/3, pause the sender, and inspect actors/1 from the observer. Both unmodified revisions still list the terminated actor; the fixed candidate does not.','',
'Previously stop/2 sent monitor notifications before retracting PID/thread mappings. The receiver could run actors/1 inside that window. The fix retracts those mappings before delivery, under the existing lifecycle/registry locks; it preserves monitor withdrawal synchronization and computes the exit reason before retirement. No sleeps or relaxed assertions are added to runtime behavior.','',
'The new deterministic [regression test](source/retirement_order_tests.pl) fails on both unchanged images and passes with the fix. It is part of T0. All eight native tiers pass on local SWI-Prolog 11.0.0: LINT, TEXT, T0, T1_NATIVE, T2, T3_NATIVE, T4_NATIVE and T5. This includes monitor/postmortem, supervision, remote interoperation and HTTP ownership checks. The fixed runtime also passes the original case1,000 times with unchanged engine bytes.','',
'Published source: ['+source_commit[:7]+'](https://github.com/torbjornlager/swi-prolog-node/commit/'+source_commit+'). The candidate was tested as an explicit overlay on the current image; its actor-file hash matches the committed source. Consumer dependency pins and live images have not yet selected this fix.','',
'## What remains','',
'This follow-up accounts for 121 capacity refusals, repairs one old race, and leaves the cause of one transport error open. It does not repair the existing retained-context, Trealla SR-015, browser B-SV-006 or other supporting findings in the full report. The source fix needs the normal consumer qualification and deployment before the live SWI nodes benefit. The cause of the one transient N6 localhost transport error remains an open attribution question despite three passing replays.','',
'Production service identities/images match their before snapshot. Owned probe containers are removed. JSON evidence, operator source, setup-attempt logs and native validation logs are retained; exported artifacts are covered by [SHA-256 hashes](files-sha256.json).','']
text='\n'.join(lines).rstrip()+'\n'
for a,b in [('not124','not 124'),('|121','| 121'),('|2 SWI','| 2 SWI'),('|1 N6','| 1 N6'),('remaining55','remaining 55'),('waits303','waits 303'),('runs54','runs 54'),('separate303','separate 303'),('final303','final 303'),('All56','All 56'),('pass:58','pass: 58'),('cascading503','cascading 503'),('only61','only 61'),('for300','for 300'),('SWI11','SWI 11'),('nativea2','native a2'),('NU-003,1,000','NU-003, 1,000'),('between3 and2','between 3 and 2'),('case1,000','case 1,000')]:text=text.replace(a,b)
(D/'REPORT.md').write_text(text)
hashes={str(f.relative_to(D)):hashlib.sha256(f.read_bytes()).hexdigest() for f in D.rglob('*') if f.is_file()};(D/'files-sha256.json').write_text(json.dumps(hashes,indent=2)+'\n');print('Exported',len(hashes),'follow-up artifacts;source',source_commit)
