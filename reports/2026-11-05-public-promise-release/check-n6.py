from pathlib import Path
import subprocess,json,time,urllib.request,urllib.parse,secrets
O=Path(__file__).resolve().parent;name='promise-release-n6-candidate'
def run(*args):return subprocess.check_output(['docker',*args],text=True).strip()
try:
 run('run','-d','--name',name,'--network','trinity_n6_host','-p','127.0.0.1::3060','--user','0:0','--read-only','--tmpfs','/tmp:size=128m,mode=1777','--cap-drop','ALL','--cap-add','KILL','--cap-add','SETGID','--cap-add','SETUID','--cap-add','SYS_CHROOT','--security-opt','no-new-privileges:true','--pids-limit','384','--memory','1g','--cpus','.75','-e','N6_PUBLIC_URL=https://n6.elfenbenstornet.se','-e','N6_PUBLIC_EXECUTION=yes','-e','N6_CONTAINMENT=yes','-e','N6_OWNER_NETWORK_PILOT=yes','-e','N6_ASSET_URL=http://n6_assets:3051','trinity-promise-n6:20261105')
 port=json.loads(run('inspect',name))[0]['NetworkSettings']['Ports']['3060/tcp'][0]['HostPort'];url='http://127.0.0.1:'+port
 for _ in range(100):
  try:
   with urllib.request.urlopen(url+'/healthz',timeout=1):break
  except Exception:time.sleep(.1)
 else:raise TimeoutError('candidate readiness')
 for label,args in [('public',['tools/test_n6_public.py','--url',url,'--host','n6.elfenbenstornet.se']),('fields',[str(O/'check-fields.py'),'--url',url,'--host','n6.elfenbenstornet.se','--node','candidate-n6','--output',str(O/'candidate-n6-fields.json')])]:
  with (O/('candidate-n6-'+label+'.log')).open('w') as log:p=subprocess.run(['python3',*args],cwd='/Users/lager/trinity-demonstrator',stdout=log,stderr=subprocess.STDOUT)
  if p.returncode:raise RuntimeError(label+' failed')
 checks=["rpc('https://n1.elfenbenstornet.se',X=ok,[http_timeout(2),request_header('X-Release'=['狐','狸']),user_agent([a,p,p])]),X==ok", "promise('https://n1.elfenbenstornet.se',X=ok,Ref,[template(v(X)),http_timeout(2),request_header('X-Release'=[]),user_agent(appendix)]),yield(Ref,success([v(ok)],false))", "catch((rpc('https://n1.elfenbenstornet.se',true,[request_header('Host'='unapproved.example')]),fail),error(outbound_denied,_),Caught=true),Caught==true"]
 rows=[]
 for goal in checks:
  query=dict(goal='('+goal+'),ReleaseCheck=passed',template='ReleaseCheck',format='prolog')
  req=urllib.request.Request(url+'/call?'+urllib.parse.urlencode(query),headers={'Host':'n6.elfenbenstornet.se','X-Web-Prolog-Query-Owner':secrets.token_hex(32)})
  with urllib.request.urlopen(req,timeout=10) as response:body=response.read().decode()
  ok=''.join(body.split())=='success([passed],false).';rows.append(dict(goal=goal,body=body,status='pass' if ok else 'fail'))
  assert ok,body
 (O/'candidate-n6-worker-broker.json').write_text(json.dumps(dict(scope='actual contained GNU worker to broker to approved TLS peer; custom fields and pinned Host policy',results=rows),indent=2)+'\n')
 print('PASS N6 candidate: public contract, 59 shared field assertions, actual worker/broker custom fields and Host policy',flush=True)
finally:
 subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
