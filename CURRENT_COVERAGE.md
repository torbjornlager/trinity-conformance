# Current Web Prolog conformance coverage

Updated **20 November 2026**, after the admission rollout; the complete sweep below ran on 19 November after the HTTP-context and actor-retirement fixes were deployed. The refreshed run covers **78 manifests / 1,984 main input rows** at suite revision `58cbd6b`. **It is not all-green.** Every row has current observations or explicit blocked/applicability outcomes; four retained-context return assertions remain blocked. Repeated historical packs, modes and routes are not independent language features.

[Full report](reports/2026-11-19-upgraded-live-conformance/REPORT.md) · [per-file results](reports/2026-11-19-upgraded-live-conformance/SUMMARY.json) · [case inventory](reports/2026-11-19-upgraded-live-conformance/verification.json) · [exact inputs](reports/2026-11-19-upgraded-live-conformance/suite-inputs.json).

## Later admission rollout

The [configurable admission rollout](reports/2026-11-19-public-admission/REPORT.md)
selects native `e25b230`, Trealla `2d5042b`, ECLiPSe adapter `31dcdfc` and browser
package `0d024e5`, preserving all engine bytes and existing resource bounds.
Public N1–N7 use explicit 120-entry presets with their documented accounting
units. All 980 live finite HTTP probes pass; paced HTTP prompt checks pass
19/19 each on N2/N3/N4/N5. The owned OPEN exercise check passes 34 entries /
136 checks at the public preset and 16 actor/session slots.

This separate regression qualification does not repeat all 78 manifests. The
full-sweep tables below retain the earlier source/configuration scope and
failures, including context restoration and the live Trealla cut finding.

## Full-sweep public observations

At that full sweep, native SWI N0–N4 ran `a2ff186` / 11.0.0 and Trealla N5 ran `3a5b761` / 3.14.20. At that sweep, N6 and N7 were unchanged comparative deployments. Public N0 is RELATION, N1/N6 ISOBASE, N2 ISOTOPE and N3/N4/N5/N7 ACTOR. Private-only ownership and unbounded controls use owned image-backed fixtures; the private admin endpoint is not certified by this sweep.

| Node | Primary public selection |
|---|---|
| N0 | 1 pass |
| N1 | 12 pass |
| N2 | 12 pass |
| N3 | 118 pass |
| N4 | 118 pass |
| N5 | 118 pass |
| N6 | 12 pass |
| N7 | 113 pass, 5 fail |

N3/N4/N5 each pass all 118 selected ACTOR/HTTP cases. N7’s five original 429 refusals remain in the files; all five pass after the requested 61-second quiet period and 15-second pauses. Its remaining primary cases used the longer pauses.

## Live library versions 0.1–0.4

The four versions contain 842 input rows per transport. Each selected mode checks the original helper source, deterministic finite results and bounded prefixes with recovery. Retained WebSocket controls also stop their producer; stateless HTTP recovery alone does not prove reclamation.

| Node | HTTP | Retained WSS |
|---|---|---|
| N1 | 842 pass | not exposed |
| N2 | 842 pass | not exposed |
| N3 | 842 pass | 842 pass |
| N4 | 842 pass | 842 pass |
| N5 | 842 pass | 842 pass |
| N6 | 838 pass, 4 fail | not exposed |
| N7 | 842 pass | 842 pass |

N6 retains four original HTTP 503 query-capacity refusals on STDLIB-292–295. All four unchanged assertions pass in separate paused controls; the final quiet period and recovery check exceed the verified 300-second idle lifetime. Original refusals remain in the table.

N7 stateless requests each create a public engine. Its 20-starts/minute rule requires slower HTTP traffic; final HTTP completion pauses four seconds after each request. Original capacity refusals and carried-forward observations remain explicit. No live limit was changed.

## Additional current evidence

- All 19 live HTTP prompt cases pass on N2/N3/N4/N5 with session-creation pacing; race requests are unchanged.
- Live N5 retained HTTP ordinary names pass HCTX-002. Its supplementary ready-producer promise isolation/collection control also passes. Pending-producer barriers remain controlled-fixture measurements.
- The three exact-image private gates each pass 45 ACTOR cases plus seven source-directive cases with separate execution-only principals.
- Owned authenticated/anonymous HTTP context controls pass 3/3 each; native naming passes 16/16; all three bounded noncompletion controls pass; enabled HTTP prompt fixtures pass 19/19 per native runtime.
- The source-aware native monitor selection records 94 pass / 4 fail; preflight records 44 pass / 4 fail. MC-028/029 conflict with documented URI text acceptance.
- Real Chromium Worker/main browser-only compatibility records 4 pass / 2 fail (B-SV-006) using package `ce96659`, engine 10.1.19. This is not public UI certification.
- Runner tooling unit tests pass 114/114, outside conformance case counts.

## Findings and limits

The retained-context matrix remains red at **46 pass / 11 fail / 4 blocked**, with six passing closure controls. Trealla outbound-client isolation and controlled promise routes fail; automatic origin-context return remains unresolved. Attachment instrumentation still fails its setup boundary.

Live Trealla SR-015 fails in the extended run and unchanged repeats while the owned fixture passes. Diagnostic lists retain both inner alternatives at all three wait settings; this is a public execution-path cut finding. URI/deadline/HTTP/document supporting selections retain failures. TXT-019/026 reach an invalid prompt-reference response before their text comparison. The report separates those protocol/fixture limits, exact-profile admission expectations, original wrong-transport attempts, and real assertion outcomes.

No runtime source, versioned assertion, installed engine, live configuration or quota changed during the run. Persistent service container/image identities were preserved. Main input rows are accounted for, but blocked operations are never passes, and this is not complete ISO, every configuration, every browser mode, admin, UI or security certification.

## Historical evidence

The [earlier full SWI 11 run](reports/2026-11-19-deployed-conformance/REPORT.md), [repair checkpoint](reports/2026-11-19-conformance-repairs/REPORT.md), [naming alignment](reports/2026-11-19-client-naming/REPORT.md), [connection-cleanup diagnosis](reports/2026-11-19-connection-cleanup/REPORT.md), [HTTP context checkpoint](reports/2026-11-19-http-context/REPORT.md), and [OPEN repair](reports/2026-11-19-open-exercise-repair/REPORT.md) remain unchanged. Their pre-deployment boundaries describe their dates, not current live selection.

The [Appendix B matrix](docs/APPENDIX_B_COVERAGE.md) and [library clause inventory](docs/LIBRARY_TEST_GAPS.md) retain their scoped obligation evidence. Current observations do not silently rewrite historical failures or expand those claims.
