# Current Web Prolog conformance coverage

Updated **20 November 2026** after a fresh complete sweep of the admission release. The inventory contains **78 manifests / 1,984 input rows**, at suite revision `aeb1329`. **It is not all-green.** Repeated versions, modes and routes are not independent language features; blocked assertions are not passes.

[Full report](reports/2026-11-20-live-conformance/REPORT.md) · [per-file results](reports/2026-11-20-live-conformance/SUMMARY.json) · [case inventory](reports/2026-11-20-live-conformance/verification.json) · [frozen inputs](reports/2026-11-20-live-conformance/suite-inputs.json).

## Focused regression follow-up

The [targeted follow-up](reports/2026-11-20-regression-triage/REPORT.md)
compares matching previous passes with the full sweep below. Its 124 changed
observations comprise 121 N6 capacity refusals, two SWI NU-003 observations,
and one N6 localhost transport error. All 55 supporting capacity assertions
and LOCAL-001 pass after the expiry precondition; LOCAL-001 passes three
consecutive repetitions. The earlier 66 library refusals already have passing
paused controls. The exact localhost transport-error cause remains unproven.

NU-003 reproduces on both unchanged SWI revisions: 3/1,000 failures on
`a2ff186`, 2/1,000 on `e25b230`. A deterministic barrier confirms the existing
retirement-order race. Source fix `0c11f2c` retires PID mappings before monitor
notification; its new regression test and all eight native tiers pass, and
the original NU-003 passes 1,000/1,000. This candidate is committed and pushed;
consumer pins and live images still select the preceding runtime. The full
sweep and its original failures below remain immutable.

## Current release

Native SWI `e25b230` / 11.0.0, Trealla `2d5042b` / 3.14.20, ECLiPSe adapter `31dcdfc` and browser package `0d024e5` are the selected sources. The [admission deployment](reports/2026-11-19-public-admission/REPORT.md) documents configurable public 120-entry presets and their distinct accounting units. Engine versions and concurrency/resource bounds are unchanged. Browser-local execution has no server admission budget.

## Primary public selections

| Node | Result |
|---|---|
| N0 | 1 pass |
| N1 | 12 pass |
| N2 | 12 pass |
| N3 | 118 pass |
| N4 | 118 pass |
| N5 | 118 pass |
| N6 | 12 pass |
| N7 | 118 pass |

N0 selects RELATION error admission, N1/N2/N6 select the HTTP baseline, and N3/N4/N5/N7 select 106 ACTOR cases plus 12 HTTP cases. N7 now passes its complete primary selection without the previous sweep’s five rate refusals. Broader supporting API observations are separate and remain mixed. This run additionally covers N7 in that extended selection; those new observations are not automatically regressions.

## Live standard-library versions 0.1–0.4

The four versions contain 842 input rows per transport; the live matrix records 9,262 observations. Stateless requests have 0.8-second start spacing, retained sessions preserve stop/recovery assertions, and N6 receives 303-second quiet periods before bounded generators.

| Node | HTTP | Retained WSS |
|---|---|---|
| N1 | 842 pass | not exposed |
| N2 | 842 pass | not exposed |
| N3 | 842 pass | 842 pass |
| N4 | 842 pass | 842 pass |
| N5 | 842 pass | 842 pass |
| N6 | 776 pass, 66 fail | not exposed |
| N7 | 842 pass | 842 pass |

N6’s original query-capacity refusals remain in the first-observation files. Separate unchanged controls after the retention-expiry pause record **66 pass**. These are HTTP 503 capacity outcomes, distinct from timed admission and from language assertion failures. Passing controls do not erase the original refusals.

## Additional finite admission and HTTP prompts

The run also records 95 paced live HTTP prompt observations on N2/N3/N4/N5/N7 and 980 fresh finite admission probes on N1–N7 after the broader sweep. Their actual outcomes, 120-entry metadata and unchanged-policy comparisons are in the full report, outside the 78-manifest input-row count. N7’s prompt pack is additional coverage relative to the previous report.

## Owned and supplementary observations

The three current-image private ACTOR gates pass 45 release plus seven source-directive cases each. Authenticated and anonymous retained HTTP contexts pass 3/3 each, client naming passes 16/16, bounded noncompletion passes 3/3, and enabled owned HTTP prompts pass 19/19 per native runtime. Runner tooling passes all 114 unit tests. Live prompt counts and all twelve directed ACTOR interoperation pairs are in the full report.

The retained-context selection records **46 pass / 11 fail / 4 blocked**, with six passing closure controls. Source/export and attachment-instrumentation limits remain explicit. The real Chromium browser compatibility selection records **4 pass / 2 fail**, retaining B-SV-006 in Worker and main modes. MC-028/029 preserve their original URI expectations; portable-text, document, deadline, HTTP-field and public receive findings retain their raw scope and outcomes.

No runtime, installed engine, assertion, live setting or quota was changed by the sweep. Persistent service/container image identities match the before snapshot, and owned fixture containers were removed. Private admin operations, public browser UI, all security boundaries and external ISO obligations are not certified.

Fresh N7 retained-HTTP prompt coverage: **19 pass**. This uses the maintained ECLiPSe branch and adds coverage absent from the previous report.

## Historical records

The [19 November complete sweep](reports/2026-11-19-upgraded-live-conformance/REPORT.md) remains immutable, including its original N7 rate refusals, N6 capacity refusals and passing paused controls. The [separate admission qualification](reports/2026-11-19-public-admission/REPORT.md) retains its 980 finite live requests and deployment evidence. Neither record is silently substituted for this fresh sweep.


The [earlier SWI11 sweep](reports/2026-11-19-deployed-conformance/REPORT.md), [repair checkpoint](reports/2026-11-19-conformance-repairs/REPORT.md), [naming alignment](reports/2026-11-19-client-naming/REPORT.md), [connection-cleanup diagnosis](reports/2026-11-19-connection-cleanup/REPORT.md), [HTTP context checkpoint](reports/2026-11-19-http-context/REPORT.md), and [OPEN repair](reports/2026-11-19-open-exercise-repair/REPORT.md) retain their dated scope. The [Appendix B matrix](docs/APPENDIX_B_COVERAGE.md) and [library clause inventory](docs/LIBRARY_TEST_GAPS.md) retain their separate obligation evidence.
