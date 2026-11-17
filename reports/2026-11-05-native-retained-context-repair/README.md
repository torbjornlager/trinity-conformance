# Native retained-context repair — 5 November 2026

The development repair passes **all 51 probes**, with **zero failures, blocked
cases or fixture errors**, across SWI → SWI, SWI → Trealla, Trealla → SWI and
Trealla → Trealla. This includes all nine original counterexamples and all
11 previously blocked cases. Independent initial, repeat and final all-route
runs each pass 51 probes; the final source fingerprints match the checkout.

The [original audit](../2026-11-05-native-retained-context/README.md) retains its
31-pass/nine-fail/11-blocked evidence unchanged. These results qualify selected
context rules on development sources, not full Appendix B conformance or a
public release. Consumer pins, installed engines and public services are unchanged.

## Repairs

- SWI fresh HTTP interactions have distinct promise identities even when they
  share credentials. Resource accounting remains principal-wide. Cached producers
  preserve their identity while paging; unretained retirement disposes promises.
- Native descendants carry a server-issued context token and origin URI across
  remote nodes. Returning descendants rejoin the original namespace. Transport
  attachments do not own the original client's lifetime, and unknown origin-local
  tokens cannot recreate a closed context. A close received before the first spawn
  also rejects that delayed admission.
- Trealla ordinary names, reservations, lookup, unregister and publication use
  the client namespace. Public services remain node-wide. Outgoing connections
  and routes are cached per context; default transport bindings are immutable.
- Context closure retires admission, names and promises and propagates through
  outgoing routes. Legacy lineage-only peers retain connection-scoped identity.
  Transport commands and descendants never gain node-owner authority.
- SWI publicly exports `promise_cleanup/1`. Trealla restores guarded catch, yield,
  spawn and other executable terms before exporting source/goals, including
  outgoing toplevel calls. Hosted local actor addresses use canonical node URIs;
  standalone clients retain connection return endpoints.

Trealla preserves delegated account tokens but retains its existing resource
accounting policy; this repair does not claim SWI's aggregate delegated-account
quota implementation. Network partitions still provide no remote-cancellation
completion guarantee.

## Evidence

- [Final 51-probe results](results.json), [initial](initial.json), [repeat](repeat.json),
  [fingerprint verification](verification.json), [environment](environment.json).
- [SWI repair patch](swi-repair.patch), [Trealla repair patch](trealla-repair.patch),
  [adapter snapshot](adapter-source.py). Apply patches to the recorded revisions;
  fixtures configure explicit synthetic receiving and outgoing peer credentials.
- SWI layering check, all **1,060 node tests**, and HTTP visitor ownership pass:
  [final gate](swi-final-node-suite.txt). Other default native tiers passed in the
  [initial suite](swi-initial-suite.txt); that first run records the five obsolete
  HTTP expectation failures, corrected before the final node gate.
- Trealla's full [unit suite](trealla-unit.txt) passes. Added focused checks cover
  [stable contexts and 20 creation-race iterations](trealla-context-regressions.txt),
  [restricted transport authority](trealla-authority-regressions.txt),
  [source restoration and variable sharing](trealla-source-regressions.txt), and
  [native SWI wire compatibility](swi-trealla-lineage-focused.txt).

- The interoperability [prefix](trealla-interop-prefix.txt) passes its selected
  protocol, source, actor, toplevel, supervisor and statechart checks before the
  browser-terminal fixture stalls. Hosted return-path transports now require
  explicit peer authority in both directions. The fixture was corrected, and
  the [browser-terminal check](browser-terminal-final.txt) and [remaining
  authentication/IP gates](trealla-interop-final-tail.txt) pass. The permanent
  fixture change is included in the Trealla patch. Temporary runners increase
  startup waits from 0.2 to 1 second for this host; the tail runner keeps the
  initial echo handshakes so its one-shot fixture can exit normally.

Existing tests that required authenticated stateless HTTP promise sharing or
node-wide ordinary-name visibility were changed to the agreed context rules.
Positive lineage name checks now execute in that lineage; an independent observer
checks an unconstrained lookup result against `undefined`.

The coverage ledger preserves the historical failures as evidence candidates and
returns repaired units to **unverified**, pending complete mapping of every
obligation. A passing narrow probe is not a whole-paragraph certificate. Deferred
Neumerkel/library semantic decisions and the separate book draft are untouched.
