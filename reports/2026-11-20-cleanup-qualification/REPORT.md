# Trealla cleanup qualification — 20 November 2026

**Both reported qualification blockers are resolved in the local test harness. The complete Trealla unit suite passes on macOS and Linux: 111 check groups on each. Runtime cleanup code, production pins and live services are unchanged.** The pending numeric-RPC candidate from the first batch is included without further changes.

[Current issue inventory](../../CURRENT_ISSUES.md) · [summary](SUMMARY.json) · [complete unit results](complete-unit-summary.json) · [test patch](cleanup-fixtures.patch).

## Sandbox/cascade fixture

The original t145 snapshot runs after a fixed 100 ms sleep. Startup of the root actor does not guarantee that its child and grandchild have started. The [diagnostic snapshot](readiness-diagnostic.json) contains the session, root and child; a later snapshot contains all four actors. The cardinality assertion fails before cascade teardown. The fixture's halt call was after its assertions, so failure left the tree running and process shutdown reached the watchdog. [Trace](t145-readiness.txt).

The fixture now receives an explicit readiness message from the grandchild, after both source-copying generations have completed. The same four-actor assertion, link-chain checks, three exact down reasons and final session-only snapshot remain. The session is owned by setup_call_cleanup, so failure or exception also closes it. The new readiness wait has the existing two-second bound; the 30-second process watchdog is unchanged.

Standalone t145 and the complete sandbox group pass in [the focused results](sandbox-focused.json). Two deliberately failing controls retain nonzero exit status and reclaim all four actors: [failure/exception controls](failure-controls.json). The exception control also preserves its original injected exception. These are fixture fault-injection controls, not substituted conformance passes.

## HTTP cache properties

The old group runs five production-sized cache properties in one process under a single 30-second watchdog. Each property creates roughly 100 producers. An unchanged-source timing probe completed all five in 27.6 seconds on the two-CPU fixture, leaving little margin for scheduling and setup overhead. [Timing evidence](cache-timing-diagnostic.json).

That probe used a diagnostic-only 120-second watchdog to observe completion; it is not qualification evidence under an enlarged deadline. The earlier 30-second watchdog failures remain in the [first-batch report](../2026-11-20-backlog-baseline/REPORT.md).

The maintained unit runner now runs each property in a fresh process under the same 30-second limit. This allocates five separate process budgets instead of one shared budget; the family’s maximum combined process budget is consequently 150 seconds. Language-level receive/deadline assertions are unchanged. The FIFO, multiple-eviction, checkout-before-eviction, concurrent-checkout and interruption property bodies are byte-identical. The real default cache capacity stays 100. Producer-retirement and claim-leak checks now run after every property; the aggregate run/0 entry remains available. [Preservation checks](cache-property-preservation.json).

A supplementary run of the revised aggregate entry point also passes all five properties together in one process, preserving combined-state coverage. It completes in 39.2 seconds with the explicit 150-second family budget; it is not counted as a 30-second qualification run. [Combined result](cache-combined-candidate.json), [full log](cache-combined-candidate.txt).

## Verification and scope

- macOS: all 111 unit check groups pass, including sandbox/cascade and all five cache properties. [Full log](mac-unit-candidate.txt).
- Linux: all 111 groups pass with the same per-check watchdog, two CPUs, 2 GiB memory, 512 PID ceiling and no external network. The owned image contains the unchanged live N5 Trealla engine/library bytes. [Full log](linux-unit-candidate.txt), [execution record](linux-unit-candidate.json).
- All 123 conformance-runner unit tests pass. [Runner log](conformance-runner-tests.txt).
- Deliberate failure and exception controls exit with the expected status 1 in about one second and verify all four fixture actors reclaimed.
- The frozen source snapshot matches the tested working tree. The previous RPC edits are unchanged. Core actor, node, isolation, toplevel and native-thread cleanup files match the 2d5042b base exactly. [Source preservation](source-preservation.json).

These changes address test readiness, failure cleanup and watchdog allocation. They do not establish another runtime cleanup repair or close the broader language-conformance findings. The original first-batch qualification failures remain immutable and linked; the current inventory records the successful follow-up separately. Full interoperation, consumer pin qualification, GitHub CI and deployment are subsequent release steps.

Owned containers and probe processes are removed. The live recovery guard and selected service identities are unchanged. Artifact integrity is recorded in [SHA-256 hashes](files-sha256.json).
