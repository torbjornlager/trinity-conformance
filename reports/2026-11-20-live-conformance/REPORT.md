# Live conformance after the admission rollout — 20 November 2026

This fresh run uses suite `aeb1329a1ad49317cdc906e122e2f655163791db` and covers **78 manifests / 1,984 input rows**. The outcome is **not all-green**. Passing, failed, blocked, diagnostic and inapplicable observations remain separate. Repeated historical versions, routes and modes are not independent language features.

[Per-file observations](SUMMARY.json) · [case-by-case inventory](verification.json) · [frozen inputs](suite-inputs.json) · [runtime provenance](execution/provenance.json) · [service preservation](preservation.json).

## Release and execution conditions

All 78 versioned manifest files and the pre-existing runner/adapter files match the previous sweep byte for byte; the [input comparison](execution/input-comparison.json) records this. The sweep follows the [configurable admission deployment](../2026-11-19-public-admission/REPORT.md). Native SWI uses `e25b230` / SWI 11.0.0, Trealla `2d5042b` / 3.14.20, the ECLiPSe adapter `31dcdfc` / its unchanged engine, and browser package `0d024e5` / SWI 10.1.19. The source selection is shared deployment `21284ba`. Actual container/image identities were captured before testing and compared afterwards.

Each public endpoint has one sequential controller. In the extended API and library phases, stateless HTTP calls are spaced at least 0.8 seconds between starts. Session-based selections use 2.1-second creation spacing; HTTP prompts use four seconds before session creation while preserving reply/abort/halt races. Quiet periods separate library and prompt phases. GNU N6 receives 303-second quiet periods before each bounded HTTP generator, exceeding its existing 300-second idle query lifetime. Public interoperation starts after the involved endpoint streams finish; unrelated N6 expiry controls can continue independently. No runtime, assertion, installed engine, live service setting, quota or deployment was changed for the tests.

## Primary public selections

| Node | Profile | Result |
|---|---|---|
| N0 | RELATION | 1 pass |
| N1 | ISOBASE | 12 pass |
| N2 | ISOTOPE | 12 pass |
| N3 | ACTOR | 118 pass |
| N4 | ACTOR | 118 pass |
| N5 | ACTOR | 118 pass |
| N6 | ISOBASE | 12 pass |
| N7 | ACTOR | 118 pass |

N0 selects RELATION error admission. N1/N2/N6 select the 12-case HTTP baseline. ACTOR endpoints select the release/public behavior packs plus HTTP baseline. Broader API selections are indexed under `observations/live-more/`, including explicit lower-profile applicability outcomes.

## Four library versions on live endpoints

Versions 0.1–0.4 contain 112, 146, 289 and 295 rows: 842 per transport. Original helper source, finite answer checks, ordered bounded prefixes and recovery assertions are unchanged. Retained sessions also stop the producer; stateless recovery does not establish internal producer reclamation.

| Node | Stateless HTTP | Retained WSS |
|---|---|---|
| N1 | 842 pass | not exposed |
| N2 | 842 pass | not exposed |
| N3 | 842 pass | 842 pass |
| N4 | 842 pass | 842 pass |
| N5 | 842 pass | 842 pass |
| N6 | 776 pass, 66 fail | not exposed |
| N7 | 842 pass | 842 pass |

The initial N6 library phase began after the generic 61-second phase pause, before queries retained by earlier API checks had necessarily reached their 300-second idle expiry. This scheduling choice produced 66 HTTP 503 query_limit_exceeded refusals at the start of version 0.1. Those refusals remain in the table. Separate unchanged controls wait 303 seconds after the N6 pipeline ends; all 66 pass in the [paused controls](observations/live-controls/n6-paused-library.json). The six bounded-generator cases each receive their own 303-second quiet period. No capacity setting was raised.

## HTTP prompts and directed ACTOR interoperation

| Endpoint | HTTP prompt pack |
|---|---|
| N2 | 19 pass |
| N3 | 19 pass |
| N4 | 19 pass |
| N5 | 19 pass |
| N7 | 19 pass |

Each directed pair selects the same three finite actor interoperation cases. This does not certify remote promise/context ownership.

| Caller → peer | N3 | N4 | N5 | N7 |
|---|---|---|---|---|
| N3 | — | 3 pass | 3 pass | 3 pass |
| N4 | 3 pass | — | 3 pass | 3 pass |
| N5 | 3 pass | 3 pass | — | 3 pass |
| N7 | 3 pass | 3 pass | 3 pass | — |

## Additional finite admission probes

After all other live phases and a 61-second quiet period, the maintained admission probe records 980 fresh finite HTTP observations: N1 pass, N2 pass, N3 pass, N4 pass, N5 pass, N6 pass, N7 pass. Each node is sent 140 requests with 0.6-second start spacing. Applied rate metadata is checked against 120 per 60-second unit. These observations are outside the 78-manifest input-row counts and do not establish concurrency or producer reclamation.

[Admission evidence](execution/admission-summary.json).

## Owned fixtures and supporting controls

Private identity preconditions and unbounded computations use disposable, isolated fixtures built from the current deployed runtime files/images. They are not live endpoint observations. N2-image ACTOR fixtures do not change live N2’s ISOTOPE profile. Real Chromium compatibility tests cover Worker/main local execution, not the public browser UI.

| Selection | Recorded result |
|---|---|
| Private image swi-n134 | 45-case release gate passed; source directives 7 pass |
| Private image swi-n2 | 45-case release gate passed; source directives 7 pass |
| Private image trealla-n5 | 45-case release gate passed; source directives 7 pass |
| Authenticated HTTP contexts | 3 pass |
| Anonymous HTTP contexts | 3 pass |
| Native client naming | 16 pass |
| Retained contexts and controlled promises | 46 pass, 11 fail, 4 blocked |
| Context closure | 6 pass |
| Bounded noncompletion | 3 pass |
| Enabled HTTP prompt fixtures | 38 pass |
| Browser compatibility | 4 pass, 2 fail |

Runner tooling: **114 unit tests pass**, outside language-conformance counts. The initial host test attempt used an obsolete Node.js and failed three adapter tests before the intended environment was selected; unchanged tests pass under Node.js 22. Browser fixture setup initially lacked npm; the maintained Playwright 1.62.1 tooling was supplied separately. Promise-fixture attempts also stopped before case execution because the archive lacked Git provenance and then copied-file ownership differed inside the container. An exact shallow suite commit and correct owned-file ownership resolve those setup preconditions without changing frozen source bytes. Those setup attempts are retained as infrastructure observations, not runtime-language findings.

## Failures and incomplete assertions

All raw outcomes are retained. The table lists files with failed/error assertions in applicable current observations; diagnostic errors, profile exclusions and blocked rows retain their separate classifications. A refusal or fixture protocol failure is not automatically attributable to language semantics.

| Evidence | Result |
|---|---|
| [public-extra/results.json](observations/public-extra/results.json) | 117 pass, 3 fail |
| [live-more/n1/isobase-error-admission-0.1.json](observations/live-more/n1/isobase-error-admission-0.1.json) | 1 fail |
| [live-more/n1/local-node-rpc-0.1.json](observations/live-more/n1/local-node-rpc-0.1.json) | 5 pass, 2 fail |
| [live-more/n1/partial-page-errors-0.1.json](observations/live-more/n1/partial-page-errors-0.1.json) | 10 pass, 1 fail, 7 not_applicable |
| [live-more/n1/rpc-timeout-0.1.json](observations/live-more/n1/rpc-timeout-0.1.json) | 16 pass, 4 fail |
| [live-more/n2/local-node-rpc-0.1.json](observations/live-more/n2/local-node-rpc-0.1.json) | 5 pass, 2 fail |
| [live-more/n2/partial-page-errors-0.1.json](observations/live-more/n2/partial-page-errors-0.1.json) | 10 pass, 1 fail, 7 not_applicable |
| [live-more/n2/rpc-timeout-0.1.json](observations/live-more/n2/rpc-timeout-0.1.json) | 16 pass, 4 fail |
| [live-more/n3/local-node-rpc-0.1.json](observations/live-more/n3/local-node-rpc-0.1.json) | 5 pass, 2 fail |
| [live-more/n3/monitor-contracts-0.1.json](observations/live-more/n3/monitor-contracts-0.1.json) | 47 pass, 2 fail |
| [live-more/n3/monitor-preflight-0.1.json](observations/live-more/n3/monitor-preflight-0.1.json) | 22 pass, 2 fail |
| [live-more/n3/node-uri-io-0.1.json](observations/live-more/n3/node-uri-io-0.1.json) | 4 pass, 9 fail |
| [live-more/n3/portable-text-0.2.json](observations/live-more/n3/portable-text-0.2.json) | 21 pass, 4 fail, 1 blocked |
| [live-more/n3/rpc-timeout-0.1.json](observations/live-more/n3/rpc-timeout-0.1.json) | 16 pass, 4 fail |
| [live-more/n4/local-node-rpc-0.1.json](observations/live-more/n4/local-node-rpc-0.1.json) | 5 pass, 2 fail |
| [live-more/n4/monitor-contracts-0.1.json](observations/live-more/n4/monitor-contracts-0.1.json) | 47 pass, 2 fail |
| [live-more/n4/monitor-preflight-0.1.json](observations/live-more/n4/monitor-preflight-0.1.json) | 22 pass, 2 fail |
| [live-more/n4/node-uri-io-0.1.json](observations/live-more/n4/node-uri-io-0.1.json) | 4 pass, 9 fail |
| [live-more/n4/portable-text-0.2.json](observations/live-more/n4/portable-text-0.2.json) | 21 pass, 4 fail, 1 blocked |
| [live-more/n4/rpc-timeout-0.1.json](observations/live-more/n4/rpc-timeout-0.1.json) | 16 pass, 4 fail |
| [live-more/n5/http-transport-options-0.1.json](observations/live-more/n5/http-transport-options-0.1.json) | 53 pass, 6 fail |
| [live-more/n5/local-node-rpc-0.1.json](observations/live-more/n5/local-node-rpc-0.1.json) | 5 pass, 2 fail |
| [live-more/n5/monitor-contracts-0.1.json](observations/live-more/n5/monitor-contracts-0.1.json) | 47 pass, 2 fail |
| [live-more/n5/monitor-preflight-0.1.json](observations/live-more/n5/monitor-preflight-0.1.json) | 22 pass, 2 fail |
| [live-more/n5/node-uri-io-0.1.json](observations/live-more/n5/node-uri-io-0.1.json) | 3 pass, 10 fail |
| [live-more/n5/partial-page-errors-0.1.json](observations/live-more/n5/partial-page-errors-0.1.json) | 17 pass, 1 fail |
| [live-more/n5/portable-text-0.2.json](observations/live-more/n5/portable-text-0.2.json) | 21 pass, 4 fail, 1 blocked |
| [live-more/n5/rpc-timeout-0.1.json](observations/live-more/n5/rpc-timeout-0.1.json) | 18 pass, 2 fail |
| [live-more/n5/selective-receive-0.2.json](observations/live-more/n5/selective-receive-0.2.json) | 28 pass, 1 fail |
| [live-more/n6/error-contract-0.1.json](observations/live-more/n6/error-contract-0.1.json) | 12 pass, 1 fail |
| [live-more/n6/http-fields-0.1.json](observations/live-more/n6/http-fields-0.1.json) | 59 pass, 2 fail |
| [live-more/n6/local-node-rpc-0.1.json](observations/live-more/n6/local-node-rpc-0.1.json) | 4 pass, 3 fail |
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
| [live-more/n7/partial-page-errors-0.1.json](observations/live-more/n7/partial-page-errors-0.1.json) | 12 pass, 6 fail |
| [live-more/n7/portable-text-0.2.json](observations/live-more/n7/portable-text-0.2.json) | 21 pass, 4 fail, 1 blocked |
| [live-more/n7/reference-contracts-0.1.json](observations/live-more/n7/reference-contracts-0.1.json) | 3 pass, 1 fail, 4 blocked |
| [live-more/n7/successor-validation-0.1.json](observations/live-more/n7/successor-validation-0.1.json) | 41 pass, 2 fail |
| [live-library/n6/standard-library-0.1.json](observations/live-library/n6/standard-library-0.1.json) | 46 pass, 66 fail |
| [live-controls/trealla-sr015-exact-controls.json](observations/live-controls/trealla-sr015-exact-controls.json) | 3 fail |
| [native/http-transport-options-0.1/results.json](observations/native/http-transport-options-0.1/results.json) | 112 pass, 6 fail |
| [native/isobase-diagnostics-0.1/results.json](observations/native/isobase-diagnostics-0.1/results.json) | 2 pass, 10 fail |
| [native/local-node-rpc.json](observations/native/local-node-rpc.json) | 14 pass, 7 fail |
| [native/monitor-contracts-0.1/results.json](observations/native/monitor-contracts-0.1/results.json) | 94 pass, 4 fail |
| [native/monitor-preflight-0.1/results.json](observations/native/monitor-preflight-0.1/results.json) | 44 pass, 4 fail |
| [native/node-uri-io/results.json](observations/native/node-uri-io/results.json) | 12 pass, 14 fail |
| [native/portable-text-0.2/swi-portable-text.json](observations/native/portable-text-0.2/swi-portable-text.json) | 24 pass, 2 fail |
| [native/portable-text-0.2/trealla-portable-text.json](observations/native/portable-text-0.2/trealla-portable-text.json) | 24 pass, 2 fail |
| [native/retained-context/contexts/results.json](observations/native/retained-context/contexts/results.json) | 46 pass, 11 fail, 4 blocked |
| [native/rpc-timeout-0.1/results.json](observations/native/rpc-timeout-0.1/results.json) | 34 pass, 6 fail |
| [followup-native/monitor-contracts-0.1-source-aware/results.json](observations/followup-native/monitor-contracts-0.1-source-aware/results.json) | 94 pass, 4 fail |
| [followup-native/monitor-preflight-0.1-source-aware/results.json](observations/followup-native/monitor-preflight-0.1-source-aware/results.json) | 44 pass, 4 fail |
| [followup-native/standalone-boundaries.json](observations/followup-native/standalone-boundaries.json) | 299 pass, 24 fail |
| [extras/prompt-http.json](observations/extras/prompt-http.json) | 19 pass, 19 fail |
| [extras/results.json](observations/extras/results.json) | 181 pass, 8 fail, 24 observed |
| [browser-compat/browser-local-compatibility-0.1.json](observations/browser-compat/browser-local-compatibility-0.1.json) | 4 pass, 2 fail |

### Focused findings

- Retained context and controlled promise routes remain at 46 pass / 11 fail / 4 blocked, with six passing closure controls. Source/export refusals block four return assertions; attachment instrumentation still cannot complete its precondition.
- MC-028/029 retain URI-form rejection expectations that conflict with the documented accepted text forms. The main monitor pack records 47 pass / 2 fail per ACTOR node; preflight records 22 pass / 2 fail. This run does not revise those assertions.
- Real Chromium compatibility retains B-SV-006 in Worker and main modes: 4 pass / 2 fail across the three-case pack. The naming cases pass; the failing supervisor case remains separate from public-UI certification.
- Public Trealla SR-015 fails. [Unchanged repeated controls](observations/live-controls/trealla-sr015-exact-controls.json) record 3 fail. Its owned-fixture result and supplemental projections remain separately indexed; timing/diagnostic variants are not substituted for the assertion.
- The new extended N7 selection exposes additional HTTP-field, callback and supervisor-lifecycle differences. Those rows were not covered by the previous six-node extended selection and are not automatically regressions. Protocol, installed-service availability and fixture failures do not by themselves isolate an engine defect.
- The newly selected N7 retained-HTTP prompt pack records 19 pass. This uses the maintained ECLiPSe branch with unchanged race assertions; the earlier full sweep did not qualify this pack on N7.

### Input rows without a completed execution observation

- `retained-context-0.1`: `CTX-016-swi-b`, `CTX-017-swi-b`, `CTX-016-trealla-b`, `CTX-017-trealla-b`.

## Comparison and limits

The [previous complete sweep](../2026-11-19-upgraded-live-conformance/REPORT.md) remains unchanged, including its original N7 rate refusals and N6 query-capacity refusals. This run starts every selection fresh against the admission release; no old pass was copied into its observations. It additionally applies the broader public API selection and retained-HTTP prompt pack to N7; the previous extended selection covered N1–N6, so newly exposed N7 findings are not automatically regressions. The separate admission qualification remains available for boundary, refusal/recovery and sustained-throughput evidence.

Current remote-context, monitor, URI, source/document, portable-text and public receive findings must be interpreted with their fixture and profile boundaries. Blocked source/export and attachment-instrumentation controls do not establish the later assertions they could not reach. MC-028/029 retain their original URI-form expectations; assertions have not been revised to produce passes.

No private-admin or public-browser-UI certification is implied. Public diagnostics, exact-profile negative expectations, browser-only expectations on native engines, owned fixture controls and direct APIs are classified separately. See the machine inventory rather than adding heterogeneous results into a conformance percentage.

Execution plans and report tooling are archived under [orchestration](orchestration/). Exported evidence is covered by [SHA-256 hashes](files-sha256.json). Production credentials and private fixture tokens are excluded.
