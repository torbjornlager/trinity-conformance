#!/usr/bin/env python3
"""Publish the separate promise draft matrix without rewriting baseline evidence."""
import argparse,json
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);a=p.parse_args();root=a.directory
 def report(name):return json.loads((root/(name+'.json')).read_text())
 def cell(name):
  d=report(name);c=d['counts'];return f"[{c['pass']} pass, {c['fail']} fail]({name}.json)"
 promise_reports=[report(f'{c}-promise-yield-to-{p}') for c in ['swi','trealla'] for p in ['swi','trealla']]
 http_reports=[report(f'{c}-interop-http-to-{p}') for c in ['swi','trealla'] for p in ['swi','trealla']]
 passed=sum(d['counts']['pass'] for d in promise_reports);failed=sum(d['counts']['fail'] for d in promise_reports)
 total=sum(len(d['results']) for d in promise_reports)
 lines=['# Promise/yield draft 0.1 — 24 October 2026','',
 'Identical public-interface goals were run on disposable native SWI/Trealla nodes.',
 'This separately versioned pack does not change baseline 0.1. GNU and SWI-WASM',
 'network behaviour are **not measured**. No runtime code or installed engine was changed.','',
 '## Promise/yield selections','',
 '| Caller → HTTP peer | SWI | Trealla |','| --- | --- | --- |']
 for caller in ['swi','trealla']:lines.append('| '+caller+' | '+' | '.join(cell(f'{caller}-promise-yield-to-{peer}') for peer in ['swi','trealla'])+' |')
 lines+=['',f'**{passed}/{total} assertions pass; {failed} failures remain.**',
 'Failures within this draft pack are not waived by separate diagnostic controls.','',
 '## Existing HTTP interoperability selection','',
 'HC-002 is reused for sharing/caller independence; HC-001 retains its paging',
 f"assertion. **{sum(d['counts']['pass'] for d in http_reports)}/{sum(len(d['results']) for d in http_reports)} selections pass**.",'',
 '| Caller → HTTP peer | SWI | Trealla |','| --- | --- | --- |']
 for caller in ['swi','trealla']:lines.append('| '+caller+' | '+' | '.join(cell(f'{caller}-interop-http-to-{peer}') for peer in ['swi','trealla'])+' |')
 lines+=['','## Separate diagnostics','',
 'PYD-001 (ordinary actor send), PYD-002 (unification-only timeout callback) and',
 'PYD-003 (throwing callback followed by retry) all complete their assertions in',
 'the four directions. Individual outcomes are listed below; they do not waive',
 'required failures or establish an exact implementation cause.','']
 for caller in ['swi','trealla']:
  for peer in ['swi','trealla']:
   n=f'{caller}-promise-diagnostics-to-{peer}';d=json.loads((root/'diagnostics'/(n+'.json')).read_text());lines.append(f"- [{caller} → {peer}](diagnostics/{n}.json): {d['counts']['observed']} observed, {d['counts']['diagnostic_error']} diagnostic errors.")
 lines+=['','## Required failures','']
 for caller in ['swi','trealla']:
  for peer in ['swi','trealla']:
   n=f'{caller}-promise-yield-to-{peer}'
   for row in report(n)['results']:
    if row['status']=='fail':lines.append(f"- **{row['id']} — {caller} → {peer}**: {row.get('detail','').replace(chr(10),' ')} [report]({n}.json).")
 lines+=['','## Provenance and limits','',
 'Native SWI source is the demonstrator manifest pin',
 '`f316e65503bff863dfbd2e182f7487988c91480c`; Trealla uses the separately built',
 'unmodified v3.14.10 engine and matching libraries. Exact Web Prolog source',
 'revisions, commands, binary hashes and fixture configuration are in',
 '[provenance.json](provenance.json). Both fixture pairs were stopped after use.',
 'Read [REPORT.md](REPORT.md) for method, schema/accounting checks, preservation',
 'and the timing-fixture qualifications. No full-suite, GUI, GNU, browser-network,',
 'TLS, cancellation or general lifecycle certification is claimed.']
 (root/'COVERAGE.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()
