from pathlib import Path
import subprocess,concurrent.futures,json,time
P=Path(__file__).resolve().parents[1]
def one(node):
 with (P/'logs'/('public-'+node+'.log')).open('w') as out:r=subprocess.run(['python3',str(P/'orchestration/public.py'),node],stdout=out,stderr=subprocess.STDOUT)
 return dict(node=node,exit_code=r.returncode)
with concurrent.futures.ThreadPoolExecutor(8) as pool:
 rows=list(pool.map(one,['n0','n1','n2','n3','n4','n5','n6','n7']))
(P/'public-jobs.json').write_text(json.dumps(rows,indent=2)+'\n')
