# Runtime introspection and Appendix B audit

Audit started 4 November and continued 5 November 2026. This is development
source verification; public deployment and dependency pins are unchanged.

`runtime_property/1` now enumerates only the five Appendix B capabilities.
Isolation values are `independent` or `cooperative`; implementation identity is
kept in diagnostics and deployment metadata. Private browser engine-mode facts
preserve naming and statechart startup behavior.

All **25 shared capability assertions pass** across SWI, Trealla, GNU, WASM
Worker and WASM main. The identical corrected pre-repair selection has 15
failures, all retained under diagnostics. An initial fixture used two GNU
library helpers not admitted by its query policy; that fixture issue was
removed from the capability checks and retained as separate library probes.

Native LINT/TEXT/T0/T1_NATIVE/T2/T3_NATIVE/T4_NATIVE pass (1055 T4 cases).
Trealla full unit and SWI/Trealla interoperability pass. The packaged browser
statechart, schema, mailbox, standalone and full semantic suites pass. The
consumer source smoke passes against the explicit development package; pinned
startup correctly refuses dirty native code. No dependency validation guard
was disabled, no pin promoted, and no public service changed.

The [source-unit matrix](../../docs/APPENDIX_B_COVERAGE.md) inventories 353
manuscript units. These are grouped requirements/signatures, not a percentage
of language semantics. Most older evidence still needs complete clause mapping.
The validator rejects manuscript drift, wrong targets, absent/duplicate cases,
unsupported profile waivers and false passing annotations; seven checks pass.

The audit retains **two failing GNU library probes** (`memberchk/2`, `forall/2`)
and **one failing same-context promise diagnostic**. A real WASM child receives
its parent's reference but raises `existence_error(promise,Ref)` when collecting
it. The main-engine store gap is identified by source inspection; a main-parent
reproducer is still pending. The promise diagnostic uses real WASM actors and
the real coordinator, with only remote HTTP mocked. These are unresolved
conformance findings, not passing checks or introspection regressions.

[verification.json](verification.json) records counts, regression commands and
hashes. [The ownership design](../../docs/PROMISE_CONTEXT_PLAN.md) sets out the
trusted context registry, teardown rules and acceptance cases for the next repair.
