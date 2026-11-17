from pathlib import Path
import subprocess,json,time,urllib.request,urllib.error
O=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-demonstrator')
assert R==Path('/Users/lager/trinity-demonstrator')
Q=O
ci=json.loads((Q/'consumer-ci/results.json').read_text())
assert len(ci)==38 and all(r['exit_code']==0 for r in ci),'all pinned consumer groups must pass'
# Runtime pins are unchanged from the preceding fully qualified release.
previous=json.loads((O.parent/'2026-11-05-native-context-release'/'verification.json').read_text())
for kind,pin in previous['pins'].items():
    assert json.loads((R/'dependencies'/(kind+'.json')).read_text())==pin
rev=(O/'consumer-revision.txt').read_text().strip();old={r['name']:r for r in json.loads((O/'rollback-images.json').read_text())}
def run(cmd,env=None):return subprocess.check_output(cmd,cwd=R,text=True,stderr=subprocess.STDOUT,env=env).strip()
def inspect(name):return json.loads(run(['docker','inspect',name]))[0]
def compose(project,files,env):
 cmd=['docker','compose','--env-file','Deployment/'+env,'-p',project]
 for file in files:cmd+=['-f','Deployment/'+file]
 return cmd
rollback_main=compose('deployment',['compose.yaml','compose.trealla-n5.yaml','compose.trealla-n5-public.yaml','compose.peer-transport-volumes.yaml','compose.gprolog-n6-caddy.yaml'],'.env')
main=compose('deployment',['compose.yaml','compose.trealla-n5.yaml','compose.trealla-n5-public.yaml','compose.peer-transport-volumes.yaml','compose.gprolog-n6-caddy.yaml','compose.peer-transport-n5-volumes.yaml'],'.env')
hub=compose('web-prolog-hub',['compose.hub-attach.yaml'],'.env')
nh=compose('trinity-n6-host',['compose.gprolog-n6-local.yaml','compose.gprolog-n6-host.yaml','compose.gprolog-n6-public.yaml'],'.env.n6')
nl=compose('trinity-n6-local',['compose.gprolog-n6-local.yaml'],'.env.n6')
plans=[]
for n in range(1,5):plans.append(dict(name=f'deployment-wp_n{n}-1',service=f'wp_n{n}',tag=f'deployment-wp_n{n}',image='trinity-cluster-policy-native:20261105-cluster',cmd=main,url=f'https://n{n}.elfenbenstornet.se/node_info'))
plans += [dict(name='deployment-wp_admin-1',service='wp_admin',tag='deployment-wp_admin',image='trinity-cluster-policy-native:20261105-cluster',cmd=main,url='http://127.0.0.1:3054/healthz'),dict(name='deployment-wp_n5-1',service='wp_n5',tag='deployment-wp_n5',image='trinity-cluster-policy-n5:20261105-cluster',cmd=main,url='https://n5.elfenbenstornet.se/node_info')]
for prefix,cmd in [('trinity-n6-host',nh),('trinity-n6-local',nl)]:
 plans.append(dict(name=prefix+'-n6_assets-1',service='n6_assets',tag='trinity-n6-assets:latest',image='trinity-cluster-policy-native:20261105-cluster',cmd=cmd,internal_port=3051))
 plans.append(dict(name=prefix+'-wp_n6-1',service='wp_n6',tag=prefix+':latest',image='trinity-cluster-policy-n6:20261105-cluster',cmd=cmd,url='https://n6.elfenbenstornet.se/node_info' if prefix.endswith('host') else 'http://127.0.0.1:3057/healthz'))
plans.append(dict(name='trinity-n6-local-n6_hub-1',service='n6_hub',tag='trinity-n6-assets:latest',image='trinity-cluster-policy-native:20261105-cluster',cmd=nl,url='http://127.0.0.1:3058/node_info'))
plans.append(dict(name='web-prolog-hub-n0-1',service='n0',tag='web-prolog-hub-n0',image='trinity-cluster-policy-hub:20261105-cluster',cmd=hub,url='https://n0.elfenbenstornet.se/node_info'))
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
    current_env=state['Config']['Env']
    if p['name']=='deployment-wp_n5-1':
     values=dict(x.split('=',1) for x in current_env)
     assert values['WP_PEER_TRANSPORT_TOKENS_FILE']=='/run/peer-transport/peers.pl'
     expected_old=','.join(json.loads((O/'public-spawn-policy-before.json').read_text())['graph']['https://n5.elfenbenstornet.se'])
     assert values['WP_LOAD_URI_ORIGINS'].split(',')==['https://n2.elfenbenstornet.se','https://n3.elfenbenstornet.se','https://n4.elfenbenstornet.se','https://n5.elfenbenstornet.se']
     current_env=[('WP_LOAD_URI_ORIGINS='+expected_old) if x.startswith('WP_LOAD_URI_ORIGINS=') else x for x in current_env]
    assert hashlib.sha256(json.dumps(sorted(current_env)).encode()).hexdigest()==old[p['name']]['environment_sha256'],'unexpected environment change'
    assert state['Config']['User']==old[p['name']]['user'], 'runtime user changed'
    assert {k:state['HostConfig'].get(k) for k in old[p['name']]['controls']}==old[p['name']]['controls'], 'resource or security controls changed'
    mounts=state['Mounts']
    if p['name']=='deployment-wp_n5-1':
     peer=next(m for m in mounts if m['Destination']=='/run/peer-transport')
     assert peer['Name']=='trinity-n5-peer-transport' and not peer['RW']
    assert sorted([{'name':m.get('Name'),'destination':m['Destination']} for m in mounts],key=lambda m:m['destination'])==sorted(old[p['name']]['volumes'],key=lambda m:m['destination']),'persistent mounts changed'
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
  try:
   run(['docker','tag',old[p['name']]['rollback_tag'],p['tag']])
   cmd=p['cmd']
   if p['name']=='deployment-wp_n5-1':
    override=O/'rollback-n5-policy.yaml';before=','.join(json.loads((O/'public-spawn-policy-before.json').read_text())['graph']['https://n5.elfenbenstornet.se'])
    override.write_text('services:\n  wp_n5:\n    environment:\n      WP_LOAD_URI_ORIGINS: '+before+'\n')
    cmd=cmd+['-f',str(override.resolve())]
   run(cmd+['up','-d','--no-build','--no-deps',p['service']])
  except Exception as e:print('Rollback failed for',p['name'],str(e),flush=True)
 raise
print('PASS all 12 runtime and asset services updated; state/log/credential mounts and security controls retained; only the three requested peer permissions added',flush=True)
