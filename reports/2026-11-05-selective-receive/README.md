# Selective receive audit and repair — 5 November 2026

**29/29 cases pass on all four ACTOR modes:** native SWI, Trealla, real Chrome
Worker and real Chrome main. The [native](native/results.json) and
[browser](browser.json) reports each have 58 passes, for **116 observations**.
Version 0.2 preserves SR-001–006 and adds 23 assertions, SR-007–029.
GNU ISOBASE is outside this ACTOR requirement; it is not assigned passing cases.

The source repairs are committed and pushed:

- Native SWI: `80e3e79`, relative receive timeout precedence.
- Browser runtime: `9fe8a60`, receive budgets/deadlines and request identifier repair.
- Trealla needs no runtime change for these assertions.

The book already specifies the tested rules. Public consumer pins and services
are unchanged; this report qualifies development sources rather than a rollout.
[Verification](verification.json) pins commits, exact test inputs and counts.
The executed runtime file hashes match the committed files.

## Assertions and repairs

The selection checks message arrival order before clause order, first-accepting
clause commitment, consumed messages after body failure/exception, all alternatives
of one selected body, cut scope, one-sided matching, tentative binding rollback,
first-solution guards and ordinary guard exceptions. It also checks empty clauses,
default/zero timeouts and callback success, failure, exceptions and alternatives.

Deadline checks exercise past and future absolute times, relative timeout
precedence in both directions and continuous unmatched traffic during relative
and absolute waits. The producer explicitly receives its helper source. A ready
message and first-noise barrier precede the wait; queued noise is checked after
expiration, then the producer is killed and its monitor notification consumed.
An external eight-second query bound prevents a broken wait from running forever.

Native SWI previously let an expired absolute deadline defeat a supplied positive
relative timeout. It now validates the options, removes the superseded absolute
deadlines and computes one relative wait deadline. Zero remains a queue poll;
original callback options and control-safe message acquisition are preserved.

Both browser modes previously ignored absolute deadline options and restarted a
relative timeout whenever a new unmatched message arrived. They now resolve one
budget at receive entry, retain it across skipped/control-filtered messages, and
compute the remaining time before each wait. Relative timeout takes precedence;
expired absolute waits run their timeout callback.

Two Worker cases also stopped before receive began. Delayed-send/cancel payloads
used `id`, overwriting the request's transport correlation ID. The coordinator's
reply therefore could not find the pending request. These operations now carry
`delayId`, while internal request ID/action fields are assigned after the payload.
SR-026 exercises a supplied timer identifier; SR-027 confirms cancel returns and
prevents that scheduled delivery. These are single-actor controls; cross-actor
identifier isolation and the complete cancel contract remain separate mapping.

## Ledger changes and remaining clause

The [clause map](clause-map.json) maps the receive signature and nine prose units,
B-098–103 and B-105–108, to exact passing case IDs on every applicable mode.
This adds **ten verified source units** per ACTOR target: 33 verified each on
SWI, Trealla, Worker and main. GNU remains at 23 verified and 244 inapplicable.
The [previous ledger](previous-ledger.json) is retained.

**B-104 stays unverified.** Ordinary guard errors and rollback pass; actual abort,
termination and enforced execution-limit signals during a running guard still
need common controlled probes, including original mailbox position. The broad
regression suites contain supporting control observations, but are not silently
used as complete clause mapping. Other Appendix B requirements and external ISO
semantics remain separate work. The 43 mapped library obligations stay covered.

## Regression qualification

All 98 [conformance runner checks](runner-tests.txt) pass. Native
[LINT/TEXT](native-LINT-TEXT.txt), [T0/T2](native-T0-T2.txt) and
[T1_NATIVE/T3_NATIVE/T4_NATIVE](native-T1-T3-T4.txt) pass, including the acquisition
handoff and zero-poll controls. Native tests now include relative precedence over
expired deadlines in both option orders and zero-poll precedence.

All six [packaged browser groups](browser-regressions/results.json) pass:
worker mailbox, standalone, full semantic contracts, standard-library browser,
session API browser and selective receive browser. [Schema equivalence](browser-schema.txt)
and [statechart units](browser-statechart.txt) also pass. The engine and schema
pins are unchanged. The upstream runner now maintains the receive browser group.

The qualified package was built with the passing 27-case selection; its exact
[fixture](packaged-regression-manifest.json) and [package manifest](qualified-browser-package-manifest.json)
are retained. Two final absolute-deadline checks then extended the common and
upstream fixture to 29 cases; all 29 ran on all four modes in the final reports.
The runtime code is identical between those runs. This distinction avoids
claiming that the packaged regression group itself ran 29 cases.

## Preserved baseline and fixture observations

The corrected 25-case baseline had [one native failure](before-native/results.json)
and [six browser failures](before-browser.json). Its first 25 definitions are
unchanged in the final selection. Native SR-023 exposed timeout precedence;
browser SR-021 and SR-025 exposed ignored deadlines and restarted timeouts;
Worker SR-022/023 additionally exposed delayed-send request correlation.

`initial-invalid-producer/` preserves the earlier helper-copy mistake. SR-025's
child lacked its source, so those producer failures do not establish timeout
semantics. Explicit child source fixes the fixture; it does not widen policy.
`deadline-repair-before-id-fix/` retains the intermediate 50 native passes and
48 browser passes/two Worker failures. The [delay diagnostic](delay-diagnostic/)
shows references succeeding while Worker delayed sends cannot complete.
`before-bridge-fix-regressions/` preserves the packaged regression failure before
the identifier repair. `passing-27-case-selection/` retains the first fully
passing matrix. None of these intermediate totals are added to final coverage.

## Reproduction

```sh
python3 adapters/local_actor_cases.py \
  --swipl /path/to/swipl --tpl /path/to/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --manifest cases/selective-receive-0.2.json --output /fresh/native-output

LIBRARY_RUNTIME_ROOT=/absolute/path/to/swi-wasm-node \
LIBRARY_MANIFEST=/absolute/path/to/cases/selective-receive-0.2.json \
LIBRARY_REPORT=/fresh/browser.json NODE_PATH=/path/to/playwright/node_modules \
node adapters/wasm_actor_cases.cjs

python3 runner/appendix_coverage.py --manual /path/to/appendix-B-current-manual.tex --check
python3 runner/library_coverage.py --check
```
