# Browser/native context transport

The maintained selection passes **44 real-Chrome observations**: eleven cases
in both browser modes against native SWI and Trealla. Disposable local nodes
use their canonical advertised addresses and allow only the fixture's browser
origin. Public services, credentials, consumer pins and deployment policy are
unchanged.

The repair exports remote goals and toplevel control goals without their
caller's outer module qualification, matching native serialization. Nested
qualifications, data and shared variables are preserved. Trealla now accepts
`main@localhost` and `statechart@localhost` as connection-bound browser return
recipients, preserving variables during structural import.

Both native peers advertise `context_close:true`. The parameterless
`context_close` command retires only the requesting connection's ordinary-name
and promise scopes and replies with a correlated `context_closed`. It cannot
select another client's namespace; delegated lineage fields still require
internal transport authority. Existing actors and interactions survive while
new creation is rejected. Browser closure returns a promise for peer
acknowledgements, rejects unsupported/lost/unconfirmed retirement, prevents
reconnection as a fresh context, and closes admission before a delayed handshake
can dispatch pending creation. Full disposal remains a separate teardown.

## Cases and boundaries

| Case | Checked behavior |
|---|---|
| BN-001 | Native actor replies return to the originating browser actor. |
| BN-002 | Forwarding a browser promise reference grants neither native collection nor cleanup authority; the browser still collects. |
| BN-003 | Browser collection of a native reference is denied; a same-context native sibling collects after the creator exits. |
| BN-004 | A native descendant returns a request to a pre-existing browser child; that child sees its original ordinary name and collects its original context's promise in its own engine. |
| BN-005 | Independent browser clients with equal anonymous authority cannot collect or clean up each other's native promise. Closing the foreign context leaves the owner intact. |
| BN-006 | Acknowledged closure retires native names/promises, rejects late registration, and preserves an existing actor's ability to answer. |
| BN-007 | A raw late spawn frame is rejected by native admission, independently of browser-side guards. |
| BN-008 | Promise and RPC values/variable sharing work through a same-origin fixture proxy to the actual native HTTP endpoint. This is not a certificate for public cross-origin HTTP policy. |
| BN-009 | Forged delegated scope selection is denied, leaving the legitimate context open. |
| BN-010 | Closing the transport after scope retirement cannot reconnect the closed browser context as a fresh context. |
| BN-011 | A real native welcome is held before browser processing; closure wins, the handshake only retires its native scope, and no pending spawn frame is dispatched. |

[Final observations](final/results.json) and [input provenance](final/provenance.json)
record exact clean native revisions, the browser package manifest, driver hashes,
and unchanged inputs throughout execution. The wrapper rejects missing,
duplicate, unexpected and nonpassing rows using the maintained strict validator.
[All eleven browser package groups](browser-regressions/results.json),
[all three native context gate groups](native-regressions/results.json), the
[full SWI suite](swi-full.txt), [full Trealla unit/interop suite](trealla-full.txt)
and [104 runner tests](runner-tests.txt) pass. Native protocol tests additionally
cover unnegotiated closure denial, idempotence, isolation, surviving actors,
late creation and variable integrity.

Browsers advertise no inbound node endpoint. BN-004 tests a permitted callback
over an established connection to an existing browser actor; it does not invent
a URL through which a native peer can spawn a new browser actor. The broader
browser-origin, native-to-native attachment/return topology still needs its own
mapping and tests before B-004/B-354 can be certified as whole source units.
B-296 ownership now has scoped evidence across all five runtime targets, with
the separate GNU report completing the ISOBASE boundary.

## Diagnostic history

The initial [baseline](baseline/results.json) records Trealla caller-module
rejections and accepted late raw creation. Its BN-006 bound-answer assertion
could mistake a wait timeout for success; those particular positive rows are
invalidated, not qualification evidence. The [diagnostic](diagnostic/results.json)
uses unbound replies followed by nonvar/result checks and exposes the issue.
Fixture addresses were also corrected to match the native nodes' advertised
canonical addresses; no URI equivalence rule was added.

[First repair](first/results.json) exposes Trealla's missing special-recipient
route and remaining toplevel caller qualification. The [second run](second/INVALIDATED.txt)
is diagnostic only: a source file was edited while its fixture was active.
The final wrapper fingerprints inputs before startup and rejects such changes.
The [third run](third/results.json) exposes rejection of interactions with
surviving Trealla actors after scope retirement. The [fourth run](fourth/results.json)
then receives the successful state assertion twice; the fixture now asks once
for this Boolean assertion rather than requiring one proof. No timeout or retry
policy was changed. The [fifth](fifth/results.json),
[expanded](expanded/results.json), [clean qualification](qualified/results.json)
and final strict selection pass.

The initial SWI protocol unit test expected a string where the existing request
parser returns an atom: [initial output](swi-unit-initial.txt). The
[corrected unit selection](swi-unit-final.txt) passes. Original failures remain
archived. Text logs have trailing whitespace normalized; JSON observations and
source/package hashes are unchanged.
