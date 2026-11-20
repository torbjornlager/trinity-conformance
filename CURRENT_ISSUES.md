# Current conformance issues

The primary deployment checks pass. The broader contract backlog remains open.

**This is the current triage view.** [Historical full sweep](reports/2026-11-20-live-conformance/REPORT.md) · [Machine inventory](backlog/current.json) · [Reviewed decisions](backlog/decisions.json).

Families are work queues, not independently proven root causes. Case IDs and observations are not feature/defect counts. Candidate repairs do not close deployed findings.

Original failures are retained. Later passing controls are linked to exact observations; neither unrelated passes nor candidate-only repairs turn production green. `open` means unresolved evidence, not a proven runtime defect.

The reviewed baseline has 416 applicable failed observations. 207 remain unresolved failed observations. These figures count repeated runs and projections, not independent defects. Blocked selections are counted separately.

There are 4 full-sweep input rows without a completed execution anywhere. Repeated blocked projections onto live endpoints are listed separately; they are not additional demonstrated defects.

## Work queues

| Queue | Original observations | Current disposition | Next action |
|---|---:|---|---|
| Call admission and tutorial availability | 6 | 6 open | Verify public profile/service preconditions before changing language behavior. |
| Browser supervisor recovery | 2 | 2 open | Reproduce B-SV-006 in Worker/main and repair sibling preservation and valid retry. |
| N6 retained-query scheduling | 121 | 121 correct preconditions verified | Use expiry/owned-query cleanup at phase boundaries; keep concurrency bounds. |
| Client contexts and promise ownership | 263 | 252 blocked precondition, 11 open | Investigate foreign collection and round-trip restoration separately; leave blocked routes explicit. |
| Error envelopes and partial pages | 24 | 24 open | Separate profile boundaries, page protocol and error payload assertions. |
| HTTP option vocabulary and fields | 32 | 32 open | Compare approved option vocabulary, then test rejection before dispatch with a recording peer. |
| Library and noncompletion | 7 | 7 blocked precondition | Separate capacity refusals from producer lifecycle and finite-answer assertions. |
| Supervisor lifecycle and callbacks | 9 | 9 open | Resolve N7 source/profile preconditions, then isolate lifecycle/validation behavior. |
| Same-node RPC and caller-side source | 22 | 21 open, 1 passing replay cause open | Separate producer profile/setup from source preparation and local ownership. |
| Monitor URI contract drift | 32 | 32 superseded assertion | Use version 0.2 and the recorded 17 November contract; retain 0.1 evidence. |
| Retained HTTP prompt fixture | 95 | 76 blocked precondition, 19 fixture precondition | Use the enabled disposable adapter and one preflight; missing routes block execution and fail qualification. |
| Selective receive and guard handling | 39 | 7 open, 32 blocked precondition | Reproduce SR-015 with exact goals and fix receive-body semantics without changing the case. |
| Reference types and ownership | 17 | 16 blocked precondition, 1 open | Reproduce with distinct identities and supported profiles. |
| RPC/promise timeout validation | 30 | 30 repaired deployed | Numeric-option failures are repaired/deployed; retain destination/transport timeout separation for further controlled-peer review. |
| Successor option validation | 3 | 3 open | Verify remaining N7 validation against the shared contract. |
| Portable text and prompt wire protocol | 24 | 4 blocked precondition, 20 open | Supply controlled source routes and correlated prompt references; retain language literal assertions. |
| URI routing and source transport | 77 | 71 open, 2 repaired deployed, 4 fixture precondition | Qualify exact native images and demonstrator consumers, deploy canonical routing with context-scoped Trealla peer caches, then replay live URI/context cases; N6/N7/browser remain separate. |

## Contract correction

The recorded author-directed decision of 17 November supersedes the earlier atom-only URI proposal. The old manual text and MC-028/029 rejection expectations were stale. Monitor packs 0.2 test accepted text forms against the same actor and actual monitor delivery; 0.1 remains immutable. The stale manual wording is corrected against that decision.

## Evidence by queue

### Call admission and tutorial availability

Cases: `CA-002`, `CA-013`, `CA-014`, `DEMO-019`, `OPT-004`.

- [followup-native/standalone-boundaries.json](reports/2026-11-20-live-conformance/observations/followup-native/standalone-boundaries.json)
- [live-more/n7/call-arity-admission-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/call-arity-admission-0.1.json)
- [live-more/n7/demonstrator-tutorials-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/demonstrator-tutorials-0.1.json)

### Browser supervisor recovery

Cases: `B-SV-006`.

- [browser-compat/browser-local-compatibility-0.1.json](reports/2026-11-20-live-conformance/observations/browser-compat/browser-local-compatibility-0.1.json)

### N6 retained-query scheduling

Cases: `OPT-001`, `OPT-002`, `OPT-003`, `PE-017`, `RF-004`, `RPC-TIME-001`, `RPC-TIME-002`, `RPC-TIME-003`, `RPC-TIME-004`, `RPC-TIME-005`, `RPC-TIME-006`, `RPC-TIME-007`, `RPC-TIME-008`, `RPC-TIME-009`, `RPC-TIME-010`, `RPC-TIME-011`, `RPC-TIME-012`, `RPC-TIME-013`, `RPC-TIME-014`, `RPC-TIME-015`, `RPC-TIME-016`, `RPC-TIME-017`, `RPC-TIME-018`, `RPC-TIME-019`, `RPC-TIME-020`, `RT-001`, `RT-002`, `RT-003`, `RT-004`, `RT-005`, `RT-HTTP-001`, `RT-HTTP-002`, `RT-HTTP-003`, `RT-HTTP-004`, `RT-HTTP-005`, `STDLIB-001`, `STDLIB-002`, `STDLIB-003`, `STDLIB-004`, `STDLIB-005`, `STDLIB-006`, `STDLIB-007`, `STDLIB-008`, `STDLIB-009`, `STDLIB-010`, `STDLIB-011`, `STDLIB-012`, `STDLIB-013`, `STDLIB-014`, `STDLIB-015`, `STDLIB-016`, `STDLIB-017`, `STDLIB-018`, `STDLIB-019`, `STDLIB-020`, `STDLIB-021`, `STDLIB-022`, `STDLIB-023`, `STDLIB-024`, `STDLIB-025`, `STDLIB-026`, `STDLIB-027`, `STDLIB-028`, `STDLIB-029`, `STDLIB-030`, `STDLIB-031`, `STDLIB-032`, `STDLIB-033`, `STDLIB-034`, `STDLIB-035`, `STDLIB-036`, `STDLIB-037`, `STDLIB-038`, `STDLIB-039`, `STDLIB-040`, `STDLIB-041`, `STDLIB-042`, `STDLIB-043`, `STDLIB-044`, `STDLIB-045`, `STDLIB-046`, `STDLIB-047`, `STDLIB-048`, `STDLIB-049`, `STDLIB-050`, `STDLIB-051`, `STDLIB-052`, `STDLIB-053`, `STDLIB-054`, `STDLIB-055`, `STDLIB-056`, `STDLIB-057`, `STDLIB-058`, `STDLIB-059`, `STDLIB-060`, `STDLIB-061`, `STDLIB-062`, `STDLIB-063`, `STDLIB-064`, `STDLIB-065`, `STDLIB-066`, `SU-HTTP-001`, `SU-HTTP-002`, `SU-HTTP-003`, `SU-HTTP-004`, `SU-HTTP-005`, `SU-HTTP-006`, `SU-HTTP-007`, `SU-HTTP-008`, `SU-HTTP-009`, `SU-HTTP-010`, `SU-HTTP-011`, `SU-HTTP-012`, `SU-HTTP-013`, `SU-HTTP-014`, `SU-HTTP-015`, `SU-HTTP-017`, `SU-HTTP-018`, `SU-HTTP-019`, `SU-HTTP-020`, `URI-003`.

- [live-library/n6/standard-library-0.1.json](reports/2026-11-20-live-conformance/observations/live-library/n6/standard-library-0.1.json)
- [live-more/n6/partial-page-errors-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n6/partial-page-errors-0.1.json)
- [live-more/n6/reference-contracts-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n6/reference-contracts-0.1.json)
- [live-more/n6/rpc-timeout-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n6/rpc-timeout-0.1.json)
- [live-more/n6/runtime-introspection-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n6/runtime-introspection-0.1.json)
- [live-more/n6/successor-validation-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n6/successor-validation-0.1.json)
- [live-more/n6/uri-atoms-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n6/uri-atoms-0.1.json)

### Client contexts and promise ownership

Cases: `CP-001-swi-b`, `CP-001-trealla-a`, `CP-001-trealla-b`, `CTX-001`, `CTX-002`, `CTX-003`, `CTX-004`, `CTX-005`, `CTX-006`, `CTX-007`, `CTX-008`, `CTX-009`, `CTX-010`, `CTX-011`, `CTX-012-swi-b`, `CTX-012-trealla-b`, `CTX-013-swi-b`, `CTX-013-trealla-b`, `CTX-014-swi-b`, `CTX-014-trealla-b`, `CTX-015-swi-b`, `CTX-015-trealla-b`, `CTX-016-swi-b`, `CTX-016-trealla-b`, `CTX-017-swi-b`, `CTX-017-trealla-b`, `CTX-018-swi-b`, `CTX-018-trealla-b`, `CTX-019-swi-b`, `CTX-019-trealla-b`, `CTX-020`, `HCTX-001`, `HCTX-002`, `OL-001`, `OL-002`, `OL-003`, `OL-004`.

- [live-more/n3/http-session-context-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n3/http-session-context-0.1.json)
- [live-more/n3/ownership-lifecycle-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n3/ownership-lifecycle-0.1.json)
- [live-more/n3/retained-context-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n3/retained-context-0.1.json)
- [live-more/n4/http-session-context-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n4/http-session-context-0.1.json)
- [live-more/n4/ownership-lifecycle-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n4/ownership-lifecycle-0.1.json)
- [live-more/n4/retained-context-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n4/retained-context-0.1.json)
- [live-more/n5/http-session-context-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/http-session-context-0.1.json)
- [live-more/n5/ownership-lifecycle-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/ownership-lifecycle-0.1.json)
- [live-more/n5/retained-context-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/retained-context-0.1.json)
- [live-more/n7/http-session-context-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/http-session-context-0.1.json)
- [live-more/n7/ownership-lifecycle-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/ownership-lifecycle-0.1.json)
- [live-more/n7/retained-context-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/retained-context-0.1.json)
- [native/retained-context/contexts/results.json](reports/2026-11-20-live-conformance/observations/native/retained-context/contexts/results.json)

### Error envelopes and partial pages

Cases: `ER-007`, `ER-010`, `IBD-001`, `IBD-002`, `IBD-003`, `IBD-004`, `IBD-005`, `PE-008`, `PE-014`, `PE-015`, `PE-016`, `PE-017`, `PE-018`.

- [live-more/n1/isobase-error-admission-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n1/isobase-error-admission-0.1.json)
- [live-more/n1/partial-page-errors-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n1/partial-page-errors-0.1.json)
- [live-more/n2/partial-page-errors-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n2/partial-page-errors-0.1.json)
- [live-more/n5/partial-page-errors-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/partial-page-errors-0.1.json)
- [live-more/n6/error-contract-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n6/error-contract-0.1.json)
- [live-more/n6/partial-page-errors-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n6/partial-page-errors-0.1.json)
- [live-more/n7/partial-page-errors-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/partial-page-errors-0.1.json)
- [native/isobase-diagnostics-0.1/results.json](reports/2026-11-20-live-conformance/observations/native/isobase-diagnostics-0.1/results.json)

### HTTP option vocabulary and fields

Cases: `HTTP-CTL-promise-0`, `HTTP-CTL-promise-127`, `HTTP-CTL-promise-13`, `HTTP-CTL-promise-31`, `HTTP-CTL-rpc-0`, `HTTP-CTL-rpc-127`, `HTTP-CTL-rpc-13`, `HTTP-CTL-rpc-31`, `HTTP-FIELD-012`, `HTTP-FIELD-024`, `HTTP-FIELD-025`, `HTTP-FIELD-026`, `HTTP-FIELD-039`, `HTTP-FIELD-051`, `HTTP-FIELD-052`, `HTTP-FIELD-053`.

- [extras/results.json](reports/2026-11-20-live-conformance/observations/extras/results.json)
- [followup-native/standalone-boundaries.json](reports/2026-11-20-live-conformance/observations/followup-native/standalone-boundaries.json)
- [live-more/n5/http-transport-options-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/http-transport-options-0.1.json)
- [live-more/n6/http-fields-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n6/http-fields-0.1.json)
- [live-more/n7/http-fields-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/http-fields-0.1.json)
- [native/http-transport-options-0.1/results.json](reports/2026-11-20-live-conformance/observations/native/http-transport-options-0.1/results.json)

### Library and noncompletion

Cases: `STDLIB-296`.

- [live-more/n1/library-noncompletion-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n1/library-noncompletion-0.1.json)
- [live-more/n2/library-noncompletion-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n2/library-noncompletion-0.1.json)
- [live-more/n3/library-noncompletion-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n3/library-noncompletion-0.1.json)
- [live-more/n4/library-noncompletion-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n4/library-noncompletion-0.1.json)
- [live-more/n5/library-noncompletion-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/library-noncompletion-0.1.json)
- [live-more/n6/library-noncompletion-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n6/library-noncompletion-0.1.json)
- [live-more/n7/library-noncompletion-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/library-noncompletion-0.1.json)

### Supervisor lifecycle and callbacks

Cases: `LC-082`, `LC-083`, `LC-087`, `LC-088`, `SL-011`, `SL-014`, `SL-015`, `SL-016`, `SL-017`.

- [live-more/n7/native-library-callbacks-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/native-library-callbacks-0.1.json)
- [live-more/n7/native-supervisor-lifecycle-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/native-supervisor-lifecycle-0.1.json)

### Same-node RPC and caller-side source

Cases: `LOCAL-001`, `LOCAL-002`, `LOCAL-003`, `LOCAL-004`, `LOCAL-005`, `LOCAL-006`, `LOCAL-007`.

- [live-more/n1/local-node-rpc-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n1/local-node-rpc-0.1.json)
- [live-more/n2/local-node-rpc-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n2/local-node-rpc-0.1.json)
- [live-more/n3/local-node-rpc-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n3/local-node-rpc-0.1.json)
- [live-more/n4/local-node-rpc-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n4/local-node-rpc-0.1.json)
- [live-more/n5/local-node-rpc-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/local-node-rpc-0.1.json)
- [live-more/n6/local-node-rpc-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n6/local-node-rpc-0.1.json)
- [live-more/n7/local-node-rpc-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/local-node-rpc-0.1.json)
- [native/local-node-rpc.json](reports/2026-11-20-live-conformance/observations/native/local-node-rpc.json)

### Monitor URI contract drift

Cases: `MC-028`, `MC-029`.

- [followup-native/monitor-contracts-0.1-source-aware/results.json](reports/2026-11-20-live-conformance/observations/followup-native/monitor-contracts-0.1-source-aware/results.json)
- [followup-native/monitor-preflight-0.1-source-aware/results.json](reports/2026-11-20-live-conformance/observations/followup-native/monitor-preflight-0.1-source-aware/results.json)
- [live-more/n3/monitor-contracts-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n3/monitor-contracts-0.1.json)
- [live-more/n3/monitor-preflight-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n3/monitor-preflight-0.1.json)
- [live-more/n4/monitor-contracts-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n4/monitor-contracts-0.1.json)
- [live-more/n4/monitor-preflight-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n4/monitor-preflight-0.1.json)
- [live-more/n5/monitor-contracts-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/monitor-contracts-0.1.json)
- [live-more/n5/monitor-preflight-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/monitor-preflight-0.1.json)
- [live-more/n7/monitor-contracts-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/monitor-contracts-0.1.json)
- [live-more/n7/monitor-preflight-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/monitor-preflight-0.1.json)
- [native/monitor-contracts-0.1/results.json](reports/2026-11-20-live-conformance/observations/native/monitor-contracts-0.1/results.json)
- [native/monitor-preflight-0.1/results.json](reports/2026-11-20-live-conformance/observations/native/monitor-preflight-0.1/results.json)

### Retained HTTP prompt fixture

Cases: `PT-004`, `PT-005`, `PT-006`, `PT-007`, `PT-008`, `PT-009`, `PT-010`, `PT-011`, `PT-012`, `PT-013`, `PT-014`, `PT-015`, `PT-016`, `PT-017`, `PT-018`, `PT-019`, `PT-020`, `PT-021`, `PT-022`.

- [extras/prompt-http.json](reports/2026-11-20-live-conformance/observations/extras/prompt-http.json)
- [live-more/n3/prompt-http-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n3/prompt-http-0.1.json)
- [live-more/n4/prompt-http-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n4/prompt-http-0.1.json)
- [live-more/n5/prompt-http-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/prompt-http-0.1.json)
- [live-more/n7/prompt-http-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/prompt-http-0.1.json)

### Selective receive and guard handling

Cases: `RG-001`, `RG-002`, `RG-003`, `RG-004`, `RG-005`, `RG-006`, `RG-007`, `RG-008`, `SR-015`.

- [live-controls/trealla-sr015-exact-controls.json](reports/2026-11-20-live-conformance/observations/live-controls/trealla-sr015-exact-controls.json)
- [live-more/n3/receive-control-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n3/receive-control-0.1.json)
- [live-more/n4/receive-control-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n4/receive-control-0.1.json)
- [live-more/n5/receive-control-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/receive-control-0.1.json)
- [live-more/n5/selective-receive-0.2.json](reports/2026-11-20-live-conformance/observations/live-more/n5/selective-receive-0.2.json)
- [live-more/n7/receive-control-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/receive-control-0.1.json)
- [public-extra/results.json](reports/2026-11-20-live-conformance/observations/public-extra/results.json)

### Reference types and ownership

Cases: `RF-004`, `RF-005`, `RF-006`, `RF-007`, `RF-008`.

- [live-more/n3/reference-contracts-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n3/reference-contracts-0.1.json)
- [live-more/n4/reference-contracts-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n4/reference-contracts-0.1.json)
- [live-more/n5/reference-contracts-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/reference-contracts-0.1.json)
- [live-more/n7/reference-contracts-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/reference-contracts-0.1.json)

### RPC/promise timeout validation

Cases: `RPC-TIME-001`, `RPC-TIME-002`, `RPC-TIME-003`, `RPC-TIME-010`, `RPC-TIME-011`, `RPC-TIME-012`.

- [followup-native/standalone-boundaries.json](reports/2026-11-20-live-conformance/observations/followup-native/standalone-boundaries.json)
- [live-more/n1/rpc-timeout-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n1/rpc-timeout-0.1.json)
- [live-more/n2/rpc-timeout-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n2/rpc-timeout-0.1.json)
- [live-more/n3/rpc-timeout-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n3/rpc-timeout-0.1.json)
- [live-more/n4/rpc-timeout-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n4/rpc-timeout-0.1.json)
- [live-more/n5/rpc-timeout-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/rpc-timeout-0.1.json)
- [native/rpc-timeout-0.1/results.json](reports/2026-11-20-live-conformance/observations/native/rpc-timeout-0.1/results.json)

### Successor option validation

Cases: `SU-016`, `SU-HTTP-016`.

- [live-more/n6/successor-validation-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n6/successor-validation-0.1.json)
- [live-more/n7/successor-validation-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/successor-validation-0.1.json)

### Portable text and prompt wire protocol

Cases: `TXT-018`, `TXT-019`, `TXT-023`, `TXT-024`, `TXT-026`.

- [live-more/n3/portable-text-0.2.json](reports/2026-11-20-live-conformance/observations/live-more/n3/portable-text-0.2.json)
- [live-more/n4/portable-text-0.2.json](reports/2026-11-20-live-conformance/observations/live-more/n4/portable-text-0.2.json)
- [live-more/n5/portable-text-0.2.json](reports/2026-11-20-live-conformance/observations/live-more/n5/portable-text-0.2.json)
- [live-more/n7/portable-text-0.2.json](reports/2026-11-20-live-conformance/observations/live-more/n7/portable-text-0.2.json)
- [native/portable-text-0.2/swi-portable-text.json](reports/2026-11-20-live-conformance/observations/native/portable-text-0.2/swi-portable-text.json)
- [native/portable-text-0.2/trealla-portable-text.json](reports/2026-11-20-live-conformance/observations/native/portable-text-0.2/trealla-portable-text.json)

### URI routing and source transport

Cases: `NU-001`, `NU-002`, `NU-003`, `NU-004`, `NU-005`, `NU-006`, `NU-007`, `NU-008`, `NU-009`, `NU-010`, `NU-011`, `NU-012`, `NU-013`, `URI-001`, `URI-002`, `URI-004`, `URI-005`, `URI-006`, `URI-007`, `URI-010`, `URI-011`.

- [extras/results.json](reports/2026-11-20-live-conformance/observations/extras/results.json)
- [followup-native/standalone-boundaries.json](reports/2026-11-20-live-conformance/observations/followup-native/standalone-boundaries.json)
- [live-more/n3/node-uri-io-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n3/node-uri-io-0.1.json)
- [live-more/n4/node-uri-io-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n4/node-uri-io-0.1.json)
- [live-more/n5/node-uri-io-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n5/node-uri-io-0.1.json)
- [live-more/n6/uri-atoms-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n6/uri-atoms-0.1.json)
- [live-more/n7/node-uri-io-0.1.json](reports/2026-11-20-live-conformance/observations/live-more/n7/node-uri-io-0.1.json)
- [native/node-uri-io/results.json](reports/2026-11-20-live-conformance/observations/native/node-uri-io/results.json)

## Reviewed decisions

- **N6-CAPACITY-LIBRARY**: 66 exact assertions pass after the documented retention-expiry precondition; original refusals remain. [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json) [Evidence](reports/2026-11-20-live-conformance/observations/live-controls/n6-paused-library.json)
- **N6-CAPACITY-SUPPORTING**: 55 exact assertions pass after the documented retention-expiry precondition; original refusals remain. [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json) [Evidence](reports/2026-11-20-regression-triage/n6/results.json)
- **SWI-RETIREMENT-DEPLOYED**: Native 0c11f2c is deployed; N3/N4 each pass 100 unchanged repetitions. Other URI failures remain open. [Evidence](reports/2026-11-20-retirement-live/live/n3-nu003.json) [Evidence](reports/2026-11-20-retirement-live/live/n4-nu003.json)
- **N6-LOCAL-REPLAY**: Three passing replays do not establish the cause of the original transport error. [Evidence](reports/2026-11-20-regression-triage/n6/results.json)
- **MONITOR-URI-VERSION**: The author-directed 17 November decision accepts URI text, including monitor targets. Version 0.2 verifies real delivery to the same actor; the atom-only 0.1 cases and old reports remain unchanged. [Evidence](reports/2026-11-20-backlog-baseline/contract-review.json) [Evidence](reports/2026-11-20-backlog-baseline/browser-monitor-text.json) [Evidence](reports/2026-11-20-backlog-baseline/live-monitor-text.json) [Evidence](reports/2026-11-20-backlog-baseline/monitor-contracts-v2.json) [Evidence](reports/2026-11-20-backlog-baseline/monitor-preflight-v2.json)
- **PROMPT-ROUTE-PRECONDITION**: Standalone Trealla requires http_sessions(true). Both enabled fixtures pass all 38 assertions. New preflight blocks cases and returns a failing run when the route is absent. [Evidence](reports/2026-11-20-backlog-baseline/http-prompts.json) [Evidence](reports/2026-11-20-backlog-baseline/prompt-disabled.json)
- **RPC-NUMERIC-CANDIDATE-SWI**: At the baseline checkpoint: SWI explicitly supplied variable/none timeouts now fail validation before dispatch; omitted defaults remain unchanged. Production findings remain open pending qualification/deployment. See the later deployed decision for current status. [Evidence](reports/2026-11-20-backlog-baseline/validation-candidate.json) [Evidence](reports/2026-11-20-backlog-baseline/validation-candidate.json) [Evidence](reports/2026-11-20-backlog-baseline/validation-candidate.json) [Evidence](reports/2026-11-20-backlog-baseline/validation-candidate.json)
- **RPC-NUMERIC-CANDIDATE-TREALLA**: At the baseline checkpoint: Trealla explicitly supplied infinite timeouts are rejected as non-numeric. Production findings remain open pending qualification/deployment. See the later deployed decision for current status. [Evidence](reports/2026-11-20-backlog-baseline/validation-candidate.json) [Evidence](reports/2026-11-20-backlog-baseline/validation-candidate.json)
- **RPC-NUMERIC-DEPLOYED-SWI**: Committed repair deployed and verified on the corresponding runtime nodes. Exact-image and live unchanged assertions pass; omitted defaults remain unchanged. Original observations remain immutable. [Evidence](reports/2026-11-20-rpc-validation-live/live/n1-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n2-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n3-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n4-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/execution/image-rpc-summary.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n1-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n2-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n3-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n4-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/execution/image-rpc-summary.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n1-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n2-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n3-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n4-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/execution/image-rpc-summary.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n1-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n2-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n3-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n4-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/execution/image-rpc-summary.json)
- **RPC-NUMERIC-DEPLOYED-TREALLA**: Committed repair deployed and verified on the corresponding runtime nodes. Exact-image and live unchanged assertions pass; omitted defaults remain unchanged. Original observations remain immutable. [Evidence](reports/2026-11-20-rpc-validation-live/live/n5-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/execution/image-rpc-summary.json) [Evidence](reports/2026-11-20-rpc-validation-live/live/n5-rpc-timeout.json) [Evidence](reports/2026-11-20-rpc-validation-live/execution/image-rpc-summary.json)
- **URI-OWNED-PEER-CREDENTIALS**: Four owned native observations require explicit credentials for both tested logical URL spellings. Identical assertions pass with that fixture correction on both platforms. Production policy is unchanged; no live observation is closed by this decision. [Evidence](reports/2026-11-20-uri-source-triage/alias-credentials-control.json) [Evidence](reports/2026-11-20-uri-source-triage/final-uri-pack.json) [Evidence](reports/2026-11-20-uri-source-triage/linux-uri-pack.json) [Evidence](reports/2026-11-20-uri-source-triage/alias-credentials-control.json) [Evidence](reports/2026-11-20-uri-source-triage/final-uri-pack.json) [Evidence](reports/2026-11-20-uri-source-triage/linux-uri-pack.json) [Evidence](reports/2026-11-20-uri-source-triage/alias-credentials-control.json) [Evidence](reports/2026-11-20-uri-source-triage/final-uri-pack.json) [Evidence](reports/2026-11-20-uri-source-triage/linux-uri-pack.json) [Evidence](reports/2026-11-20-uri-source-triage/alias-credentials-control.json) [Evidence](reports/2026-11-20-uri-source-triage/final-uri-pack.json) [Evidence](reports/2026-11-20-uri-source-triage/linux-uri-pack.json)
- **TREALLA-CLAUSE-IO-CANDIDATE**: Trealla d1ad920 restores public write/writeln clause reflection and variable sharing; final source passes all 112 unit groups on macOS and Linux. N5 still runs e99126b. This candidate does not close deployed NU-011 findings. [Evidence](reports/2026-11-20-uri-source-triage/final-uri-pack.json) [Evidence](reports/2026-11-20-uri-source-triage/linux-uri-pack.json) [Evidence](reports/2026-11-20-uri-source-triage/complete-unit-summary.json) [Evidence](reports/2026-11-20-uri-source-triage/complete-unit-summary.json)
- **CANONICAL-URI-NATIVE-CANDIDATE**: Version 0.2 separates caller visibility from explicit-URL routing; canonical alias credentials/topology/address/delivery assertions pass on both platforms. Old mixed 0.1 goals remain immutable and are not claimed to pass unchanged. These are candidate controls, not live observations; production dispositions remain open. [Evidence](reports/2026-11-20-canonical-uri-qualification/macos-uri-pack.json) [Evidence](reports/2026-11-20-canonical-uri-qualification/linux-uri-pack.json) [Evidence](reports/2026-11-20-canonical-uri-qualification/qualification-checks.json)

## Additional qualification findings

- **TPL-SANDBOX-CASCADE**: Resolved in the local test candidate. The fixed 100 ms snapshot raced grandchild startup; an explicit readiness message preserves the four-actor and cascade assertions. Session cleanup now runs on failure/exception too. Both complete unit suites pass, and injected failures still fail promptly while reclaiming all four actors. Production runtime cleanup code is unchanged. [Evidence](reports/2026-11-20-backlog-baseline/qualification-limitations.json) [Evidence](reports/2026-11-20-cleanup-qualification/complete-unit-summary.json) [Evidence](reports/2026-11-20-cleanup-qualification/failure-controls.json)
- **TPL-CACHE-EVICTION-LINUX**: Resolved in the local test candidate. Five unchanged production-sized cache properties shared one 30-second watchdog; a timing probe completed the old aggregate in 27.6 seconds. Each property now has a fresh process and the same 30-second watchdog, plus a reclamation check. All five bodies and the real cache capacity 100 are unchanged. Complete macOS and Linux unit suites pass; the aggregate entry point remains available. [Evidence](reports/2026-11-20-backlog-baseline/linux-qualification-limitations.json) [Evidence](reports/2026-11-20-cleanup-qualification/complete-unit-summary.json)

Regenerate: `python3 runner/backlog.py`. Historical report directories are never edited.
