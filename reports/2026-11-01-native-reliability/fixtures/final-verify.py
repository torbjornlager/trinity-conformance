import subprocess,pathlib,json,concurrent.futures,os,time
root=pathlib.Path('/work'); src=root/'final-sources'
cases={'swi-native':(['/bin/bash','./tools/test.sh'],src/'swi'), 'trealla-native':(['/bin/sh','./tools/test.sh','unit'],src/'trealla'), 'release':(['python3','adapters/local_actor_release.py','--sources',str(src),'--output','/work/verified-release'],root/'conformance')}
def run(item):
 name,(cmd,folder)=item;start=time.monotonic()
 with (root/('verified-'+name+'.log')).open('w') as log:
  try:
   p=subprocess.run(cmd,cwd=folder,stdout=log,stderr=subprocess.STDOUT,env=dict(os.environ,SWIPL='/usr/bin/swipl',TPL='/opt/trealla/tpl',TPL_LIBRARY_PATH='/opt/trealla/library'),timeout=300);status=p.returncode
  except subprocess.TimeoutExpired:status='timeout'
 row={'status':status,'seconds':time.monotonic()-start,'command':cmd,'cwd':str(folder)};(root/('verified-'+name+'.json')).write_text(json.dumps(row,indent=2));print(name,row,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(run,cases.items()))
