from pathlib import Path
import json,subprocess,concurrent.futures,time,sys
P=Path(__file__).resolve().parents[1]
def one(node):
 rows=[];stages=['public.py']+(['live_more.py','live_library.py'] if node!='n0' else [])+(['prompt_live_paused.py'] if node in ['n2','n3','n4','n5'] else [])
 for script in stages:
  phase={'public.py':'public','live_more.py':'more','live_library.py':'library','prompt_live_paused.py':'paused-prompt'}[script]
  print('START',node,phase,flush=True);t=time.monotonic()
  with (P/'logs'/(phase+'-'+node+'.log')).open('w') as log:
   result=subprocess.run([sys.executable,str(P/'orchestration'/script),node],stdout=log,stderr=subprocess.STDOUT)
  rows.append(dict(node=node,phase=phase,exit_code=result.returncode,seconds=round(time.monotonic()-t,3)));(P/(node+'-jobs.json')).write_text(json.dumps(rows,indent=2)+'\n');print('DONE',node,phase,result.returncode,flush=True)
 (P/'logs'/('endpoint-'+node+'.done')).write_text('complete\n');return rows
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:rows=list(executor.map(one,['n0','n1','n2','n3','n4','n5','n6','n7']))
(P/'endpoint-jobs.json').write_text(json.dumps(rows,indent=2)+'\n');print('All public endpoint pipelines complete',flush=True)
