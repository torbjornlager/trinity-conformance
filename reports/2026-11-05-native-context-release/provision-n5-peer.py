"""Provision only the public N5 self-route token; never log token values.
N3/N4 routes keep their existing trusted private-Docker transport boundary.
"""
from pathlib import Path
import subprocess,json
O=Path(__file__).resolve().parent
name='deployment-wp_n5-1';volume='trinity-n5-peer-transport'
d=json.loads(subprocess.check_output(['docker','inspect',name],text=True))[0]
env=dict(x.split('=',1) for x in d['Config']['Env'] if '=' in x)
subprocess.run(['docker','volume','create',volume],check=True,stdout=subprocess.DEVNULL)
helper=r'''
import json,sys,urllib.request,os,re
from pathlib import Path
cfg=json.load(sys.stdin);base='http://wp_n5:3060';path=Path('/credentials/peers.pl')
headers={'Authorization':'Bearer '+cfg['admin'],'Content-Type':'application/json'}
def request(method,body=None):
 req=urllib.request.Request(base+'/admin/tokens',data=json.dumps(body).encode() if body else None,headers=headers,method=method)
 with urllib.request.urlopen(req,timeout=10) as r:return json.load(r)
if path.exists():
 text=path.read_text();match=re.fullmatch(r"\['https://n5\.elfenbenstornet\.se'-'(wp_[a-f0-9]+_[a-f0-9]+)'\]\.\s*",text)
 if not match:raise RuntimeError('Existing owner peer file has unexpected shape; preserved')
 token=match[1];id=token.split('_')[1]
 records=request('GET')['tokens']
 if not any(str(x['id'])==id and not x.get('revoked',False) for x in records):raise RuntimeError('Existing peer token is unavailable; owner file preserved')
 action='reused'
else:
 data=request('POST',{'principal':'node:n5-self-transport','capabilities':['execute','internal_transport'],'label':'Native retained-context release: N5 public self-route'})
 token=data['token'];id=data['id']
 if not re.fullmatch(r'wp_[a-f0-9]+_[a-f0-9]+',token):raise RuntimeError('Unexpected issued token format')
 temp=path.with_suffix('.tmp');temp.write_text("['https://n5.elfenbenstornet.se'-'"+token+"'].\n")
 os.chown(temp,10001,10001);os.chmod(temp,0o400);os.replace(temp,path);action='issued'
print(json.dumps({'status':action,'token_id':id,'peer_count':1,'destinations':['https://n5.elfenbenstornet.se'],'mode':'0400','owner_uid':10001,'incoming_store':'existing persistent N5 /state/tokens.pl','private_peer_routes':'N3/N4 unchanged trusted Docker transports'}))
'''
r=subprocess.run(['docker','run','--rm','-i','--network','deployment_wp_net','--user','0:0','-v',volume+':/credentials','--entrypoint','python3','trinity-native-context-native:20261105-context','-c',helper],input=json.dumps({'admin':env['WP_ADMIN_TOKEN']}),capture_output=True,text=True,check=True)
record=json.loads(r.stdout);record['volume']=volume
(O/'n5-peer-provisioning.json').write_text(json.dumps(record,indent=2)+'\n')
p=Path('/Users/lager/trinity-demonstrator/Deployment/.env');text=p.read_text();lines=text.splitlines();key='WP_N5_PEER_TOKENS_VOLUME'
lines=[line for line in lines if not line.startswith(key+'=')];lines.append(key+'='+volume);p.write_text('\n'.join(lines)+'\n')
print('PASS N5 persistent self-route credential provisioned in owner-only external volume; secrets not logged')
