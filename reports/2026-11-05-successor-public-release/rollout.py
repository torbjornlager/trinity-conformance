from pathlib import Path
import subprocess,json,time,urllib.request,hashlib
O=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-demonstrator');name='deployment-wp_n5-1'
ci=json.loads((O/'consumer-ci/results.json').read_text());assert len(ci)==38 and all(r['exit_code']==0 for r in ci),'qualify consumer CI first'
candidate=json.loads((O/'candidate-n5-library.json').read_text());assert candidate['counts']=={'pass':311,'fail':0},candidate['counts']
old=next(r for r in json.loads((O/'before-services.json').read_text()) if r['name']==name);rev=(O/'consumer-revision.txt').read_text().strip();tag='deployment-wp_n5';image='trinity-successor-n5:20261105'
def run(cmd):return subprocess.check_output(cmd,cwd=R,text=True,stderr=subprocess.STDOUT).strip()
def inspect():return json.loads(run(['docker','inspect',name]))[0]
files=old['compose_files'].split(',');assert [Path(f).name for f in files]==['compose.yaml','compose.trealla-n5.yaml','compose.trealla-n5-public.yaml','compose.peer-transport-volumes.yaml','compose.gprolog-n6-caddy.yaml','compose.peer-transport-n5-volumes.yaml'],files
compose=['docker','compose','--env-file','Deployment/.env','-p','deployment']
for f in files:compose+=['-f',f]
assert inspect()['Image']==old['image_id'],'deployment changed since snapshot'
expected=run(['docker','image','inspect',image,'--format','{{.Id}}']);attempted=False
try:
 run(['docker','tag',image,tag]);attempted=True
 run(compose+['up','-d','--no-build','--no-deps','wp_n5'])
 for _ in range(90):
  d=inspect()
  if d['State']['Running'] and d['State'].get('Health',{}).get('Status')=='healthy':break
  time.sleep(1)
 else:raise RuntimeError('N5 readiness deadline exceeded')
 assert d['Image']==expected and d['Config']['Labels']['org.opencontainers.image.revision']==rev
 assert hashlib.sha256(json.dumps(sorted(d['Config']['Env'])).encode()).hexdigest()==old['environment_sha256']
 assert d['Config']['User']==old['user'] and d['Config']['Entrypoint']==old['entrypoint'] and d['Config']['Cmd']==old['command']
 assert {k:d['HostConfig'].get(k) for k in old['controls']}==old['controls']
 mounts=[{k:m.get(k) for k in ['Type','Name','Destination','RW']} for m in d['Mounts']]
 assert sorted(mounts,key=lambda m:m['Destination'])==sorted(old['mounts'],key=lambda m:m['Destination'])
 expected_pin=json.loads((R/'dependencies/trealla-port.json').read_text());pin=json.loads(run(['docker','exec',name,'cat','/usr/share/doc/trealla/runtime-pins.json']));assert pin==expected_pin
 sha=run(['docker','exec',name,'sha256sum','/app/integer_relations.pl']).split()[0];assert sha==hashlib.sha256(Path('/Users/lager/trealla-port/integer_relations.pl').read_bytes()).hexdigest()
 with urllib.request.urlopen('https://n5.elfenbenstornet.se/node_info',timeout=10) as response:assert response.status==200 and json.load(response)['profile']=='actor'
 rows=[]
 for before in json.loads((O/'before-services.json').read_text()):
  current=json.loads(run(['docker','inspect',before['name']]))[0]
  assert current['State']['Running']
  if before['name']!=name:assert current['Image']==before['image_id'],before['name']
  rows.append(dict(name=before['name'],image_id=current['Image'],changed=before['name']==name))
 (O/'rollout-results.json').write_text(json.dumps(dict(consumer_revision=rev,trealla_revision=pin['revision'],n5_image=expected,status='deployed',services=rows,environment_and_controls_unchanged=True,mounts_unchanged=True,integer_relation_sha256=sha),indent=2)+'\n')
 print('PASS N5 updated and healthy; exact pin/source verified; environment, controls and volumes unchanged; eleven other images unchanged',flush=True)
except BaseException:
 if attempted:
  run(['docker','tag',old['rollback_tag'],tag]);run(compose+['up','-d','--no-build','--no-deps','wp_n5'])
  print('Restored N5 rollback image after rollout validation failure',flush=True)
 raise
