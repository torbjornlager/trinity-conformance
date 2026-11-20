# Targeted regression triage — 20 November 2026

**The N6 failures clear under correct resource preconditions. A pre-existing SWI actor-retirement race is reproduced and fixed in a tested source candidate.** The fix is committed and pushed; the live nodes still use the preceding runtime revision.

[Comparison data](comparison.json) · [N6 replays](n6/results.json) · [source fix](source/fix.patch) · [summary](SUMMARY.json). The [full sweep](../2026-11-20-live-conformance/REPORT.md) and [preceding sweep](../2026-11-19-upgraded-live-conformance/REPORT.md) remain immutable.

## Comparison method

The comparison matches report path, case ID, candidate, route and peer in directly comparable files. It selects earlier passes that became failures; it excludes out-of-scope and superseded/invalid attempts. These are observation transitions, not 124 distinct defects or language features. New extended N7 coverage is not classified as a regression without an earlier matching execution.

| Matched transitions | Evidence and disposition |
|---|---|
| 121 N6 query-capacity refusals|66 library cases already pass in paused controls in the full report; the remaining 55 supporting cases all pass in this follow-up|
| 2 SWI NU-003 failures, on N3/N4|One shared, pre-existing retirement race; reproduced in both source revisions and repaired in the candidate|
| 1 N6 LOCAL-001 transport error|The original assertion passes on three consecutive replays after the initial expiry; the specific transport-error cause remains unproven|

## N6 clean replay

One sequential client waits 303 seconds before starting. It runs 54 finite supporting assertions, then LOCAL-001 three times. PE-017, whose first page deliberately retains a continuation, has a separate 303-second quiet period before execution. A final 303-second expiry and finite recovery check complete the run. No production quota, idle timeout or concurrency bound changes.

All 56 distinct target assertions pass. The two additional LOCAL-001 repetitions also pass: 58 recorded observations in total. The four supporting groups that previously suffered cascading 503s are ordinary timeout-option validation, introspection, successor and URI checks; their failures did not establish broken language assertions because admission refused execution.

The earlier full sweep allowed retained queries from preceding API tests to consume N6 slots, then continued other cases and began its library phase after only 61 seconds. N6 retains idle queries for 300 seconds. This was a scheduling error in the test orchestration. Future runs must apply the retention-expiry precondition at relevant case/group boundaries, or use disposable fixtures for continuation-owning tests; pacing only by requests/minute is insufficient.

LOCAL-001 returning a generic transport error is consistent with a refused nested localhost request, but this follow-up does not prove that mechanism. An additional uncontained-controller diagnostic could not establish a passing clean baseline. Its loopback/auth environment differs from the public presenter/broker. Those [unqualified diagnostics](n6/owned-capacity/results.json) are retained and excluded from causal conclusions and passing case counts.

## SWI NU-003 reproduction and fix

The old/current images use identical SWI 11.0.0 engine inventories. Their actor implementation is unchanged between native a2ff186 and e25b230. The original NU-003 case and helper source are unchanged. Fixtures have the same generous admission budgets and resource bounds so this comparison does not measure public quotas.

| Runtime source | Original NU-003, 1,000 repetitions |
|---|---|
| Previous a2ff186 | 997 pass, 3 cleanup failures |
| Current e25b230 | 998 pass, 2 cleanup failures |
| Fixed candidate 0c11f2c | 1,000 pass, 0 failures |

The small difference between 3 and 2 failures is not evidence of a changed failure rate. Both reproduce the same old bug. A controlled delivery barrier establishes the mechanism deterministically: through the existing send hook, deliver down/3, pause the sender, and inspect actors/1 from the observer. Both unmodified revisions still list the terminated actor; the fixed candidate does not.

Previously stop/2 sent monitor notifications before retracting PID/thread mappings. The receiver could run actors/1 inside that window. The fix retracts those mappings before delivery, under the existing lifecycle/registry locks; it preserves monitor withdrawal synchronization and computes the exit reason before retirement. No sleeps or relaxed assertions are added to runtime behavior.

The new deterministic [regression test](source/retirement_order_tests.pl) fails on both unchanged images and passes with the fix. It is part of T0. All eight native tiers pass on local SWI-Prolog 11.0.0: LINT, TEXT, T0, T1_NATIVE, T2, T3_NATIVE, T4_NATIVE and T5. This includes monitor/postmortem, supervision, remote interoperation and HTTP ownership checks. The fixed runtime also passes the original case 1,000 times with unchanged engine bytes.

Published source: [0c11f2c](https://github.com/torbjornlager/swi-prolog-node/commit/0c11f2c55604aaff66b1a0bf32c3e3eb75fa5c8b). The candidate was tested as an explicit overlay on the current image; its actor-file hash matches the committed source. Consumer dependency pins and live images have not yet selected this fix.

## What remains

This follow-up accounts for 121 capacity refusals, repairs one old race, and leaves the cause of one transport error open. It does not repair the existing retained-context, Trealla SR-015, browser B-SV-006 or other supporting findings in the full report. The source fix needs the normal consumer qualification and deployment before the live SWI nodes benefit. The cause of the one transient N6 localhost transport error remains an open attribution question despite three passing replays.

Production service identities/images match their before snapshot. Owned probe containers are removed. JSON evidence, operator source, setup-attempt logs and native validation logs are retained; exported artifacts are covered by [SHA-256 hashes](files-sha256.json).
