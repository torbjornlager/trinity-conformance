from pathlib import Path
import subprocess,json
P=Path(__file__).resolve().parents[1];name='conformance-upgraded-procps-20261119';rows=[]
common=['--swipl','/usr/bin/swipl','--tpl','/opt/trealla/tpl','--swi-root','/opt/swi-prolog-node','--trealla-root','/work/trealla','--demonstrator-root','/app']
for label,script,extra in [('promises','local_promises.py',[]),('promise-diagnostics','local_promises.py',['--diagnostics-only']),('portable-text-0.2','local_portable_text.py',['--trusted-loopback-transport'])]:
 with (P/'logs'/('procps-'+label+'.log')).open('w') as out:r=subprocess.run(['docker','exec',name,'python3','/work/suite/adapters/'+script,*common,*extra,'--output','/work/output/'+label],stdout=out,stderr=subprocess.STDOUT)
 rows.append(dict(label=label,exit_code=r.returncode));(P/'procps-rerun-jobs.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,r.returncode,flush=True)
subprocess.run(['docker','cp',name+':/work/output',str(P/'procps-rerun')],check=True)
