from pathlib import Path
import subprocess,json,time,urllib.request,urllib.error
O=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-demonstrator')
assert R==Path('/Users/lager/trinity-demonstrator')
ci=json.loads((O/'pinned-ci/results.json').read_text())
assert len(ci)==36 and all(r['exit_code']==0 for r in ci), 'all consumer CI groups must pass'
assert 'PASS N6 candidate' in (O/'candidate-n6-driver.txt').read_text()
assert 'PASS native containment' in (O/'candidate-n6-containment.txt').read_text()
rev=(O/'consumer-revision.txt').read_text().strip();old={r['name']:r for r in json.loads((O/'rollback-images.json').read_text())}
def run(cmd):return subprocess.check_output(cmd,cwd=R,text=True,stderr=subprocess.STDOUT).strip()
def inspect(name):return json.loads(run(['docker','inspect',name]))[0]
def compose(project,files,env):
 cmd=['docker','compose','--env-file','Deployment/'+env,'-p',project]
 for file in files:cmd+=['-f','Deployment/'+file]
 return cmd
main=compose('deployment',['compose.yaml','compose.trealla-n5.yaml','compose.trealla-n5-public.yaml','compose.peer-transport-volumes.yaml','compose.gprolog-n6-caddy.yaml'],'.env')
hub=compose('web-prolog-hub',['compose.hub-attach.yaml'],'.env')
nh=compose('trinity-n6-host',['compose.gprolog-n6-local.yaml','compose.gprolog-n6-host.yaml','compose.gprolog-n6-public.yaml'],'.env.n6')
nl=compose('trinity-n6-local',['compose.gprolog-n6-local.yaml'],'.env.n6')
plans=[]
for n in range(1,5):plans.append(dict(name=f'deployment-wp_n{n}-1',service=f'wp_n{n}',tag=f'deployment-wp_n{n}',image='trinity-standard-library-native:20261105',cmd=main,url=f'https://n{n}.elfenbenstornet.se/node_info'))
plans += [dict(name='deployment-wp_admin-1',service='wp_admin',tag='deployment-wp_admin',image='trinity-standard-library-native:20261105',cmd=main,url='http://127.0.0.1:3054/healthz'),dict(name='deployment-wp_n5-1',service='wp_n5',tag='deployment-wp_n5',image='trinity-standard-library-n5:20261105',cmd=main,url='https://n5.elfenbenstornet.se/node_info')]
for prefix,cmd in [('trinity-n6-host',nh),('trinity-n6-local',nl)]:
 plans.append(dict(name=prefix+'-n6_assets-1',service='n6_assets',tag='trinity-n6-assets:latest',image='trinity-standard-library-native:20261105',cmd=cmd,internal_port=3051))
 plans.append(dict(name=prefix+'-wp_n6-1',service='wp_n6',tag=prefix+':latest',image='trinity-standard-library-n6:20261105',cmd=cmd,url='https://n6.elfenbenstornet.se/node_info' if prefix.endswith('host') else 'http://127.0.0.1:3057/healthz'))
plans.append(dict(name='trinity-n6-local-n6_hub-1',service='n6_hub',tag='trinity-n6-assets:latest',image='trinity-standard-library-native:20261105',cmd=nl,url='http://127.0.0.1:3058/node_info'))
plans.append(dict(name='web-prolog-hub-n0-1',service='n0',tag='web-prolog-hub-n0',image='trinity-standard-library-hub:20261105',cmd=hub,url='https://n0.elfenbenstornet.se/node_info'))
for p in plans:assert inspect(p['name'])['Image']==old[p['name']]['image_id'],'deployment changed since snapshot: '+p['name']
rows=[];attempted=[]
def save(): (O/'rollout-results.json').write_text(json.dumps(rows,indent=2)+'\n')
try:
 for p in plans:
  print('Updating',p['name'],flush=True)
  run(['docker','tag',p['image'],p['tag']]);attempted.append(p)
  started=time.monotonic();run(p['cmd']+['up','-d','--no-build','--no-deps',p['service']])
  expected=run(['docker','image','inspect',p['image'],'--format','{{.Id}}'])
  last=None
  for _ in range(90):
   try:
    state=inspect(p['name']);assert state['State']['Running'];assert state['Image']==expected
    assert state['Config']['Labels']['org.opencontainers.image.revision']==rev
    import hashlib
    assert hashlib.sha256(json.dumps(sorted(state['Config']['Env'])).encode()).hexdigest()==old[p['name']]['environment_sha256'], 'environment changed'
    assert state['Config']['User']==old[p['name']]['user'], 'runtime user changed'
    assert {k:state['HostConfig'].get(k) for k in old[p['name']]['controls']}==old[p['name']]['controls'], 'resource or security controls changed'
    assert sorted([{'name':m.get('Name'),'destination':m['Destination']} for m in state['Mounts']],key=lambda m:m['destination'])==sorted(old[p['name']]['volumes'],key=lambda m:m['destination']), 'persistent mounts changed'
    health=state['State'].get('Health',{}).get('Status');assert health not in ('unhealthy','starting')
    if p.get('url'):
     with urllib.request.urlopen(p['url'],timeout=4) as response:assert response.status==200
    else:
     run(['docker','exec',p['name'],'python3','-c',"import urllib.request;urllib.request.urlopen('http://127.0.0.1:"+str(p['internal_port'])+"/healthz',timeout=3).close()"])
    break
   except Exception as e:last=str(e);time.sleep(1)
  else:raise RuntimeError(p['name']+' did not become ready: '+str(last))
  rows.append(dict(name=p['name'],status='deployed',image_id=expected,consumer_revision=rev,seconds=round(time.monotonic()-started,2),rollback_tag=old[p['name']]['rollback_tag']));save();print('Ready',p['name'],flush=True)
except BaseException:
 print('Rollout failed; restoring attempted services',flush=True)
 for p in reversed(attempted):
  try:run(['docker','tag',old[p['name']]['rollback_tag'],p['tag']]);run(p['cmd']+['up','-d','--no-build','--no-deps',p['service']])
  except Exception as e:print('Rollback failed for',p['name'],str(e),flush=True)
 raise
print('PASS all 12 runtime and asset services updated; persistent volumes and admission configuration retained',flush=True)
