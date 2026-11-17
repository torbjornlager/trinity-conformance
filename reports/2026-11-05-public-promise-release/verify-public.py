from pathlib import Path
import json,urllib.request,urllib.parse,hashlib,secrets,subprocess,time
O=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-demonstrator')
assert 'PASS all 12' in (O/'rollout.txt').read_text(),'complete rollout first'
expected=json.loads((R/'dependencies/swi-wasm-node.json').read_text());package=Path('/tmp/promise-release-browser-20261105')
expected_assets={url:hashlib.sha256((package/file).read_bytes()).hexdigest() for url,file in [('vendor/swi-wasm-node.js','web/vendor/swi-wasm-node.js'),('swi_wasm_actor_worker.js','web/swi_wasm_actor_worker.js')]}
checks=[]
def save():
 (O/'public-verification.json').write_text(json.dumps(dict(scope='public readiness, exact browser bytes and non-destructive RPC/promise checks',browser_revision=expected['revision'],counts={s:sum(x['status']==s for x in checks) for s in ['pass','fail']},results=checks),indent=2)+'\n')
def record(title,fn):
 try:obs=fn();row=dict(title=title,status='pass',observation=obs)
 except Exception as e:row=dict(title=title,status='fail',detail=str(e))
 checks.append(row);save();print(title,row['status'],flush=True)
 return row['status']=='pass'
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'Cache-Control':'no-cache'}),timeout=15) as response:return response.status,response.read()
def call(n,goal):
 time.sleep(1.5)
 q=dict(goal='once(('+goal+')),ReleaseCheck=passed',template='ReleaseCheck',format='prolog',limit=1)
 req=urllib.request.Request(f'https://n{n}.elfenbenstornet.se/call?'+urllib.parse.urlencode(q),headers={'X-Web-Prolog-Query-Owner':secrets.token_hex(32)})
 with urllib.request.urlopen(req,timeout=15) as response:body=response.read().decode();assert response.status==200
 assert ''.join(body.split())=='success([passed],false).',body
 return body
for n,profile in enumerate(['relation','isobase','isotope','actor','actor','actor','isobase']):
 def info(n=n,profile=profile):
  code,body=get(f'https://n{n}.elfenbenstornet.se/node_info');d=json.loads(body);assert code==200 and d['profile']==profile and d['auth']=='open';return dict(profile=d['profile'],auth=d['auth'])
 record(f'N{n} public readiness/profile',info)
 for path,digest in expected_assets.items():
  def asset(n=n,path=path,digest=digest):
   code,body=get(f'https://n{n}.elfenbenstornet.se/{path}?appendix_b={expected["revision"]}');sha=hashlib.sha256(body).hexdigest();assert code==200 and sha==digest,(code,sha);return sha
  record(f'N{n} exact browser asset {path}',asset)
for n in range(1,7):
 for peer in range(1,7):
  if n==6 and peer==6:continue
  goal=f"rpc('https://n{peer}.elfenbenstornet.se',X=ok,[http_timeout(2),request_header('X-Appendix-B'=['狐','狸']),user_agent(appendix_b)]),X==ok"
  record(f'N{n} -> N{peer} RPC with common HTTP fields',lambda n=n,goal=goal:call(n,goal))
for n in [1,5,6]:
 goal="promise('https://n1.elfenbenstornet.se',X=ok,Ref,[template(v(X)),http_timeout(2),request_header('X-Appendix-B'=[]),user_agent(appendix_b)]),yield(Ref,success([v(ok)],false)),var(X)"
 record(f'N{n} promise with common HTTP fields',lambda n=n,goal=goal:call(n,goal))
record('N6 pinned Host cannot be overridden',lambda:call(6,"catch((rpc('https://n1.elfenbenstornet.se',true,[request_header('Host'='unapproved.example')]),fail),error(outbound_denied,_),Caught=true),Caught==true"))
print('public checks',len(checks),'fail',sum(x['status']=='fail' for x in checks),flush=True)
raise SystemExit(any(x['status']=='fail' for x in checks))
