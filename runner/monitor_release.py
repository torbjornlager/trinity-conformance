#!/usr/bin/env python3
"""Run the shared monitor contract and remote observation-owner controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from context_release import validate

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'cases/monitor-contracts-0.1.json'


def fingerprint(paths):
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for flag in ['swipl','tpl','swi-root','trealla-root','runtime-root','node']:p.add_argument('--'+flag,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=False)
    pack=json.loads(MANIFEST.read_text());common=['--swipl',a.swipl,'--tpl',a.tpl,'--swi-root',a.swi_root,'--trealla-root',a.trealla_root]
    files=[MANIFEST,Path(__file__),ROOT/'runner/context_release.py']+list((ROOT/'adapters').glob('*.py'))+[ROOT/'adapters/browser_native_context.cjs',ROOT/'adapters/wasm_actor_cases.cjs']
    files+=list((Path(a.swi_root)/'prolog').rglob('*.pl'))+list(Path(a.trealla_root).glob('*.pl'))
    before=fingerprint(files);groups=[]
    native=[dict(candidate=m,id=c['id']) for m in ['swi','trealla'] for c in pack['cases']]
    browser=[dict(candidate=m,id=c['id']) for m in ['swi-wasm-worker','swi-wasm-main'] for c in pack['cases']]
    remote=[dict(candidate=m,id=f'BN-{i:03}-{peer}') for m in ['swi-wasm-worker','swi-wasm-main'] for peer in ['swi','trealla'] for i in range(1,17)]
    barriers=[dict(candidate='swi',id='MON-SELECTED-DOWN'),dict(candidate='trealla',id='MON-WRITER-RETRY')]
    plans=[
        ('native',[sys.executable,str(ROOT/'adapters/local_actor_cases.py'),*common,'--manifest',str(MANIFEST),'--output',str(a.output/'native')],native,a.output/'native/results.json',{}),
        ('browser',[a.node,str(ROOT/'adapters/wasm_actor_cases.cjs')],browser,a.output/'browser.json',dict(LIBRARY_RUNTIME_ROOT=a.runtime_root,LIBRARY_MANIFEST=str(MANIFEST),LIBRARY_REPORT=str(a.output/'browser.json'))),
        ('remote',[sys.executable,str(ROOT/'adapters/local_browser_context.py'),*common,'--runtime-root',a.runtime_root,'--node',a.node,'--return-barriers','--output',str(a.output/'remote')],remote,a.output/'remote/results.json',{}),
        ('barriers',[sys.executable,str(ROOT/'adapters/local_monitor_barriers.py'),*common,'--output',str(a.output/'barriers')],barriers,a.output/'barriers/results.json',{})]
    for label,command,expected,path,extra in plans:
        row=dict(group=label,command=command,status='fail')
        try:
            with (a.output/(label+'.txt')).open('w') as log:
                result=subprocess.run(command,cwd=ROOT,env=dict(os.environ,**extra),stdout=log,stderr=subprocess.STDOUT,timeout=300)
            row['exit_code']=result.returncode
            validate(json.loads(path.read_text()),expected)
            if result.returncode:raise ValueError('adapter exited nonzero')
            if label=='remote':
                provenance=json.loads((path.parent/'provenance.json').read_text())
                if provenance.get('selection_status')!='pass' or not provenance.get('inputs_unchanged_during_run'):raise ValueError('remote qualification invalidated')
            row['status']='pass'
        except (OSError,ValueError,KeyError,TypeError,subprocess.TimeoutExpired) as e:row['detail']=str(e)
        groups.append(row);print(label,row['status'],flush=True)
    unchanged=fingerprint(files)==before
    report=dict(suite=pack['suite'],inputs_sha256=before,inputs_unchanged_during_run=unchanged,groups=groups,
                status='pass' if unchanged and all(g['status']=='pass' for g in groups) else 'fail')
    (a.output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    return int(report['status']!='pass')


if __name__=='__main__':raise SystemExit(main())
