# Browser ordinary-name context closure

Both browser modes now retire ordinary names and promises through one host
lifecycle hook, `closeSwiWasmClientContext()`. Closure removes ordinary aliases,
rolls back pending named startup, and rejects registration, reservation,
publication and commit. Existing committed actors and owner service names keep
their separate lifetimes. `dispose()` closes admission before interruption and
then tears down the runtime. The promise-only close hook retains its narrower
meaning.

Named creation now awaits coordinator commit acknowledgement in both modes.
New child allocation and deferred remote dispatch reject a closed context.
This prevents source arriving after retirement from creating a child whose
startup ownership has already been removed. The browser runtime documentation
records these lifetime rules; Appendix B needs no revision.

## Maintained checks

The real-Chrome driver is packaged and runs through `tools/test.py`. Each case
executes in a fresh page with real Prolog engines and child Workers. Coordinator
barriers choose the ordering; they do not replace actors or language execution.

| Case | Assertion |
|---|---|
| BC-001 | Scope closure removes ordinary names, rejects late parent/child registration, cancels promises, rejects late promise creation, preserves an existing actor and its owner service name, and is idempotent. |
| BC-002 | Closure before publication rolls back the prepared child and reservation; the caller cannot report success. |
| BC-003 | Closure after publication approval but before its reply prevents commit and reclaims the child. |
| BC-004 | Closure before coordinator commit prevents success; Worker callers must await confirmation. |
| BC-005 | Closing one runtime does not affect an independent runtime's same-named actor. |
| BC-006 | Disposal during held publication retires admission/reservations synchronously, rejects pending work and reclaims startup ownership and the child. |
| BC-007 | Commit before closure preserves the actor; its ordinary alias disappears and the retained actor still answers queries. |
| BC-008 | URI source completes after closure; no child or name reservation leaks. The source response is a browser network fixture for an allowed URI, not a request to a public node or evidence about remote source permissions. |

The [clean package results](final.json) contain **16 passing observations**,
eight in each mode. The [full packaged regression](qualified/results.json)
records eleven selected groups, including the semantic contracts and all browser
groups. Engine/schema dependencies and consumer pins are unchanged; native and
consumer integration were not selected. Package/source hashes and gate counts
are recorded in [verification](verification.json).

## Counterexamples and diagnostic history

The clean pre-repair package is browser commit
`84bda8e845625ba2a8d06425c2f047fac49eca50`. The
[baseline selection](baseline-final.json) fails all fourteen then-defined
observations. Most require the missing combined scope-close hook; disposal
already exposes retained reservations. The old unacknowledged commit protocol
also cannot support a held commit reply. These are distinct failures, not
fourteen independent defects.

The [first baseline attempt](baseline.json) corrupted the engine bytes because
the fixture omitted UTF-8 response/document declarations. It is a fixture error,
not language evidence. The [corrected baseline](baseline-fixed.json),
[first repair](first.json), [diagnostic run](diagnostic.json),
[reinforced disposal checks](second.json) and
[commit-first expansion](third.json) are retained. All completed repaired runs
pass their then-current selection.

The first broad regression has six nonpassing semantic scenarios:
[first regression](regressions-initial/results.json). Fixtures extracted methods
using the old adjacent-method boundary and returned a synchronous commit value.
They now include the new lifecycle method boundary and asynchronous commit reply;
the parent runner also prints nonzero child exit/signal/stderr even after partial
passing output. The [fixture-corrected run](regressions-fixtures/results.json)
retains its full observations. It precedes the source-completion repair.

The additional source barrier then [fails in both modes](source-before.json):
after the reservation was retired, source completion could allocate a child
without a startup rollback owner. Closed-context allocation/dispatch checks fix
that real leak; the [expanded development selection](fourth.json) passes all
sixteen observations before clean-package qualification.

The [final negative controls](final-negative.json) deliberately permit late
registration, retain pending reservations and permit their commit in a disposable
copy of the clean package. All four selected observations must **fail** on the
intended assertions: late registration succeeds and late creation reports
successful publication. The [exact mutation](final-negative-runtime.diff) and
[mutated manifest](final-negative-manifest.json) are retained; production source
and installed engines are not changed by these controls.

## Coverage boundary

The [context audit](../../docs/CONTEXT_LIFETIME_AUDIT.md) and B-354 ledger now
include these exact cases. Browser whole-unit status remains unverified pending
browser/native context attachment and closure-propagation transport controls.
Coordinator barriers do not certify remote authentication, reconnection, or
context return. Historical public timeouts remain separate.

All runner tests and ledger validation pass. No public nodes, credentials,
deployment policies or release dependency pins changed.
