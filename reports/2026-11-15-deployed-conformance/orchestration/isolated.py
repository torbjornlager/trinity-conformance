from pathlib import Path
import json,subprocess,socket,time,secrets,os,tarfile,io,concurrent.futures,hashlib
os.umask(0o077);O=Path(__file__).parent;R=O/'conformance';net='trinity-conformance-'+secrets.token_hex(4);images={'swi-n134':'sha256:e80b9fdcd51648351a3f353eb46e33f6b6bc3e0270c5419d1f1571006a9c2366','swi-n2':'sha256:6008beb8ad14a65a43d492ed56b2d77ae0e92e99d8c24f482bcdfc087b392dfa','trealla-n5':'sha256:a3181f84d8f4637c42f1c410ea8f45afa25ab6232858f42c799c5f5b89362067'}
def docker(*a):return subprocess.check_output(['docker',*map(str,a)],stderr=subprocess.STDOUT)
def one(label,image):
 F=O/'isolated'/label;F.mkdir(parents=True);name=net+'-'+label;owned=False;row=dict(candidate=label,image=image)
 with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
 owner=secrets.token_hex(24);observer=secrets.token_hex(24)
 if label.startswith('swi'):
  source=":- consult('/opt/swi-prolog-node/load.pl').\n:- use_module(library(http/json)).\nmain :- set_setting(http:public_host,'127.0.0.1'),set_setting(http:public_port,"+str(port)+"),set_setting(http:public_scheme,http),node:node(3069,[profile(actor),sandbox(blacklist),auth(private)]),node_tokens:issue_token(conformance_owner,[execute],[],A),node_tokens:issue_token(conformance_observer,[execute],[],B),open('/tmp/conformance-creds.json',write,S),json_write_dict(S,_{owner:A,observer:B}),close(S),thread_get_message(stop).\n";cmd=['swipl','-f','none','-q','-s','/app/conformance-fixture.pl','-g','main','-t','halt']
 else:
  source=":- asserta(user:file_search_path(library,'/app')).\n:- use_module('/app/web_prolog.pl').\nmain :- web_prolog:web_prolog_node(3069,[bind_address('0.0.0.0'),node_url('http://127.0.0.1:"+str(port)+"'),profile(actor),sandbox(blacklist),auth(private),bearer_token(conformance_owner,'"+owner+"',[execute]),bearer_token(conformance_observer,'"+observer+"',[execute])]),thread_get_message(stop).\n";cmd=['/opt/trealla/tpl','-q','-f','/app/conformance-fixture.pl','-g','main']
 fixture=F/'fixture.private.pl';fixture.write_text(source);fixture.chmod(0o644)
 try:
  docker('create','--name',name,'--network',net,'--memory','768m','--cpus','1','--pids-limit','256','--no-healthcheck','-p',f'127.0.0.1:{port}:3069','--entrypoint','/usr/bin/env',image,*cmd);owned=True;docker('cp',fixture,name+':/app/conformance-fixture.pl');docker('start',name)
  deadline=time.monotonic()+25
  while True:
   if not json.loads(docker('inspect',name))[0]['State']['Running']:raise RuntimeError('fixture startup exited')
   try:
    if label.startswith('swi'):
     data=docker('cp',name+':/tmp/conformance-creds.json','-')
     with tarfile.open(fileobj=io.BytesIO(data)) as t:c=json.loads(t.extractfile(next(m for m in t if m.isfile())).read())
     owner=c['owner'];observer=c['observer']
    with socket.create_connection(('127.0.0.1',port),timeout=.2):pass
    break
   except Exception:
    if time.monotonic()>deadline:raise TimeoutError('fixture startup readiness')
    time.sleep(.1)
  env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','FIXTURE_OWNER_TOKEN':owner,'FIXTURE_OBSERVER_TOKEN':observer};out=F/'release'
  with (F/'release.log').open('wb') as f:p=subprocess.run(['python3',str(R/'runner/release.py'),'--ws-url',f'ws://127.0.0.1:{port}/ws','--candidate',label,'--token-env','FIXTURE_OWNER_TOKEN','--observer-token-env','FIXTURE_OBSERVER_TOKEN','--disposable-fixture','--output',str(out)],env=env,stdout=f,stderr=f,timeout=420)
  row.update(exit_code=p.returncode,summary=json.loads((out/'release-summary.json').read_text()),scope='Exact deployed image in disposable private node; two independent execution-only principals; default gate manifests/timeouts; no owner services or live proxy')
 except Exception as e:row.update(error=type(e).__name__+': '+str(e))
 finally:
  if owned:
   log=subprocess.run(['docker','logs',name],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout
   for token in [owner,observer]:log=log.replace(token.encode(),b'[REDACTED_FIXTURE_TOKEN]')
   (F/'node.private.log').write_bytes(log);subprocess.run(['docker','rm','-f','-v',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  row['cleanup_complete']=subprocess.run(['docker','inspect',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0;(F/'summary.json').write_text(json.dumps(row,indent=2)+'\n');print(label,'exit',row.get('exit_code'),'error',row.get('error'),'cleanup',row['cleanup_complete'],flush=True)
 return row
try:
 docker('network','create','--internal',net)
 with concurrent.futures.ThreadPoolExecutor(3) as pool:rows=list(pool.map(lambda kv:one(*kv),images.items()))
 (O/'isolated-summary.json').write_text(json.dumps(rows,indent=2)+'\n')
finally:subprocess.run(['docker','network','rm',net],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
