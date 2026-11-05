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
issued=[];tokens={};metadata=[]
try:
 for name,port in [('swi-a',3053),('swi-b',3055),('trealla-a',None)]:
  body=dict(principal='context-release-verification-'+secrets.token_hex(6),capabilities=['execute'],expires_in=1800,label='Temporary retained-context release probe')
  r=native(port,'POST',body) if port else n5('POST',body)
  tokens[name]=r['token'];issued.append((port,r['id']));metadata.append(dict(candidate=name,id=r['id'],capabilities=['execute'],expiry_seconds=1800))
 tokens['trealla-b']=tokens['trealla-a'];tokens['swi-c']=tokens['swi-b']
 (O/'ephemeral-test-credentials.json').write_text(json.dumps(metadata,indent=2)+'\n')
 with tempfile.TemporaryDirectory(prefix='context-public-credentials-') as tmp:
  p=Path(tmp)/'credentials.json';p.write_text(json.dumps(tokens));p.chmod(0o600)
  cmd=['python3',str(O/'check-context-public.py'),'--credentials-file',str(p),'--swipl','/usr/local/bin/swipl','--tpl','/Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl','--swi-root','/Users/lager/swi-prolog-node','--trealla-root','/Users/lager/trealla-port','--output',str(O/'public-contexts'),'--routes','swi-a:swi-b','swi-a:trealla-b','trealla-a:swi-b','trealla-a:trealla-b']
  result=subprocess.run(cmd)
  if result.returncode:raise SystemExit(result.returncode)
  observed=json.loads((O/'public-contexts/results.json').read_text());assert observed['counts']=={'pass':51,'fail':0,'blocked':0,'error':0},observed['counts']
  assert len(observed['results'])==51 and all(r['status']=='pass' for r in observed['results'])
  subprocess.run(['python3',str(O/'check-policy-denials.py'),'--credentials-file',str(p),'--output',str(O/'public-policy-denials.json')],check=True)
finally:
 cleanup=[]
 for port,id in issued:
  try:
   r=native(port,'DELETE',id=id) if port else n5('DELETE',id=id);cleanup.append(dict(node_port=port,id=id,revoked=r.get('revoked')==True))
  except Exception as e:cleanup.append(dict(node_port=port,id=id,revoked=False,error=type(e).__name__))
 (O/'ephemeral-credential-cleanup.json').write_text(json.dumps(cleanup,indent=2)+'\n')
