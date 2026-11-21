# Full live conformance after the 21 November release — 21 November 2026

Fresh execution of **81 manifests / 2,081 input rows** at suite `a7a4a7bd5600f14e24e83396ba9b4a699ea072f3`, against the live nodes after the 21 November conformance release. Every result was executed for this run; nothing was copied from earlier runs. Repeated cases, versions, transports and nodes are separate observations, not independent defects or a conformance percentage.

[Per-file outcomes](SUMMARY.json) · [case inventory](verification.json) · [comparison with 20 November](COMPARISON.json) · [frozen inputs](suite-inputs.json) · [provenance](execution/provenance.json) · [preservation](preservation.json) · [orchestration changes](execution/orchestration-changes.json)

## Runtime selection and conditions

N0–N4 and admin: native SWI `9239028` / SWI-Prolog 11.0.0, demonstrator `6fc9db8`, browser `4c784f9`. N5: Trealla `49377b5` / 3.14.20. N6: gprolog-port `8eeb3f8`. N7: eclipse-node `a1aef63` worker and adapter. Owned native fixtures use snapshots of these deployed images.

The orchestration is the 20 November sweep's, with only paths, dates and pins changed; every other change is listed in [orchestration-changes.json](execution/orchestration-changes.json). Admission budgets and pacing are unchanged: one sequential controller per endpoint, HTTP calls 0.8 s apart, retained sessions 2.1 s, prompt sessions 4 s, N6 waits 303 s before its library phase. No runtime, setting or quota changed during the run, and no persistent service restarted (in contrast to 20 November, when N5 restarted on its own).

Suite changes since 20 November (`6dd7809` → `a7a4a7b`): six files, no added or removed manifests ([input-comparison.json](execution/input-comparison.json)). Runner self-tests: 126 pass.

**After the sweep, N5 was rolled back** to its pre-release behaviour because of the receive-guard regression below. N5 results in this report describe Trealla `49377b5` as it ran during the sweep.

## Primary public selections

| Node | Profile | Fresh result |
|---|---|---|
| N0 | RELATION | 1 pass |
| N1 | ISOBASE | 12 pass |
| N2 | ISOTOPE | 12 pass |
| N3 | ACTOR | 118 pass |
| N4 | ACTOR | 118 pass |
| N5 | ACTOR | 118 pass |
| N6 | ISOBASE | 12 pass |
| N7 | ACTOR | 118 pass |

## Comparison with 20 November

Rows are matched by file, case, candidate and occurrence ([COMPARISON.json](COMPARISON.json)). **263 rows changed from fail to pass, 6 from pass to fail, and 129 still fail.** Failed rows fell from 399 to 135.

150 rows exist only on 20 November: the N6 capacity-refusal replays (none were needed this time: zero N6 capacity refusals) and native promise outputs that this run records under the provenance reruns instead (`procps-rerun/`), as 20 November also did.

| Node / fixture | Failed 20 Nov | Failed 21 Nov | Fixed | New failures |
|---|---|---|---|---|
| n1 | 5 | 4 | 1 | 0 |
| n2 | 5 | 4 | 1 | 0 |
| n3 | 17 | 13 | 4 | 0 |
| n4 | 17 | 13 | 4 | 0 |
| n5 | 82 | 13 | 69 | 0 |
| n6 | 78 | 6 | 65 | 0 |
| n7 | 81 | 22 | 59 | 0 |
| fixture | 4 | 0 | 4 | 0 |
| fixture:gnu | 6 | 0 | 6 | 0 |
| fixture:gnu-direct-api | 8 | 2 | 6 | 0 |
| fixture:swi | 39 | 27 | 12 | 0 |
| fixture:swi-wasm-main | 1 | 1 | 0 | 0 |
| fixture:swi-wasm-worker | 1 | 1 | 0 | 0 |
| fixture:trealla | 55 | 29 | 32 | 6 |

### By pack and node

Only packs with a failure on either day.

| Pack | Node / fixture | Failed 20 Nov | Failed 21 Nov |
|---|---|---|---|
| (aggregate adapter) | fixture:gnu | 6 | 0 |
| (aggregate adapter) | fixture:gnu-direct-api | 8 | 2 |
| (aggregate adapter) | fixture:swi | 3 | 0 |
| (aggregate adapter) | fixture:trealla | 9 | 1 |
| (aggregate adapter) | n5 | 3 | 0 |
| (aggregate adapter) | n6 | 7 | 0 |
| browser-local-compatibility-0.1 | fixture:swi | 2 | 2 |
| browser-local-compatibility-0.1 | fixture:swi-wasm-main | 1 | 1 |
| browser-local-compatibility-0.1 | fixture:swi-wasm-worker | 1 | 1 |
| browser-local-compatibility-0.1 | fixture:trealla | 2 | 2 |
| browser-local-compatibility-0.1 | n3 | 2 | 2 |
| browser-local-compatibility-0.1 | n4 | 2 | 2 |
| browser-local-compatibility-0.1 | n5 | 2 | 2 |
| browser-local-compatibility-0.1 | n7 | 2 | 2 |
| call-arity-admission-0.1 | n7 | 3 | 0 |
| demonstrator-tutorials-0.1 | n7 | 1 | 0 |
| error-contract-0.1 | n6 | 1 | 1 |
| http-fields-0.1 | n6 | 2 | 2 |
| http-fields-0.1 | n7 | 10 | 0 |
| http-transport-options-0.1 | fixture:trealla | 6 | 0 |
| http-transport-options-0.1 | n5 | 6 | 0 |
| isobase-diagnostics-0.1 | fixture:swi | 5 | 5 |
| isobase-diagnostics-0.1 | fixture:trealla | 5 | 5 |
| isobase-error-admission-0.1 | n1 | 1 | 1 |
| isobase-error-admission-0.1 | n2 | 1 | 1 |
| isobase-error-admission-0.1 | n3 | 1 | 1 |
| isobase-error-admission-0.1 | n4 | 1 | 1 |
| isobase-error-admission-0.1 | n5 | 1 | 1 |
| isobase-error-admission-0.1 | n7 | 1 | 1 |
| local-node-rpc-0.1 | fixture:trealla | 7 | 0 |
| local-node-rpc-0.1 | n1 | 2 | 2 |
| local-node-rpc-0.1 | n2 | 2 | 2 |
| local-node-rpc-0.1 | n3 | 2 | 2 |
| local-node-rpc-0.1 | n4 | 2 | 2 |
| local-node-rpc-0.1 | n5 | 2 | 2 |
| local-node-rpc-0.1 | n6 | 2 | 2 |
| local-node-rpc-0.1 | n7 | 2 | 2 |
| monitor-contracts-0.1 | fixture:swi | 4 | 4 |
| monitor-contracts-0.1 | fixture:trealla | 4 | 4 |
| monitor-contracts-0.1 | n3 | 2 | 2 |
| monitor-contracts-0.1 | n4 | 2 | 2 |
| monitor-contracts-0.1 | n5 | 2 | 2 |
| monitor-contracts-0.1 | n7 | 2 | 2 |
| monitor-preflight-0.1 | fixture:swi | 4 | 4 |
| monitor-preflight-0.1 | fixture:trealla | 4 | 4 |
| monitor-preflight-0.1 | n3 | 2 | 2 |
| monitor-preflight-0.1 | n4 | 2 | 2 |
| monitor-preflight-0.1 | n5 | 2 | 2 |
| monitor-preflight-0.1 | n7 | 2 | 2 |
| native-library-callbacks-0.1 | n7 | 4 | 0 |
| native-supervisor-lifecycle-0.1 | n7 | 5 | 4 |
| node-uri-io-0.1 | fixture:swi | 3 | 3 |
| node-uri-io-0.1 | fixture:trealla | 3 | 3 |
| node-uri-io-0.1 | n3 | 3 | 3 |
| node-uri-io-0.1 | n4 | 3 | 3 |
| node-uri-io-0.1 | n5 | 3 | 3 |
| node-uri-io-0.1 | n7 | 13 | 0 |
| node-uri-io-0.2 | n7 | 21 | 6 |
| partial-page-errors-0.1 | n1 | 1 | 0 |
| partial-page-errors-0.1 | n2 | 1 | 0 |
| partial-page-errors-0.1 | n5 | 1 | 0 |
| partial-page-errors-0.1 | n6 | 4 | 0 |
| partial-page-errors-0.1 | n7 | 7 | 2 |
| portable-text-0.2 | fixture | 4 | 0 |
| portable-text-0.2 | n3 | 4 | 0 |
| portable-text-0.2 | n4 | 4 | 0 |
| portable-text-0.2 | n5 | 4 | 0 |
| portable-text-0.2 | n7 | 4 | 0 |
| receive-control-0.1 | fixture:trealla | 0 | 6 |
| reference-contracts-0.1 | n6 | 1 | 0 |
| reference-contracts-0.1 | n7 | 1 | 0 |
| relation-error-admission-0.1 | n1 | 1 | 1 |
| relation-error-admission-0.1 | n2 | 1 | 1 |
| relation-error-admission-0.1 | n3 | 1 | 1 |
| relation-error-admission-0.1 | n4 | 1 | 1 |
| relation-error-admission-0.1 | n5 | 1 | 1 |
| relation-error-admission-0.1 | n6 | 1 | 1 |
| relation-error-admission-0.1 | n7 | 1 | 1 |
| retained-context-0.1 | fixture:swi | 4 | 4 |
| rpc-timeout-0.1 | fixture:swi | 9 | 0 |
| rpc-timeout-0.1 | fixture:trealla | 11 | 0 |
| rpc-timeout-0.1 | n6 | 20 | 0 |
| runtime-introspection-0.1 | n6 | 10 | 0 |
| selective-receive-0.2 | n5 | 4 | 0 |
| standard-library-0.4 | n5 | 51 | 0 |
| statechart-document-0.1 | fixture:swi | 5 | 5 |
| statechart-document-0.1 | fixture:trealla | 4 | 4 |
| successor-validation-0.1 | n6 | 20 | 0 |
| successor-validation-0.1 | n7 | 2 | 0 |
| uri-atoms-0.1 | n6 | 10 | 0 |

## Brief expectations

Expected to stop failing:

| Rows | 20 Nov | 21 Nov |
|---|---|---|
| PE-008 | 2 pass, 5 fail | 6 pass, 1 fail |
| SR-015 on N5 | 7 fail | 7 pass |
| PE-014..018 on N6 and N7 | 1 pass, 8 fail, 2 not_applicable | 8 pass, 2 not_applicable |
| SU-HTTP-016 on N6 and N7 | 3 fail | 2 pass |
| URI-001..006, URI-010 on N6 | 1 pass, 13 fail | 7 pass |
| TXT-019/023/024/026 | 16 fail, 12 not_applicable | 16 pass, 12 not_applicable |
| OPT-004, URI-007, URI-011 on SWI and Trealla (live and fixtures) | 15 pass, 6 fail, 6 not_applicable | 20 pass, 1 fail, 6 not_applicable |
| HTTP-FIELD-024..026, 051..053 on N5 | 6 fail | 6 pass |
| CA-002, CA-013/014 on N7 | 3 fail | 3 pass |
| LC-082/083/087/088 on N7 | 4 fail | 4 pass |
| N7 failed rows reporting "Invalid request or goal" | 37 | 0 |

Remaining PE-008 failure: N7 with `limit=5&timeout=1` returns `success([a],true)`; `timeout` alone gives `resource_error(time)`. URI-007 still fails in the owned Trealla fixture (standalone boundaries); it passes on live N5 and the SWI fixture.

Expected to remain:

| Rows | 20 Nov | 21 Nov |
|---|---|---|
| NU-020/021 on N7 | 2 fail | 2 fail |
| ER-007 on N6 | 1 fail | 1 fail |
| HTTP-CTL on N6 | 6 pass, 2 fail | 6 pass, 2 fail |
| SL-014..017 on N7 | 4 fail | 4 fail |
| LOCAL-006/007 live | 14 fail | 14 fail |

SL-014..017 on sandbox-off N7 are still recorded as failures; marking them not applicable is a harness change that has not been made.

## Regression: receive guards on Trealla

Receive-control RG-001, RG-002, RG-003, RG-005, RG-006 and RG-007 pass on 20 November and fail in this run in the owned Trealla fixture (`timed out`, `missing_time_error`, `missing_termination`). They check that abort, the configured execution limit and actor termination propagate while an entered receive guard waits in `rpc/2`.

Controls in the same lab image: predecessor Trealla `d451596` passes all eight cases; `7a8e8ce`, `a4739ed` and `49377b5` each fail the same six. The regression is introduced by `7a8e8ce` ("Keep receive body cuts local and align rpc timeouts and options with the manual"): `rpc.pl` now maps every `time_limit_exceeded` raised during the HTTP read to `rpc_error(http_timeout)`, including the owner's execution limit, and inside a guard an rpc error is a non-match. Live N5 was rolled back after this sweep; the fix belongs in trealla-port.

## Remaining failures by category

Categories follow the 20 November status classification. Rows that do not match a recorded category are left unclassified rather than guessed.

| Category | Rows | Packs |
|---|---|---|
| Superseded 0.1 assertions (the 0.2 pack passes on the same node/fixture) | 47 | monitor-contracts-0.1, monitor-preflight-0.1, node-uri-io-0.1 |
| Unclassified: unchanged since 20 November, needs triage | 32 | (aggregate adapter), browser-local-compatibility-0.1, isobase-diagnostics-0.1, isobase-error-admission-0.1, node-uri-io-0.2, partial-page-errors-0.1, retained-context-0.1, statechart-document-0.1 |
| Out-of-scope rows (profile or environment exclusion) | 24 | browser-local-compatibility-0.1, isobase-error-admission-0.1, relation-error-admission-0.1 |
| Live prerequisite missing: needs a peer serving local_node_loaded/1 | 14 | local-node-rpc-0.1 |
| Real defect: regression in Trealla 7a8e8ce (N5 rolled back after the sweep) | 6 | receive-control-0.1 |
| GNU classification and NUL representation (expected to remain) | 5 | (aggregate adapter), error-contract-0.1, http-fields-0.1 |
| Sandbox-only rows on N7 (should be not applicable with sandbox off) | 4 | native-supervisor-lifecycle-0.1 |
| N7 design gap: one peer connection per spawn | 2 | node-uri-io-0.2 |
| N7 defect: explicit limit plus timeout returns a truncated page | 1 | partial-page-errors-0.1 |

N6 capacity refusals: none in this run (62 replayed rows on 20 November).

Unclassified rows include N7 NU-015/016/017/019 (URI 0.2), N7 PE-001, ER-010 on N1 and N7, and owned-fixture rows in isobase-diagnostics, retained-context (CTX-016/017 b), statechart-document and the browser B-SV-006 case. Every one of them also failed on 20 November.

## Live standard library

842 rows per transport, original source and assertions.

| Node | Stateless HTTP | Retained WSS |
|---|---|---|
| N1 | 842 pass | not exposed |
| N2 | 842 pass | not exposed |
| N3 | 842 pass | 842 pass |
| N4 | 842 pass | 842 pass |
| N5 | 842 pass | 842 pass |
| N6 | 842 pass | not exposed |
| N7 | 842 pass | 842 pass |

## Finite admission

980 fresh finite HTTP probes, 140 per node on N1–N7, 0.6 s apart after all other endpoint work; outside manifest row counts. Overall: pass.

| Node | Probe result | Admission policy unchanged |
|---|---|---|
| N1 | pass | True |
| N2 | pass | True |
| N3 | pass | True |
| N4 | pass | True |
| N5 | pass | True |
| N6 | pass | True |
| N7 | pass | True |

Blocked, unsupported and inapplicable rows are accounted for without being called passes; every unexecuted row keeps its reason in verification.json. Persistent service container and image IDs match the pre-run snapshot, and all owned fixture containers were removed.

[Completion checks](execution/completion-verification.json) · [artifact hashes](files-sha256.json)
