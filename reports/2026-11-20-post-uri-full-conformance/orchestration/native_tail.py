import subprocess,json,time
from pathlib import Path
P=Path(__file__).resolve().parents[1];C='conformance-upgraded-live-native-20261119';R=str(P/'suite-snapshot');rows=[]
while True:
 check="import pathlib; p="+repr(str(P/'orchestration/native.py'))+"; print(any(p.encode() in (f/'cmdline').read_bytes().split(b'\\0') for f in pathlib.Path('/proc').iterdir() if f.name.isdigit() and (f/'cmdline').exists()))"
 try:busy=subprocess.check_output(['docker','exec',C,'python3','-c',check],text=True).strip()=='True'
 except Exception:busy=True
 if not busy:break
 time.sleep(3)
common=['--swipl','/usr/bin/swipl','--tpl','/opt/trealla/tpl','--swi-root','/opt/swi-prolog-node','--trealla-root','/work/trealla']
plans=[('followup',['python3',str(P/'orchestration/followup-native.py')]),('extras',['python3',str(P/'orchestration/extras.py')])]
for n,extra in [('http-context-authenticated',[]),('http-context-anonymous',['--anonymous-http-sessions'])]:
 plans.append((n,['python3',R+'/adapters/local_retained_context.py',*common,'--http-session-context-only',*extra,'--output',str(P/'supplemental'/n)]))
plans.append(('client-naming',['python3',R+'/adapters/local_client_naming.py',*common,'--output',str(P/'supplemental/client-naming')]))
for label,cmd in plans:
 with (P/'logs'/('tail-'+label+'.log')).open('w') as out:code=subprocess.run(['docker','exec',C,*cmd],stdout=out,stderr=subprocess.STDOUT).returncode
 rows.append(dict(label=label,exit_code=code));(P/'native-tail-jobs.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,code,flush=True)
