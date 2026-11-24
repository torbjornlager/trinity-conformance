import json,subprocess,time,sys
from pathlib import Path
R=Path('/Users/lager/trinity-demonstrator/.trinity/conformance-post-xn-20261124/suite-snapshot');O=Path('/Users/lager/trinity-demonstrator/.trinity/conformance-post-xn-20261124');F=O/'followup-native';F.mkdir();C=['--swipl','/usr/bin/swipl','--tpl','/opt/trealla/tpl','--swi-root','/opt/swi-prolog-node','--trealla-root','/work/trealla'];plans=[]
for label,extra in [('promises-valid',[]),('promise-diagnostics-valid',['--diagnostics-only'])]:plans.append((label,[sys.executable,str(R/'adapters/local_promises.py'),*C,'--demonstrator-root','/app','--output',str(F/label),*extra]))
for suite in ['monitor-contracts-0.1','monitor-preflight-0.1']:plans.append((suite+'-source-aware',[sys.executable,str(R/'adapters/local_actor_cases.py'),*C,'--sandbox','blacklist','--manifest',str(R/'cases'/(suite+'.json')),'--output',str(F/(suite+'-source-aware'))]))
suites=['uri-atoms-0.1','manual-option-sources-0.1','supervisor-common-0.1','statechart-document-0.1','rpc-timeout-0.1','http-transport-options-0.1','appendix-library-probes-0.1']
args=[sys.executable,str(R/'adapters/local_manual_boundaries.py'),*C,'--gnu-worker','/work/gnu/isobase/query-worker','--output',str(F/'standalone-boundaries.json')]
for suite in suites:args+=['--suite',suite]
plans.append(('standalone-boundaries',args));plans.append(('boolean-resource-controls',[sys.executable,str(R/'adapters/native_boolean_options.py'),'--swi-root','/opt/swi-prolog-node','--trealla-root','/work/trealla','--tpl','/opt/trealla/tpl','--output',str(F/'boolean-resource-controls')]))
rows=[]
for label,cmd in plans:
 print('START',label,flush=True);t=time.monotonic()
 with (O/'logs'/('followup-'+label+'.log')).open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=900)
 rows.append(dict(label=label,exit_code=r.returncode,seconds=round(time.monotonic()-t,3)));(O/'followup-native-jobs.json').write_text(json.dumps(rows,indent=2)+'\n');print('DONE',label,r.returncode,flush=True)
