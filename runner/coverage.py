#!/usr/bin/env python3
"""Generate the published matrix from raw reports, preserving failed/missing rows."""
import argparse
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('directory',type=Path);args=parser.parse_args();directory=args.directory
    provenance=json.loads((directory/'provenance.json').read_text());reports={}
    for run in provenance['runs']:
        if run['report']:
            reports[run['label']]=json.loads((directory/run['report']).read_text())
    def cell(label,na='not measured'):
        report=reports.get(label)
        if not report:return na
        c=report['counts'];total=len(report['results'])
        text=f"{c['pass']}/{total}";bad=c.get('fail',0)
        if bad:text+=f"; {bad} fail"
        if c.get('observed',0):text=f"{c['observed']}/{total} observed"
        if c.get('diagnostic_error',0):text+=f"; {c['diagnostic_error']} incomplete"
        return f'[{text}]({label}.json)'
    lines=['# Coverage matrix — interoperability baseline 0.1','',
      'Recorded 2026-10-21. Status: **scoped draft; known failures remain**. See the',
      '[baseline](../../baselines/0.1.md), [difference register](../../docs/BASELINE_DIFFERENCES.md)',
      'and [reproduction guide](../../docs/BASELINE_RUNNER.md). Counts describe executed',
      'cases, not complete language/profile certification. Links point to raw evidence.','',
      '## Required local/server selections','',
      '| Pack | Native SWI | Native Trealla | GNU ISOBASE | WASM Worker | WASM main |',
      '|---|---|---|---|---|---|']
    for pack in ['isobase-http','language-actor','wire-capabilities']:
        cells=[]
        for name in ['swi','trealla','gnu','swi-wasm-worker','swi-wasm-main']:
            label=name+'-'+pack
            na='not applicable' if (name=='gnu' and pack!='isobase-http') or (name.startswith('swi-wasm') and pack!='language-actor') else 'not measured'
            cells.append(cell(label,na))
        lines.append('| '+pack+' | '+' | '.join(cells)+' |')
    lines+=['','Browser rows execute the same seven LC assertions in real SWI-WASM engines',
      'under Node with test coordinator plumbing. They are not browser UI/network',
      'or server-wire certification. Native HTTP/ACTOR fixtures use public sandboxed',
      'server routes. GNU advertises ISOBASE and is not tested for actor features.','',
      '## Required HTTP interoperability','',
      'Rows are callers; columns are HTTP destinations. Each cell covers HC-001',
      '(RPC paging) and HC-002 (promise template/caller independence).','',
      '| Caller → peer | SWI | Trealla | GNU |','|---|---|---|---|']
    for caller in ['swi','trealla','gnu']:
        lines.append('| '+caller+' | '+' | '.join(cell(caller+'-interop-http-to-'+peer) for peer in ['swi','trealla','gnu'])+' |')
    lines+=['','## Required ACTOR interoperability','',
      'Three public cases per direction: remote source/synchronous paging, canonical',
      'asynchronous answers, and unrelated monitor/message preservation. GNU is',
      'outside ACTOR; browser real-network interoperation is not measured here.','',
      '| Caller → peer | SWI | Trealla |','|---|---|---|']
    for caller in ['swi','trealla']:
        lines.append('| '+caller+' | '+' | '.join(cell(caller+'-interop-actor-to-'+peer) for peer in ['swi','trealla'])+' |')
    lines+=['','## Separately versioned supporting ACTOR contracts','',
      '| Suite | SWI | Trealla |','|---|---|---|']
    for suite in ['actor-core','actor-workers','actor-behaviours','actor-supervisors']:
        lines.append('| '+suite+'-0.1 | '+cell('swi-'+suite)+' | '+cell('trealla-'+suite)+' |')
    lines+=['','These suites retain their own scopes and IDs. Their numeric identity check',
      'does not define the baseline language representation; baseline LC-001 uses',
      'opaque identity. They are not claimed as complete browser-engine tests.','',
      '## Required failures — retained without waivers','']
    failures=[]
    for label,report in reports.items():
        if report.get('scope')!='required':continue
        for row in report['results']:
            if row['status']=='fail':failures.append((label,row))
    if not failures:lines.append('No selected required failure was observed in this run.')
    for label,row in failures:
        detail=row.get('detail','').replace('\n',' ')
        lines.append(f"- **{row['id']} — {label}**: {detail} [Raw report]({label}.json).")
    lines+=['','The failed HTTP source-loading cases remain required failures. The Trealla',
      'HTTP callable context reports `rpc/3` and `promise/4` unavailable even though',
      'its ACTOR paths provide them. GNU → Trealla HC-002 reports a worker timeout;',
      'the unparenthesized operator-goal diagnostic records a related HTTP framing',
      'difference, but this run does not establish a complete causal repair. No',
      'runtime change or expected-failure substitution was made.','',
      '## Separate diagnostics and experimental text','',
      '| Diagnostic suite | SWI | Trealla | GNU |','|---|---|---|---|']
    for suite in ['isobase-diagnostics','supervisor-diagnostics','worker-diagnostics','portable-text']:
        lines.append('| '+suite+' | '+' | '.join(cell(name+'-'+suite,'not applicable') for name in ['swi','trealla','gnu'])+' |')
    lines+=['','Diagnostic/experimental counts are excluded from required totals. Existing',
      'SCD-001 preserves the static/runtime-bound nested supervisor admission',
      'difference. A timeout means an observation is incomplete, not a semantic',
      'pass. GNU contract 0.2.0 has additional obligations; these observations do',
      'not waive them or rerun its historical broad/39-probe audit.','',
      '## Provenance and coverage limits','',
      '[provenance.json](provenance.json) records source revisions, dirty test/doc',
      'paths, configuration, binary hashes, input-file hashes and subprocess exits.',
      'The test-only browser export is the only executable runtime-repository edit.',
      'GNU binaries were already built; no runtime source or installed engine was',
      'repaired or upgraded. Existing N3/N5 processes were left running unchanged.','',
      'Not established: full ISO mode coverage, hostile-input/security containment,',
      'all resource bounds, cache-expiry policies, arbitrary source-fetch/network',
      'policies, RELATION, complete ISOTOPE HTTP sessions, remote cancellation or',
      'delegated-lineage cleanup. Receiver wire tests do not replace client-side',
      'fault-injection regressions for every spawn-wait race.','',
      '## Execution completeness','',
      '| Invocation | Exit | Evidence |','|---|---|---|']
    for run in provenance['runs']:
        evidence=f"[report]({run['report']})" if run['report'] else '**missing report**'
        lines.append(f"| {run['label']} | {run['exit_code']} | {evidence} |")
    (directory/'COVERAGE.md').write_text('\n'.join(lines)+'\n')
    print(directory/'COVERAGE.md')
if __name__=='__main__':main()
