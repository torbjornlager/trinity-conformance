from pathlib import Path
import subprocess,json,time
P=Path(__file__).resolve().parents[1];rows=[];time.sleep(61)
for label,script in [('more','live_more.py'),('library','live_library.py')]:
 with (P/'logs'/(label+'-n2.log')).open('w') as out:r=subprocess.run(['python3',str(P/'orchestration'/script),'n2'],stdout=out,stderr=subprocess.STDOUT)
 rows.append(dict(phase=label,exit_code=r.returncode));(P/'n2-http-jobs.json').write_text(json.dumps(rows,indent=2)+'\n')
