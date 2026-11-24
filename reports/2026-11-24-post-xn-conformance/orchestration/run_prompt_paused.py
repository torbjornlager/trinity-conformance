from pathlib import Path
import concurrent.futures,subprocess,json
P=Path(__file__).resolve().parents[1]
def one(n):
 with (P/'logs'/('paused-prompt-'+n+'.log')).open('w') as out:r=subprocess.run(['python3',str(P/'orchestration/prompt_live_paused.py'),n],stdout=out,stderr=subprocess.STDOUT)
 return dict(node=n,exit_code=r.returncode)
with concurrent.futures.ThreadPoolExecutor(4) as pool:rows=list(pool.map(one,['n2','n3','n4','n5']))
(P/'paused-prompt-jobs.json').write_text(json.dumps(rows,indent=2)+'\n')
