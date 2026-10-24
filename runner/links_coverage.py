#!/usr/bin/env python3
"""Render the local links/monitors draft from raw reports, retaining failures."""
import argparse,json
from pathlib import Path

def render(directory):
 reports={name:json.loads((directory/(name+'-links-monitors.json')).read_text()) for name in ['swi','trealla']}
 total=sum(len(d['results']) for d in reports.values())
 passed=sum(d['counts']['pass'] for d in reports.values())
 failed=sum(d['counts']['fail'] for d in reports.values())
 lines=['# Links and monitors draft 0.1 — 24 October 2026','',
  f'**{passed}/{total} selected assertions pass; {failed} failures.**',
  'Identical public-interface goals execute on disposable native ACTOR nodes.',
  'This separate draft does not amend baseline 0.1 or certify arbitrary lifecycle',
  'interleavings. GNU ACTOR, SWI-WASM and remote monitoring are not measured.','',
  '| Case | SWI | Trealla |','| --- | --- | --- |']
 ids=list(dict.fromkeys(row['id'] for d in reports.values() for row in d['results']))
 for case in ids:
  cells=[]
  for name,d in reports.items():
   row=next((r for r in d['results'] if r['id']==case),None)
   cells.append(f"[{row['status']}]({name}-links-monitors.json)" if row else 'not measured')
  lines.append('| '+case+' | '+' | '.join(cells)+' |')
 lines+=['','## Failures','']
 failures=[(name,row) for name,d in reports.items() for row in d['results'] if row['status']=='fail']
 if not failures:lines.append('No selected required failure was observed in this run.')
 for name,row in failures:lines.append(f"- **{name} / {row['id']}**: {row.get('detail','').replace(chr(10),' ')}")
 lines+=['','## Evidence and limits','',
  'See [REPORT.md](REPORT.md) for method, selected contracts and preservation.',
  '[provenance.json](provenance.json) identifies exact source revisions, engine',
  'hashes, commands, node configuration and test input hashes. The SWI source is',
  'the demonstrator manifest pin, loaded from its separate native repository.',
  'Cases use no fixed sleeps, runtime imports or private registry access.',
  'LM-006 deliberately injects down-shaped application data to isolate scoped',
  'mailbox flushing, then checks a genuine notification on the retained monitor.',
  'Both fixture nodes were stopped; runtime code, installed runtimes and n3/n5',
  'were unchanged. No GUI, TLS, remote-link, resource-limit or general cleanup',
  'certification is claimed.']
 (directory/'COVERAGE.md').write_text('\n'.join(lines)+'\n')

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('directory',type=Path);args=parser.parse_args();render(args.directory)
if __name__=='__main__':main()
