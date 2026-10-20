# Focused native SWI–Trealla comparison, 20 October 2026

This is an assessment of the listed public-interface cases, not a claim of full
language conformance. No runtime repair was made during this assessment.

## Source and configuration

The requested implementation/documentation batches were committed and pushed
before testing:

- Trealla `71ec226`: paging deadlines, private producer reply correlation,
  connection-thread stack limits, actual-length paging offsets, server-promise
  setup/send cleanup, and removal of silent solution-count caps.
- Trinity demonstrator `a9cb4b7`: shared manual and Admin UI explanations.
- Book `405e5dc`: manual/offset explanations and the existing changed tracked PDF.
  This assessment did not rebuild the book.

Candidates were fresh disposable processes on loopback ports 39860 (SWI-Prolog
10.1.17) and 39861 (Trealla 3.13.10), using ACTOR, open authentication and blacklist
sandboxing. Trealla used owner `time_limit(10)`; other owner settings used their
runtime defaults. SWI loaded `library(sgml)` and `library(option)` before the node.
These are development configurations, not public deployment recommendations.
The running n3 and n5 were not restarted or reconfigured. Both disposable
processes were stopped after each run.

## Results

| Group | Native SWI | Native Trealla |
|---|---:|---:|
| ACTOR Core 0.1 | 7/7 pass | 7/7 pass |
| ACTOR Behaviours 0.1, initial run | 8/10 pass | 10/10 pass |
| Behaviours after isolated checks of failures | 9/10 observed passing | 10/10 pass |
| Supplemental recent-repair probes, corrected harness | 7/7 pass | 5/7 pass |

The JSON files with matching date/prefix retain the original group results,
isolated SWI rechecks and supplemental probe results. The supplemental probes
are reproducible with `2026-10-20-focused-probes.py` against already-running test
nodes; they are not a new formal profile.

### Confirmed differences

1. **SWI nested-supervisor replacement times out (BH-009).** The shared case
   starts a nested supervisor plus an independent sibling, kills the inner
   supervisor, and checks that only its subtree is replaced. It timed out in
   the initial 4-second test and again in isolation with an 8-second timeout.
   Trealla passed. The timeout has been reproduced; its root cause has not
   been established. Next work should locate the blocked operation before
   choosing a repair.
2. **Trealla public worker-call routing differs from local tests.** Fresh
   source-less WebSocket toplevels report missing `parallel/1`,
   `first_solution/2` or `first_solution/3` for ordinary direct calls. Under
   `catch(parallel([exit(killed)]),Error,true)`, the caught error instead reports
   missing `exit/1`. Thus the supplemental expected `worker_exit/2` assertion
   fails, and the `first_solution/3` continue-policy probe raises an existence
   error. Diagnostic event traces are retained in `focused-diagnostics.json`.
   These results do not invalidate the local worker regression tests; they
   expose a public execution-context/routing gap requiring separate diagnosis.

### Behaviour matching in this run

Both candidates passed transport negotiation, public self identity, ordinary
paging, guarded/selective receive, browser input and nested toplevel input.
Both passed asynchronous server correlation, callback replacement, ordinary
supervisor startup/dynamic operations, restart strategies and restart policies.

The corrected supplemental probes passed on both candidates for:

- HTTP requested/omitted sizes above 1,000 and continuation offsets;
- WebSocket initial page sizes and changed `next` sizes above 1,000;
- promise timeout callback, retry, answer collection and consumed-reference errors;
- promise ordinary failure delivery and nonexistent-reference rejection;
- failed server-promise reference setup followed by a successful monitored request.

The last probe is an observable smoke check, not a black-box proof that every
failed-setup monitor is reclaimed; the implementation-specific regression suite
checks monitor state and selective notification flushing.

### Intermittent observations and harness corrections

SWI BH-001 (server state threading) timed out initially but passed on its isolated
recheck. Do not classify it as a fixed or reliably reproduced defect.
An early SWI worker probe also observed an actor-ownership permission error during
cleanup; isolated and final probes passed. That observation remains unclassified.

The initial supplemental harness used the wrong wire field for changing a page
limit and assumed that a success must precede child `down` notifications. Both
were harness errors. The final supplemental report uses the documented numeric
`limit` field and permits preceding `down` events. It replaces the initial
supplemental results; the formal-profile reports were not affected.
An attempted stage-tracing variant for BH-009 produced an instantiation error;
it did not localize the timeout and is retained only as a diagnostic trace.

## Suggested next batch

Investigate Trealla's public `parallel/1` and `first_solution/2-3` routing first:
it blocks simple documented calls despite passing local tests. Then investigate
the reproducible SWI nested-supervisor timeout. Keep the intermittent SWI
observations pending until a reliable reproducer exists. HTTP option alignment
and further supervisor rollback parity remain separate work.

## Subsequent worker-routing repair

A later bounded implementation batch addresses the Trealla public worker-routing
finding. See `2026-10-20-worker-routing-repair.md` for its cause, scope and new
regression evidence. The original comparison results above remain historical.

## Subsequent nested-supervisor investigation

The reported SWI nested-supervisor timeout was traced to an immediate admission
error hidden by the runner, not a blocked restart. With explicit nested child
specifications, both candidates pass all 17 shared core/behaviour cases. The
runtime-bound nested-list admission difference is retained separately. See
`2026-10-20-nested-supervisor-investigation.md` for the evidence and scope.
