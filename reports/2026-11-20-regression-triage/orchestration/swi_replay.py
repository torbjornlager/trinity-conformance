from pathlib import Path
import subprocess,json,concurrent.futures
P=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-conformance');versions={}
for label,day in [('previous','2026-11-19-upgraded-live-conformance'),('current','2026-11-20-live-conformance')]:
 d=json.loads((R/'reports'/day/'preservation.json').read_text());image=next(r['image'] for r in d['before'] if r['name']=='/deployment-wp_n3-1')
 identity=subprocess.check_output(['docker','run','--rm','--network','none','--entrypoint','sh',image,'-c','git -C /opt/swi-prolog-node rev-parse HEAD; swipl --version; find /usr/lib/swipl -type f -exec sha256sum {} + | sort | sha256sum'],text=True);versions[label]=dict(image=image,identity=identity.splitlines())
(P/'swi/versions.json').write_text(json.dumps(versions,indent=2)+'\n');assert versions['previous']['identity'][1:]==versions['current']['identity'][1:],'Engine identity differs'
def one(label):
 name='conformance-delta-'+label+'-20261120';image=versions[label]['image'];F=P/'swi'/label;F.mkdir(exist_ok=True)
 try:
  subprocess.run(['docker','create','--user','root','--name',name,'--network','none','--memory','1g','--cpus','2','--pids-limit','256','--no-healthcheck','--entrypoint','sh',image,'-c','exec sleep infinity'],check=True,stdout=subprocess.DEVNULL);subprocess.run(['docker','start',name],check=True,stdout=subprocess.DEVNULL);subprocess.run(['docker','exec',name,'mkdir','-p','/work/suite'],check=True)
  for folder in ['runner','adapters','cases','fixtures','profiles']:subprocess.run(['docker','cp',str(R/folder),name+':/work/suite/'],check=True)
  subprocess.run(['docker','cp',str(P/'nu_probe.py'),name+':/work/nu_probe.py'],check=True)
  with (P/'logs'/('swi-'+label+'.log')).open('w') as log:r=subprocess.run(['docker','exec',name,'python3','/work/nu_probe.py',label,'1000'],stdout=log,stderr=subprocess.STDOUT)
  subprocess.run(['docker','cp',name+':/work/results/.',str(F)],check=True);print(label,'exit',r.returncode,flush=True)
 finally:subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(one,['previous','current']))
(P/'swi-raw.complete').write_text('complete\n')
