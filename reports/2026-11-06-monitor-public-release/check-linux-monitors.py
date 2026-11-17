from pathlib import Path
import hashlib,json,subprocess,sys,time,socket,urllib.request
O=Path(__file__).resolve().parent;ROOT=O.parents[1];sys.path.insert(0,str(ROOT/'runner'))
from baseline import query_case
pack=json.loads((ROOT/'cases/monitor-contracts-0.1.json').read_text());rows=[]
def docker(*args):return subprocess.check_output(['docker',*args],text=True).strip()
for mode,image,entry,args in [
 ('swi','trinity-monitor-public-native:20261106','swipl',['-f','none','-q','-s','/app/load.pl','-g','node(3060,[profile(actor),auth(open),max_session_spawns_per_window(1000)]),thread_get_message(stop)']),
 ('trealla','trinity-monitor-public-n5:20261106','/opt/trealla/tpl',['-g','use_module(distribution),web_prolog:web_prolog_node(3060,[sandbox(blacklist),max_session_spawns_per_window(1000),max_call_requests_per_window(1000)])'])]:
 name='monitor-linux-'+mode
 try:
  docker('run','-d','--name',name,'-p','127.0.0.1::3060','--entrypoint',entry,image,*args)
  port=int(json.loads(docker('inspect',name))[0]['NetworkSettings']['Ports']['3060/tcp'][0]['HostPort'])
  for _ in range(200):
   try:
    with urllib.request.urlopen(f'http://127.0.0.1:{port}/healthz',timeout=.5) as response:
     assert response.status==200
     break
   except (OSError,AssertionError):time.sleep(.1)
  else:raise TimeoutError(mode+' readiness')
  for case in pack['cases']:
   row=dict(candidate=mode,id=case['id'])
   try:row.update(status='pass',observation=query_case(dict(case,source=pack['source']+'\n'+case.get('source','')),f'ws://127.0.0.1:{port}/ws',10,None))
   except Exception as e:row.update(status='fail',detail=str(e))
   rows.append(row);print(mode,case['id'],row['status'],flush=True)
 finally:
  (O/'linux-monitors.json').write_text(json.dumps(dict(suite=pack['suite'],scope='Actual committed-source Linux SWI and Trealla images, fresh ACTOR session per case',results=rows),indent=2)+'\n')
  (O/('linux-'+mode+'.txt')).write_text(docker('logs',name))
  subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
assert len(rows)==98 and all(r['status']=='pass' for r in rows)
print('PASS 98 Linux monitor assertions',flush=True)
