# Trealla connection-cleanup probe follow-up — 19 November 2026

The missed termination notification in the [naming report](../2026-11-19-client-naming/REPORT.md#reproduction-and-evidence)
was caused by delayed cleanup in the SWI test client. This follow-up repairs the
harness and adds transport regressions. No runtime repair was necessary for
this reproducer. Earlier reports and failed observations remain unchanged.

## Cause and repair

`wire_checks/3` succeeds with a remaining choicepoint. In Prolog,
`setup_call_cleanup/3` does not run its cleanup merely because a nondeterministic
body returns its first answer: cleanup waits for commitment, exhaustion or an
exception. The old focused probe therefore awaited a termination notification
while its owner socket was still open.

A controlled experiment used the same Trealla runtime and actor scenario twice.
The [uncommitted body](raw.log) returned with both its determinism flag and
close callback pending. Cutting the choicepoint then ran the callback, and the
observer received `down` with the matching monitor reference and reason `kill`.
With [once/1 around the body](once.log), the callback ran before control returned
and the notification arrived normally. Neither experiment extended a timeout.

The maintained `trealla-port/swi_lineage_compat.pl` now commits the observer and
owner setup bodies with `once/1`. An explicit cleanup-completed assertion checks
the owner boundary before the reconnect probe. The additional cleanup scenarios
use the same discipline. The harness repair is committed and pushed as Trealla `7946acd`,
on top of `6041ea3`; the [summary](SUMMARY.json) identifies exact source hashes. The complete [harness patch](harness.patch) applies to
that base revision.

## Stronger transport regression

Each scenario opens an ordinary observer plus two authenticated peer
connections. The peers deliberately reuse the same credential and lineage token
on different connections. Each owns a root actor, an unlinked child and a
toplevel. The child reports readiness before the observer installs language-level
monitors. Exact monitor references distinguish the six monitored actors.

After the observer acknowledges readiness, the client closes the first peer.
The observer requires `down(..., Ref, kill)` for its root, child and toplevel,
with five-second receive deadlines. It then requires distinct root and child
pong messages from the other connection; the client also runs a query on that
connection's toplevel. Finally the client closes the survivor connection and
requires all three remaining termination notifications. The observer query must
finish successfully with `more:false`.

This passes for both a WebSocket close handshake and a stream close without a
WebSocket close frame (EOF). It does not infer disposal from hidden names or a
fresh reconnect. It does not use raw wire-monitor authority across connections;
the independent observer uses the public language-level `monitor/2` API.

## Verification

- All **69 interoperability groups passed**, including both new close modes.
- The final formatted source, with the extra assertion at the original owner
  boundary, passed the [focused interoperability run](focused.log).
- Removing only the original body's `once/1` fails immediately with
  [`connection_cleanup_still_pending`](negative.log).
- Replacing the first close with a no-op fails with
  [`missing_root_down`](held-open.log) at the existing five-second deadline.

The two deliberate negative mutations are retained as
[pending-cleanup](pending-cleanup-negative.patch) and
[held-open](held-open-negative.patch) patches. Apply them independently to a
throwaway copy of the final test source, never to a runtime or live fixture.
They are expected failures, not conformance passes. The full interoperability
run preceded the final formatting and original-boundary assertion; both source
hashes are recorded separately. Retained logs include stream/import warnings;
the successful results are based on assertions and process exit status.

The disposable, network-isolated Linux lab paired Trealla 3.14.20 with its
matching library and SWI-Prolog 11.0.0 with native node revision `26e1ce7`.
The Trealla source tree was an archive of `6041ea3` overlaid with only this test
change. A sibling native checkout and public fixtures supported the standard
runner; the readiness shim implements only `nc -z HOST PORT`.

Run in an equivalent disposable fixture with those inputs:

```sh
TPL=/opt/trealla/tpl SWIPL=/usr/bin/swipl TEST_PORT_BASE=24060 ./tools/test.sh interop
```

The runner provisions its peer credential and invokes `swi_lineage_compat:run/3`.
The default per-process timeout remains 30 seconds. Raw full-suite logs,
launchers and source snapshots are retained privately under
`trinity-demonstrator/.trinity/cleanup-investigation-20261119`; exported records
and their hashes are in this directory.

## Boundary

This resolves the earlier focused-probe uncertainty for the tested delegated
transport paths. It is not a full ACTOR certification or evidence for every
runtime's disconnect behavior. Promise ownership, HTTP client contexts and
remote round-trip context requirements remain separate work. No runtime source,
consumer pin, engine, live service, deployment configuration or quota changed.
