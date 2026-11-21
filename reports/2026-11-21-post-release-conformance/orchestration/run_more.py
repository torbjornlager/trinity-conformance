import concurrent.futures,subprocess,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def one(n):
 with (P/'logs'/('more-'+n+'.log')).open('w') as out:r=subprocess.run(['python3',str(P/'orchestration/live_more.py'),n],stdout=out,stderr=subprocess.STDOUT)
 return dict(node=n,exit_code=r.returncode)
with concurrent.futures.ThreadPoolExecutor(6) as pool:rows=list(pool.map(one,['n1','n2','n3','n4','n5','n6']))
(P/'more-jobs.json').write_text(json.dumps(rows,indent=2)+'\n')
