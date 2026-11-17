from pathlib import Path
import json,hashlib,subprocess,datetime,shutil
O=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-demonstrator')
ci=json.loads((O/'pinned-ci/results.json').read_text());assert len(ci)==34 and all(x['exit_code']==0 for x in ci)
qualification=json.loads((O/'browser-release-suite/results.json').read_text());assert all(x['exit_code']==0 for x in qualification['runs'])
rollout=json.loads((O/'rollout-results.json').read_text());assert len(rollout)==12 and all(x['status']=='deployed' for x in rollout)
reports={name:json.loads((O/(name+'.json')).read_text()) for name in ['public-verification','public-capabilities','public-browser']}
assert reports['public-verification']['counts']=={'pass':60,'fail':0}
assert reports['public-capabilities']['counts']=={'pass':30,'fail':0}
assert reports['public-browser']['counts']=={'pass':42,'fail':0}
for p in list(O.rglob('*.log')):shutil.copyfile(p,p.with_suffix('.txt'))
for p in list(O.rglob('__pycache__')):shutil.rmtree(p)
manifest=Path('/tmp/promise-release-browser-20261105/manifest.json');shutil.copyfile(manifest,O/'browser-package-manifest.json')
repositories=['swi-prolog-node','trealla-port','gprolog-port','swi-wasm-node','trinity-demonstrator','trinity-conformance']
commits={name:subprocess.check_output(['git','-C','/Users/lager/'+name,'rev-parse','HEAD'],text=True).strip() for name in repositories}
pins={p.stem:json.loads(p.read_text()) for p in (R/'dependencies').glob('*.json') if p.stem in ['swi-prolog-node','swi-wasm-node','trealla-port','gprolog-port']}
record=dict(recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='public promotion of portable runtime capabilities and context-wide browser promises; not full Appendix B certification',status='deployed',deployed_consumer_commit=(O/'consumer-revision.txt').read_text().strip(),pins=pins,source_commits=commits,consumer_ci_groups=34,consumer_wasm_scenarios=json.loads((O/'consumer-scenarios.json').read_text())['count'],clean_browser_qualification_groups=len(qualification['runs']),public_counts={name:d['counts'] for name,d in reports.items()},selected_public_assertions_pass=132,selected_public_assertions_fail=0,runtime_services_updated=12,preserved=['per-service environment fingerprints','runtime users','resource and security controls','persistent mounts','existing admission services'],rollback='Twelve previous image tags retained in rollback-images.json',diagnostics='An initial candidate N6 harness used the wrong working directory; corrected harness passes. Original failure is retained separately. The first live browser harness targeted the optional minimal-host download route; the corrected run uses the supported public demonstrator page and preserves the initial diagnostics.')
record['evidence_sha256']={p.relative_to(O).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(O.rglob('*')) if p.is_file() and p.name not in ['verification.json','README.md'] and p.suffix!='.log'}
(O/'verification.json').write_text(json.dumps(record,indent=2)+'\n')
print('PASS release evidence: 132 live assertions; 34 consumer groups; 12 services')

(O/'README.md').write_text("""# Public promise and capability release — 5 November 2026

**Committed, pushed and deployed to N0–N6.** Twelve runtime/asset services use
images built from clean consumer commit `"""+record['deployed_consumer_commit']+"""`.
The four runtime dependencies are exact commits; the browser package is clean
and its native schema provenance matches the consumer pin.

- All **34 consumer CI groups** pass, including **109 runtime/consumer scenarios**.
- The clean browser package passes all six qualification groups, including
  **102 semantic scenarios**, **59 ownership checks** in real Chrome/HTTP and
  **81 existing browser session checks**.
- All **132 selected live assertions** pass: 60 readiness/asset/RPC/transport
  checks, 30 shared runtime capability checks on N1–N6, and 42 browser checks
  loading the deployed assets from every N0–N6 hostname in both execution modes.
- The live browser checks use real N1 HTTPS calls. Same-context children collect
  parent promises; another browser context cannot collect or dispose of them;
  the owning context still collects after the foreign cleanup attempt.
- A disposable N6 passes its public contract, 59 HTTP-field assertions, actual
  contained worker/broker transport checks, and Linux containment controls.

Every replaced service preserves its environment fingerprint, runtime user,
resource/security controls and persistent mounts. Admission proxies and operator
credentials retain their existing configuration. Twelve rollback tags remain
available in `rollback-images.json`. Candidate containers were removed.

An initial N6 test harness ran from the wrong working directory. The corrected
candidate run passes; the original harness failure remains in `diagnostics`. The
initial live browser harness targeted the optional minimal-host download route.
The corrected run uses the supported public demonstrator page; its initial
diagnostics are also retained.

[verification.json](verification.json) records exact pins, source commits,
qualification scopes and evidence hashes. [rollout-results.json](rollout-results.json)
records image identities; [public-browser.json](public-browser.json) records the
live browser assertions. This release does not certify all Appendix B clauses.
""")
