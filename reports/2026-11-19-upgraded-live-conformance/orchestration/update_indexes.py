from pathlib import Path
import json
R=Path('/Users/lager/trinity-conformance');D=R/'reports/2026-11-19-upgraded-live-conformance';O=Path(__file__).resolve().parents[1]
assert (O/'completion-verification.json').exists(),'Complete the selected runs before updating the current index'
results=json.loads((D/'RESULTS.json').read_text());base='reports/2026-11-19-upgraded-live-conformance/'
def fmt(c):return ', '.join(str(c[k])+' '+k for k in ['pass','fail','blocked','unsupported','not_applicable','observed'] if c.get(k)) or 'not selected'
lines=['# Current Web Prolog conformance coverage','',
'Updated **19 November 2026**, after the HTTP-context and actor-retirement fixes were deployed. The refreshed run covers **78 manifests / 1,984 main input rows** at suite revision `58cbd6b`. **It is not all-green.** Every row has current observations or explicit blocked/applicability outcomes; four retained-context return assertions remain blocked. Repeated historical packs, modes and routes are not independent language features.','',
f'[Full report]({base}REPORT.md) · [per-file results]({base}SUMMARY.json) · [case inventory]({base}verification.json) · [exact inputs]({base}suite-inputs.json).','',
'## Current public observations','',
'Native SWI N0–N4 runs `a2ff186` / 11.0.0; Trealla N5 runs `3a5b761` / 3.14.20. N6 and N7 are unchanged comparative deployments. Public N0 is RELATION, N1/N6 ISOBASE, N2 ISOTOPE and N3/N4/N5/N7 ACTOR. Private-only ownership and unbounded controls use owned image-backed fixtures; the private admin endpoint is not certified by this sweep.','',
'| Node | Primary public selection |','|---|---|']
for n,c in results['primary'].items():lines.append('| '+n.upper()+' | '+fmt(c)+' |')
lines+=['',
'N3/N4/N5 each pass all 118 selected ACTOR/HTTP cases. N7’s five original 429 refusals remain in the files; all five pass after the requested 61-second quiet period and 15-second pauses. Its remaining primary cases used the longer pauses.','',
'## Live library versions 0.1–0.4','',
'The four versions contain 842 input rows per transport. Each selected mode checks the original helper source, deterministic finite results and bounded prefixes with recovery. Retained WebSocket controls also stop their producer; stateless HTTP recovery alone does not prove reclamation.','',
'| Node | HTTP | Retained WSS |','|---|---|---|']
for n,m in results['live_library'].items():lines.append('| '+n.upper()+' | '+fmt(m['http'])+' | '+(fmt(m['wss']) if n in ['n3','n4','n5','n7'] else 'not exposed')+' |')
lines+=['',
'N6 retains four original HTTP 503 query-capacity refusals on STDLIB-292–295. All four unchanged assertions pass in separate paused controls; the final quiet period and recovery check exceed the verified 300-second idle lifetime. Original refusals remain in the table.','',
'N7 stateless requests each create a public engine. Its 20-starts/minute rule requires slower HTTP traffic; final HTTP completion pauses four seconds after each request. Original capacity refusals and carried-forward observations remain explicit. No live limit was changed.','',
'## Additional current evidence','',
'- All 19 live HTTP prompt cases pass on N2/N3/N4/N5 with session-creation pacing; race requests are unchanged.',
'- Live N5 retained HTTP ordinary names pass HCTX-002. Its supplementary ready-producer promise isolation/collection control also passes. Pending-producer barriers remain controlled-fixture measurements.',
'- The three exact-image private gates each pass 45 ACTOR cases plus seven source-directive cases with separate execution-only principals.',
'- Owned authenticated/anonymous HTTP context controls pass 3/3 each; native naming passes 16/16; all three bounded noncompletion controls pass; enabled HTTP prompt fixtures pass 19/19 per native runtime.',
'- The source-aware native monitor selection records 94 pass / 4 fail; preflight records 44 pass / 4 fail. MC-028/029 conflict with documented URI text acceptance.',
'- Real Chromium Worker/main browser-only compatibility records 4 pass / 2 fail (B-SV-006) using package `ce96659`, engine 10.1.19. This is not public UI certification.',
'- Runner tooling unit tests pass 114/114, outside conformance case counts.','',
'## Findings and limits','',
'The retained-context matrix remains red at **46 pass / 11 fail / 4 blocked**, with six passing closure controls. Trealla outbound-client isolation and controlled promise routes fail; automatic origin-context return remains unresolved. Attachment instrumentation still fails its setup boundary.','',
'Live Trealla SR-015 fails in the extended run and unchanged repeats while the owned fixture passes. Diagnostic lists retain both inner alternatives at all three wait settings; this is a public execution-path cut finding. URI/deadline/HTTP/document supporting selections retain failures. TXT-019/026 reach an invalid prompt-reference response before their text comparison. The report separates those protocol/fixture limits, exact-profile admission expectations, original wrong-transport attempts, and real assertion outcomes.','',
'No runtime source, versioned assertion, installed engine, live configuration or quota changed during the run. Persistent service container/image identities were preserved. Main input rows are accounted for, but blocked operations are never passes, and this is not complete ISO, every configuration, every browser mode, admin, UI or security certification.','',
'## Historical evidence','',
'The [earlier full SWI 11 run](reports/2026-11-19-deployed-conformance/REPORT.md), [repair checkpoint](reports/2026-11-19-conformance-repairs/REPORT.md), [naming alignment](reports/2026-11-19-client-naming/REPORT.md), [connection-cleanup diagnosis](reports/2026-11-19-connection-cleanup/REPORT.md), [HTTP context checkpoint](reports/2026-11-19-http-context/REPORT.md), and [OPEN repair](reports/2026-11-19-open-exercise-repair/REPORT.md) remain unchanged. Their pre-deployment boundaries describe their dates, not current live selection.','',
'The [Appendix B matrix](docs/APPENDIX_B_COVERAGE.md) and [library clause inventory](docs/LIBRARY_TEST_GAPS.md) retain their scoped obligation evidence. Current observations do not silently rewrite historical failures or expand those claims.']
(R/'CURRENT_COVERAGE.md').write_text('\n'.join(lines)+'\n')
p=R/'README.md';s=p.read_text();start=s.index('## Current consolidated results');end=s.index('The following earlier qualification records retain their dated scope;')
new='''## Current consolidated results

The [fresh live-node run](reports/2026-11-19-upgraded-live-conformance/REPORT.md)
covers all **78 manifests / 1,984 main input rows** after deployment of native
`a2ff186` and Trealla `3a5b761`. **It is not all-green.** Live applicable cases,
owned-image private controls, supporting diagnostics, blocked assertions and
superseded harness attempts are reported separately. Every input row is
accounted for; four context-return assertions remain blocked.

N3/N4/N5 pass the 118-case ACTOR/HTTP primary selection. N7's five initial 429
refusals pass with the requested quiet period and longer pauses; the originals
remain visible. All four historical library versions ran on the live HTTP and
selected retained WebSocket endpoints. N6's four initial query-capacity
refusals also have separate passing paused controls. HTTP prompt tests pass 19/19 on each
N2/N3/N4/N5 with paced creation. The three image-backed private gates pass
45+7 each, and the runner's 114 unit tests pass.

The wider context matrix remains red at 46 pass / 11 fail / 4 blocked. The run
also exposes a reproducible public Trealla receive-body cut difference, retains
URI/deadline/document and prompt-reference findings, and records browser
B-SV-006 failures in both real Chromium modes. No runtime, assertion, installed
engine, live service configuration or quota was changed by this test run.

[Current matrix](CURRENT_COVERAGE.md),
[per-file observations](reports/2026-11-19-upgraded-live-conformance/SUMMARY.json),
[case inventory](reports/2026-11-19-upgraded-live-conformance/verification.json)
and [input hashes](reports/2026-11-19-upgraded-live-conformance/suite-inputs.json)
make the scope reviewable. These repeated versions/modes are not a percentage
of language conformance. Public browser UI, private admin operations and all
configuration/security boundaries are not certified here.

The common [client naming contract](profiles/client-naming-0.1.md) keeps ordinary
names client scoped and published services node-wide. The
[deployment and smoke record](https://github.com/torbjornlager/trinity-demonstrator/blob/84cc9b02a0ef7860d1f04c64080719f55e6652aa/docs/verification/http-context-live-2026-11-19/REPORT.md)
identifies the live release. The [earlier full run](reports/2026-11-19-deployed-conformance/REPORT.md)
and all repair/naming/OPEN checkpoints retain their original failures and
pre-deployment boundaries. The fixes have since been deployed.

'''
p.write_text(s[:start]+new+s[end:]);print('Updated README and current matrix from the completed report')
