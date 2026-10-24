# Promise/yield 0.1 — separate draft conformance pack

This pack selects public promise/yield behaviour already documented in the
shared [language manual](https://github.com/torbjornlager/trinity-demonstrator/blob/main/web/manual.html#promise/3-4).
It is a separately versioned draft, not an amendment to baseline 0.1, a new
advertised node profile or certification of every promise lifecycle interleaving.
`scope: required` means each listed assertion is required within this pack.
Its report baseline identifier is `promise-yield-0.1`.

The [manifest](../cases/promise-yield-0.1.json) supplies identical goals for all
caller/peer combinations. Callers use public ACTOR WebSocket sessions; promises
perform HTTP calls to the selected peer. Pids and references remain opaque;
error context/prose is ignored while the documented error structure is checked.
Assertions are not wrapped in once/1 to hide extra answers. The existing runner
requires a single final result with no continuation.

| ID | Observable assertion |
| --- | --- |
| PY-001 | A pending yield with timeout(0) returns timeout; retry collects success without binding the caller's template variable. |
| PY-002 | A timeout callback binds the answer and emits exactly one message; retry succeeds and unrelated actor data remains available. |
| PY-003 | once(true) with limit(2) returns both first-slice answers and More=false on the finite three-answer fixture. |
| PY-004 | Logical failure is failure; an explicit remote throw is error with the original literal payload. |
| PY-005 | A fresh unknown reference and a previously collected reference raise existence_error(promise,Ref). |
| PY-006 | Invalid timeout options raise type_error(number,bad) before collection; a subsequent valid yield can collect. |

[HC-002](../cases/interop-http-0.1.json) is reused for repeated-variable sharing
and caller independence rather than copied into this pack. Its companion RPC
paging case HC-001 remains unchanged and is reported separately.

Pending-response fixtures use sleep(0.5) on the peer, a zero-time first wait and
a five-second retry bound. This is a scheduling fixture, not a hard guarantee
that a severely delayed caller must still observe a pending response. Any failure
remains visible and needs classification; assertions must not be weakened or
retried into a pass. Callback duplication is observed through public actor
messages, not private counters or mailbox internals. Query/server errors,
transport failures and promise error answers are not interchangeable successes.

PY-004 covers an explicit remote goal exception through the public endpoint; it
does not inject an internal worker failure, broken stream or malformed response.
Such failures need a separate controlled transport fixture. This batch does not
establish reclamation timing, expiry, concurrent collectors, cross-client
ownership, cancellation or resource bounds. GNU and SWI-WASM network execution
are explicitly unmeasured. Installed runtimes and live nodes are not test fixtures.

Separate [diagnostic controls](../cases/promise-diagnostics-0.1.json) distinguish
ordinary actor sending from built-in callback operations. Their observations do
not turn a PY-002 failure into a pass; see the dated coverage matrix.
