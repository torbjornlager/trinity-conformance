from pathlib import Path
import json,collections
P=Path(__file__).resolve().parents[1];R=Path('/private/tmp/claude-502/-Users-lager-trinity-demonstrator/58219eb7-1e68-4089-a2dd-25c3117837f6/scratchpad/tc');D=R/'reports/2026-11-24-post-xn-conformance';data=json.loads((D/'RESULTS.json').read_text());assert (P/'completion-verification.json').exists()
def fmt(c):return ', '.join(str(c[k])+' '+k for k in ['pass','fail','blocked','error','unsupported','not_applicable','observed','diagnostic_error'] if c.get(k)) or 'none'
lines=['# Current Web Prolog conformance coverage','',
'Updated **20 November 2026** after a fresh complete sweep of the admission release. The inventory contains **78 manifests / 1,984 input rows**, at suite revision `aeb1329`. **It is not all-green.** Repeated versions, modes and routes are not independent language features; blocked assertions are not passes.','',
'[Full report](reports/2026-11-24-post-xn-conformance/REPORT.md) · [per-file results](reports/2026-11-24-post-xn-conformance/SUMMARY.json) · [case inventory](reports/2026-11-24-post-xn-conformance/verification.json) · [frozen inputs](reports/2026-11-24-post-xn-conformance/suite-inputs.json).','',
'## Current release','',
'Native SWI `e25b230` / 11.0.0, Trealla `2d5042b` / 3.14.20, ECLiPSe adapter `31dcdfc` and browser package `0d024e5` are the selected sources. The [admission deployment](reports/2026-11-19-public-admission/REPORT.md) documents configurable public 120-entry presets and their distinct accounting units. Engine versions and concurrency/resource bounds are unchanged. Browser-local execution has no server admission budget.','',
'## Primary public selections','',
'| Node | Result |','|---|---|']
for n,c in data['primary'].items():lines.append('| '+n.upper()+' | '+fmt(c)+' |')
lines+=['','N0 selects RELATION error admission, N1/N2/N6 select the HTTP baseline, and N3/N4/N5/N7 select 106 ACTOR cases plus 12 HTTP cases. N7 now passes its complete primary selection without the previous sweep’s five rate refusals. Broader supporting API observations are separate and remain mixed. This run additionally covers N7 in that extended selection; those new observations are not automatically regressions.','',
'## Live standard-library versions 0.1–0.4','',
'The four versions contain 842 input rows per transport; the live matrix records 9,262 observations. Stateless requests have 0.8-second start spacing, retained sessions preserve stop/recovery assertions, and N6 receives 303-second quiet periods before bounded generators.','',
'| Node | HTTP | Retained WSS |','|---|---|---|']
for n,m in data['live_libraries'].items():lines.append('| '+n.upper()+' | '+fmt(m['http'])+' | '+(fmt(m['wss']) if n in ['n3','n4','n5','n7'] else 'not exposed')+' |')
controls=json.loads((P/'live-controls/n6-paused-library.json').read_text()) if (P/'live-controls/n6-paused-library.json').exists() else dict(results=[])
lines+=['',f"N6’s original query-capacity refusals remain in the first-observation files. Separate unchanged controls after the retention-expiry pause record **{fmt(dict(collections.Counter(r['status'] for r in controls['results'])))}**. These are HTTP 503 capacity outcomes, distinct from timed admission and from language assertion failures. Passing controls do not erase the original refusals.",'',
'## Additional finite admission and HTTP prompts','',
'The run also records 95 paced live HTTP prompt observations on N2/N3/N4/N5/N7 and 980 fresh finite admission probes on N1–N7 after the broader sweep. Their actual outcomes, 120-entry metadata and unchanged-policy comparisons are in the full report, outside the 78-manifest input-row count. N7’s prompt pack is additional coverage relative to the previous report.','',
'## Owned and supplementary observations','',
'The three current-image private ACTOR gates pass 45 release plus seven source-directive cases each. Authenticated and anonymous retained HTTP contexts pass 3/3 each, client naming passes 16/16, bounded noncompletion passes 3/3, and enabled owned HTTP prompts pass 19/19 per native runtime. Runner tooling passes all 114 unit tests. Live prompt counts and all twelve directed ACTOR interoperation pairs are in the full report.','',
'The retained-context selection records **46 pass / 11 fail / 4 blocked**, with six passing closure controls. Source/export and attachment-instrumentation limits remain explicit. The real Chromium browser compatibility selection records **4 pass / 2 fail**, retaining B-SV-006 in Worker and main modes. MC-028/029 preserve their original URI expectations; portable-text, document, deadline, HTTP-field and public receive findings retain their raw scope and outcomes.','',
'No runtime, installed engine, assertion, live setting or quota was changed by the sweep. Persistent service/container image identities match the before snapshot, and owned fixture containers were removed. Private admin operations, public browser UI, all security boundaries and external ISO obligations are not certified.','',
'## Historical records','',
'The [19 November complete sweep](reports/2026-11-19-upgraded-live-conformance/REPORT.md) remains immutable, including its original N7 rate refusals, N6 capacity refusals and passing paused controls. The [separate admission qualification](reports/2026-11-19-public-admission/REPORT.md) retains its 980 finite live requests and deployment evidence. Neither record is silently substituted for this fresh sweep.','']
n7_prompt=json.loads((P/'live-controls/paused-prompt-http-n7.json').read_text());lines[lines.index('## Historical records'):lines.index('## Historical records')]=['Fresh N7 retained-HTTP prompt coverage: **'+fmt(dict(collections.Counter(r['status'] for r in n7_prompt['results'])))+'**. This uses the maintained ECLiPSe branch and adds coverage absent from the previous report.','']
lines+=['','The [earlier SWI11 sweep](reports/2026-11-19-deployed-conformance/REPORT.md), [repair checkpoint](reports/2026-11-19-conformance-repairs/REPORT.md), [naming alignment](reports/2026-11-19-client-naming/REPORT.md), [connection-cleanup diagnosis](reports/2026-11-19-connection-cleanup/REPORT.md), [HTTP context checkpoint](reports/2026-11-19-http-context/REPORT.md), and [OPEN repair](reports/2026-11-19-open-exercise-repair/REPORT.md) retain their dated scope. The [Appendix B matrix](docs/APPENDIX_B_COVERAGE.md) and [library clause inventory](docs/LIBRARY_TEST_GAPS.md) retain their separate obligation evidence.','']
(R/'CURRENT_COVERAGE.md').write_text('\n'.join(lines).rstrip()+'\n')
p=R/'README.md';s=p.read_text();start=s.index('## Current consolidated results');end=s.index('The following earlier qualification records',start)
intro='''## Current consolidated results

The [fresh 20 November sweep](reports/2026-11-24-post-xn-conformance/REPORT.md)
covers **78 manifests / 1,984 input rows** against the configurable admission
release, including **9,262 live library observations** across the selected
transports. **It is not all-green.** All four ACTOR nodes pass their 118-case
primary selection; wider API, context and browser findings remain explicit.
The report also includes 95 paced HTTP prompt observations and 980 fresh
finite admission probes, outside the manifest input-row count.

The run starts every observation fresh. Original N6 query-capacity refusals
and separate paused controls are retained. Private identity and unbounded
controls use owned fixtures, not public endpoint claims. The current-image
private gates pass 45+7 cases each and the runner’s 114 unit tests pass.
Four retained-context return assertions remain blocked.

[Current matrix](CURRENT_COVERAGE.md),
[per-file observations](reports/2026-11-24-post-xn-conformance/SUMMARY.json),
[case inventory](reports/2026-11-24-post-xn-conformance/verification.json) and
[frozen inputs](reports/2026-11-24-post-xn-conformance/suite-inputs.json) identify
scope, provenance and failures. No live runtime, setting or quota was changed
by the tests. Repeated versions and modes are not a conformance percentage.

The [admission deployment](reports/2026-11-19-public-admission/REPORT.md)
records the selected runtime pins, configurable 120-entry public presets,
unchanged engine/resource bounds and throughput qualification. Browser-local
execution has no server admission budget. The [previous full sweep](reports/2026-11-19-upgraded-live-conformance/REPORT.md)
retains its original pre-admission scope and findings.

The common [client naming contract](profiles/client-naming-0.1.md) keeps
ordinary names client scoped and published services node-wide.

'''
s=s[:start]+intro+s[end:];s=s.replace('current\nfailures and incomplete controls are described in the 19 November report.','current\nfailures and incomplete controls are described in the 20 November report.');p.write_text(s)
print('Updated current coverage and README while retaining historical reports')
