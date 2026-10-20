# Bounded public worker-combinator conformance batch

## Added

- Opt-in `actor-workers-0.1` contract and manifest, eight stable WC cases.
- Candidate-neutral public WebSocket implementations of every case in the shared
  runner. There is no SWI/Trealla branch in the assertions or fixtures.
- Independent `worker-diagnostics-0.1` manifest for exploratory repeated-call
  ownership-race probes. Its result is never included in worker-profile counts.
- Usage documentation and runner regression tests protecting final-page checking,
  terminal error handling, child notification ordering and expected failure.

This batch changes the conformance repository only. It does not fix a runtime
failure, change language semantics or modify book examples.

## Coverage

Bindings and empty goals, logical failure, exception fidelity, both first_solution
arities, empty solver lists, continued failure/exception/unexplained exits, stop
policies, supplied-source resolution and answer variable sharing, loser/sibling
cleanup, and preservation of unrelated mailbox contents and application monitors.

All cases except the inherently source-dependent WC-006 exercise the same goal
with and without supplied source. Cases are reported atomically: if one variant
fails, the case fails. Queries use `limit(1)` and must produce a final success page;
no once wrapper or compensating next request masks nondeterminism.

Continue cases use monitor/message barriers to ensure the rejected solver exits
before the winner is released. Cleanup cases check the loser's absence and the
unrelated witness's presence in public actor enumeration immediately after the
combinator returns, before waiting for the gate to finish. These are observable
completed-call checks, not assertions about hidden native thread/heap state.

## Configuration

Fresh native SWI-Prolog 10.1.17 and Trealla 3.13.10 processes, ACTOR profile,
blacklist mode, open authentication, accessed through localhost endpoints
39860 and 39861. Trealla's execution ceiling was 10 seconds; other resource
settings used runtime defaults. The source is the current working tree,
including the uncommitted Trealla public-routing and selectchk determinism
repairs from preceding batches. These are not release-tag or public-deployment
certification results. Test nodes were stopped; running n3 and n5 were unchanged.

## Results

| Manifest | Native SWI | Native Trealla |
|---|---:|---:|
| ACTOR Workers 0.1 | 7 pass, 1 fail | 8 pass, 0 fail |
| Separate repeated-call diagnostic | ownership error reproduced | passed tested attempts |

SWI WC-004 fails with `permission_error(exit,actor,Pid)` during continued solver
handling/cleanup. This occurred in two runs with the normal linked coordination
actors. It is retained as a failure of the agreed continued-winner requirement;
its unresolved cause does not justify weakening the assertion or moving that
core case into the diagnostics manifest.

The separate WCD-001 stress probe independently observed the same category of
ownership error on SWI (iteration 4 in one run, iteration 3 in another). Trealla
passed its eight source-less/source-loaded iterations. Passing a finite stress
probe does not prove the race absent. Raw current reports have names
`2026-10-20-{swi,trealla}-actor-workers-0.1.json` and
`2026-10-20-{swi,trealla}-worker-diagnostics-0.1.json`. Earlier SWI reports are
preserved with the `-first-run` suffix.

Eight Python runner regression tests pass. A lower-profile smoke invocation
reports all eight worker cases as unsupported without contacting the endpoint.

## Fixture correction and exclusions

An initial exploratory fixture requested `link(false)`, which native SWI reserves
for the node owner. This was a fixture error, not a worker defect. The maintained
cases use ordinary `link(true)` actors and require no detached-creation privilege.
The saved current and first-run reports mentioned above use those corrected actors.

This batch does not claim partial-startup fault injection, caller interruption,
hard-abort behaviour, remote cancellation, namespace teardown, equal blacklist
policies, identical HTTP options or runtime-bound nested-supervisor admission.
Existing reports retain those unresolved differences separately. No runtime
security checks were changed for the conformance run.

## Next investigation

The barrier-based WC-004 now provides a maintained public reproducer for SWI's
cleanup ownership error. Investigate whether cleanup is checking a worker's
ownership after its termination has removed the ownership record, while retaining
rejection of live actors outside the caller's tree. This is a hypothesis, not a
root-cause finding or an authorization to weaken ownership checks.

The conformance changes, reports and prior runtime repairs remain uncommitted.
