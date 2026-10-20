# ACTOR Supervisor Cleanup 0.1

Status: **draft executable profile**
Required advertised node profile: `actor`
Wire protocol version: `1`

This opt-in profile extends the ordinary supervisor behaviour checks with
publicly observable startup, replacement and restart-budget cleanup. It uses
identical submitted Prolog source and assertions for SWI and Trealla. It does
not import implementation modules or inject failures through private hooks.

## Contract checked

1. Initial startup that encounters an occupied child name terminates with an
   exception, releases names created earlier in that attempt, and leaves the
   unrelated actor occupying the conflicting name available.
2. A failed dynamic addition returns `error(Error)`, preserves siblings and
   their state, and permits adding the failed id after removing the conflict.
3. A failed explicit respawn returns `error(Error)`, retains the inactive
   specification and sibling pid, and permits retry. Native successful retry
   returns `ok(NewPid)`; running and missing ids retain their documented errors.
4. Exhaustion starts no excess replacement and stops remaining children under
   their policies before the supervisor terminates with `shutdown`. Cases cover
   all three strategies at zero budget and two permitted one-for-one restarts.
   A blocked server callback exercises numeric-timeout escalation; another child
   exercises `brutal_kill`. Infinite-policy servers complete graceful shutdown.

The metadata and provenance are in
[`actor-supervisors-0.1.json`](../cases/actor-supervisors-0.1.json).
Name-conflict assertions intentionally accept the original nonvariable error
term without prescribing runtime-specific context formatting.

## Boundaries

Public observations establish child termination reasons, name release, retry,
sibling identity, and monitor/message preservation. They do not expose the pid
of a provisional child that never published successfully, inspect private
monitor tables, prove exact internal stop-request order, or inject failures
between thread creation and admission. The runtime regression suites retain
those stronger implementation-specific checks. A failed-name release alone is
not proof of thread reclamation for a never-published provisional actor.

Each case uses its own ordinary names, closes owned actors in cleanup handlers,
and runs in a new WebSocket session. Use an isolated node: Trealla's ordinary
names are node-wide. Receive deadlines bound failure detection; request/reply
barriers establish successful restart completion without arbitrary sleeps.

## Separate diagnostics

[`supervisor-diagnostics-0.1.json`](../cases/supervisor-diagnostics-0.1.json)
is excluded from this profile's pass count:

- SCD-001 remains a runtime difference: a nested child list bound earlier in
  the submitted query is rejected at SWI static admission and accepted by
  Trealla.
- SCD-002 retains the original redundant monitoring/cleanup of already retired
  fixture actors. It now passes with the native zero-time polling repair.
- SCD-003–005 retain replacement-name-conflict checks for one-for-one,
  one-for-all and rest-for-one. Earlier full runs exposed SWI timeouts under
  each strategy; tracing showed completed supervisor/child termination and
  a later stall in final monitor flushing. They now all pass after the native
  zero-time polling repair, as do thirty further checks (ten per strategy).
  Trealla passes all three unchanged.

The latter four cases stay under their diagnostic identifiers for this repair
batch; the eight-case shared profile and reserved SC-004–006 slots are unchanged.
This avoids silently rewriting earlier reports or counting historical diagnostics
as shared-profile passes. See
[the repair report](../reports/2026-10-20-zero-poll-repair.md) and its raw results.
The native runtime carries a standalone upstream draft/reproducer for the
pending-signal host poll; it has not been submitted.

Shared fixture cleanup records consumed termination notifications and skips
redundant finalization of those pids. The diagnostic preserves the original path.
Namespace scope, startup-reporting variants and other intermittent runtime
observations remain outside this bounded contract.
