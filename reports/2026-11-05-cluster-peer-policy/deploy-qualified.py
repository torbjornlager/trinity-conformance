from pathlib import Path
import subprocess,json,time,shutil
O=Path(__file__).resolve().parent
ci=O/'consumer-ci';rows=json.loads((ci/'results.json').read_text())
assert len(rows)==38 and all(x['exit_code']==0 for x in rows)
print('PASS all 38 consumer groups; starting rollout',flush=True)
for label,file,args in [('rollout','rollout.py',[]),('pins','check-running-pins.py',[]),('policy','inspect-policy.py',[]),('contexts','run-context-public.py',[]),('peer-credential','verify-peer-configuration.py',[]),('public-smoke','verify-public.py',[])]:
 print('START',label,flush=True)
 with (O/(label+'-driver.txt')).open('w') as log:r=subprocess.run(['python3',str(O/file),*args],stdout=log,stderr=subprocess.STDOUT)
 print('DONE',label,r.returncode,flush=True)
 if r.returncode:raise SystemExit(r.returncode)
print('PASS cluster policy deployment and public gates',flush=True)
