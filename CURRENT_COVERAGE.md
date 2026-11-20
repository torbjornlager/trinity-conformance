# Current Web Prolog conformance coverage

The [current issue inventory](CURRENT_ISSUES.md) is the authoritative triage
view. The dated sweep totals below retain their original observations.

Updated **20 November 2026** after the full post-upgrade conformance run.
Repeated versions, modes and routes are observations, not independent defects
or a conformance percentage. Blocked assertions are not passes.

The [fresh full conformance run](reports/2026-11-20-post-uri-full-conformance/REPORT.md) covers
**81 manifests / 2,081 input rows** against the upgraded live
nodes. All primary public selections pass: N0 1; N1/N2/N6 12 each;
N3/N4/N5/N7 118 each. Broader failures, diagnostics, profile exclusions and
4 input rows without execution observations are retained in the report.
N5 automatically restarted during the library run, leaving 51 retained-session
assertions incomplete; those connection failures are reported separately. The complete library,
prompt, cross-node and owned-fixture selections are freshly recorded.

This is fresh execution evidence. The earlier **183-observation** figure belongs
to a reviewed historical repair inventory and is not this sweep's failure count.
[Per-file outcomes](reports/2026-11-20-post-uri-full-conformance/SUMMARY.json),
[case accounting](reports/2026-11-20-post-uri-full-conformance/verification.json) and
[frozen inputs](reports/2026-11-20-post-uri-full-conformance/suite-inputs.json) define the new scope.
No runtime source, deployment setting or quota was changed during testing.

## Canonical URI and context deployment

The [canonical URI deployment](reports/2026-11-20-canonical-uri-live/REPORT.md)
verifies **63/63 live URI/context checks** across N3/N4/N5, **44/44** against the
exact SWI/Trealla images and all **136** visible OPEN exercise checks in the SWI
image. Both CI jobs, all 36 integration groups and the broader live smoke gates
pass. Nine unchanged failure observations are repaired and fifteen mixed
address/visibility assertions are superseded with separate context controls.
That release checkpoint retained **183 unresolved failed observations**; these are repeated
evidence rows, not independent defects. This focused replay preserves the
historical full sweep. Other-runtime URI follow-up remains separate.

## Canonical URI and context candidate

The [canonical URI follow-up](reports/2026-11-20-canonical-uri-qualification/REPORT.md)
records 44/44 on both macOS and Linux against version `node-uri-io-0.2`.
The previous sources record 32 pass / 12 fail under the same case goals,
with both literal aliases authorized for the old exact-key credential fixture.
Only an empty root path is canonicalized; non-root paths and authority,
scheme and port distinctions remain intact. Credentials, topology and controls
share the canonical key. Client context assertions are now separate from
address assertions, and Trealla's peer cache preserves ordinary-name isolation
between hosted clients. Real-peer lifecycle checks observe remote reclamation
through an independent connection. At that candidate checkpoint, production
was unchanged and 207 failed observations remained unresolved. The deployed
follow-up above reconciles only its individually reviewed observations.
N6, N7 and browser URI follow-up and a fresh full sweep remain pending.

## URI/source repair candidate and fixture triage

The [URI/source follow-up](reports/2026-11-20-uri-source-triage/REPORT.md)
qualifies Trealla `d1ad920`: public `clause/2` preserves submitted `write/1`
and `writeln/1` bodies and variable sharing. All 112 unit groups pass on each
of macOS and Linux. The final regression fails on the prior source and passes
on the repair. At that checkpoint N5 was still on `e99126b`; the deployed
follow-up above now includes this repair.

That checkpoint authorized both exact URL spellings in its disposable fixture.
With unchanged case goals, it recorded 17 pass / 9 fail on each platform. Four
original owned credential-precondition failures were classified as fixture
setup. It closed no live findings and retained 207 unresolved failed
observations, down from 211. The later candidate qualification above addresses
canonical returned addresses, qualified local delivery and versioned self-URL
context assertions. All prior reports stay immutable.

## Deployed RPC timeout validation

The [fresh RPC validation follow-up](reports/2026-11-20-rpc-validation-live/REPORT.md)
verifies native SWI `0bf7286` on N0–N4/admin and Trealla `e99126b` on N5,
with demonstrator runtime source `ed70764` and browser provenance `ca8e689`.
All 100 unchanged timeout assertions pass across N1–N5; both exact images
pass all 20 timeout goals and the 45-case ACTOR release gate. All 36 local
integration groups and both GitHub CI jobs pass. Public primary cases pass
354/354, OPEN exercises 30/30, HTTP prompts 76/76 and finite sustained
probes 700/700. Engine bytes, access modes and limits are unchanged.

The inventory now marks 30 repeated timeout failure observations repaired
and deployed: unresolved failed observations decrease from 241 to 211.
These counts are evidence rows, not independent defects. The full sweep
and its raw failures remain immutable; other work queues remain open.
The browser pin changes provenance only; its executable/schema bytes match.

## Local cleanup qualification

The [cleanup follow-up](reports/2026-11-20-cleanup-qualification/REPORT.md)
clears both first-batch Trealla qualification blockers in local test source:
all 111 unit groups pass on macOS and Linux with 30 seconds per check.
The fixes use explicit descendant readiness and unconditional fixture cleanup,
and isolate the five unchanged cache properties. The production cache capacity
and runtime cleanup implementation are unchanged. That checkpoint preceded the RPC deployment above; it does not close other language findings.

## Deployed retirement repair

The [fresh live follow-up](reports/2026-11-20-retirement-live/REPORT.md)
verifies native SWI `0c11f2c` on N0–N4 and admin: N3/N4 each pass all
118 primary ACTOR cases and 100 unchanged NU-003 repetitions. All 30
anonymous exercise checks, 57 HTTP prompt cases and 560 finite sustained
requests pass. The deterministic regression passes in all four candidate
images and the private ACTOR gate passes 45/45. Both GitHub CI jobs pass.
The initial local WASM failure and its passing controls/recheck remain
explicit in the report; the full WASM recheck retains its original assertions
and deadlines.

This focused follow-up resolves the SWI retirement finding on the deployed
selection. It does not rerun the complete library/API suite or close the
other findings below. The complete sweep below ran on predecessor SWI
`e25b230`; its original observations remain immutable.

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
the original NU-003 passes 1,000/1,000. At this triage stage the candidate was
committed and pushed; the subsequent live verification above records its
adoption. The full sweep and its original failures below remain immutable.

## Current release

Native SWI `0c11f2c` / 11.0.0, Trealla `2d5042b` / 3.14.20, ECLiPSe adapter `31dcdfc` and browser package `b2fd3fe` are the selected sources. Demonstrator runtime source is `8318918`. The [admission deployment](reports/2026-11-19-public-admission/REPORT.md) documents configurable public 120-entry presets and their distinct accounting units. Engine versions and concurrency/resource bounds are unchanged. Browser-local execution has no server admission budget.

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

The retained-context selection records **46 pass / 11 fail / 4 blocked**, with six passing closure controls. Source/export and attachment-instrumentation limits remain explicit. The real Chromium browser compatibility selection records **4 pass / 2 fail**, retaining B-SV-006 in Worker and main modes. Monitor packs 0.1 retain the superseded atom-only MC-028/029 expectations. Active packs 0.2 follow the recorded 17 November URI-text contract; their focused verification is in the current issue inventory. Portable-text, document, deadline, HTTP-field and public receive findings retain their raw scope and outcomes.

No runtime, installed engine, assertion, live setting or quota was changed by the sweep. Persistent service/container image identities match the before snapshot, and owned fixture containers were removed. Private admin operations, public browser UI, all security boundaries and external ISO obligations are not certified.

Fresh N7 retained-HTTP prompt coverage: **19 pass**. This uses the maintained ECLiPSe branch and adds coverage absent from the previous report.

## Historical records

The [19 November complete sweep](reports/2026-11-19-upgraded-live-conformance/REPORT.md) remains immutable, including its original N7 rate refusals, N6 capacity refusals and passing paused controls. The [separate admission qualification](reports/2026-11-19-public-admission/REPORT.md) retains its 980 finite live requests and deployment evidence. Neither record is silently substituted for this fresh sweep.


The [earlier SWI11 sweep](reports/2026-11-19-deployed-conformance/REPORT.md), [repair checkpoint](reports/2026-11-19-conformance-repairs/REPORT.md), [naming alignment](reports/2026-11-19-client-naming/REPORT.md), [connection-cleanup diagnosis](reports/2026-11-19-connection-cleanup/REPORT.md), [HTTP context checkpoint](reports/2026-11-19-http-context/REPORT.md), and [OPEN repair](reports/2026-11-19-open-exercise-repair/REPORT.md) retain their dated scope. The [Appendix B matrix](docs/APPENDIX_B_COVERAGE.md) and [library clause inventory](docs/LIBRARY_TEST_GAPS.md) retain their separate obligation evidence.
