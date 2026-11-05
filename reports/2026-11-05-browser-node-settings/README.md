# Browser execution-host node settings

Both browser execution modes now export `node_setting/2`. The exact relation is
`profile-actor` and `sandbox-off`: these hosts expose the ACTOR API without
Prolog goal filtering. Browser/WASM confinement and remote-node access policies
are separate. The implementation reports no invented serving URI, authentication
mode, HTTP timeout or admission ceiling. All fourteen other documented public
keys are unavailable and fail, as do unknown and private keys.

The [clean pre-repair baseline](baseline.json), browser source
`deb11db4ff58c27b4565f7125d29b0deec6627f7`, fails all twenty shared observations
(ten cases in each mode). The [first development run](host-first.json) passes all
36 observations. The [clean committed package run](final.json) repeats those
36 checks: ten shared cases plus eight browser-host cases per mode, in real
Chrome through the public session API.

Host cases cover the exact relation, private source helpers, source-loaded child
actors, copied private helpers, nested retained sessions, receive guards and
bodies, unavailable HTTP keys, reverse lookup and bound-value mismatches. The
shared manifest is byte-identical to `cases/node-settings-0.1.json`. Tests are
maintained in the browser runtime package and included in `tools/test.py`.

The [packaged regression results](regressions/results.json) record all ten selected
runtime groups passing. Native and consumer integration were not selected. The
[qualification metadata](verification.json) records package provenance and
checks that the tested development package and committed package have identical
runtime and test bytes; only README/runtime documentation changed between them.
Engine and schema dependency pins are unchanged. The conformance runner also
passes its 104 unit tests; see [runner log](runner-tests.log).

B-339–B-346 now have scoped source evidence in all five targets. This is browser
execution-host qualification, not certification of a public HTTP deployment or
of every obligation in Appendix B. Public nodes and demonstrator dependency pins
were not changed.
