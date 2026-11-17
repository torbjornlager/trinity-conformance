# Context races and remote monitors

This qualification covers browser-origin native-to-native returns, late return
admission after closure, GNU continuation/retirement orderings, and remote
monitor withdrawal. It uses disposable local services and development sources.
Public nodes, consumer pins and the manuscript are unchanged.

## Assertions

The [final browser selection](browser-final/results.json) contains **64 passing
observations**, sixteen cases in each browser mode against SWI and Trealla.
[Provenance](browser-final/provenance.json) records the immutable browser package,
exact native revisions, source hashes and unchanged inputs. The wrapper rejects
missing, duplicate, unexpected and nonpassing observations.

| Addition | Assertions |
|---|---|
| BN-012 | Browser → native origin → other native runtime → original native origin → existing browser child. Both returning engines resolve their original ordinary name and collect the promise belonging to their original node/context. |
| BN-013 | A real returning native frame pauses before admission; origin closure commits; release rejects `closed_client_context`. The name stays absent and the held actor cannot report revival. |
| BN-014 | Spawn and explicit monitors remain independent; foreign removal is harmless; duplicate queued notifications flush without consuming unrelated messages; a live target survives removal; successful removal without flush preserves queued notifications. |
| BN-015 | Actual socket loss discharges the reference with `connection_closed`; held old frames cannot restore it, and explicit reconnection/new creation does not recreate it. |
| BN-016 | Held coordinator withdrawal raises the exact timeout error, retains the observation and queued notification, cancels late timed-out withdrawal, and permits retry while another reference still receives termination. |

BN-013 uses [test-only instrumentation](../../adapters/return_barriers.py) in
disposable native copies; it does not add hooks to production runtimes. The
pause is before the real admission lock, so the test can commit closure while
the returning frame is held. Its recorded admission result is checked in
addition to public name lookup. Browser returns target existing actors over
established connections; browsers advertise no inbound node endpoint.

[GNU race results](gnu-races-final.json) cover three maintained implementation
groups. `GRACE-RESUME-FIRST` pauses after the retained query becomes busy under
the admission mutex. A real expiry scan sees it busy, the original worker stays
alive, and its original pending promise completes with one producer request.
`GRACE-RETIRE-FIRST` holds the real retirement decision under that mutex. A later
continuation creates a fresh execution and second producer request after the
old execution and transport are retired. Matching numeric references in fresh
processes are not interpreted as ownership. `GRACE-NEGATIVE-ACTIVE` removes the
busy guard in a disposable controller and must observe unsafe active retirement.
A separate retained probe crosses the admission mutex without reusing the old
query slot. The controller/source/binary hashes are recorded. No GNU runtime
change was needed; `make promise-context-race-test` and `local-test` maintain the
selection.

[Native monitor results](native-monitors/results.json) cover SWI's selected-down
versus withdrawal orderings and Trealla's real writer ownership/acknowledgement,
flush, stopped writer, unresponsive writer and timeout/retry paths. SWI pauses
actual notification delivery while the lifecycle mutex is held; removal and
flush cannot overtake it. Withdrawal-first excludes that reference from later
selection. Trealla confirms the serialized writer update before local removal
and flush. Timeout preserves the local record and queued notification; retry
removes it while another reference remains. These are implementation controls,
not additional portable language cases. The full Trealla suite also runs its
public monitor contracts against both native peers.

## Browser repair

The coordinator now discharges connection loss with Appendix B's
`connection_closed`. It owns the observation filter: removing it and returning
an ordered acknowledgement prevents later down delivery before `flush` runs.
Peer bookkeeping is best effort on the already-open connection and cannot
reconnect a withdrawn observation. Unconfirmed withdrawal has a two-second
bound and returns `error(remote_demonitor_timeout(Pid), Context)` without flushing
or destroying retry state. A delayed cancelled operation cannot remove that
state after timeout. Declared loss already discharges the observation, so local
withdrawal then suffices. This is the same observation-owner boundary used by
SWI's lifecycle mutex and Trealla's serialized writer; it is not a new peer-wire
acknowledgement protocol.

## Validation and diagnostic history

The [baseline monitor run](monitor-baseline/results.json) preserves four passing
independence cases and eight failures: wrong connection-loss reason and missing
bounded confirmation. [Development repair](monitor-development/results.json)
passes all twelve selected rows. Diagnostic subsets intentionally fail the
wrapper's complete-inventory check; their individual rows remain diagnostics.
The [complete development selection](browser-development/results.json) passes
all 64 rows. The final selection adds the explicit successful-no-flush assertion.

The initial [source-helper diagnostic](multihop-source-diagnostic/results.json)
failed during helper export (`src_predicates`) before establishing the desired
return behavior. This report does not qualify that source-copy form. The
inline diagnostic then exposed a successful-root-exit race in the test mailbox;
the test now ignores successful root exit and waits for its existing browser
child. Native pid equality is asserted on the native node rather than comparing
wire renderings of bare and qualified pid data. The intermediate reports are
preserved. These fixture refinements do not change context rules or timeouts.

The [initial broader browser regression](browser-regression-initial/results.json)
failed one statechart scenario because its coordinator stand-in lacked the new
confirmation method. The [corrected focused scenario](browser-statechart-fixture.txt)
and [clean full browser regression](browser-regressions/results.json) pass.
The final [SWI full suite](swi-full.txt), [Trealla full unit/interop suite](trealla-full.txt),
[GNU full local suite](gnu-full.txt) and [104 runner tests](runner-tests.txt) pass.
The native full suites precede small additional test assertions for foreign
ownership, queued messages without flush and complete down-frame shape; the
final native monitor selection executes those assertions on committed sources.

Commands and source identities are in the observation/provenance files and
[qualification inputs](inputs.json). GNU races additionally passed two earlier
runs, retained as `gnu-races-first.json` and `gnu-races-second.json`.
Archived text logs have trailing whitespace normalized; JSON observations and
source/package hashes are unchanged.

The [clause audit](../../docs/CONTEXT_LIFETIME_AUDIT.md) records the profile-conditioned
B-004/B-354 mapping. Monitor B-054/B-055 now have scoped evidence in the four
ACTOR targets. B-049/B-050/B-053 have new candidate evidence, but remain unverified as
whole units: local-name resolution, fresh-reference rules, the complete set
of private wait combinations and demonitor option/value/errors still need mapping. GNU does not
advertise ACTOR monitor APIs. Passing this report is not full Appendix B
conformance, a public deployment certificate or a proof of all thread schedules.
