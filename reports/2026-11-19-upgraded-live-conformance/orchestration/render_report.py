from pathlib import Path
import json,collections,hashlib,sys
R=Path('/Users/lager/trinity-conformance');O=Path(__file__).resolve().parents[1];D=O/'report-draft' if '--draft' in sys.argv else R/'reports/2026-11-19-upgraded-live-conformance'
def read(p):return json.loads(p.read_text())
def rs(p):return read(p).get('results',[]) if p.exists() else []
def counts(rows):return dict(collections.Counter(r['status'] for r in rows))
def text_counts(c):return ', '.join(str(c[k])+' '+k for k in ['pass','fail','blocked','error','unsupported','not_applicable','deferred','observed','diagnostic_error'] if c.get(k)) or 'pending'
verification=read(D/'verification.json');summary=read(D/'SUMMARY.json');revision=summary['suite_revision']
primary={n:counts([r for f in (O/'observations'/n).glob('*.json') for r in rs(f)]) for n in ['n0','n1','n2','n3','n4','n5','n6','n7']}
library={}
for n in ['n1','n2','n3','n4','n5','n6','n7']:
 rows=[r for f in (O/'live-library'/n).glob('*.json') for r in rs(f)]
 library[n]={m:counts([r for r in rows if r.get('candidate','').endswith('-'+m)]) for m in ['http','wss']}
not_executed=[(p['suite'],[p['cases'][i]['id'] for i in p['not_executed_case_indexes']]) for p in verification['coverage'] if p['not_executed_case_indexes']]
lines=['# Conformance after the HTTP-context deployment — 19 November 2026','',
'**The run is not all-green.** The frozen inventory contains **78 manifests / 1,984 main input rows**. Every row has a current observation or an explicit blocked/applicability outcome. A blocked operation is not a pass or a completed language assertion. Historical versions, modes and routes repeat obligations; their totals are not a language-conformance percentage.','',
f'The suite revision is `{revision}`. Live N0–N4 use native `a2ff186` / SWI 11.0.0; live N5 uses Trealla `3a5b761` / 3.14.20. N6 and N7 were not upgraded in this release and supply comparative observations. Source identities and owned-image provenance are in [provenance](execution/provenance.json). The private admin endpoint and public browser UI are not certified by this public-node sweep.','',
'[Exact inputs](suite-inputs.json), [per-file observations](SUMMARY.json), [case inventory](verification.json), and [preservation](preservation.json) separate current results from first attempts and fixture-only evidence. The [earlier full run](../2026-11-19-deployed-conformance/REPORT.md) is unchanged.','',
'## Public-node observations','',
'| Node | Primary selection | Scope |','|---|---|---|']
for n in primary:
 scope='RELATION error admission only' if n=='n0' else 'ISOBASE HTTP baseline' if n in ['n1','n2','n6'] else '106 ACTOR cases + 12 HTTP cases'
 lines.append('| '+n.upper()+' | '+text_counts(primary[n])+' | '+scope+' |')
lines += ['',
'N7’s five original HTTP 429 admission refusals remain in its base files. All **five pass** in the [user-requested paused controls](execution/n7-paced-controls.json), after a 61-second quiet period and with 15-second pauses between cases/session starts. Remaining primary cases completed with those longer pauses. This gives passing observations for every primary case; the earlier refusals are not rewritten.','',
'The broader API selections are under `observations/live-more/`. They include Boolean validation, callbacks, supervisor IDs/lifecycle, naming, selective receive, monitors, runtime settings, URI forms, source copying, paging, errors, RPC, HTTP fields and document validation. Lower-profile N1/N2/N6 assertions use their HTTP API; WebSocket-only operations are not applicable there. Policy/availability diagnostics and browser compatibility expectations are not native language certificates.','',
'## All four library versions on the live nodes','',
'The manifests contain 112, 146, 289 and 295 cases: **842 per selected transport**. Stateless HTTP uses each pack’s original helper source and deterministic answer assertions. Retained WebSocket tests use the maintained per-pack session lifetime, including ordered bounded prefixes, stop and recovery.','',
'| Node | HTTP, versions 0.1–0.4 | Retained WSS, versions 0.1–0.4 |','|---|---|---|']
for n,modes in library.items():lines.append('| '+n.upper()+' | '+text_counts(modes['http'])+' | '+(text_counts(modes['wss']) if n in ['n3','n4','n5','n7'] else 'not exposed by this live endpoint')+' |')
lines += ['',
'N6’s first library sweep records **838 pass / 4 HTTP 503 `query_limit_exceeded` refusals**, on STDLIB-292–295. All four unchanged bounded-prefix assertions pass in [separate paused controls](observations/live-controls/n6-paused-library.json). The first two controls used 61-second quiet periods; later controls and the final recovery check used 303 seconds, exceeding the verified live 300-second idle lifetime. These controls supplement the original results; they do not erase the refusals or establish internal producer reclamation. No live limit was changed.','',
'N7’s [verified live admission policy](execution/n7-admission-policy.json) allows 20 fresh engine starts per client per minute, at most four public engines globally and two per client. Each stateless HTTP call uses a fresh engine. The initial library attempt exceeded the start allowance; its 429 outcomes are retained separately. The completion uses **four seconds after each completed HTTP request**, and 15 seconds between new WebSocket sessions. Completed first observations are carried forward with their origin recorded; refused or unexecuted rows are retried. No capacity, quota, policy or live runtime was changed.','',
'## Controlled conditions requiring owned fixtures','',
'Public OPEN access cannot establish the private identity preconditions for every ownership test, and unbounded computations must not be left running on live nodes. Those selections use disposable, network-isolated fixtures built from the deployed images/runtime files. Their results are **not live endpoint observations**. The N2-image fixture advertises ACTOR for its release gate; live N2 remains ISOTOPE.','',
'| Selection | Result |','|---|---|',
'| Three exact deployed-image private ACTOR gates | 45/45 release + 7/7 source-directives each; two distinct execution-only principals |',
'| Controlled retained HTTP namespaces, authenticated and anonymous | 3/3 in each mode; retained Trealla HTTP routes enabled in the owned fixture |',
'| Shared native client naming | 16/16, SWI and Trealla |',
'| Bounded countall noncompletion | 3/3 SWI/Trealla/GNU entry, external-stop and recovery controls |',
'| HTTP prompt API with session routes enabled | 19/19 SWI and 19/19 Trealla |',
'| Promise/yield and HTTP interoperation | 24 promise selections + 8 HTTP interoperation selections pass; diagnostics remain observations |',
'| Retained-context matrix | 46 pass / 11 fail / 4 blocked, including six controlled-producer rows |',
'| Context closure controls | 6/6 |',
'| Source-aware monitor contracts | 94 pass / 4 fail; preflight 44 pass / 4 fail |',
'| Native node-URI I/O | 12 pass / 14 fail |',
'| Portable text 0.2 | 24 pass / 2 fail per native engine |',
'| Browser-only compatibility in real Chromium Worker/main | 4 pass / 2 fail (B-SV-006), using the deployed browser package; not a public UI certificate |',
'| Runner unit tests | 114 pass, outside conformance case totals |','',
'Owned native library versions and supporting RPC/deadline, HTTP-field and document fixtures also ran. Use the per-file index for their raw outcomes. The live HTTP prompt pack passes 19/19 on each N2, N3, N4 and N5. N5’s enabled retained-HTTP route also passes HCTX-002 ordinary-name isolation and the ready-producer promise ownership control. Pending-producer/release barriers remain separate owned-fixture measurements.','',
'## Remaining findings','',
'- **Remote context ownership remains red.** SWI round-trip origin-name/promise restoration fails. Trealla outbound-client isolation and controlled promise routes fail, and four return assertions are blocked by a preceding source/export refusal. The [remote-context design](../../profiles/remote-client-context-design.md) distinguishes outbound client isolation from explicit return-context restoration. These are separate from the passing local ordinary-name and retained HTTP namespace checks.',
'- **Monitor expectation drift remains visible.** MC-028/029 require rejecting URI text forms accepted by the current documented URI contract. They fail on the live upgraded ACTOR nodes and source-aware native fixtures. Assertions were not revised to produce passes.',
'- **Live public receive failure.** Trealla SR-015 failed in the extended live run while the owned fixture passed. Three repeats with original source options fail; three explicit-empty-program variants also fail. Separate diagnostic projections return `[one-a,one-b,two-a,two-b]` at timeout 0, 0.05 and 0.2; the case expects `[one-a,two-a]`. The result identifies a cut-semantics difference in this live public execution path; the diagnostic waits do not change it. The diagnostic variants are observations, never conformance passes.',
'- **Supporting URI/deadline/document failures remain.** Generic RPC, local-node RPC, HTTP options, source-relative documents and protocol/error envelopes have differing admission and fixture contexts. Raw failures do not by themselves isolate a defect to an engine.',
'- **Text input fixture limits remain.** TXT-019/026 return `invalid_prompt_ref` in the maintained portable-text client before their intended text comparison. The separately enabled HTTP prompt pack passes. This run retains the text failures and does not relabel them as Unicode-runtime findings.',
'- **Incomplete auxiliary controls remain.** The retained-context attachment instrumentation no longer matches its source boundary. A failed instrumentation precondition supplies no attachment-ordering assertion result. This keeps the wider gate incomplete.', '',
'### Input rows without a completed execution observation','']
for suite,ids in not_executed:lines.append('- `'+suite+'`: '+', '.join('`'+i+'`' for i in ids)+'.')
if not not_executed:lines.append('None in the main inventory; configuration applicability and auxiliary controls still limit qualification.')
lines += ['',
'## Harness corrections and preservation','',
'Exact-profile RELATION/ISOBASE negative admission expectations are not applicable to higher-profile ACTOR nodes; browser-only compatibility expectations on native runtimes are also out of scope. Their raw attempts remain indexed with those classifications. The browser-only pack has separate real-Chromium observations.\n\nThe run retains earlier overlapping worker attempts, wrong WebSocket transport attempts on HTTP-only nodes, and the initial HTTPS/WSS page-control call-site error. Corrected serialized/HTTP/page-control observations are separate files. The process selector was corrected for macOS’s `Python` executable name; the N7 quiet period was restarted after the old worker was actually stopped. The final paused runs use one worker per endpoint.','',
'Two owned adapters initially stopped before case execution because the minimal image lacked `ps`; a test-only image adds procps. Its first copied runner snapshot also lacked profile files used for provenance hashing; those frozen files were copied verbatim before rerunning. These setup failures are not runtime-language failures. Runtime implementation files, versioned manifests, assertions and installed engines were not changed.','',
'No live service was restarted or reconfigured during this run. Persistent Compose container/image identities match the before snapshot. Owned fixture containers were removed and their observations retained. This identity check does not certify every internal mutable value: tests intentionally create and retire their own actors, sessions and private data.','',
'The run does not certify every browser mode, private admin operation, public UI flow, runtime configuration, external ISO obligation or security boundary. Earlier browser/obligation reports retain their dated scope. Operator source and execution plans are archived under [orchestration](orchestration/build_report.py); exported evidence is covered by [files-sha256.json](files-sha256.json).']
extra=rs(O/'public-extra/results.json')
supplementary=[r for r in extra if r.get('suite') in ['supervisor-diagnostics-0.1','worker-diagnostics-0.1','native-terminal-newline-0.1','portable-text-0.1','wire-capabilities-0.1']]
actors=['n3','n4','n5','n7'];matrix=['## Directed public ACTOR interoperability','','Each cell contains the three unchanged interoperation cases. These finite actor controls do not establish remote promise/context ownership.','',
'Supplementary public diagnostics, text, terminal and wire selections: '+text_counts(counts(supplementary))+' across N3/N4/N5/N7. DEMO-019 on N3: '+text_counts(counts([r for r in extra if r.get("suite")=="demonstrator-tutorials-0.1"]))+'.','','| Caller → peer | N3 | N4 | N5 | N7 |','|---|---|---|---|---|']
for a in actors:
 cells=[]
 for b in actors:
  selected=[r for r in extra if r.get('suite')=='interop-actor-0.1' and r.get('candidate')==a and r.get('peer')==b]
  cells.append('—' if a==b else text_counts(counts(selected)))
 matrix.append('| '+a.upper()+' | '+' | '.join(cells)+' |')
naming=[r for r in extra if r.get('suite')=='client-naming-0.1' and r.get('candidate')=='n7'];matrix+=['','Fresh N7 multi-client naming: '+text_counts(counts(naming))+'.','']
pos=lines.index('## All four library versions on the live nodes');lines[pos:pos]=matrix
(D/'REPORT.md').write_text('\n'.join(lines)+'\n')
writeback=dict(primary=primary,live_library=library,n6_paused_library=counts(rs(O/'live-controls/n6-paused-library.json')),case_rows_without_completed_execution=not_executed)
(D/'RESULTS.json').write_text(json.dumps(writeback,indent=2)+'\n')
hashes={str(p.relative_to(D)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(D.rglob('*')) if p.is_file() and p.name!='files-sha256.json'}
(D/'files-sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
print('Rendered report and verified inventory of',len(hashes),'artifacts')
