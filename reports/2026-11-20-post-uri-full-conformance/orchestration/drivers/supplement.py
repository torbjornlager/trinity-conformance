from pathlib import Path
import subprocess,time,json
P=Path(__file__).resolve().parent;name='conformance-post-uri-lab-20261120'
while not (P/'owned-native.complete').exists():time.sleep(3)
common=['--swipl','/usr/bin/swipl','--tpl','/opt/trealla/tpl','--swi-root','/opt/swi-prolog-node','--trealla-root','/work/trealla'];rows=[]
plans=[]
for label,extra in [('http-context-authenticated',[]),('http-context-anonymous',['--anonymous-http-sessions'])]:plans.append((label,['python3',str(P/'suite-snapshot/adapters/local_retained_context.py'),*common,'--http-session-context-only',*extra,'--output',str(P/'supplemental'/label)]))
plans.append(('client-naming',['python3',str(P/'suite-snapshot/adapters/local_client_naming.py'),*common,'--output',str(P/'supplemental/client-naming')]))
s=(P/'orchestration/prompt_enabled_fixture.py').read_text().replace("P=Path('/work');R=P/'suite';F=P/'output';F.mkdir()",'P=Path('+repr(str(P))+" );R=P/'suite-snapshot';F=P/'prompt-enabled';F.mkdir()")
(P/'orchestration/prompt_enabled_fixture.py').write_text(s);subprocess.run(['docker','cp',str(P/'orchestration/prompt_enabled_fixture.py'),name+':'+str(P/'orchestration/prompt_enabled_fixture.py')],check=True)
plans.append(('prompt-enabled',['python3',str(P/'orchestration/prompt_enabled_fixture.py')]))
try:
 for label,cmd in plans:
  print('START',label,flush=True)
  with (P/'logs'/('supplement-'+label+'.log')).open('w') as log:r=subprocess.run(['docker','exec',name,*cmd],stdout=log,stderr=subprocess.STDOUT)
  rows.append(dict(label=label,exit_code=r.returncode));(P/'supplement-jobs.json').write_text(json.dumps(rows,indent=2)+'\n');print('DONE',label,r.returncode,flush=True)
 for folder in ['supplemental','prompt-enabled','logs']:
  subprocess.run(['docker','cp',name+':'+str(P/folder),str(P)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
finally:
 subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 (P/'lab-cleanup.json').write_text(json.dumps(dict(owned_container=name,removed=True,production_containers_modified=False),indent=2)+'\n')
(P/'supplement.complete').write_text('complete\n')
