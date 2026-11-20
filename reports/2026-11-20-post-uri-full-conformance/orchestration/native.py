import json,subprocess,os,sys,time,signal
from pathlib import Path
R=Path('/Users/lager/trinity-demonstrator/.trinity/conformance-post-uri-20261120/suite-snapshot');O=Path('/Users/lager/trinity-demonstrator/.trinity/conformance-post-uri-20261120');F=O/'native';F.mkdir(exist_ok=True)
COMMON=['--swipl','/usr/bin/swipl','--tpl','/opt/trealla/tpl','--swi-root','/opt/swi-prolog-node','--trealla-root','/work/trealla']
plans=[]
def add(label,script,args,suites,timeout=600):plans.append(dict(label=label,command=[sys.executable,str(R/script),*args],suites=suites,timeout=timeout))
exclude={'local-node-rpc-0.1','relation-error-admission-0.1','isobase-error-admission-0.1','interop-http-0.1','promise-yield-0.1','promise-diagnostics-0.1','interop-actor-0.1','interop-successor-0.1'}
for manifest in sorted((R/'cases').glob('*.json')):
 p=json.loads(manifest.read_text());suite=p['suite'];transports={c.get('transport','case_function') for c in p['cases']}
 if suite.startswith('standard-library-') or suite in exclude or '__PEER__' in manifest.read_text():continue
 if transports <= {'http','query','query_rejection','profile_policy'}:
  add(suite,'adapters/local_runtime_contracts.py',[*COMMON,'--manifest',str(manifest),'--output',str(F/suite)],[suite])
  if any('whitelist' in c.get('only_sandbox_modes',[]) for c in p['cases']):
   add(suite+'-whitelist','adapters/local_runtime_contracts.py',[*COMMON,'--mode','whitelist','--manifest',str(manifest),'--output',str(F/(suite+'-whitelist'))],[suite])
for ver in ['0.1','0.2','0.3','0.4']:
 suite='standard-library-'+ver
 add(suite,'adapters/local_standard_library.py',[*COMMON,'--gnu-root','/work/gnu','--manifest',str(R/'cases'/(suite+'.json')),'--output',str(F/suite)],[suite],900)
add('partial-page-errors','adapters/local_page_errors.py',[*COMMON,'--output',str(F/'partial-page-errors')],['partial-page-errors-0.1','error-contract-0.1'])
add('node-uri-io-0.1','adapters/node_uri_io.py',[*COMMON,'--manifest',str(R/'cases/node-uri-io-0.1.json'),'--output',str(F/'node-uri-io-0.1')],['node-uri-io-0.1'])
add('node-uri-io-0.2','adapters/node_uri_io.py',[*COMMON,'--manifest',str(R/'cases/node-uri-io-0.2.json'),'--output',str(F/'node-uri-io-0.2')],['node-uri-io-0.2'])
add('retained-context','runner/context_release.py',[*COMMON,'--output',str(F/'retained-context')],['retained-context-0.1'],1200)
add('receive-controls','adapters/local_receive_controls.py',[*COMMON,'--output',str(F/'receive-controls')],['receive-control-0.1'])
add('library-noncompletion','adapters/local_library_noncompletion.py',[*COMMON,'--gnu-root','/work/gnu','--output',str(F/'library-noncompletion')],['library-noncompletion-0.1'])
add('local-node-rpc','adapters/local_node_rpc.py',[*COMMON,'--gnu-node','/work/gnu/isobase/isobase-node','--output',str(F/'local-node-rpc.json')],['local-node-rpc-0.1'])
add('promises','adapters/local_promises.py',[*COMMON,'--demonstrator-root','/app','--output',str(F/'promises')],['promise-yield-0.1','interop-http-0.1'])
add('promise-diagnostics','adapters/local_promises.py',[*COMMON,'--demonstrator-root','/app','--diagnostics-only','--output',str(F/'promise-diagnostics')],['promise-diagnostics-0.1'])
add('portable-text-0.2','adapters/local_portable_text.py',[*COMMON,'--demonstrator-root','/app','--trusted-loopback-transport','--output',str(F/'portable-text-0.2')],['portable-text-0.2'])
add('rpc-timeouts-fixtures','adapters/local_rpc_timeouts.py',[*COMMON,'--gnu-root','/work/gnu','--output',str(F/'rpc-timeouts-fixtures')],['rpc-timeout-0.1'],900)
add('http-transport-fixtures','adapters/local_http_transport_options.py',[*COMMON,'--gnu-root','/work/gnu','--output',str(F/'http-transport-fixtures')],['http-transport-options-0.1'],900)
add('statechart-document-fixtures','adapters/local_statechart_documents.py',[*COMMON,'--output',str(F/'statechart-document-fixtures')],['statechart-document-0.1'])
(O/'native-plan.json').write_text(json.dumps(plans,indent=2)+'\n');results=[]
for plan in plans:
 start=time.monotonic();print('START',plan['label'],flush=True)
 with (O/'logs'/('native-'+plan['label']+'.log')).open('w') as log:
  proc=subprocess.Popen(plan['command'],cwd=R,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  try:code=proc.wait(timeout=plan['timeout'])
  except subprocess.TimeoutExpired:
   os.killpg(proc.pid,signal.SIGTERM)
   try:proc.wait(timeout=3)
   except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
   code=124
 results.append(dict(label=plan['label'],exit_code=code,seconds=round(time.monotonic()-start,3),suites=plan['suites']))
 (O/'native-jobs.json').write_text(json.dumps(results,indent=2)+'\n');print('DONE',plan['label'],code,flush=True)
