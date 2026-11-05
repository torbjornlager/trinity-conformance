from pathlib import Path
import json,hashlib,subprocess,datetime
O=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-demonstrator')
def read(f):return json.loads((O/f).read_text())
ci=read('pinned-ci/results.json');assert len(ci)==36 and all(r['exit_code']==0 for r in ci)
assert len(read('build-results.json'))==6 and all(r['exit_code']==0 for r in read('build-results.json'))
assert len(read('rollout-results.json'))==12 and all(r['status']=='deployed' for r in read('rollout-results.json'))
assert len(read('running-runtime-pins.json'))==12
assert read('native.json')['counts']=={'pass':560,'fail':0}
assert read('browser.json')['counts']=={'pass':226,'fail':0}
assert len(read('browser-suite.json')['runs'])==7 and all(r['exit_code']==0 for r in read('browser-suite.json')['runs'])
counts={}
for file,expected in [('public-verification.json',60),('public-localhost.json',34),('public-browser.json',42),('public-library.json',672),('public-library-browser.json',1568)]:
 data=read(file);assert data['counts']=={'pass':expected,'fail':0},file;counts[file]=data['counts']
ping=read('public-pingpong.json');assert len(ping['results'])==3 and all(r['status']=='pass' for r in ping['results']);counts['public-pingpong.json']={'pass':3,'fail':0}
assert read('candidate-n5-library.json')['counts']=={'pass':238,'fail':0}
assert (O/'trealla-final-unit.txt').read_text().rstrip().endswith('ALL unit TESTS PASSED')
assert 'PASS N5 candidate' in (O/'candidate-n5-driver.txt').read_text()
assert 'PASS N6 candidate' in (O/'candidate-n6-driver.txt').read_text()
assert 'PASS native containment' in (O/'candidate-n6-containment.txt').read_text()
assert (O/'trealla-upstream.txt').read_text().rstrip().endswith('ALL all TESTS PASSED')
manifest_hash=hashlib.sha256((O/'manifest.json').read_bytes()).hexdigest()
for f in ['native.json','browser.json','public-library.json','public-library-browser.json']:assert read(f)['manifest_sha256']==manifest_hash
pins={n:json.loads((R/'dependencies'/f'{n}.json').read_text()) for n in ['swi-prolog-node','swi-wasm-node','trealla-port','gprolog-port']}
rev=(O/'consumer-revision.txt').read_text().strip()
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
changed=subprocess.check_output(['git','diff','--name-only',rev,head],cwd=R,text=True).splitlines()
assert set(changed)<= {'DEVIATIONS.md','Deployment/README.md'}
(O/'README.md').write_text(f'''# Standard-library release — 5 November 2026

**Committed, pushed and deployed to N0–N6.** All twelve runtime and asset services
run clean images built from consumer commit `{rev}`.

Appendix B's required library forms and callback semantics now work consistently
across native SWI, Trealla, GNU and both browser modes. Missing higher `maplist`
forms and `countall` are supplied automatically; GNU also supplies the required
`memberchk` and `forall`. Trealla retains private callback scope, cut scope and
remote source export while applying the current sandbox policy.

Library callbacks validate when invoked: uninstantiated values raise
`instantiation_error`; invalid values raise `type_error(callable, Value)` with
the original culprit. Empty iteration and vacuous `forall` tests do not invoke
unused callbacks. Application exceptions propagate unchanged. ISO `call/N`
retains its existing runtime-specific error refinement; its shared control checks
only the accepted category and culprit, while library cases require exact callable errors.

- **112 shared cases** cover every required predicate and arity, positional
  callback arguments, relational modes, binding isolation, cuts, exceptions,
  lazy callbacks and exact callable errors.
- **786/786 committed-source observations** pass: 560 checks in five runtime
  modes, 224 retained-session checks and two browser child controls.
- Native SWI and GNU full regression suites pass. Trealla passed **89 unit and 71 interoperability groups** before the nested
  follow-up; the final repair reruns all 89 unit groups and adds **239 library
  and sandbox controls**. The Linux N5 candidate passes **238 individual, nested
  and batch controls**. The clean browser package passes **seven groups**.
- All **36 pinned consumer CI groups** pass. The clean N6 image passes its public
  contract, 59 HTTP-field assertions, worker/broker checks and Linux containment.
- **2,379/2,379 public checks** pass: 672 shared assertions on N1–N6, 1,568 in
  real Chrome on N0–N6 across both modes, and 139 previous transport, localhost,
  ownership, asset and N5–N4 ping-pong regressions.

All services retain their environment fingerprint, runtime user, resource and
security controls, and persistent mounts. Existing admission configuration is
retained. Exact running pins were checked in all twelve services. Rollback images
are recorded in [rollback-images.json](rollback-images.json).

An initial public probe exposed premature `forall/2` test validation on N5
inside nested meta-calls. The final pinned repair guards both callbacks at
invocation and retains public source export. The failed probe and initial
deployment evidence remain in [initial-attempt](initial-attempt/); the final
release repeats image builds, pinned consumer CI, candidate gates and live checks.

The source-unit ledger remains at 11 verified units per runtime: this repair
strengthens the four required-library units rather than certifying the full ISO
mode/error inventory. Native retained-context propagation remains a separate audit.
The [earlier development report](../2026-11-05-standard-library/README.md) retains
the original 57-case baseline and subsequent 65-case qualification; its manifests
are historical and have not been replaced by the 112-case release selection.

[verification.json](verification.json) records pins, counts and evidence hashes.
''')
artifacts={str(p.relative_to(O)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(O.rglob('*')) if p.is_file() and p.name!='verification.json'}
record=dict(recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='deployed',scope='Required Appendix B library forms, selected callback formal errors and public regression checks; not full ISO certification',deployed_consumer_commit=rev,consumer_documentation_commit=head,pins=pins,local_observations=786,consumer_ci_groups=36,public_counts=counts,selected_public_checks_pass=2379,selected_public_checks_fail=0,runtime_services_updated=12,artifacts_sha256=artifacts)
(O/'verification.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS release evidence: 786 committed-source observations, 36 CI groups, 2379 live checks, 12 services')
