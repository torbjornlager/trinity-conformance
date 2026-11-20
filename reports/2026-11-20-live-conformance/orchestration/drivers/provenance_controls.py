"""Supply exact shallow Git provenance for archive-based fixtures, then rerun setup failures."""
from pathlib import Path
import subprocess,json,hashlib
P=Path(__file__).resolve().parent;S=P/'suite-snapshot';R=Path('/Users/lager/trinity-conformance');revision=json.loads((P/'inputs.json').read_text())['revision']
def git(where,*args,**kwargs):return subprocess.check_output(['git','-C',str(where),*args],**kwargs)
if not (S/'.git').exists():
 subprocess.run(['git','init','-q',str(S)],check=True)
 lines=git(R,'ls-tree','-r','-t',revision,text=True).splitlines();trees={line.split()[2] for line in lines if line.split()[1]=='tree'};trees.add(git(R,'rev-parse',revision+'^{tree}',text=True).strip());objects=[revision,*sorted(trees)]
 packed=git(R,'pack-objects','--stdout',input=('\n'.join(objects)+'\n').encode());git(S,'index-pack','--stdin',input=packed)
 git(S,'symbolic-ref','HEAD','refs/heads/frozen');git(S,'update-ref','refs/heads/frozen',revision);(S/'.git/shallow').write_text(revision+'\n');(S/'.git/info/exclude').write_text('__pycache__/\n*.pyc\n')
 git(S,'read-tree',revision);tracked=git(S,'ls-files','-z');git(S,'update-index','--skip-worktree','-z','--stdin',input=tracked)
 present=[str(f.relative_to(S)) for f in S.rglob('*') if f.is_file() and '.git' not in f.relative_to(S).parts and '__pycache__' not in f.parts and f.suffix!='.pyc']
 git(S,'hash-object','-w','--stdin-paths',input='\n'.join(present)+'\n',text=True);git(S,'update-index','--no-skip-worktree','--stdin',input='\n'.join(present)+'\n',text=True)
assert git(S,'rev-parse','HEAD',text=True).strip()==revision;assert not git(S,'status','--porcelain',text=True).strip()
print('Exact shallow suite Git provenance restored; frozen file bytes unchanged',flush=True)
name='conformance-live-provenance-20261120';subprocess.run(['docker','create','--name',name,'--network','none','--memory','2g','--cpus','2','--pids-limit','512','--no-healthcheck','--entrypoint','sh','local/conformance-live-lab:20261120','-c','exec sleep infinity'],check=True,stdout=subprocess.DEVNULL);subprocess.run(['docker','start',name],check=True,stdout=subprocess.DEVNULL)
try:
 subprocess.run(['docker','exec',name,'mkdir','-p',str(S),str(P/'procps-rerun')],check=True);subprocess.run(['docker','cp',str(S)+'/.',name+':'+str(S)],check=True);subprocess.run(['docker','exec',name,'chown','-R','0:0',str(S)],check=True)
 common=['--swipl','/usr/bin/swipl','--tpl','/opt/trealla/tpl','--swi-root','/opt/swi-prolog-node','--trealla-root','/work/trealla'];rows=[]
 plans=[('promises','local_promises.py',['--demonstrator-root','/app']),('promise-diagnostics','local_promises.py',['--demonstrator-root','/app','--diagnostics-only']),('boolean-owner-off','local_runtime_contracts.py',['--mode','off','--manifest',str(S/'cases/boolean-boundary-diagnostics-0.1.json')])]
 for label,script,extra in plans:
  print('START',label,flush=True)
  with (P/'logs'/('provenance-'+label+'.log')).open('w') as log:r=subprocess.run(['docker','exec',name,'python3',str(S/'adapters'/script),*common,*extra,'--output',str(P/'procps-rerun'/label)],stdout=log,stderr=subprocess.STDOUT)
  rows.append(dict(label=label,exit_code=r.returncode));(P/'provenance-control-jobs.json').write_text(json.dumps(rows,indent=2)+'\n');print('DONE',label,r.returncode,flush=True)
 subprocess.run(['docker','cp',name+':'+str(P/'procps-rerun'),str(P)],check=True)
finally:subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
(P/'provenance-controls.complete').write_text('complete\n')
