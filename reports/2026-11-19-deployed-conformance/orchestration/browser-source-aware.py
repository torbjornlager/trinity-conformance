import os,json,subprocess,time,sys
from pathlib import Path
R=Path('/Users/lager/trinity-conformance');O=Path('/Users/lager/trinity-demonstrator/.trinity/conformance-full-20261119');F=O/'browser-source-aware';F.mkdir();P=Path('/runtime')
plans=json.loads((O/'browser-plan.json').read_text());end=time.monotonic()+1800
while True:
 rows=json.loads((O/'browser-jobs.json').read_text())
 if len(rows)==len(plans):break
 if time.monotonic()>end:raise TimeoutError('waiting for prior browser batches')
 time.sleep(2)
os.environ.update(NODE_PATH='/modules',CHROME_PATH='/usr/bin/chromium',LIBRARY_RUNTIME_ROOT=str(P),WP_WASM_SOURCE_DIR=str(O/'browser-fixture'),PYTHONDONTWRITEBYTECODE='1')
# This existing real-session adapter loads both common and per-case private source.
suites=['actor-error-contract-0.1','browser-local-compatibility-0.1','copying-isolation-0.1','local-naming-0.1','node-settings-0.1','receive-callback-context-0.1','server-waits-0.1','source-copying-0.1','monitor-preflight-0.1']
results=[]
for suite in suites:
 env=dict(os.environ,LIBRARY_MANIFEST=str(R/'cases'/(suite+'.json')),LIBRARY_REPORT=str(F/(suite+'.json')));start=time.monotonic();print('START source-aware',suite,flush=True)
 with (O/'logs'/('source-aware-browser-'+suite+'.log')).open('w') as log:r=subprocess.run(['node',str(R/'adapters/wasm_actor_cases.cjs')],env=env,cwd=R,stdout=log,stderr=subprocess.STDOUT,timeout=300)
 results.append(dict(suite=suite,exit_code=r.returncode,seconds=round(time.monotonic()-start,3)));(O/'browser-source-aware-jobs.json').write_text(json.dumps(results,indent=2)+'\n');print('DONE source-aware',suite,r.returncode,flush=True)
