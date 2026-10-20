# Public supervisor cleanup conformance — 2026-10-20

Subsequent batch: the native zero-time polling repair resolves the timeout
observations recorded below. See [the repair and upstream-reproducer results](2026-10-20-zero-poll-repair.md).
The following is the original assessment; its raw results have not been changed.

## Final shared cases

The new draft `actor-supervisors-0.1` contains eight identical public-interface cases. Both native SWI and Trealla pass all eight:

- Initial startup name-conflict rollback releases earlier child names and preserves the conflicting actor.
- Failed dynamic addition preserves the sibling and permits retry after removing the conflict.
- Failed explicit respawn retains the inactive specification and sibling pid, returns an error, and permits retry.
- Zero restart budget under each of the three strategies performs graceful sibling cleanup and reports supervisor `shutdown`.
- Two permitted one-for-one restarts precede budget exhaustion.
- Exhaustion honours numeric-timeout escalation and brutal-kill policy; application monitors and unrelated messages survive the waits.

The existing actor-behaviour suite also passes all ten cases on each runtime. Total final shared result: **18 cases per runtime, 36 passes**. The runner's eight Python unit tests pass. Both manifest case sets resolve to registered functions, and diff checks pass.

## Diagnostic results, excluded from conformance counts

The separate `supervisor-diagnostics-0.1` manifest retains five identical exploratory cases:

| Case | Observation in the final run |
|---|---|
| SCD-001, runtime-bound nested list | SWI rejects at static admission with instantiation error; Trealla succeeds. |
| SCD-002, repeated cleanup of retired fixture actors | SWI times out; Trealla succeeds. |
| SCD-003, one-for-one name-conflict replacement failure | Both succeed in the final run; SWI timed out in earlier runs. |
| SCD-004, one-for-all name-conflict replacement failure | Both succeed in the final run; SWI timed out in an earlier run. |
| SCD-005, rest-for-one name-conflict replacement failure | SWI times out in the final run; earlier runs succeeded. Trealla succeeds. |

One exploratory full eleven-case run passed on both runtimes. Repetition exposed SWI timeouts across the replacement-failure family, so all three strategies remain together as diagnostics rather than treating a single passing run as conformance. SC-004 through SC-006 are reserved in the draft. The raw earlier reports retained below show one-for-one and one-for-all failures; the final diagnostic report records rest-for-one failure. The runner timeout was four seconds. These observations do not isolate supervisor cleanup, public monitor/wait routing or fixture finalization as the cause, and do not establish an engine bug. **The next useful investigation is a reduction of these SWI public-path timeouts**, not another runtime repair based only on a hypothesis.

Initial fixture work also corrected source-atom backslash escaping in the candidate-neutral runner and removed explicit detached spawning, which native SWI correctly forbids for ordinary clients. Fixture servers receive explicit callback sources. Shared fixture cleanup records consumed termination notifications and avoids re-monitoring those already terminated pids. The original redundant cleanup remains executable as SCD-002. No runtime-specific branch or implementation-private hook is used by a shared case.

## Scope and evidence

Name conflicts trigger failures through public server/supervisor APIs. Cases check reported errors without prescribing implementation-specific error-context formatting. Public monitors establish termination reasons, name lookup establishes release, and requests establish surviving sibling/conflicting-actor usability. The suite does not expose never-published provisional pids, inspect monitor tables or prove the exact internal stop order; implementation-specific regression tests retain that coverage.

Final machine-readable reports have prefix `2026-10-20-supervisor-shared-nested-recheck-` (two runtimes, shared supervisor cases, existing behaviour cases and separate diagnostics). The inherited `nested-recheck` filename/candidate label is only a launcher label. Prior full-profile SWI probes are retained as `2026-10-20-supervisor-full-probe-one-for-one.json` and `2026-10-20-supervisor-full-probe-one-for-all.json`; their evolving draft case sets must not be confused with the final eight-case profile.

The run used disposable local nodes on ports 39860 (SWI) and 39861 (Trealla v3.13.10), with ACTOR, open authentication and blacklist sandbox configuration. The runner uses the public WebSocket protocol and submitted Prolog source. Both disposable processes were stopped afterward; n3/n5 were unchanged.

Reproduce against an isolated running candidate:

```sh
python3 runner/run.py --manifest cases/actor-supervisors-0.1.json --ws-url ws://127.0.0.1:39860/ws --candidate swi --timeout 4 --report /tmp/swi-supervisors.json
python3 runner/run.py --manifest cases/supervisor-diagnostics-0.1.json --ws-url ws://127.0.0.1:39860/ws --candidate swi --timeout 4 --report /tmp/swi-supervisor-diagnostics.json
```

Use the same manifests/arguments with the Trealla endpoint. Diagnostics are not expected-pass classifications and do not enter the shared profile's pass count.

Corrected stale runtime qualifications for dynamic addition, explicit respawn and explicit termination in both the shared HTML manual and Appendix B source. Runtime implementation code, book examples and PDF were not changed.
