from pathlib import Path
import subprocess,json,tempfile,secrets,urllib.request,urllib.parse
O=Path(__file__).resolve().parent
container='deployment-wp_n5-1'
def n5(method,body=None,id=None):
 d=json.loads(subprocess.check_output(['docker','inspect',container],text=True))[0];env=dict(x.split('=',1) for x in d['Config']['Env'] if '=' in x)
 helper="""import sys,json,urllib.request
c=json.load(sys.stdin);u='http://wp_n5:3060/admin/tokens'+(('?id='+c['id']) if c.get('id') else '')
r=urllib.request.Request(u,data=json.dumps(c['body']).encode() if c.get('body') else None,headers={'Authorization':'Bearer '+c['admin'],'Content-Type':'application/json'},method=c['method'])
with urllib.request.urlopen(r,timeout=10) as s:print(s.read().decode())
"""
 r=subprocess.run(['docker','run','--rm','-i','--network','deployment_wp_net','--entrypoint','python3','trinity-native-context-native:20261105-context','-c',helper],input=json.dumps(dict(admin=env['WP_ADMIN_TOKEN'],method=method,body=body,id=id)),capture_output=True,text=True,check=True)
 return json.loads(r.stdout)
def native(port,method,body=None,id=None):
 u=f'http://127.0.0.1:{port}/admin/tokens'+('?'+urllib.parse.urlencode(dict(id=id)) if id else '')
 q=urllib.request.Request(u,data=json.dumps(body).encode() if body else None,headers={'Content-Type':'application/json'},method=method)
 with urllib.request.urlopen(q,timeout=10) as r:return json.load(r)
issued=None
try:
 body=dict(principal='self-route-diagnostic-'+secrets.token_hex(6),capabilities=['execute'],expires_in=900,label='Temporary public self-route diagnostic')
 r=n5('POST',body);issued=r['id']
 (O/'credential-metadata.json').write_text(json.dumps(dict(id=issued,capabilities=['execute'],expiry_seconds=900),indent=2)+'\n')
 with tempfile.TemporaryDirectory(prefix='self-route-diagnostic-') as tmp:
  p=Path(tmp)/'credential.json';p.write_text(json.dumps(dict(token=r['token'])));p.chmod(0o600)
  result=subprocess.run(['python3',str(O.parents[1]/'adapters/public_promise_self_route.py'),'--url','https://n5.elfenbenstornet.se','--credentials-file',str(p),'--attempts','20','--output',str(O/'observations')])
  raise SystemExit(result.returncode)
finally:
 if issued:
  r=n5('DELETE',id=issued)
  (O/'credential-cleanup.json').write_text(json.dumps(dict(id=issued,revoked=r.get('revoked')==True),indent=2)+'\n')
