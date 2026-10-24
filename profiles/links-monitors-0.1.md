# Links and monitors 0.1 — separate draft conformance pack

This pack selects local ACTOR behaviour from the shared
[language manual](https://github.com/torbjornlager/trinity-demonstrator/blob/main/web/manual.html#monitor/2).
It is separately versioned, does not amend baseline 0.1 and is not a new advertised
node profile. Required assertions apply within this pack. Both candidates run
identical [manifest goals](../cases/links-monitors-0.1.json) through public ACTOR
WebSocket sessions; no implementation module or private registry is accessed.

| Case | Selected observation |
| --- | --- |
| LM-001 | Spawn-time monitoring catches immediate success, failure, literal exception and explicit exit with exact pid/reference/reason. |
| LM-002 | An additional explicit reference is distinct from the spawn reference; both notifications arrive and unrelated data remains available. |
| LM-003 | Monitoring an actor after its observed termination returns no_process with the new reference. |
| LM-004 | A child finishes normally while its parent remains able to answer a ping and then stop normally. |
| LM-005 | Readiness handshakes identify root, child and grandchild; a root/die exit cascades child/kill and grandchild/kill with exact notifications under one deadline. |
| LM-006 | Withdrawal before termination suppresses only that reference; flush removes multiple pending matching down terms while retaining other-reference data, application data and another live monitor. Repeated demonitor is idempotent. |

Pids/references are opaque; there is no digit-width or runtime-format assertion.
Spawn references equal the spawned pid as documented. The explicit monitor is
independent and therefore has a distinct reference. Parent-child links are
one-way: parent termination stops linked descendants, not the reverse.

There are no sleep/1 calls. Ready/pong messages and exact termination notifications
synchronize the fixtures. LM-001 intentionally needs no readiness handshake:
atomic spawn-time monitoring is what it tests. LM-005 uses one two-second deadline
for all three notifications, not a renewed timeout for each. Unmatched data must
remain available. The runner requires one final successful query result without
wrapping assertions in once/1 to conceal additional alternatives.

The scoped flush part of LM-006 queues controlled application-sent down-shaped
terms using valid owned references. This makes pending-message removal
independent of notification scheduling, without private mailbox inspection. Its
other monitor must then deliver a genuine termination notification. This is a
mailbox-filter observation, not a claim that down-shaped data cannot be spoofed.
No assertion requires a particular order between independent notifications.

Every trial uses a fresh session. Cases consume their expected notifications and
retire explicit references on success; the session's existing link cleanup and
disposable node teardown bound failed fixtures. This does not certify actor
reclamation timing, arbitrary link races, namespace teardown or hard cancellation.
Monitoring the session itself, cross-client ownership and hostile-input security
are not covered. Remote links/monitor transport, GNU ACTOR and SWI-WASM execution
are explicitly unmeasured in this batch. Failures stay failures and are not waived
by unrelated diagnostic passes.
