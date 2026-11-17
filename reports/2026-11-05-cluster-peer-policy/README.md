# Cluster peer-policy release — 5 November 2026

The requested N3–N5 policy changes are committed, pushed and deployed. All twelve
runtime/asset services run images built from consumer
`1581acc2c1ad0680c276feac19210220335b6226`. Native SWI `c826111`, Trealla `62e93c3`
and browser `f5fbafb` pins are unchanged from the preceding release.

N3 and N4 now allow source loading and remote spawning at N5. N5 now allows N3.
The [live graph](public-spawn-policy.json), compared with the
[previous graph](public-spawn-policy-before.json), has exactly these three additions.
External destinations remain denied. Existing users, limits, admission settings,
state/log volumes and peer credential mounts are preserved. N5's persistent
self-route credential remains active, owner-only (0400, UID 10001) and mounted
read-only. Existing private-Docker peer transport remains configured.

## Verification

- **51/51 public retained-context cases pass, with no exclusions**, on all four
  directed routes and their return paths: N3→N4, N3→N5, N5→N4 and N5→N5.
  [Final observations](public-contexts/results.json) and the
  [first run](public-contexts-first-run/results.json) both pass all 51 cases.
- **6/6 external-origin controls pass**: spawn and source loading are rejected
  on N3, N4 and N5, and each retained session remains usable afterward.
  [Results](public-policy-denials.json).
- **60/60 public smoke checks pass**: readiness, exact browser bytes, cross-node RPC and promise controls
  are recorded in [public verification](public-verification.json).
- Four focused native policy tests, three Compose checks and the deployed
  Trealla policy guard pass. They cover allowed peers and external denials.
- **38/38 consumer CI groups qualify**, with the rerun qualification below.
  [Qualified groups](consumer-ci/results.json).

Six clean images were built from the committed archive; [rollout](rollout-results.json)
records twelve updates. [Installed pins](running-runtime-pins.json),
[rollback images](rollback-images.json) and the guarded rollout driver are retained.
All temporary execute-only verification credentials were revoked; their cleanup
records contain token IDs only. No bearer or administrator secrets are retained.

## Retained failures and limits

An intermediate unchanged public run passed 50 cases and timed out in
`CTX-015-trealla-b` (N5 self-route owner collection after a foreign attempt).
It returned `Outcome=timeout` after the collector's two-second wait, rather than
a promise ownership error. The [observation](public-contexts-repeat-timeout/results.json)
is retained. Both surrounding complete runs passed without changing runtime,
policy, test logic or deadlines. The cause remains undiagnosed; passing reruns
do not establish absence of intermittent timing problems.

The initial consumer CI run passed 37 groups and failed the browser worker
interruption cleanup scenario. Three focused replays and the complete WASM group
rerun passed on unchanged sources and pins. The qualified record combines the
37 original passing groups with that complete rerun. The original failure remains
in [initial CI](consumer-ci-initial/results.json); [qualification notes](ci-rerun-note.json)
do not claim a browser fix.

The first external-source negative fixture incorrectly supplied `src_uri` to
`toplevel_call` on SWI. Its option-domain errors are preserved in
[invalid fixture results](public-policy-denials-invalid-fixture.json). The corrected
fixture calls `rpc(localhost,true,[src_uri(...)])`, reaching source-policy validation
on all three nodes; all six corrected controls pass. An initial smoke wrapper also
referenced the wrong rollout log filename; the corrected wrapper ran the checks.

These are selected observations, not full Appendix B certification. Broader
library/browser suites from the [previous release](../2026-11-05-native-context-release/README.md)
were not rerun for this policy-only change, and their counts are not added here.
The shared collector script retains its historical localhost-only module docstring;
its actual public URLs, scope, routes and executed byte hash are in each report.
Whole-unit conformance statuses remain unchanged pending complete obligation mapping.
