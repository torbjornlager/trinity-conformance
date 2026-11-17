from pathlib import Path
import json,subprocess,time,urllib.request,urllib.parse,secrets
name='localhost-n6-candidate';image='trinity-localhost-n6-dev2:20261105';rows=[]
def docker(*args):return subprocess.check_output(['docker',*args],text=True).strip()
try:
 docker('run','-d','--name',name,'--network','trinity_n6_host','-p','127.0.0.1::3060','--user','0:0','--read-only','--tmpfs','/tmp:size=128m,mode=1777','--cap-drop','ALL','--cap-add','KILL','--cap-add','SETGID','--cap-add','SETUID','--cap-add','SYS_CHROOT','--security-opt','no-new-privileges:true','--pids-limit','384','--memory','1g','--cpus','.75','-e','N6_PUBLIC_URL=https://n6.elfenbenstornet.se','-e','N6_PUBLIC_EXECUTION=yes','-e','N6_CONTAINMENT=yes','-e','N6_OWNER_NETWORK_PILOT=yes','-e','N6_ASSET_URL=http://n6_assets:3051',image)
 port=json.loads(docker('inspect',name))[0]['NetworkSettings']['Ports']['3060/tcp'][0]['HostPort'];base='http://127.0.0.1:'+port
 for _ in range(100):
  try:
   urllib.request.urlopen(base+'/healthz',timeout=.5).close();break
  except Exception:time.sleep(.1)
 else:raise RuntimeError('candidate readiness')
 with open('/tmp/localhost-contained-public.txt','w') as log:
  subprocess.run(['python3','tools/test_n6_public.py','--url',base,'--host','n6.elfenbenstornet.se'],cwd='/Users/lager/trinity-demonstrator',stdout=log,stderr=subprocess.STDOUT,check=True)
 pack=json.loads(Path('/Users/lager/trinity-conformance/cases/local-node-rpc-0.1.json').read_text())
 for case in pack['cases'][:5]:
  params=case['requests'][0]['params']
  req=urllib.request.Request(base+'/call?'+urllib.parse.urlencode(params),headers={'Host':'n6.elfenbenstornet.se','X-Web-Prolog-Query-Owner':secrets.token_hex(32)})
  with urllib.request.urlopen(req,timeout=8) as response:body=response.read().decode()
  ok=''.join(body.split())=='success([passed],false).';rows.append(dict(id=case['id'],status='pass' if ok else 'fail',body=body));print(case['id'],body.strip(),flush=True)
 for id,goal in [('REPORTED',"rpc(localhost,ancestor_descendant(X,Y),[src_uri('https://n2.elfenbenstornet.se')])"),('PROMISE-URI',"promise(localhost,ancestor_descendant(X,Y),R,[src_uri('https://n2.elfenbenstornet.se'),template(pair(X,Y)),once(true)]),yield(R,Answer)")]:
  req=urllib.request.Request(base+'/call?'+urllib.parse.urlencode(dict(goal=goal,format='json')),headers={'Host':'n6.elfenbenstornet.se','X-Web-Prolog-Query-Owner':secrets.token_hex(32)})
  with urllib.request.urlopen(req,timeout=8) as response:body=json.load(response)
  ok=body.get('type')=='success' and bool(body.get('data'));rows.append(dict(id=id,status='pass' if ok else 'fail',observation=body));print(id,json.dumps(body),flush=True)
 Path('/tmp/localhost-contained.json').write_text(json.dumps(dict(scope='real contained GNU worker, live broker, fixed local controller and pinned real N2 HTTPS source; disposable development image',image=image,results=rows,counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']}),indent=2)+'\n')
 assert all(r['status']=='pass' for r in rows),rows
finally:
 subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
