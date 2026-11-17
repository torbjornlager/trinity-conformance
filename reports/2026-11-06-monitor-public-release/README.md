# Public runtime rollout — 6 November 2026

**Deployed to N0–N6.** All twelve runtime/asset services run images from consumer
commit `745d5a53b4f87a730ba9d378be675974ca763335`. All are running and ready. Their
environment fingerprints, users, entrypoints, commands, resource/security
controls and persistent mount identities match the pre-rollout snapshot.
Admission proxies and credentials retain their configuration; rollback images
remain available. The consumer documentation follow-up does not change the image
source revision.

[Verification](verification.json), [rollout](rollout-results.json),
[rollback inventory](rollback-images.json) and [installed pins](running-runtime-pins.json)
record the exact state. Runtime pins are native SWI `cfaec8c`, Trealla `677be65`,
GNU `dfea5e1`, and browser `3905d63`. Engine pins are unchanged. Browser schema
provenance now matches the native pin; [equivalence](schema-check.txt) confirms
unchanged shared schema/runtime bytes. The first schema check selected the
unpackaged source directory, which lacks assembled WASM inputs; that diagnostic
is retained. The corrected check uses the actual clean package.

The rollout includes the accumulated library, context-ownership and monitor
repairs qualified in the development reports. All 49 shared monitor cases pass
on each public ACTOR node, N3/N4/N5: **147 observations**. The stale consumer
browser assertion now distinguishes an explicit monitor on a dead actor
(`no_process`) from its spawn monitor (actual recorded completion).

## Qualification

- All **38 consumer CI groups** are qualified. The initial invocation passed 37;
  WASM exposed the stale consumer assertion. After changing only that test file,
  the complete WASM group passed. [Qualification provenance](consumer-ci/qualification.json)
  records both consumer revisions and the single changed file. This is not
  described as one all-passing invocation. Original [CI results](consumer-ci-initial/results.json)
  and the corrected [results](consumer-ci/results.json) remain.
- Final committed-source Linux images pass **98 monitor assertions**: all 49
  shared cases on SWI and Trealla, with a fresh ACTOR session per case.
  [Results](linux-monitors.json) and [driver](linux-monitor-driver.txt) identify
  the observations. An initial harness waited only for Docker's TCP proxy;
  its failed upgrades did not reach a ready Prolog server. The corrected harness
  waits for `/healthz`; production admission settings were not changed.
- The final contained GNU image passes its public contract, **59 HTTP-field
  controls**, five localhost controls, real worker/broker/TLS checks, and
  [native containment](candidate-n6-containment.txt).
  [Candidate driver](candidate-n6-driver.txt) records the successful isolated
  probe. A preceding unchanged-image probe returned an outbound
  `http_transport_error`; it remains in
  [the diagnostic](candidate-final-first-attempt/candidate-n6-driver.txt).
  No production timeout or egress policy was changed, and no transport fix is
  claimed from that rerun. Candidate checks were repeated on the final images;
  an unavailable untagged initial image was not treated as an equivalence proof.

## Public observations

**302 selected observations pass; one additional context observation fails with
a transport error.** Counts from separate Linux/development suites are not added
to this public total.

| Selection | Pass | Fail |
|---|---:|---:|
| [Shared monitor contract on N3/N4/N5](public-monitors.json) | 147 | 0 |
| [Readiness, exact browser bytes and cross-node RPC/promise smoke](public-verification.json) | 60 | 0 |
| [Real Chrome on all seven hosts, both modes](public-browser.json) | 42 | 0 |
| [Retained contexts, all four directed native routes and returns](public-contexts/results.json) | 50 | 1 |
| [N5–N4 tutorial and inline ping-pong](public-pingpong.json) | 3 | 0 |

The remaining failure is `CTX-015-trealla-b`: an N5 self-route promise owner
receives an HTTP 502 from its underlying RPC, rather than the expected successful
`mark` answer. The original two-second collection timeout is preserved in the
[short-wait run](public-contexts-short-wait-diagnostic/results.json). An explicit
bounded retry of the same reference in the revised probe reveals the transport
error; the [admission proxy diagnostic](n5-self-route-proxy-errors.txt) reports
an upstream connection closing before response headers. This is an open
transport follow-up. The failed observation is not waived, relabelled as a pass,
or claimed fixed. The owner received a completed error answer; the expected
successful end-to-end answer has not been established for this case.

The first public monitor harness mistakenly used `/call`, whose effective
profile is ISOBASE. Its [profile denials](public-monitors-http-profile-diagnostic.json)
are diagnostic, not ACTOR conformance evidence. The final monitor selection uses
WSS with temporary execute-only credentials. The first context attempt then
lacked its policy-graph input; [that fixture diagnostic](public-contexts-fixture-diagnostic/results.json)
is also preserved. The graph was read from the deployed configuration and
[verified unchanged](public-spawn-policy.json) against the earlier recorded
reference. No new source/spawn permission was introduced.

All **nine temporary credentials were revoked**, including failure paths:
[monitor phase](monitor-ephemeral-credential-cleanup.json),
[short-wait context phase](short-wait-ephemeral-credential-cleanup.json), and
[final context phase](ephemeral-credential-cleanup.json).
The existing N5 peer credential remains active, scoped, owner-only (UID 10001,
mode 0400), and mounted read-only; [verification](n5-peer-configuration-verification.json)
confirms it survived the restart. Its value is not stored in this report.

The context failure prevents an all-passing retained-context release certificate.
The new monitor checks and normal public smoke checks pass, and all services
remain ready. This report does not claim full Appendix B or external ISO
conformance. Temporary consumer CI shared-database fixtures are gzip-compressed to preserve
their exact source bytes. Text logs have trailing whitespace normalised; original JSON
observations and source/package hashes are retained.
