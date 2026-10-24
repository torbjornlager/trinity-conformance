# Initial synchronous wait test construction run

This run is retained for transparency, **not as conformance coverage**. Its
executed-manifest.json identifies the initial test inputs. Both candidates
reported four passes and two failures; TW-002 timed out and TW-004 failed.

The gate helper in the outer source was not supplied to the separately created
toplevel. Readiness waits also lacked failure callbacks, so timeout could succeed
without observing readiness. In particular TW-003's reported pass did not prove
its intended gated execution. TW-004 additionally expected next to reply after
paging had finished, which is outside the selected contract.

The corrected run embeds the gate in each query, uses explicit readiness failure
callbacks and tests mismatched outputs while continuations exist. It adds a gated
next-timeout correlation check. See ../2026-10-24-toplevel-waits/REPORT.md for the
final selection and coverage. No runtime code was changed or timeout increased.
Both initial disposable nodes were stopped; all preservation checks passed.
