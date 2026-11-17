# Bounded member/length generation — 5 November 2026

**295/295 shared cases pass in all five runtime modes.** Version 0.4 retains
all 289 earlier definitions and their source prefix and adds six externally
bounded generation cases, STDLIB-290–295. No runtime, consumer pin, manuscript
or public deployment changes were needed.

The [native report](native/results.json) records **1,475 passes**, 295 each
through SWI/Trealla fresh HTTP and retained sessions plus GNU HTTP. The
[real Chrome report](browser.json) records **592 passes**: 295 each in Worker
and main modes plus two existing child controls. This is 2,065 standard-case
observations across seven surfaces, plus two child controls. All
[87 runner self-tests](runner-tests.txt) pass. The [verification record](verification.json)
pins the executed manifest, adapters, helper, current ledger and runtime sources.
The runtime reports also retain executable/library or browser artifact hashes.

## Assertions and bounds

- Member generates a fresh list with its matching element at successive positions.
  Cases cover both fresh arguments, a supplied atom and a compound whose two
  arguments share one variable. Every preceding cell remains fresh and independent;
  the matching position preserves the original element; the open tail remains
  an independent variable.
- Length with both arguments fresh generates proper lists of lengths zero through
  five. Partial lists beginning with a supplied atom or two references to the same
  variable generate increasing proper completions. Newly introduced cells are
  distinct fresh variables, independent of the retained prefix variables.

Every new goal uses call_nth to expose the answer ordinal, a previously tested
common predicate. Validation inspects existing structure and variable identity;
it does not fill in missing structure. A bad generated answer throws immediately
instead of filtering that answer out. The adapter must observe ordinals 1–3 and
4–6 in order, with `more=true` after each page. Nothing exhausts these infinite
relations or uses once to disguise a continuation.

Native HTTP uses independent requests at offsets zero and three, followed by a
service recovery query. Native retained sessions and real browser sessions use
next for page two, stop the unfinished query, then execute a deterministic query
in the same session. Every case checks both the answer pages and recovery. HTTP
recovery does not by itself prove internal producer reclamation.

Native calls have an eight-second client deadline. Browser execution has a
120-second watchdog in the host Node process, outside the page running Prolog,
and closes the disposable browser. All normal runs completed and disposed their
nodes/browser. The watchguard is a failure bound, not evidence of success.

## Coverage and remaining work

The [library inventory](../../docs/LIBRARY_TEST_GAPS.md) now records **42 covered
obligations and one needing tests**. LIB-002 and LIB-008 have common bounded
generation evidence. The member and length prose units, B-359 and B-365, are
verified on all five targets, bringing each target to **22 verified source units**.
The [previous inventory](previous-clause-inventory.json) and
[previous ledger](previous-ledger.json) are retained for comparison.

These six-answer observations are regression evidence for the described
infinite relations, not a mathematical proof of all later answers or full ISO
conformance. Signatures and external ISO contracts keep their existing limits.
The earlier 146-case public N5 certificate remains separate and unchanged.

LIB-035, infinite countall noncompletion, stays open. A suitable next fixture
needs a finite countall warm-up and an entry signal, followed by a fixed external
observation window with no count returned, termination and a recovery control.
Native HTTP execution deadlines can stop its worker. In the browser main mode,
a CPU-bound Prolog query can block JavaScript timers in that renderer; its
watchdog and termination must therefore run in the external browser controller,
using a disposable renderer/browser. A timeout alone must not be relabelled as
proof that an infinite count has been computed correctly, and admission errors
must not pass as noncompletion. This batch introduces no infinite countall query.

## Reproduction

```sh
python3 adapters/local_standard_library.py \
  --manifest cases/standard-library-0.4.json \
  --swipl /path/to/swipl --tpl /path/to/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --gnu-root /path/to/gprolog-port --output /fresh/native-output

LIBRARY_RUNTIME_ROOT=/absolute/path/to/swi-wasm-node \
LIBRARY_MANIFEST=/absolute/path/to/cases/standard-library-0.4.json \
LIBRARY_REPORT=/fresh/browser.json NODE_PATH=/path/to/playwright/node_modules \
node adapters/wasm_standard_library.cjs

python3 runner/library_coverage.py --check
python3 -m unittest discover -s runner
```
