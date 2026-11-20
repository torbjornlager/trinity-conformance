from pathlib import Path
import json,subprocess
P=Path(__file__).resolve().parent;before=json.loads((P/'preservation-before.json').read_text());image=next(r['image'] for r in before if r['name']=='/trinity-n6-host-wp_n6-1');name='conformance-n6-capacity-delta-20261120';F=P/'n6/owned-capacity';F.mkdir()
try:
 subprocess.run(['docker','create','--name',name,'--user','root','--network','none','--memory','1g','--cpus','1','--pids-limit','128','--no-healthcheck','--entrypoint','sh',image,'-c','exec sleep infinity'],stdout=subprocess.DEVNULL,check=True);subprocess.run(['docker','start',name],stdout=subprocess.DEVNULL,check=True);subprocess.run(['docker','exec',name,'mkdir','-p','/work'],check=True);subprocess.run(['docker','cp',str(P/'n6_capacity_probe.py'),name+':/work/probe.py'],check=True)
 with (P/'logs/n6-owned-capacity.log').open('w') as log:r=subprocess.run(['docker','exec',name,'python3','/work/probe.py'],stdout=log,stderr=subprocess.STDOUT,timeout=60)
 subprocess.run(['docker','cp',name+':/work/results/.',str(F)],check=True);print('Owned N6 capacity diagnostic exit',r.returncode)
finally:subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
