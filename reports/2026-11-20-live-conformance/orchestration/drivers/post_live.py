from pathlib import Path
import subprocess,time,json,sys
P=Path(__file__).resolve().parent
while not all((P/'logs'/('endpoint-'+n+'.done')).exists() for n in ['n0','n1','n2','n3','n4','n5','n7']):time.sleep(3)
rows=[]
for script in ['public-extra.py','run_http_context.py','post_n5_controls.py','receive_diagnostic.py']:
 print('START',script,flush=True)
 with (P/'logs'/('post-'+script+'.log')).open('w') as log:r=subprocess.run([sys.executable,str(P/'orchestration'/script)],stdout=log,stderr=subprocess.STDOUT)
 rows.append(dict(script=script,exit_code=r.returncode));(P/'post-live-jobs.json').write_text(json.dumps(rows,indent=2)+'\n');print('DONE',script,r.returncode,flush=True)
(P/'post-live.complete').write_text('complete\n')
