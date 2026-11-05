# Controlled promise qualification — 5 November 2026

The expanded strict gate passes **57/57 black-box observations**: the original
51-case context matrix plus six new controlled-producer cases. Separate
attachment checks pass four positive observations and two negative controls.
All **71 runner self-tests** pass, including gate rejection when the new cases
are omitted and verification that the HTTP producer cannot answer before release.

[Results](results.json), [context observations](contexts/results.json),
[attachment controls](attachments/results.json) and [runner tests](runner-tests.txt)
retain exact outcomes. Adapter/helper copies and input hashes are included.
Native source revisions remain SWI `c826111` and Trealla `62e93c3`; no product
code, deployment pin, public configuration or manuscript changed in this extension.

## New controlled assertions

The same sequence runs for SWI→SWI, SWI→Trealla, Trealla→SWI, Trealla→Trealla
and one actor-transport self-route per runtime. Each case has independent client
contexts using equal credentials and a fresh HTTP producer with explicit events:

1. A remote creator returns its promise reference. The fixture confirms that the
   promise's HTTP request arrived, and withholds its response.
2. Another client is denied collection while the answer is pending.
3. The owner times out with the unchanged two-second wait while the producer is
   still held. No response can race this pending assertion.
4. The producer is released and confirms a flushed answer. Another client still
   gets a missing-reference error.
5. The owner retries with the unchanged deadline, collects `success([mark],false)`,
   then gets a missing-reference error on a further collection. Exactly one HTTP
   request is required throughout, excluding a replacement promise/request.

Each observation records phase times, terminal events and producer arrival/flush
information. A server flush is not interpreted as proof that the caller runtime
has already installed the answer; the retry still observes delivery and collection.
The gate runs each selection once, without automatic retries.

## Initial failure and limits

The [initial run](../2026-11-05-controlled-promise-suite/README.md) hit SWI's actor
admission limit on two new cases before promise creation. Both disposable SWI
ceilings are now explicitly 256, accommodating the larger selection under the
shared test principal. The subsequent run passes with this sole adapter change.
Initial failures and their original byte hash remain intact.

The HTTP callee is a controlled loopback fixture. Actor self-routes do not repeat
N5's public HTTPS self-call or proxy path. This extension therefore verifies
pending timeout/retry and ownership behavior but does **not** diagnose or repair
the historical public `CTX-015-trealla-b` timeout. It also does not address the
separate browser interruption-cleanup observation. No full Appendix B conformance
claim or whole-source-unit promotion follows from this selection.
