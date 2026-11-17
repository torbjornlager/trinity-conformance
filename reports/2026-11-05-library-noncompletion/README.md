# Bounded countall noncompletion — 5 November 2026

**STDLIB-296 passes on all five runtime modes.** The separately pinned
`library-noncompletion-0.1` selection supplies the last missing assertion in the
current 43-obligation library inventory. The existing 295-case shared pack is
unchanged. No runtime, consumer pin, manuscript or public deployment changes
were needed.

The [native report](native/results.json) records three passes on standalone SWI,
Trealla and the GNU private query worker. The [real Chrome report](browser.json)
records Worker and main-mode passes. All [98 runner tests](runner-tests.txt)
pass. The [verification record](verification.json) pins the executed manifest,
adapters, validator, runtime/executable/library provenance and updated ledgers.

## What passes

Each mode runs these stages:

1. A finite control invokes a local HTTP entry peer from inside countall, counts
   three answers including a duplicate, checks generator binding isolation and
   failure count zero, and verifies exception propagation without binding a count.
2. The probe invokes the entry peer from inside the countall callback, then uses
   repeat as an infinite answer generator. The controller requires exactly one
   entry request with its response finished; an admission error or missing entry
   cannot pass.
3. From that observed entry, the external controller waits at least **500 ms**.
   No completed count or error may arrive; the owned process/browser must remain
   alive until termination is requested.
4. The controller terminates the disposable native process or entire browser
   and confirms its exit within **3 seconds**. The final native probes received
   SIGTERM; the browser probes were killed with SIGKILL through Playwright's
   owned browser server.
5. A fresh process/browser runs the same finite control, including its own entry
   signal. This verifies recovery in fresh execution, not same-session abort.

Native probes have a five-second entry deadline, eight-second finite-control
bounds, and terminate/kill escalation outside Prolog. The browser's entry wait,
observation interval and process kill run in the host Node controller, outside
both the Worker and the main renderer. A CPU-bound main query cannot block that
controller's timer. Browser startup is bounded and a 90-second external watchdog
also bounds the complete browser run.

The local entry peer returns the ordinary ground-goal RPC template `v`. Its URI
is bound to `LibraryEntryURI` by each adapter; the manifest's shared callback and
controls are otherwise unchanged. GNU's temporary outbound policy and Trealla's
standalone source policy allow only the disposable loopback fixture. No deployed
node policy is changed.

These observations establish no completed count during the stated interval after
callback entry. They are regression evidence, not a mathematical proof of
nontermination at arbitrary durations. They do not certify public transport,
HTTP deadline enforcement or same-session cancellation.

## Rejection and cleanup controls

The [negative manifest](negative-manifest.json) deliberately substitutes a finite
successful generator, a throwing generator, or a query without the entry signal.
All **15 controls are rejected**: [nine native](negative-native/results.json) and
[six browser](negative-browser.json), three per mode. Their `fail` statuses are
the expected rejection of invalid noncompletion fixtures, not runtime defects.
Finite warm-up controls pass and cleanup is confirmed for every rejected probe.
No-entry failures now end their controller wait as well as their Prolog process.

Unit controls also reject absent/duplicate entry, early timers, returned counts,
errors, missing finite controls and unconfirmed or late termination. Supplemental
suite validation checks its own manifest hash, target accounting, distinct case
IDs and the observation record; a `pass` label alone cannot cover LIB-035.

## Ledger changes and limits

The [library inventory](../../docs/LIBRARY_TEST_GAPS.md) now has **43 covered
obligations and zero selected test gaps**. B-381's finite evidence plus this
explicitly bounded observation verifies its prose within the recorded limits,
bringing each target to **23 verified Appendix B source units**. The
[previous inventory](previous-clause-inventory.json) and [ledger](previous-ledger.json)
remain available. Other Appendix B units, the external ISO mode/error inventory,
and public release qualification remain separate work.

## Preserved fixture-development failures

`fixture-development/` retains the unsuccessful harness observations, separately
from final qualification. Initial native controls used an unsupported RPC template
option, omitted SWI's standalone countall import, or returned the wrong ground
RPC template. Browser main startup failed when the local server omitted UTF-8
headers for the embedded engine; fixing the test server resolved it. An early
Node timer produced a 499.77 ms interval, correctly rejected; the controller now
waits against an absolute deadline.

The first negative-control run also exposed a native poll/signal cleanup race and
an entry polling loop that survived its outer Promise timeout. The native child
had already gone by the later process check. The lingering host Node process was
explicitly terminated after all six browser probes had been rejected and their
browsers closed. The final harness handles the process race, bounds the entry
loop itself, records cleanup and exits normally. Those earlier artifacts are not
silently relabelled as passing evidence; the final positive and negative runs
use the exact adapter snapshots saved beside this report.

## Reproduction

```sh
python3 adapters/local_library_noncompletion.py \
  --swipl /path/to/swipl --tpl /path/to/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --gnu-root /path/to/gprolog-port --output /fresh/native-output

LIBRARY_RUNTIME_ROOT=/absolute/path/to/swi-wasm-node \
LIBRARY_REPORT=/fresh/browser.json NODE_PATH=/path/to/playwright/node_modules \
node adapters/wasm_library_noncompletion.cjs

python3 runner/library_coverage.py --check
python3 -m unittest discover -s runner
```

For rejection controls, pass the absolute `negative-manifest.json` path using
native `--manifest` or browser `LIBRARY_MANIFEST`. The expected runner exit code
is 1, with every negative case recorded as `fail` and cleanup confirmed.
