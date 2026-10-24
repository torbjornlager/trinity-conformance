#!/usr/bin/env python3
"""Render local ACTOR draft packs from raw reports, retaining failures."""
import argparse,json
from pathlib import Path

def render(directory,suite='links-monitors'):
 titles={'links-monitors':'Links and monitors','server-waits':'Generic-server waits','selective-receive':'Selective receive','toplevel-waits':'Synchronous toplevel waits','local-naming':'Local naming and registration','copying-isolation':'Actor copying and private-source isolation','creation-validation':'Local creation-option validation'}
 if suite not in titles:raise ValueError('unknown local coverage suite: '+suite)
 reports={name:json.loads((directory/(name+'-'+suite+'.json')).read_text()) for name in ['swi','trealla']}
 total=sum(len(d['results']) for d in reports.values())
 passed=sum(d['counts']['pass'] for d in reports.values())
 failed=sum(d['counts']['fail'] for d in reports.values())
 lines=[f'# {titles[suite]} draft 0.1 — 24 October 2026','',
  f'**{passed}/{total} selected assertions pass; {failed} failures.**',
  'Identical public-interface goals execute on disposable native ACTOR nodes.',
  'This separate draft does not amend baseline 0.1 or certify arbitrary lifecycle',
  'interleavings. GNU ACTOR, SWI-WASM and remote operation are not measured.','',
  '| Case | SWI | Trealla |','| --- | --- | --- |']
 ids=list(dict.fromkeys(row['id'] for d in reports.values() for row in d['results']))
 for case in ids:
  cells=[]
  for name,d in reports.items():
   row=next((r for r in d['results'] if r['id']==case),None)
   cells.append(f"[{row['status']}]({name}-{suite}.json)" if row else 'not measured')
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
  *(['LM-006 injects controlled down-shaped application data to isolate scoped',
     'mailbox flushing, then checks a genuine notification on the retained monitor.']
    if suite=='links-monitors' else
    ['All candidate messages are self-sent before zero-time polls; no sleep is used.',
     'Guards have no external side effects, and cuts are tested inside selected bodies.']
    if suite=='selective-receive' else
    ['Gated queries announce acceptance and await explicit release messages.',
     'Sequential query barriers establish completion without fixed sleeps.']
    if suite=='toplevel-waits' else
    ['Actors acknowledge named routing and terminate only on explicit stop messages.',
     'Exact termination notifications precede stale-pid and name-reuse checks.']
    if suite=='local-naming' else
    ['Child observations and release messages establish copying/isolation barriers.',
     'Minimal dynamic declarations enable the selected private-database mutation.']
    if suite=='copying-isolation' else
    ['Formal error terms are checked without implementation-specific contexts.',
     'Valid creation and exact termination acknowledgements bound startup checks.',
     'This selection uses runtime-supplied option lists. The separate initial',
     'literal-option run retains unresolved admission-path failures; see REPORT.md.']
    if suite=='creation-validation' else
    ['Server callbacks announce acceptance and await explicit release/crash messages.',
     'A barrier request establishes reply readiness before mismatch/poll checks.']),
  'Both fixture nodes were stopped; runtime code, installed runtimes and n3/n5',
  'were unchanged. No GUI, TLS, remote-link, resource-limit or general cleanup',
  'certification is claimed.']
 (directory/'COVERAGE.md').write_text('\n'.join(lines)+'\n')

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('directory',type=Path);parser.add_argument('--suite',choices=['links-monitors','server-waits','selective-receive','toplevel-waits','local-naming','copying-isolation','creation-validation'],default='links-monitors');args=parser.parse_args();render(args.directory,args.suite)
if __name__=='__main__':main()
