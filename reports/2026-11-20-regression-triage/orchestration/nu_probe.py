from pathlib import Path
import json,sys,subprocess,time,socket,collections,hashlib
R=Path('/work/suite');sys.path[:0]=[str(R/'runner'),str(R/'adapters')];import node_uri_io
label=sys.argv[1];count=int(sys.argv[2]);out=Path('/work/results');out.mkdir();pack=json.loads((R/'cases/node-uri-io-0.1.json').read_text());case=next(c for c in pack['cases'] if c['id']=='NU-003');source=(R/pack['source_file']).read_text();url='http://127.0.0.1:3069';goal=case['goal'].replace('$SELF_SLASH',node_uri_io.prolog_quote_atom(url+'/'))
start="consult('/opt/swi-prolog-node/load.pl'),set_setting(http:public_host,'127.0.0.1'),set_setting(http:public_port,3069),set_setting(http:public_scheme,http),node:node(3069,[profile(actor),sandbox(blacklist),auth(open),max_call_requests_per_window(100000),max_session_spawns_per_window(100000),max_ws_commands_per_window(100000)]),thread_get_message(stop)"
log=(out/'node.log').open('w');proc=subprocess.Popen(['swipl','-f','none','-q','-g',start,'-t','halt'],cwd='/opt/swi-prolog-node',stdout=log,stderr=subprocess.STDOUT);rows=[]
try:
 for _ in range(200):
  if proc.poll() is not None:raise RuntimeError('Fixture startup failed')
  try:
   with socket.create_connection(('127.0.0.1',3069),timeout=.1):break
  except OSError:time.sleep(.05)
 for index in range(count):
  row=dict(trial=index+1)
  try:row.update(status='pass',observation=node_uri_io.query(url.replace('http:','ws:')+'/ws',source,goal,case,5))
  except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
  rows.append(row)
  if (index+1)%25==0 or row['status']=='fail':
   data=dict(revision_label=label,case='NU-003',unmodified_assertion=True,manifest_sha256=hashlib.sha256((R/'cases/node-uri-io-0.1.json').read_bytes()).hexdigest(),completed=len(rows),counts=dict(collections.Counter(r['status'] for r in rows)),results=rows);(out/'results.json').write_text(json.dumps(data,indent=2)+'\n');print(label,len(rows),data['counts'],flush=True)
finally:
 proc.terminate()
 try:proc.wait(timeout=3)
 except subprocess.TimeoutExpired:proc.kill();proc.wait()
 log.close()
