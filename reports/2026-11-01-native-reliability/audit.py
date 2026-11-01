#!/usr/bin/env python3
"""Check the accepted evidence counts, negative controls and artifact hashes."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
def read(path): return json.loads(path.read_text())
def require(value, message):
    if not value: raise SystemExit(message)

def main():
    observed=HERE/'observations'
    for engine in ['swi','trealla']:
        folder=observed/'accepted-final'/engine
        summary=read(folder/'release-summary.json')
        require(summary['profile']=='actor-release-0.2' and summary['passed'],engine+' gate')
        total=0
        for pack in summary['packs']:
            manifest=read(REPO/'cases'/(pack['suite']+'.json'))
            expected={c['id'] for c in manifest['cases']}
            rows=read(folder/pack['report'])['results']
            require(pack['passed'] and pack['returncode']==0 and len(rows)==len(expected)
                    and {r['id'] for r in rows}==expected
                    and all(r['status']=='pass' for r in rows),engine+' '+pack['suite'])
            total+=len(rows)
        require(total==44,engine+' case count')
    rows=read(observed/'verified-stress.json')
    expected={'websocket':200,'remote':20,'isolation':10,'sandbox':10,'synch':10}
    require(len(rows)==250 and all(r['status']==0 for r in rows),'stress result')
    for case,count in expected.items():
        selected=[r for r in rows if r['case']==case]
        require(len(selected)==count and {r['repetition'] for r in selected}==set(range(count)),case+' repetitions')
    controls=read(observed/'verified-controls.json')
    require(len(controls)==4 and len({(r['source'],r['case']) for r in controls})==4
            and all(r['status']==(1 if r['source']=='before' else 0) for r in controls),'negative controls')
    require(read(observed/'verified-swi-native.json')['status']==0,'SWI native')
    require(read(observed/'verified-trealla-complete.json')['status']==0
            and 'ALL unit TESTS PASSED' in (observed/'verified-trealla-complete.log').read_text(),'Trealla native')
    require('Ran 54 tests' in (observed/'verified-python.log').read_text()
            and (observed/'verified-python.log').read_text().rstrip().endswith('OK'),'Python tests')
    for rel,digest in read(HERE/'artifact-sha256.json').items():
        require(hashlib.sha256((HERE/rel).read_bytes()).hexdigest()==digest,'artifact hash '+rel)
    # Compare archived Prolog and gate inputs with their recorded commits,
    # rather than trusting a version string or the current working tree.
    meta=read(HERE/'environment.json')
    prov=read(observed/'accepted-final'/'provenance.json')
    for row in prov['engines']:
        repo=REPO.parent/('trealla-port' if row['engine']=='trealla' else 'swi-prolog-node')
        pin=meta['sources'][repo.name]
        require(repo.is_dir(),'missing sibling source checkout '+str(repo))
        for path,digest in row['source_hashes'].items():
            data=subprocess.check_output(['git','show',pin+':'+path],cwd=repo)
            require(hashlib.sha256(data).hexdigest()==digest,row['engine']+' source '+path)
    for path,digest in prov['inputs'].items():
        data=subprocess.check_output(['git','show',meta['sources']['trinity-conformance']+':'+path],cwd=REPO)
        require(hashlib.sha256(data).hexdigest()==digest,'gate input '+path)
    print('Verified: 88 conformance cases; 250 repeated invocations; two before/after controls; native suites; 54 Python tests; archive and source hashes.')

if __name__=='__main__': main()
