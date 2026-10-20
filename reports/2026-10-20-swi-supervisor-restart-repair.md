# Native SWI supervisor restart-failure cleanup — 2026-10-20

The native supervisor now journals replacement attempts using the existing startup scope. Explicit respawn failure reclaims its provisional child and retains the inactive specification and existing siblings for retry. Automatic failure reclaims provisional replacements, then stops remaining recorded children in reverse start order under their shutdown policies and exits with `restart_failed(Id, Reason)`. The id denotes the actual failed replacement, including later children in group strategies.

Successful group restarts retain forward stopping order. Fresh private cleanup monitors handle already retired original pids without consuming application monitor notifications. Ordinary cleanup errors retain the primary failure and do not prevent cleanup attempts for other children. Reserved runtime control transfers propagate.

## Verification

- Native behaviour regressions: all 71 test entries passed, including parameterised variants, followed by the shell empty-mailbox check. Covers all three strategies, successful and failed replacements, explicit retry, ordinary failure, source exceptions, post-creation monitor errors, numeric/infinite/brutal shutdown policies, cleanup errors and unrelated monitors/messages.
- Node/ownership regressions: all 60 entries passed, including parameterised variants. Covers replacement cleanup under ordinary owner authority, startup ownership, lifetime authority and worker ownership cleanup. An initial command appended an unavailable T3-only mailbox helper after the passing T4 tests; rerunning with the correct T4 invocation exited successfully.
- The explicit-respawn regression fails against the pre-repair supervisor implementation and passes with the repair.
- Restart-intensity accounting and exhaustion implementation match the pre-repair source byte for byte; the existing restart-intensity regression passes.
- Live public conformance: 7 actor-core and 10 actor-behaviour cases passed on each of native SWI and Trealla (34 passes total). Reports have prefix `2026-10-20-restart-failure-fixed-nested-recheck-`.
- Disposable nodes on ports 39860 and 39861 were stopped after checking. Existing n3/n5 processes were left unchanged.

The shared HTML manual and Appendix B source describe restart-failure cleanup once, with the remaining native intensity-exhaustion cleanup difference explicit. The native runtime README documents journal and monitor integration. Book examples, public reply formats, shutdown policies and intensity-exhaustion cleanup were not changed. No PDF rebuild was requested.
