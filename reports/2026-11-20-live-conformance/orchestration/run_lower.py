import concurrent.futures,subprocess,json,time
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def one(n):
 time.sleep(61)
 with (P/'logs'/('more-'+n+'.log')).open('w') as out:r=subprocess.run(['python3',str(P/'orchestration/live_more.py'),n],stdout=out,stderr=subprocess.STDOUT)
 return dict(node=n,exit_code=r.returncode)
with concurrent.futures.ThreadPoolExecutor(2) as pool:rows=list(pool.map(one,['n1','n6']))
(P/'lower-http-jobs.json').write_text(json.dumps(rows,indent=2)+'\n')
