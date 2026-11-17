from pathlib import Path
import json,urllib.request,urllib.parse,hashlib,secrets,time,subprocess,sys
sys.dont_write_bytecode=True
from inventory import invariant
O=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-demonstrator');checks=[]
expected=json.loads((R/'dependencies/swi-wasm-node.json').read_text());package=O/'runtime'
def save(): (O/'public-verification.json').write_text(json.dumps(dict(browser_revision=expected['revision'],results=checks,counts={s:sum(r['status']==s for r in checks) for s in ['pass','fail']}),indent=2)+'\n')
def record(title,fn):
 try:row=dict(title=title,status='pass',observation=fn())
 except Exception as e:row=dict(title=title,status='fail',detail=str(e))
 checks.append(row);save();print(title,row['status'],flush=True)
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'Cache-Control':'no-cache'}),timeout=15) as r:return r.status,r.read()
for n,profile in enumerate(['relation','isobase','isotope','actor','actor','actor','isobase']):
 def info(n=n,profile=profile):
  code,body=get(f'https://n{n}.elfenbenstornet.se/node_info');d=json.loads(body);assert code==200 and d['profile']==profile and d['auth']=='open';return dict(profile=d['profile'],auth=d['auth'])
 record(f'N{n} readiness and profile',info)
 for path in ['swi_wasm_actor_worker.js','vendor/swi-wasm-node.js','wasm/statechart_wasm.pl','demonstrator.html']:
  sha=hashlib.sha256(((R if path=='demonstrator.html' else package)/'web'/path).read_bytes()).hexdigest()
  def asset(n=n,path=path,sha=sha):
   asset_path='demonstrator' if path=='demonstrator.html' else path
   code,body=get(f'https://n{n}.elfenbenstornet.se/{asset_path}?release={expected["revision"]}')
   served_sha=hashlib.sha256(body).hexdigest()
   if n==6 and path=='demonstrator.html':
    config=dict(remoteNodes=[dict(url=f'https://n{i}.elfenbenstornet.se',runtime='swi' if i<5 else 'trealla') for i in range(1,6)]+[dict(url='https://n6.elfenbenstornet.se',runtime='gprolog')],discoveryHubUrl='https://n0.elfenbenstornet.se/discovery-hub',ownerLogin=False,interactionLogging=False)
    bootstrap=('<script>window.WEB_PROLOG_HOST='+json.dumps(config)+';</script>\n').encode()
    assert body.count(bootstrap)==1,'expected GNU adapter bootstrap differs'
    body=body.replace(bootstrap,b'',1)
   got=hashlib.sha256(body).hexdigest();assert code==200 and got==sha,(code,got)
   return dict(source_sha256=got,served_sha256=served_sha,adapter_bootstrap_checked=n==6 and path=='demonstrator.html')
  record(f'N{n} exact asset {path}',asset)
def call(n,goal):
 time.sleep(0.25);fields={'goal':'once(('+goal+')),ReleaseCheck=passed','format':'json','limit':1}
 req=urllib.request.Request(f'https://n{n}.elfenbenstornet.se/call?'+urllib.parse.urlencode(fields),headers={'X-Web-Prolog-Query-Owner':secrets.token_hex(32)})
 with urllib.request.urlopen(req,timeout=15) as r:d=json.load(r)
 assert d['type']=='success' and d['data'][0]['ReleaseCheck']=='passed',d
 return d
for n in range(1,7):record(f'N{n} native query',lambda n=n:call(n,'member(X,[ok]),X==ok'))
for n,peer in [(3,4),(4,3),(5,4),(6,1)]:record(f'N{n} to N{peer} RPC',lambda n=n,peer=peer:call(n,f"rpc('https://n{peer}.elfenbenstornet.se',X=ok),X==ok"))
old={r['name']:r for r in json.loads((O/'rollback-inventory.json').read_text())};updates={r['name']:r for r in json.loads((O/'rollout-results.json').read_text())};services=[]
for name,p in old.items():
 d=json.loads(subprocess.check_output(['docker','inspect',name],text=True))[0]
 assert d['State']['Running'] and d['Image']==(updates[name]['image_id'] if name in updates else p['image_id']);assert invariant(d)==p['invariant']
 services.append(dict(name=name,image_id=d['Image'],updated=name in updates,running=True,configuration_preserved=True,health=d['State'].get('Health',{}).get('Status')))
(O/'running-services.json').write_text(json.dumps(services,indent=2)+'\n')
print('PASS configuration and image identity for all 16 services',flush=True)
raise SystemExit(any(r['status']=='fail' for r in checks))
