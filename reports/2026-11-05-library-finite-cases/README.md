# Finite library modes and errors — 5 November 2026

The shared `standard-library-0.2` selection adds **34 new cases**, STDLIB-113–146,
to the byte-identical original 112 cases. The private source fixture is unchanged.
No runtime code, pins, browser fixture copy or public configuration is modified.
The native adapter adds explicit `--manifest` selection while retaining its 0.1
default. Browser tests use the upstream runner's existing manifest override.

## Results

The complete 146-case selection passes on native SWI and GNU and real Chrome
Worker/main modes. Trealla passes 144/146 through both fresh HTTP and retained
sessions. Its two failures are the same semantic defect on both transports:

- STDLIB-134: `succ(1.5,V)` reports `instantiation_error`.
- STDLIB-137: `succ(V,1.5)` reports `instantiation_error`.

Both require `type_error(integer,1.5)` with the original float culprit under the
committed integer-argument and common error rules. Separate [raw HTTP error
captures](trealla-succ-error-observations.json) confirm the actual formal terms;
the test expectations were not relaxed. Native source revisions and executable
hashes are in [native results](native/results.json).

There are 730 native observations (SWI/Trealla fresh and session surfaces, GNU
fresh): 726 pass, four fail. The [browser report](browser.json) has 294 passes:
146 shared cases per mode plus one existing child/callback control per mode.
Thus the shared cases have 1,018 passes and four failures across seven surfaces;
repeated transports are not additional language features. Browser assets and
manifest hashes are retained. All 80 [runner self-tests](runner-tests.txt) pass.

The clause inventory now has **27 covered, 15 needing tests, one failing**.
The failing clause is LIB-019; the other four modes cover it. Six finite prose
units are promoted on passing targets (append, select, nth, between, succ and
call_nth). Trealla's succ unit and the common wrong-type error rule are marked
failing against the new observations. Incomplete signatures, fresh-list
enumeration, infinite generators and broader callback combinations remain open.

## Added boundaries

The cases cover prefix removal/mismatch, pairwise freshness in partial list
construction, ordered select/nth insertion with sharing, nth1 removal, all four
out-of-range nth forms, reversed integer intervals, both bound positions'
instantiation/integer errors, succ supplied pairs/zero/invalid arguments,
call_nth negative/noninteger index validation before goal effects, bounded
selection before a throwing later alternative, and shared countall output
variables on successful and mismatched counts.

Succ's negative-input tests require the documented common domain-error form,
original culprit and a concrete domain atom; they do not invent a portable
API-specific domain name absent from the manual. Call_nth's domain name is
specified and checked exactly. Error contexts remain diagnostic.

## Invalid first fixture, retained separately

The first version of STDLIB-116 directly called a nondeterministic select goal
and expected a final one-solution page. A valid residual choicepoint produced
`More=true`; subsequent retained queries were blocked by the unfinished query.
That is a fixture mistake, not an implementation conformance failure. The
[initial manifest](invalid-initial-manifest.json), browser observations and logs
are preserved. The partial native run was interrupted after the same cascade;
its listener was cleaned up. Its driver/log remain, without a completed report.

The corrected assertion uses `findall` to exhaust the finite choices while
checking fresh variable identity and remainder order. No once-wrapper hides
extra solutions. The complete native/browser selections were rerun from clean
fixtures. Their only remaining failures are the two Trealla succ cases above.

## Reproduction

```sh
python3 adapters/local_standard_library.py \
  --manifest cases/standard-library-0.2.json \
  --swi-root /path/to/swi-prolog-node --swipl /path/to/swipl \
  --trealla-root /path/to/trealla-port --tpl /path/to/tpl \
  --gnu-root /path/to/gprolog-port --output /fresh/native-report-directory

LIBRARY_MANIFEST=/absolute/path/to/cases/standard-library-0.2.json \
LIBRARY_REPORT=/fresh/browser-report.json \
NODE_PATH=/path/to/playwright/node_modules node \
  /path/to/swi-wasm-node/tests/wasm/swi_wasm_library_browser.cjs

python3 runner/library_coverage.py --check
```

The complete manifest and executed adapter snapshots accompany the results.
This is source qualification with known failures, not a public deployment
certificate or full Appendix B certification. No Trealla repair is claimed.

The ledger also incorporates book `3edc369`, whose three formatting edits were reviewed as content-identical to the tested `364ee0b` text. No runtime rerun was needed for that layout-only source refresh.
