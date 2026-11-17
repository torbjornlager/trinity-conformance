# Finite library callback matrices — 5 November 2026

**289/289 shared cases pass in all five runtime modes.** Version 0.3 retains the
original 146 case definitions and source prefix and adds **143 finite callback
cases**, STDLIB-147–289. No runtime, consumer pin, manuscript or public deployment
changes are required for these passing assertions.

The [native report](native/results.json) has 1,445 passes across native SWI and
Trealla fresh HTTP/retained sessions plus GNU HTTP. The [real Chrome report](browser.json)
has 580 passes: 289 standard cases per mode and two existing child/callback
controls. That is 2,023 standard-case observations across seven surfaces, not
2,023 separate language features. All [82 runner self-tests](runner-tests.txt)
pass. Manifest, adapter snapshots, source/executable hashes and exact accounting
are retained in the [verification record](verification.json).

## New assertions

- Every maplist arity: nondeterministic answer order, private partial application,
  captured closure sharing and ordered exactly-once invocation. Every list
  argument can be generated from the others; unequal lengths are tested with
  each position shorter, including the opposite direction of maplist/3.
- Every foldl arity: private pre-applied arguments, nondeterministic/duplicate
  paths, alias-preserving empty accumulators and mismatched input lengths.
- Unused closure variables and callable throwing closures are left uninvoked by
  empty maplist/foldl; vacuous forall leaves its unused test variable untouched.
- Invoked uninstantiated countall/call_nth/forall callbacks raise the documented
  nonbinding error. Application exceptions retain their exact original term
  through every maplist/foldl arity, call_nth and both forall positions, directly
  and inside another meta-call.
- Forall accepts one successful alternative after a failed test branch, commits
  without extra results, preserves binding isolation, and behaves correctly
  inside maplist/findall. The formerly native-specific nested lazy-callback
  observation is now a common assertion on all five modes. Named private
  generators/tests verify caller source lookup for call_nth, countall and forall.

The order probes use a shared logical `flags(A,B)` closure. First/second
positions bind distinct flags; wrong order, repeated invocation or wrong argument
order throws. Final flag checks detect skipped callbacks, and findall detects
extra successful paths. There are no database writes, I/O effects, sleeps or
once-wrappers that could hide extra answers. All generated inputs are finite.

## Coverage changes

The [library checklist](../../docs/LIBRARY_TEST_GAPS.md) now has **40 covered
obligations and three needing tests**. The maplist, foldl and forall prose units
are newly verified on every recorded target, bringing source-unit totals to
20 verified per target. Signature/mode inventories and the common paragraph's
incorporated external ISO call/N contract are not silently promoted.

The remaining selected gaps are LIB-002 (fresh-list member generation), LIB-008
(fresh/partial-list length enumeration) and LIB-035 (noncompletion of infinite
countall generators). They need bounded answer collection or cancellable external
fixtures; no unbounded query is introduced by this batch. Full external ISO
coverage and other unmapped Appendix B units remain separate work.

## Preserved test-development observations

The [initial manifest](invalid-initial-manifest.json) used assertz for callback
tracing. ACTOR sessions and both browser modes passed all 260 initial cases,
but every stateless native source load rejected the helper's database write in
ISOBASE. The source was invalid for those endpoints; these 780 rejections are
preserved in `invalid-initial-native/`, not labelled runtime semantic defects.
No profile or permission was broadened to make the tests pass.

Replacing that trace with logical flags yielded a complete passing 260-case
run, preserved in `first-logical-flags-pass/`. A passing 279-case exception matrix
is preserved in `exception-matrix-first-pass/`. The final 289-case selection adds
callable throwing-closure empty controls and uses the exact final source in all
native and browser results. Passing intermediate counts are not added to the
final coverage totals. The previous [ledger](previous-ledger.json) and
[clause inventory](previous-clause-inventory.json) remain available for comparison.

## Reproduction

```sh
python3 adapters/local_standard_library.py \
  --manifest cases/standard-library-0.3.json \
  --swipl /path/to/swipl --tpl /path/to/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --gnu-root /path/to/gprolog-port --output /fresh/native-output

LIBRARY_MANIFEST=/absolute/path/to/cases/standard-library-0.3.json \
LIBRARY_REPORT=/fresh/browser.json NODE_PATH=/path/to/playwright/node_modules \
node /path/to/swi-wasm-node/tests/wasm/swi_wasm_library_browser.cjs

python3 runner/library_coverage.py --check
```

The existing 146-case public N5 certificate remains unchanged. These are local
source and real-browser observations, not a new public transport certificate.
