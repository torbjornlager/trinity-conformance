import json,subprocess,sys,os,time,signal,shutil
from pathlib import Path
R=Path('/Users/lager/trinity-conformance');O=Path('/Users/lager/trinity-demonstrator/.trinity/conformance-full-20261119');F=O/'browser';F.mkdir(exist_ok=True)
P=Path('/runtime');W=O/'browser-fixture';shutil.copytree(P/'web/wasm',W);shutil.copyfile(P/'tests/fixtures/wasm/shared_db.pl',W/'shared_db.pl')
os.environ.update(NODE_PATH='/modules',CHROME_PATH='/usr/bin/chromium',WP_WASM_SOURCE_DIR=str(W),LIBRARY_RUNTIME_ROOT=str(P),PYTHONDONTWRITEBYTECODE='1')
plans=[]
def add(label,cmd,suites,env=None,timeout=600):plans.append(dict(label=label,command=cmd,suites=suites,env=env or {},timeout=timeout))
# Existing embedded adapter keeps each case in a separate real WASM engine.
node_suites=['language-actor-0.1','source-directives-0.1','actor-error-contract-0.1','appendix-library-probes-0.1','browser-local-compatibility-0.1','child-specs-0.1','committed-exit-0.1','copying-isolation-0.1','creation-validation-0.1','links-monitors-0.1','local-naming-0.1','manual-option-sources-0.1','node-settings-0.1','receive-callback-context-0.1','receive-wait-options-0.1','rpc-timeout-0.1','selective-receive-0.1','selective-receive-0.2','server-waits-0.1','source-copying-0.1','statechart-document-0.1','supervisor-common-0.1','toplevel-waits-0.1','uri-atoms-0.1','http-transport-options-0.1']
for suite in node_suites:
 p=json.loads((R/'cases'/(suite+'.json')).read_text());assert all('goal' in c for c in p['cases']) and not p.get('source'),suite
 for mode in ['worker','main']:
  add(suite+'-'+mode,['node',str(R/'adapters/wasm.cjs'),str(P),mode,str(R/'cases'/(suite+'.json')),str(F/(suite+'-'+mode+'.json'))],[suite])
for version in ['0.1','0.2','0.3','0.4']:
 suite='standard-library-'+version
 add('chrome-'+suite,['node',str(R/'adapters/wasm_standard_library.cjs')],[suite],dict(LIBRARY_MANIFEST=str(R/'cases'/(suite+'.json')),LIBRARY_REPORT=str(F/('chrome-'+suite+'.json'))))
common=['--swipl','/usr/bin/swipl','--tpl','/opt/trealla/tpl','--swi-root','/opt/swi-prolog-node','--trealla-root','/work/trealla']
add('maintained-monitors',[sys.executable,str(R/'runner/monitor_release.py'),*common,'--runtime-root',str(P),'--node','/usr/local/bin/node','--output',str(F/'maintained-monitors')],['monitor-contracts-0.1'],timeout=1200)
for label,adapter,suite in [('receive-controls','wasm_receive_controls.cjs','receive-control-0.1'),('library-noncompletion','wasm_library_noncompletion.cjs','library-noncompletion-0.1')]:
 add('chrome-'+label,['node',str(R/'adapters'/adapter)],[suite],dict(LIBRARY_MANIFEST=str(R/'cases'/(suite+'.json')),LIBRARY_REPORT=str(F/('chrome-'+label+'.json'))))
# The versioned native_goal field is the pack's direct-language API assertion.
suite='boolean-options-0.1';pack=json.loads((R/'cases'/(suite+'.json')).read_text());native=dict(pack,cases=[dict(c,goal=c['native_goal']) for c in pack['cases']]);temp=F/'boolean-native-api-assertions.json';temp.write_text(json.dumps(native,indent=2)+'\n')
for mode in ['worker','main']:
 add('boolean-native-api-'+mode,['node',str(R/'adapters/wasm.cjs'),str(P),mode,str(temp),str(F/('boolean-native-api-'+mode+'.json'))],[suite],timeout=1200)
(O/'browser-plan.json').write_text(json.dumps(plans,indent=2)+'\n');results=[]
for p in plans:
 print('START',p['label'],flush=True);start=time.monotonic()
 with (O/'logs'/('browser-'+p['label']+'.log')).open('w') as log:
  proc=subprocess.Popen(p['command'],cwd=R,env=dict(os.environ,**p['env']),stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  try:code=proc.wait(timeout=p['timeout'])
  except subprocess.TimeoutExpired:
   os.killpg(proc.pid,signal.SIGTERM)
   try:proc.wait(timeout=3)
   except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
   code=124
 results.append(dict(label=p['label'],exit_code=code,seconds=round(time.monotonic()-start,3),suites=p['suites']));(O/'browser-jobs.json').write_text(json.dumps(results,indent=2)+'\n');print('DONE',p['label'],code,flush=True)
