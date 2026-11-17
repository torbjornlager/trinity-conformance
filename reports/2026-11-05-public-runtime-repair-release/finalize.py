from pathlib import Path
import json,hashlib,subprocess,datetime
O=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-demonstrator')
def read(f):return json.loads((O/f).read_text())
ci=read('pinned-ci/results.json');assert len(ci)==36 and all(r['exit_code']==0 for r in ci)
assert len(read('build-results.json'))==6 and all(r['exit_code']==0 for r in read('build-results.json'))
assert len(read('rollout-results.json'))==12
counts={}
for file,expected in [('public-verification.json',60),('public-localhost.json',34),('public-browser.json',42)]:
 data=read(file);assert data['counts']=={'pass':expected,'fail':0},file
 counts[file]=data['counts']
ping=read('public-pingpong.json');assert len(ping['results'])==3 and all(r['status']=='pass' for r in ping['results']);counts['public-pingpong.json']={'pass':3,'fail':0}
assert read('committed-localhost-native.json')['counts']=={'pass':21,'fail':0}
assert len(read('candidate-n6-localhost.json'))==5
assert 'PASS N6 candidate' in (O/'candidate-n6-driver.txt').read_text()
assert 'PASS native containment' in (O/'candidate-n6-containment.txt').read_text()
assert len(read('running-runtime-pins.json'))==12
pins={name:json.loads((R/'dependencies'/f'{name}.json').read_text()) for name in ['swi-prolog-node','swi-wasm-node','trealla-port','gprolog-port']}
rev=(O/'consumer-revision.txt').read_text().strip();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
changed=subprocess.check_output(['git','diff','--name-only',rev,head],cwd=R,text=True).splitlines();assert set(changed)<= {'DEVIATIONS.md','Deployment/README.md'}
report=f'''# Public runtime repair release — 5 November 2026

**Committed, pushed and deployed to N0–N6.** All twelve runtime/asset services
run clean images built from consumer commit `{rev}`. Later consumer changes
only update deployment documentation. The Trealla pin is
`{pins['trealla-port']['revision']}`; GNU is
`{pins['gprolog-port']['revision']}`. Native SWI and browser pins are unchanged.

The public N5–N4 ping-pong tutorial now completes, with all eight output messages
and normal actor completion. Inline remote output also passes with and without
loaded source. The private Trealla output helper stays out of exported code;
remote formatted SWI text renders normally.

`rpc(localhost, ...)` and `promise(localhost, ...)` now resolve the current node
on Trealla and contained GNU as well as native SWI. The exact reported N2-source
query returns six ancestor/descendant pairs on public N5 and N6. The GNU
controller and broker were deployed together with their matching lease protocol.

- All **36 pinned consumer CI groups** pass, including the runtime/consumer WASM
  scenarios and the new N6 broker/adapter regression groups.
- All **21 committed-source shared localhost assertions** pass on disposable
  SWI, Trealla and GNU listeners.
- The clean N6 image passes its public contract, **59 common HTTP-field checks**,
  five localhost cases, real worker/broker transport checks and Linux containment.
- All **139 selected public checks** pass: 60 readiness/asset/RPC checks,
  34 localhost RPC/promise/source checks, three N5–N4 output scenarios and
  42 real-Chrome ownership checks on all seven hosts in both execution modes.
- The upstream Trealla repair separately passed **88 unit groups and 71 interop
  groups**; its committed qualification includes output variable-sharing and
  supervisor admission controls.

Every updated service retains its environment fingerprint, runtime user,
resource/security controls and persistent mounts. Admission services and
operator credentials retain their existing configuration. Exact running pins
were checked in all twelve services. Rollback tags remain in
[rollback-images.json](rollback-images.json); disposable candidate containers
were removed.

[verification.json](verification.json) records exact revisions and evidence
hashes. [public-pingpong.json](public-pingpong.json) contains the observed tutorial
output; [public-localhost.json](public-localhost.json) records the retained local
node contract. These selected checks do not certify every Appendix B clause.
'''
(O/'README.md').write_text(report)
artifacts={str(p.relative_to(O)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(O.rglob('*')) if p.is_file() and p.name!='verification.json' and not any(part.startswith('browser-prolog-') for part in p.relative_to(O).parts)}
record=dict(recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='deployed',scope='Current-node RPC/promise resolution and portable remote formatted output; selected public regression checks',deployed_consumer_commit=rev,consumer_documentation_commit=head,pins=pins,consumer_ci_groups=36,committed_source_localhost_assertions=21,public_counts=counts,selected_public_checks_pass=139,selected_public_checks_fail=0,runtime_services_updated=12,preserved=['environment fingerprints','runtime users','resource/security controls','persistent mounts','admission services','operator credentials'],artifacts_sha256=artifacts)
(O/'verification.json').write_text(json.dumps(record,indent=2)+'\n')
print('PASS release evidence: 36 CI groups, 21 shared localhost assertions, 139 live checks, 12 services')
