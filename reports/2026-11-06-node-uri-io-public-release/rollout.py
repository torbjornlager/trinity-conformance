from pathlib import Path
import subprocess,json,time,urllib.request,sys
sys.dont_write_bytecode=True
from inventory import invariant
O=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-demonstrator')
old={r['name']:r for r in json.loads((O/'rollback-inventory.json').read_text())}
rev=(O/'consumer-revision.txt').read_text().strip()
def run(cmd):return subprocess.check_output(cmd,cwd=R,text=True,stderr=subprocess.STDOUT).strip()
def inspect(name):return json.loads(run(['docker','inspect',name]))[0]
def compose(p):
 cmd=['docker','compose','--env-file',str(R/'Deployment'/('.env.n6' if p['project'].startswith('trinity-n6-') else '.env')),'-p',p['project']]
 for file in p['compose_files'].split(','):cmd+=['-f',file]
 return cmd
updates=['deployment-wp_n1-1','deployment-wp_n2-1','deployment-wp_n3-1','deployment-wp_n4-1','deployment-wp_admin-1','deployment-wp_n5-1','trinity-n6-host-n6_assets-1','trinity-n6-local-n6_assets-1','trinity-n6-local-n6_hub-1','web-prolog-hub-n0-1']
urls={'deployment-wp_n1-1':'https://n1.elfenbenstornet.se/node_info','deployment-wp_n2-1':'https://n2.elfenbenstornet.se/node_info','deployment-wp_n3-1':'https://n3.elfenbenstornet.se/node_info','deployment-wp_n4-1':'https://n4.elfenbenstornet.se/node_info','deployment-wp_admin-1':'http://127.0.0.1:3054/healthz','deployment-wp_n5-1':'https://n5.elfenbenstornet.se/node_info','trinity-n6-host-wp_n6-1':'https://n6.elfenbenstornet.se/node_info','trinity-n6-local-wp_n6-1':'http://127.0.0.1:3057/node_info','trinity-n6-local-n6_hub-1':'http://127.0.0.1:3058/node_info','web-prolog-hub-n0-1':'https://n0.elfenbenstornet.se/node_info'}
assert all(r['exit_code']==0 for r in json.loads((O/'build-results.json').read_text()))
assert len(json.loads((O/'build-results.json').read_text()))==4
assert (O/'consumer-tests.exit').read_text().strip()=='0'
assert (O/'smoke.exit').read_text().strip()=='0'
assert 'Actor write/1 output: all regressions passed' in (O/'trealla-image-tests.log').read_text()
assert json.loads((O/'actor-release/provenance.json').read_text())['engines'] and all(e['returncode']==0 for e in json.loads((O/'actor-release/provenance.json').read_text())['engines'])
for name,p in old.items():
 d=inspect(name);assert d['Image']==p['image_id'] and invariant(d)==p['invariant'],('live deployment changed',name)
rows=[];attempted=[]
try:
 for name in updates:
  p=old[name];component='hub' if name=='web-prolog-hub-n0-1' else 'n5' if name=='deployment-wp_n5-1' else 'n6' if name in ('trinity-n6-host-wp_n6-1','trinity-n6-local-wp_n6-1') else 'native';image='trinity-node-uri-io-'+component+':20261106';expected=run(['docker','image','inspect',image,'--format','{{.Id}}'])
  print('Updating',name,flush=True);run(['docker','tag',image,p['configured_image']]);attempted.append(p)
  run(compose(p)+['up','-d','--no-build','--no-deps',p['service']]);start=time.monotonic();last=None
  for _ in range(90):
   try:
    d=inspect(name);assert d['State']['Running'] and d['Image']==expected;assert invariant(d)==p['invariant'],'runtime configuration changed';assert d['Config']['Labels']['org.opencontainers.image.revision']==rev
    assert d['State'].get('Health',{}).get('Status') not in ('starting','unhealthy')
    if name in urls:
     with urllib.request.urlopen(urls[name],timeout=4) as response:assert response.status==200
    else:
     run(['docker','exec',name,'python3','-c',"import urllib.request;urllib.request.urlopen('http://127.0.0.1:3051/healthz',timeout=3).close()"])
    break
   except Exception as e:last=str(e);time.sleep(1)
  else:raise RuntimeError(name+' not ready: '+str(last))
  rows.append(dict(name=name,image_id=expected,consumer_revision=rev,status='deployed',configuration_preserved=True,seconds=round(time.monotonic()-start,2),rollback_tag=p['rollback_tag']));(O/'rollout-results.json').write_text(json.dumps(rows,indent=2)+'\n');print('Ready',name,flush=True)
 for name,p in old.items():
  if name not in updates:
   d=inspect(name);assert d['Image']==p['image_id'] and invariant(d)==p['invariant'],('unmodified service changed',name)
except BaseException:
 print('Restoring attempted services',flush=True)
 for p in reversed(attempted):
  try:run(['docker','tag',p['rollback_tag'],p['configured_image']]);run(compose(p)+['up','-d','--no-build','--no-deps',p['service']])
  except Exception as e:print('Rollback failure',p['name'],str(e),flush=True)
 raise
print('PASS ten services updated; six other services and all configuration fingerprints preserved',flush=True)
