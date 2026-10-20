# Native SWI zero-time mailbox polling repair — 2026-10-20

## Finding and bounded repair

The apparent public supervisor replacement-cleanup failures occurred after
expected child/supervisor termination and a successful request to the unrelated
conflicting server. Final monitor flushing in test cleanup could spin in SWI
10.1.17's `thread_get_message/3` zero-time wait while a signal was pending but
handling was masked. A standalone host-only reproducer deterministically reaches
the same protected-context failure, without any actor or supervisor code.

Native actor receive now implements documented integer/float zero-time polls as
an atomic peek/read pair on the calling actor's private mailbox. Only that actor
consumes the mailbox; `sig_atomic/1` prevents signal-handler re-entry between the
peek and read. Empty polls return to the existing timeout callback logic without
entering a timed host wait. Selection still uses the existing deferred records,
one-sided matching, guard/control handling and nondeterministic clause bodies.
The existing accounting hook runs only when a message is actually consumed.

The shortcut accepts only documented timeout/on_timeout poll options, with all
supplied timeout values zero. Normal finite/negative waits, malformed option
lists, mixed duplicate timeouts and native host-option extensions retain their
original paths and validation. This is not a general repair of every finite
host wait inside a protected context. There are no supervisor-policy, protocol,
node-configuration or broader lifecycle changes.

## Local regression evidence

- Full T0: **90 test entries**, including parameterised instances, pass with
  layer-honesty and final empty-mailbox checks. This includes four isolated
  pending-signal cleanup scenarios: integer zero, float zero, selection with
  unrelated/non-ground messages, and reference-specific monitor flushing.
  Signals remain pending inside cleanup and execute after leaving it.
- Existing T0 receive tests cover failed/control guards, preserved variable
  sharing, committed selection, body alternatives and timeout callback context.
  Additional tests retain negative-timeout behavior and native malformed-list
  and host-option errors.
- Targeted T3: **55 entries**, including parameterised instances, pass across
  supervisor behaviour, restart/startup/intensity cleanup, request-monitor and
  server-promise cleanup; final empty-mailbox check passes.
- Targeted T4: **41 entries**, including parameterised instances, pass across
  lifetime authority and supervisor ownership cleanup. The new owned-actor
  accounting test checks queued/deferred counts, unchanged quota on an empty
  poll, and exactly one decrement for consumed/flushed messages, including
  unrelated monitor-shaped messages.
- The isolated empty-poll regression fails against the pre-repair `actors.pl`
  with a watchdog timeout and passes with the repair. The watchdog polls child
  process status nonblockingly and kills/reaps a stuck child; it does not depend
  on injecting a signal into the protected Prolog operation. A first harness
  attempt used an unsupported positive Unix process_wait timeout; the final
  regression uses explicit deadline polling instead.

## Public checks on real implementations

The final run loads the edited native actor runtime directly, without temporary
wrappers, tracing hooks or watchdog signals injected into the node. Disposable
ACTOR nodes use ports 39860 (SWI) and 39861 (unchanged Trealla v3.13.10), open
authentication and blacklist sandbox configuration. Existing n3/n5 are unchanged.
Both disposable processes were stopped after checking.

| Manifest/check | Native SWI | Trealla |
|---|---|---|
| Shared supervisor cleanup | 8/8 pass | 8/8 pass |
| Existing actor behaviours | 10/10 pass | 10/10 pass |
| Historical cleanup/replacement diagnostics SCD-002–005 | 4/4 pass | 4/4 pass |
| Runtime-bound nested-spec diagnostic SCD-001 | Existing admission rejection | Success |
| Further SWI replacement-failure checks | 30/30 pass, ten per strategy | Not repeated |

The diagnostic admission rejection is neither relabelled as a pass nor charged
to the shared cleanup profile. Historical diagnostic identifiers are retained;
this batch does not promote them or alter old raw reports. New report prefix:
`2026-10-20-zero-poll-fixed-`. Repeat details are saved separately as
`2026-10-20-zero-poll-fixed-replacement-repeats.json`.

## Upstream preparation

The native runtime repository contains the ready-to-review draft and standalone
three-mode reproducer:

- `docs/upstream/swi-zero-time-poll-pending-signal.md`
- `docs/upstream/repro-zero-time-poll.pl`

The tested host is macOS 26.6.2 arm64, SWI 10.1.17 (`arm64-darwin`; fat-darwin
executable). Fresh-process controls print `completed` and exit zero without a
pending signal or when using the peek/read workaround. With a pending signal,
the original native poll exceeds the external two-second watchdog. Results are
in `2026-10-20-zero-poll-upstream-reproducer.json`. The report distinguishes
observations from the proposed engine-level retry-loop explanation, links the
official signal/queue documentation and versioned engine source, and makes no
claim about untested versions/platforms. It has **not been submitted**.

The runtime README records the workaround and scope. Public receive semantics,
the language manual, book examples and PDF require no new changes for this fix;
the earlier manual qualification corrections remain in the pending diff.
