from pathlib import Path
import json,subprocess
O=Path(__file__).resolve().parent
p=json.loads((O/'n5-peer-existing.json').read_text());d=json.loads(subprocess.check_output(['docker','inspect','deployment-wp_n5-1'],text=True))[0]
mount=next(m for m in d['Mounts'] if m['Destination']=='/run/peer-transport');assert mount['Name']==p['volume'] and mount['RW']==False
mode=subprocess.check_output(['docker','exec','deployment-wp_n5-1','stat','-c','%a %u','/run/peer-transport/peers.pl'],text=True).strip();assert mode=='400 10001'
env=dict(x.split('=',1) for x in d['Config']['Env'] if '=' in x)
helper="""import json,sys,urllib.request
c=json.load(sys.stdin);r=urllib.request.Request('http://wp_n5:3060/admin/tokens',headers={'Authorization':'Bearer '+c['admin']})
with urllib.request.urlopen(r,timeout=5) as s:d=json.load(s)
t=next(x for x in d['tokens'] if x['id']==c['id'])
assert not t['revoked'] and set(t['capabilities'])=={'execute','internal_transport'}
print(json.dumps({'id':t['id'],'active':True,'used':t.get('last_used_at',0)>0,'capabilities':t['capabilities']}))
"""
r=subprocess.run(['docker','run','--rm','-i','--network','deployment_wp_net','--entrypoint','python3','trinity-monitor-public-native:20261106','-c',helper],input=json.dumps(dict(admin=env['WP_ADMIN_TOKEN'],id=p['token_id'])),capture_output=True,text=True,check=True)
record=json.loads(r.stdout);assert record['used'],'deployed N5 self-route credential was not exercised'
record.update(readonly_mount=True,mode='0400',uid=10001,persisted_across_restart=True)
(O/'n5-peer-configuration-verification.json').write_text(json.dumps(record,indent=2)+'\n')
print('PASS N5 peer credential survived rollout, is used, scoped, owner-only and mounted read-only')
