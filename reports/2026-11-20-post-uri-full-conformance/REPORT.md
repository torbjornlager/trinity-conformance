# Full live conformance after the canonical URI deployment — 20 November 2026

Fresh execution of **81 manifests / 2,081 input rows** at suite `6dd7809eb0db63a9c54656c15bbc5f285a4de7fe`. This report records the complete run, including failed assertions, blocked controls and profile exclusions. Repeated cases, versions, transports and nodes are separate observations, not independent defects or a conformance percentage.

[Per-file outcomes](SUMMARY.json) · [case inventory](verification.json) · [frozen inputs](suite-inputs.json) · [provenance](execution/provenance.json) · [preservation](preservation.json).

## Runtime selection and test conditions

The live native SWI selection is `254ae3a` / SWI-Prolog 11.0.0; Trealla is `d451596` / 3.14.20. Demonstrator runtime source is `fd7e9f8` and browser provenance `b5ec41d`. GNU/N6 and ECLiPSe/N7 retain their previous runtime selections. Owned native fixtures use snapshots of the deployed images; their synthetic Trealla/GNU Git commits identify those file snapshots. Real Chromium Worker/main compatibility uses the currently selected browser package, whose executable bytes were unchanged by the deployment.

Every result in this report was executed for this run. No old pass or failure was copied forward. One sequential controller runs per public endpoint. HTTP calls use 0.8-second start spacing, retained-session creation 2.1 seconds, and prompt session creation four seconds. Library and prompt phases have quiet periods. N6 waits 303 seconds before its library phase and each bounded generator, exceeding its 300-second query retention. Broad N6 capacity refusals are retained and replayed after a 303-second expiry pause; any repeated admission refusal is retained and retried once after another 303-second pause. No live runtime, access mode, setting, quota or deployment was changed.

[Input changes since the previous complete sweep](execution/input-comparison.json) are recorded explicitly. Auxiliary fixture adapters that write extensionless JSON are included in this export; the earlier exporter omitted those files. Both old and current contract versions are executed; known superseded expectations remain visible in their original version. A failing old expectation is not automatically evidence of a current runtime defect.

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

## URI contract versions

The two URI packs use identical source helpers. Version 0.2 separates canonical addresses from caller-context visibility and adds independent isolation/control cases. Equal-credential case NU-022 requires an owned fixture and is blocked on public endpoints; its native fixture outcome is recorded separately. Public peer routes remain the same as the previous complete sweep: N4 calls N3; other ACTOR nodes call N4. This is broader than the earlier focused cross-engine replay.

| Node | Version 0.1 | Version 0.2 |
|---|---|---|
| N3 | 10 pass, 3 fail | 21 pass, 1 blocked |
| N4 | 10 pass, 3 fail | 21 pass, 1 blocked |
| N5 | 10 pass, 3 fail | 21 pass, 1 blocked |
| N7 | 13 fail | 21 fail, 1 blocked |

## Live standard library

All four versions retain their original source, assertions and bounded-prefix checks: 842 rows per transport. Retained-session controls stop their producer; finite stateless recovery alone does not prove internal producer reclamation.

| Node | Stateless HTTP | Retained WSS |
|---|---|---|
| N1 | 842 pass | not exposed |
| N2 | 842 pass | not exposed |
| N3 | 842 pass | 842 pass |
| N4 | 842 pass | 842 pass |
| N5 | 842 pass | 791 pass, 51 fail |
| N6 | 842 pass | not exposed |
| N7 | 842 pass | 842 pass |

N5 automatically restarted during version 0.4. Its retained WSS connection first closed at STDLIB-245; that case and the remaining 50 cases on the same connection failed with connection errors. These are 51 incomplete assertions, not 51 independently established library defects. The first lost connection does not establish the cause of the restart. Stateless HTTP continued after recovery. [Restart evidence](execution/runtime-restarts.json) records the unchanged container/image and observed start time. No operator restart was performed.

## N6 capacity and paused controls

Initial refusals remain in the raw API/library outcomes. The following separate replays preserve the original assertions; they change scheduling only. A passing replay does not erase the initial refusal.

| Selection | Fresh result |
|---|---|
| Broad ISOBASE API after expiry | 55 pass, 7 fail |
| Library refusals after expiry | none |

## HTTP prompts and directed interoperation

| Node | HTTP prompt assertions |
|---|---|
| N2 | 19 pass |
| N3 | 19 pass |
| N4 | 19 pass |
| N5 | 19 pass |
| N7 | 19 pass |

Each directed actor pair uses the same three finite interoperation assertions.

| Caller → peer | N3 | N4 | N5 | N7 |
|---|---|---|---|---|
| N3 | — | 3 pass | 3 pass | 3 pass |
| N4 | 3 pass | — | 3 pass | 3 pass |
| N5 | 3 pass | 3 pass | — | 3 pass |
| N7 | 3 pass | 3 pass | 3 pass | — |

## Owned fixtures and browser execution

These observations use disposable private fixtures or direct APIs. They are not evidence that a lower-profile public node exposes ACTOR behavior. Infinite computations and privileged ownership tests remain confined to owned processes.

| Selection | Fresh result |
|---|---|
| Private image swi-n134 | 45-case release gate passed; source directives 7 pass |
| Private image swi-n2 | 45-case release gate passed; source directives 7 pass |
| Private image trealla-n5 | 45-case release gate passed; source directives 7 pass |
| Authenticated HTTP contexts | 3 pass |
| Anonymous HTTP contexts | 3 pass |
| Native client naming | 16 pass |
| Retained contexts and promises | 53 pass, 4 fail, 4 blocked |
| Context closure | 6 pass |
| Bounded noncompletion | 3 pass |
| Enabled HTTP prompt fixtures | 38 pass |
| Browser Worker/main compatibility | 4 pass, 2 fail |

Runner self-tests: **123/123 pass**, using Node.js 22.23.4. They are tooling checks outside language-conformance counts. The snapshot includes exact shallow Git provenance before owned fixtures start. Engine/source inputs and assertion files were not patched to make tests pass.

## Failures and incomplete assertions

The table retains fresh failed/error assertions from applicable public or owned observations. Diagnostics, blocked cases and profile exclusions have separate classifications in SUMMARY.json. Older superseded contract versions remain labelled by suite/version; this table is not a count of independently diagnosed runtime bugs.

| Evidence | Fresh result |
|---|---|
| [public-extra/results.json](observations/public-extra/results.json) | 117 pass, 3 fail |
| [live-more/n1/isobase-error-admission-0.1.json](observations/live-more/n1/isobase-error-admission-0.1.json) | 1 fail |
| [live-more/n1/local-node-rpc-0.1.json](observations/live-more/n1/local-node-rpc-0.1.json) | 5 pass, 2 fail |
| [live-more/n1/partial-page-errors-0.1.json](observations/live-more/n1/partial-page-errors-0.1.json) | 10 pass, 1 fail, 7 not_applicable |
| [live-more/n2/local-node-rpc-0.1.json](observations/live-more/n2/local-node-rpc-0.1.json) | 5 pass, 2 fail |
| [live-more/n2/partial-page-errors-0.1.json](observations/live-more/n2/partial-page-errors-0.1.json) | 10 pass, 1 fail, 7 not_applicable |
| [live-more/n3/local-node-rpc-0.1.json](observations/live-more/n3/local-node-rpc-0.1.json) | 5 pass, 2 fail |
| [live-more/n3/monitor-contracts-0.1.json](observations/live-more/n3/monitor-contracts-0.1.json) | 47 pass, 2 fail |
| [live-more/n3/monitor-preflight-0.1.json](observations/live-more/n3/monitor-preflight-0.1.json) | 22 pass, 2 fail |
| [live-more/n3/node-uri-io-0.1.json](observations/live-more/n3/node-uri-io-0.1.json) | 10 pass, 3 fail |
| [live-more/n3/portable-text-0.2.json](observations/live-more/n3/portable-text-0.2.json) | 21 pass, 4 fail, 1 blocked |
| [live-more/n4/local-node-rpc-0.1.json](observations/live-more/n4/local-node-rpc-0.1.json) | 5 pass, 2 fail |
| [live-more/n4/monitor-contracts-0.1.json](observations/live-more/n4/monitor-contracts-0.1.json) | 47 pass, 2 fail |
| [live-more/n4/monitor-preflight-0.1.json](observations/live-more/n4/monitor-preflight-0.1.json) | 22 pass, 2 fail |
| [live-more/n4/node-uri-io-0.1.json](observations/live-more/n4/node-uri-io-0.1.json) | 10 pass, 3 fail |
| [live-more/n4/portable-text-0.2.json](observations/live-more/n4/portable-text-0.2.json) | 21 pass, 4 fail, 1 blocked |
| [live-more/n5/http-transport-options-0.1.json](observations/live-more/n5/http-transport-options-0.1.json) | 53 pass, 6 fail |
| [live-more/n5/local-node-rpc-0.1.json](observations/live-more/n5/local-node-rpc-0.1.json) | 5 pass, 2 fail |
| [live-more/n5/monitor-contracts-0.1.json](observations/live-more/n5/monitor-contracts-0.1.json) | 47 pass, 2 fail |
| [live-more/n5/monitor-preflight-0.1.json](observations/live-more/n5/monitor-preflight-0.1.json) | 22 pass, 2 fail |
| [live-more/n5/node-uri-io-0.1.json](observations/live-more/n5/node-uri-io-0.1.json) | 10 pass, 3 fail |
| [live-more/n5/partial-page-errors-0.1.json](observations/live-more/n5/partial-page-errors-0.1.json) | 17 pass, 1 fail |
| [live-more/n5/portable-text-0.2.json](observations/live-more/n5/portable-text-0.2.json) | 21 pass, 4 fail, 1 blocked |
| [live-more/n5/selective-receive-0.2.json](observations/live-more/n5/selective-receive-0.2.json) | 28 pass, 1 fail |
| [live-more/n6/error-contract-0.1.json](observations/live-more/n6/error-contract-0.1.json) | 12 pass, 1 fail |
| [live-more/n6/http-fields-0.1.json](observations/live-more/n6/http-fields-0.1.json) | 59 pass, 2 fail |
| [live-more/n6/local-node-rpc-0.1.json](observations/live-more/n6/local-node-rpc-0.1.json) | 5 pass, 2 fail |
| [live-more/n6/partial-page-errors-0.1.json](observations/live-more/n6/partial-page-errors-0.1.json) | 7 pass, 4 fail, 7 not_applicable |
| [live-more/n6/reference-contracts-0.1.json](observations/live-more/n6/reference-contracts-0.1.json) | 1 fail, 7 not_applicable |
| [live-more/n6/rpc-timeout-0.1.json](observations/live-more/n6/rpc-timeout-0.1.json) | 20 fail |
| [live-more/n6/runtime-introspection-0.1.json](observations/live-more/n6/runtime-introspection-0.1.json) | 10 fail |
| [live-more/n6/successor-validation-0.1.json](observations/live-more/n6/successor-validation-0.1.json) | 20 fail, 23 not_applicable |
| [live-more/n6/uri-atoms-0.1.json](observations/live-more/n6/uri-atoms-0.1.json) | 10 fail |
| [live-more/n7/call-arity-admission-0.1.json](observations/live-more/n7/call-arity-admission-0.1.json) | 9 pass, 3 fail, 2 not_applicable |
| [live-more/n7/demonstrator-tutorials-0.1.json](observations/live-more/n7/demonstrator-tutorials-0.1.json) | 1 fail |
| [live-more/n7/http-fields-0.1.json](observations/live-more/n7/http-fields-0.1.json) | 51 pass, 10 fail |
| [live-more/n7/local-node-rpc-0.1.json](observations/live-more/n7/local-node-rpc-0.1.json) | 5 pass, 2 fail |
| [live-more/n7/monitor-contracts-0.1.json](observations/live-more/n7/monitor-contracts-0.1.json) | 47 pass, 2 fail |
| [live-more/n7/monitor-preflight-0.1.json](observations/live-more/n7/monitor-preflight-0.1.json) | 22 pass, 2 fail |
| [live-more/n7/native-library-callbacks-0.1.json](observations/live-more/n7/native-library-callbacks-0.1.json) | 84 pass, 4 fail |
| [live-more/n7/native-supervisor-lifecycle-0.1.json](observations/live-more/n7/native-supervisor-lifecycle-0.1.json) | 12 pass, 5 fail |
| [live-more/n7/node-uri-io-0.1.json](observations/live-more/n7/node-uri-io-0.1.json) | 13 fail |
| [live-more/n7/node-uri-io-0.2.json](observations/live-more/n7/node-uri-io-0.2.json) | 21 fail, 1 blocked |
| [live-more/n7/partial-page-errors-0.1.json](observations/live-more/n7/partial-page-errors-0.1.json) | 11 pass, 7 fail |
| [live-more/n7/portable-text-0.2.json](observations/live-more/n7/portable-text-0.2.json) | 21 pass, 4 fail, 1 blocked |
| [live-more/n7/reference-contracts-0.1.json](observations/live-more/n7/reference-contracts-0.1.json) | 3 pass, 1 fail, 4 blocked |
| [live-more/n7/successor-validation-0.1.json](observations/live-more/n7/successor-validation-0.1.json) | 41 pass, 2 fail |
| [live-library/n5/standard-library-0.4.json](observations/live-library/n5/standard-library-0.4.json) | 539 pass, 51 fail |
| [live-controls/n6-paused-more.json](observations/live-controls/n6-paused-more.json) | 55 pass, 7 fail |
| [live-controls/trealla-sr015-exact-controls.json](observations/live-controls/trealla-sr015-exact-controls.json) | 3 fail |
| [native/http-transport-options-0.1/results.json](observations/native/http-transport-options-0.1/results.json) | 112 pass, 6 fail |
| [native/isobase-diagnostics-0.1/results.json](observations/native/isobase-diagnostics-0.1/results.json) | 2 pass, 10 fail |
| [native/local-node-rpc.json](observations/native/local-node-rpc.json) | 14 pass, 7 fail |
| [native/monitor-contracts-0.1/results.json](observations/native/monitor-contracts-0.1/results.json) | 94 pass, 4 fail |
| [native/monitor-preflight-0.1/results.json](observations/native/monitor-preflight-0.1/results.json) | 44 pass, 4 fail |
| [native/node-uri-io-0.1/results.json](observations/native/node-uri-io-0.1/results.json) | 20 pass, 6 fail |
| [native/portable-text-0.2/swi-portable-text.json](observations/native/portable-text-0.2/swi-portable-text.json) | 24 pass, 2 fail |
| [native/portable-text-0.2/trealla-portable-text.json](observations/native/portable-text-0.2/trealla-portable-text.json) | 24 pass, 2 fail |
| [native/retained-context/contexts/results.json](observations/native/retained-context/contexts/results.json) | 53 pass, 4 fail, 4 blocked |
| [native/rpc-timeouts-fixtures](observations/native/rpc-timeouts-fixtures) | 61 pass, 20 fail |
| [native/statechart-document-fixtures](observations/native/statechart-document-fixtures) | 1 pass, 9 fail |
| [followup-native/monitor-contracts-0.1-source-aware/results.json](observations/followup-native/monitor-contracts-0.1-source-aware/results.json) | 94 pass, 4 fail |
| [followup-native/monitor-preflight-0.1-source-aware/results.json](observations/followup-native/monitor-preflight-0.1-source-aware/results.json) | 44 pass, 4 fail |
| [followup-native/standalone-boundaries.json](observations/followup-native/standalone-boundaries.json) | 305 pass, 18 fail |
| [extras/results.json](observations/extras/results.json) | 181 pass, 8 fail, 24 observed |
| [browser-compat/browser-local-compatibility-0.1.json](observations/browser-compat/browser-local-compatibility-0.1.json) | 4 pass, 2 fail |

## Execution accounting

| Manifest | Input rows | Rows with execution | Rows without execution |
|---|---:|---:|---:|
| actor-behaviours-0.1 | 10 | 10 | 0 |
| actor-core-0.1 | 7 | 7 | 0 |
| actor-error-contract-0.1 | 1 | 1 | 0 |
| actor-supervisors-0.1 | 8 | 8 | 0 |
| actor-workers-0.1 | 8 | 8 | 0 |
| admission-marker-controls-0.1 | 2 | 2 | 0 |
| admission-paths-0.1 | 10 | 10 | 0 |
| appendix-library-probes-0.1 | 2 | 2 | 0 |
| boolean-boundary-diagnostics-0.1 | 2 | 2 | 0 |
| boolean-options-0.1 | 234 | 234 | 0 |
| browser-local-compatibility-0.1 | 3 | 3 | 0 |
| call-arity-admission-0.1 | 14 | 14 | 0 |
| child-spec-diagnostics-0.1 | 2 | 2 | 0 |
| child-specs-0.1 | 6 | 6 | 0 |
| client-naming-0.1 | 8 | 8 | 0 |
| committed-exit-0.1 | 4 | 4 | 0 |
| copying-isolation-0.1 | 6 | 6 | 0 |
| creation-validation-0.1 | 6 | 6 | 0 |
| demonstrator-tutorials-0.1 | 1 | 1 | 0 |
| error-contract-0.1 | 13 | 13 | 0 |
| http-fields-0.1 | 61 | 61 | 0 |
| http-session-context-0.1 | 3 | 3 | 0 |
| http-transport-options-0.1 | 59 | 59 | 0 |
| interop-actor-0.1 | 3 | 3 | 0 |
| interop-http-0.1 | 2 | 2 | 0 |
| interop-successor-0.1 | 3 | 3 | 0 |
| isobase-diagnostics-0.1 | 6 | 6 | 0 |
| isobase-error-admission-0.1 | 1 | 1 | 0 |
| isobase-http-0.1 | 12 | 12 | 0 |
| language-actor-0.1 | 7 | 7 | 0 |
| library-noncompletion-0.1 | 1 | 1 | 0 |
| links-monitors-0.1 | 6 | 6 | 0 |
| local-naming-0.1 | 6 | 6 | 0 |
| local-node-rpc-0.1 | 7 | 7 | 0 |
| manual-option-sources-0.1 | 11 | 11 | 0 |
| monitor-contracts-0.1 | 49 | 49 | 0 |
| monitor-contracts-0.2 | 50 | 50 | 0 |
| monitor-preflight-0.1 | 24 | 24 | 0 |
| monitor-preflight-0.2 | 25 | 25 | 0 |
| native-library-callbacks-0.1 | 88 | 88 | 0 |
| native-supervisor-id-counts-0.1 | 41 | 41 | 0 |
| native-supervisor-lifecycle-0.1 | 17 | 17 | 0 |
| native-terminal-newline-0.1 | 2 | 2 | 0 |
| node-settings-0.1 | 14 | 14 | 0 |
| node-uri-io-0.1 | 13 | 13 | 0 |
| node-uri-io-0.2 | 22 | 22 | 0 |
| ownership-lifecycle-0.1 | 4 | 4 | 0 |
| partial-page-errors-0.1 | 18 | 18 | 0 |
| portable-text-0.1 | 7 | 7 | 0 |
| portable-text-0.2 | 26 | 26 | 0 |
| private-helper-admission-0.1 | 12 | 12 | 0 |
| promise-diagnostics-0.1 | 3 | 3 | 0 |
| promise-yield-0.1 | 6 | 6 | 0 |
| prompt-http-0.1 | 19 | 19 | 0 |
| prompt-ws-0.1 | 4 | 4 | 0 |
| receive-callback-context-0.1 | 12 | 12 | 0 |
| receive-control-0.1 | 8 | 8 | 0 |
| receive-wait-options-0.1 | 3 | 3 | 0 |
| reference-contracts-0.1 | 8 | 8 | 0 |
| relation-error-admission-0.1 | 1 | 1 | 0 |
| retained-context-0.1 | 55 | 51 | 4 |
| rpc-timeout-0.1 | 20 | 20 | 0 |
| runtime-introspection-0.1 | 10 | 10 | 0 |
| selective-receive-0.1 | 6 | 6 | 0 |
| selective-receive-0.2 | 29 | 29 | 0 |
| server-waits-0.1 | 6 | 6 | 0 |
| source-copying-0.1 | 6 | 6 | 0 |
| source-directives-0.1 | 7 | 7 | 0 |
| standard-library-0.1 | 112 | 112 | 0 |
| standard-library-0.2 | 146 | 146 | 0 |
| standard-library-0.3 | 289 | 289 | 0 |
| standard-library-0.4 | 295 | 295 | 0 |
| standard-naming-errors-0.1 | 7 | 7 | 0 |
| statechart-document-0.1 | 4 | 4 | 0 |
| successor-validation-0.1 | 43 | 43 | 0 |
| supervisor-common-0.1 | 10 | 10 | 0 |
| supervisor-diagnostics-0.1 | 5 | 5 | 0 |
| toplevel-waits-0.1 | 6 | 6 | 0 |
| uri-atoms-0.1 | 10 | 10 | 0 |
| wire-capabilities-0.1 | 3 | 3 | 0 |
| worker-diagnostics-0.1 | 1 | 1 | 0 |

Blocked, unsupported and inapplicable rows are accounted for without being called passes. Every unexecuted row retains its evidence and reason in verification.json. The historical 183-observation repair inventory belongs to an older reviewed baseline; these fresh outcomes are reported independently.

## Admission and preservation

980 fresh finite HTTP probes, 140 per node on N1–N7, use 0.6-second spacing after all other endpoint work. This is an additional throughput/admission check, outside manifest case-row counts.

| Node | Probe result | Admission metadata preserved |
|---|---|---|
| N1 | pass | True |
| N2 | pass | True |
| N3 | pass | True |
| N4 | pass | True |
| N5 | pass | True |
| N6 | pass | True |
| N7 | pass | True |

Persistent Compose service container IDs and image IDs match the pre-run snapshot. All owned fixture containers are removed. Historical reports remain unchanged. This run made no fixes or deployments.

[Completion checks](execution/completion-verification.json) · [artifact hashes](files-sha256.json).
