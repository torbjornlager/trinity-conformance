import concurrent.futures,subprocess,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def one(n):
 with (P/'logs'/('library-'+n+'.log')).open('w') as out:r=subprocess.run(['python3',str(P/'orchestration/live_library.py'),n],stdout=out,stderr=subprocess.STDOUT)
 return dict(node=n,exit_code=r.returncode)
with concurrent.futures.ThreadPoolExecutor(7) as pool:rows=list(pool.map(one,['n1','n2','n3','n4','n5','n6']))
(P/'library-jobs.json').write_text(json.dumps(rows,indent=2)+'\n')
