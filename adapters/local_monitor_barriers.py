#!/usr/bin/env python3
"""Qualify native monitor barriers in their full runtime compositions."""
import argparse
import hashlib
import json
from pathlib import Path
import os
import subprocess


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root,mode):
    files=list((root/'prolog').rglob('*.pl')) if mode=='swi' else list(root.glob('*.pl'))
    if mode=='swi':files.append(root/'tests/tiers/node/remote_demonitor_race_tests.pl')
    return {str(p.relative_to(root)):sha(p) for p in sorted(files)}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for flag in ['swipl','tpl']:p.add_argument('--'+flag,required=True)
    for flag in ['swi-root','trealla-root','output']:p.add_argument('--'+flag,type=Path,required=True)
    a=p.parse_args();a.output.mkdir(exist_ok=False,parents=True);rows=[];sources={}
    for mode in ['swi','trealla']:
        root=a.swi_root if mode=='swi' else a.trealla_root
        before=snapshot(root,mode)
        sources[mode]=dict(revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
                           tracked_diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff','HEAD','--'],cwd=root)).hexdigest(),
                           files_sha256=before)
        if mode=='swi':
            cmd=[a.swipl,'-f','none','-q','-s','tests/tiers/node/remote_demonitor_race_tests.pl',
                 '-g','run_tests(remote_demonitor_races)','-t','halt']
            id='MON-SELECTED-DOWN'
        else:
            cmd=[a.tpl,'-g',"consult(remote_demonitor_tests),(catch(remote_demonitor_tests:run,E,(writeq(E),nl,fail))->halt;halt(1))"]
            id='MON-WRITER-RETRY'
        env=dict(os.environ)
        for key in ['WP_CONFIG_FILE','SWI_HOME_DIR','SWIPL_HOME_DIR','WP_NATIVE_STATE','WP_NATIVE_MODE']:env.pop(key,None)
        if mode=='trealla':env['TPL_LIBRARY_PATH']=str(Path(a.tpl).parent/'library')
        row=dict(candidate=mode,id=id,command=cmd)
        try:
            result=subprocess.run(cmd,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=30)
            (a.output/(mode+'.txt')).write_text(result.stdout)
            row.update(status='pass' if result.returncode==0 else 'fail',exit_code=result.returncode)
        except subprocess.TimeoutExpired as e:
            row.update(status='fail',detail='native monitor selection exceeded 30 seconds')
            (a.output/(mode+'.txt')).write_bytes(e.stdout or b'')
        row['inputs_unchanged_during_run']=snapshot(root,mode)==before
        if not row['inputs_unchanged_during_run']:row.update(status='fail',detail='inputs changed during selection')
        rows.append(row);print(mode,id,row['status'],flush=True)
    report=dict(suite='native-monitor-barriers-0.1',adapter_sha256=sha(Path(__file__)),sources=sources,
                scope='Implementation regression selections; SWI selected-down/withdrawal orderings and Trealla writer confirmation/timeout/retry',results=rows)
    (a.output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    return int(any(r['status']!='pass' for r in rows))


if __name__=='__main__':raise SystemExit(main())
