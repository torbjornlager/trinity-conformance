import subprocess,pathlib,json,time,concurrent.futures
root=pathlib.Path('/work');out=root/'verified-stress';out.mkdir(exist_ok=False)
cases={'websocket':("consult('connection_stack_tests.pl'),connection_stack_tests:websocket_live(22143)",200),'remote':("consult('remote_demonitor_tests.pl'),remote_demonitor_tests:run",20),'isolation':("consult('tests.pl'),run_test_group(isolation)",10),'sandbox':("consult('tests.pl'),run_test_group(sandbox)",10),'synch':("consult('synchronous_toplevel_tests.pl'),synchronous_toplevel_tests:run",10)}
def series(names):
 for name in names:
  goal,count=cases[name]
  for i in range(count):
   start=time.monotonic()
   try:
    p=subprocess.run(['/opt/trealla/tpl','-g',f'(catch(({goal}),E,(writeq(E),nl,fail))->halt;halt(1))'],cwd=root/'final-sources/trealla',capture_output=True,text=True,timeout=30)
    r={'status':p.returncode,'output':p.stdout+p.stderr}
   except subprocess.TimeoutExpired as e:r={'status':'timeout','output':(e.stdout or b'').decode()+(e.stderr or b'').decode()}
   r.update(case=name,repetition=i,seconds=time.monotonic()-start);(out/f'{name}-{i}.json').write_text(json.dumps(r,indent=2))
   if r['status']!=0:print('FAIL',name,i,r,flush=True)
  print(name,count,'finished',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(series,[['websocket'],['remote'],['isolation','sandbox','synch']]))
rows=[json.loads(p.read_text()) for p in sorted(out.glob('*.json'))];(root/'verified-stress.json').write_text(json.dumps(rows,indent=2));raise SystemExit(any(r['status']!=0 for r in rows))
