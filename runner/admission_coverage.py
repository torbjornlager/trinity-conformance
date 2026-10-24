#!/usr/bin/env python3
"""Render diagnostic observations without calling observed errors passes."""
import argparse
import json
from pathlib import Path

def summary(row):
    if row is None:return 'not measured'
    obs=row.get('observation',{})
    if row['status']!='observed' or not obs.get('complete'):
        return 'INCOMPLETE: '+row.get('detail',obs.get('probe_error','no complete observation'))
    terminal=obs['terminal'];kind=terminal.get('type','unknown')
    parts=[kind,'entered' if obs['execution_entered'] else 'before entry']
    if kind=='success' and isinstance(terminal.get('data'),list) and len(terminal['data'])==1:
        values=terminal['data'][0]
        if 'PatternState' in values:
            state=values['PatternState']
            parts.append('pattern already bound' if state.startswith('bound(') else 'pattern '+state)
        for name in ['Matched','Reply']:
            if name in values:parts.append(name+'='+values[name])
        error=values.get('Error','')
        if 'missing_start_option' in error:parts.append('caught missing_start_option')
        elif 'domain_error(spawn_option' in error:parts.append('caught spawn_option error')
    return '; '.join(parts)

def render(directory,manifest):
    cases=json.loads(manifest.read_text())['cases']
    reports={name:json.loads((directory/(name+'-admission-paths.json')).read_text()) for name in ['swi','trealla']}
    complete=sum(r['status']=='observed' and r.get('observation',{}).get('complete',False) for d in reports.values() for r in d['results'])
    incomplete=sum(r['status']=='diagnostic_error' for d in reports.values() for r in d['results'])
    lines=['# Admission paths — diagnostic matrix, 24 October 2026','',
        f'**{complete} completed observations; {incomplete} diagnostic errors. No conformance passes are assigned.**','',
        'Each cell describes an actual response and whether the query entry marker',
        'was present. A successful response may contain a caught error or record an',
        'undispatched request; it is not an acceptance verdict.','',
        '| Probe | Surface | SWI | Trealla |','| --- | --- | --- | --- |']
    for case in cases:
        cells=[]
        for name,d in reports.items():
            row=next((r for r in d['results'] if r['id']==case['id']),None)
            label=summary(row).replace('|','\\|').replace('\n',' ')
            cells.append(f'[{label}]({name}-admission-paths.json)')
        lines.append('| '+case['id']+' | '+case['pair']+' / '+case['variant']+' | '+' | '.join(cells)+' |')
    lines+=['','## Evidence and limits','',
        '[REPORT.md](REPORT.md) explains the findings, source inspection and limits.',
        'Raw reports contain exact sent command objects and received responses,',
        'including terminal errors, entry-check responses and halt acknowledgements.',
        'No output markers, sleeps, runtime imports or private registry inspection',
        'are used. Entry is checked through an ordinary self-message on the same shell.',
        'The existing required matrices and their failures remain unchanged.',
        'Disposable nodes stopped; runtime code, installed runtimes and n3/n5 stayed unchanged.']
    (directory/'DIAGNOSTICS.md').write_text('\n'.join(lines)+'\n')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--manifest',type=Path,default=Path('cases/admission-paths-0.1.json'));a=p.parse_args();render(a.directory,a.manifest)
if __name__=='__main__':main()
