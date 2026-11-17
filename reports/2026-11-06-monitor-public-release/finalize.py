from pathlib import Path
import hashlib,json,subprocess
O=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-demonstrator')
old={x['name']:x for x in json.loads((O/'rollback-images.json').read_text())};deployed=json.loads((O/'rollout-results.json').read_text());assert len(deployed)==12
services=[]
for row in deployed:
 d=json.loads(subprocess.check_output(['docker','inspect',row['name']]))[0];before=old[row['name']]
 assert d['State']['Running'] and d['State'].get('Health',{}).get('Status') not in ['starting','unhealthy']
 assert d['Image']==row['image_id'] and d['Config']['Labels']['org.opencontainers.image.revision']==row['consumer_revision']
 assert hashlib.sha256(json.dumps(sorted(d['Config']['Env'])).encode()).hexdigest()==before['environment_sha256']
 assert d['Config']['User']==before['user'] and d['Config']['Entrypoint']==before['entrypoint'] and d['Config']['Cmd']==before['command']
 assert {k:d['HostConfig'].get(k) for k in before['controls']}==before['controls']
 assert sorted([{'name':m.get('Name'),'destination':m['Destination']} for m in d['Mounts']],key=lambda m:m['destination'])==sorted(before['volumes'],key=lambda m:m['destination'])
 services.append(dict(name=row['name'],image_id=d['Image'],running=True,health=d['State'].get('Health',{}).get('Status','HTTP readiness checked'),configuration_preserved=True))
counts={}
for label,file,count in [('monitors','public-monitors.json',147),('browser','public-browser.json',42),('readiness_assets_rpc','public-verification.json',60)]:
 data=json.loads((O/file).read_text());rows=data['results'];assert len(rows)==count and all(x['status']=='pass' for x in rows);counts[label]=dict(pass_count=count,fail_count=0)
ctx=json.loads((O/'public-contexts/results.json').read_text())
assert len(ctx['results'])==51 and ctx['counts']=={'pass':50,'fail':1,'blocked':0,'error':0}
failure=next(r for r in ctx['results'] if r['status']!='pass');assert failure['id']=='CTX-015-trealla-b' and '502' in json.dumps(failure)
counts['retained_contexts']=ctx['counts']
ping=json.loads((O/'public-pingpong.json').read_text());assert len(ping['results'])==3 and all(r['status']=='pass' for r in ping['results']);counts['pingpong']=dict(pass_count=3,fail_count=0)
cleanup=[]
for file in ['monitor-ephemeral-credential-cleanup.json','short-wait-ephemeral-credential-cleanup.json','ephemeral-credential-cleanup.json']:
 rows=json.loads((O/file).read_text());assert len(rows)==3 and all(x['revoked'] for x in rows);cleanup+=rows
assert len({(r['node_port'],r['id']) for r in cleanup})==9
pins={n:json.loads((R/'dependencies'/f'{n}.json').read_text()) for n in ['swi-prolog-node','swi-wasm-node','trealla-port','gprolog-port']}
result=dict(status='deployed_with_transport_followup',consumer_image_revision=deployed[0]['consumer_revision'],runtime_pins=pins,services=services,public_checks=counts,selected_public_passes=302,selected_public_failures=1,temporary_credentials_revoked=9,source_spawn_policy_unchanged=True,open_issues=[dict(case='CTX-015-trealla-b',summary='N5 self-route promise owner received an HTTP 502 transport error; original short-wait timeout and bounded-retry error are retained. No production deadlines or admission policies changed.',evidence='public-contexts/results.json')])
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS twelve running services and preserved configuration; 302 selected public passes, one retained N5 self-route transport failure; nine temporary credentials revoked')
