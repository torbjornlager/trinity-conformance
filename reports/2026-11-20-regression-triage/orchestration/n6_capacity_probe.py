from pathlib import Path
import subprocess,os,time,socket,json,urllib.request,urllib.parse,urllib.error
O=Path('/work/results');O.mkdir();url='http://127.0.0.1:3069';Path('/tmp/fixture-policy').write_text('http 127.0.0.1 3069 127.0.0.1\n');Path('/tmp/fixture-policy').chmod(0o600);token='f'*64;Path('/tmp/fixture-token').write_text(token+'\n');Path('/tmp/fixture-token').chmod(0o600);headers={'Authorization':'Bearer '+token,'X-Web-Prolog-Query-Owner':'a'*64,'X-Web-Prolog-Query-Budget':'b'*64}
goal='(findall(X,rpc(localhost,member(X,[a,b]),[limit(1)]),[a,b])),LocalNodeCheck=passed';rows=[]
def call(goal,template,limit=1):
 req=urllib.request.Request(url+'/call?'+urllib.parse.urlencode(dict(goal=goal,template=template,format='prolog',limit=limit)),headers=headers)
 try:r=urllib.request.urlopen(req,timeout=8)
 except urllib.error.HTTPError as e:r=e
 with r:return dict(http_status=r.status,body=r.read().decode())
for label,held in [('clean',0),('three_owned_queries',3),('four_owned_queries',4)]:
 log=(O/(label+'.log')).open('w');proc=subprocess.Popen(['/app/isobase/isobase-node','--auth-token-file','/tmp/fixture-token','--port','3069','--max-queries','8','--max-owner-queries','4','--max-budget-queries','6','--require-query-owner','1','--require-query-budget','1','--idle-ms','300000','--time-ms','2000'],cwd='/app/isobase',env=dict(os.environ,ISO_OUTBOUND_POLICY='/tmp/fixture-policy'),stdout=log,stderr=log)
 try:
  for _ in range(100):
   if proc.poll() is not None:raise RuntimeError('Controller startup failed')
   try:
    with socket.create_connection(('127.0.0.1',3069),timeout=.1):break
   except OSError:time.sleep(.05)
  holds=[call('member(X,[a,b]),Fixture='+str(i),'X') for i in range(held)]
  observed=call(goal,'LocalNodeCheck');row=dict(scenario=label,held_queries=held,holds=holds,observed=observed);rows.append(row);print(row,flush=True)
 finally:
  proc.terminate()
  try:proc.wait(timeout=3)
  except subprocess.TimeoutExpired:proc.kill();proc.wait()
  log.close()
(O/'results.json').write_text(json.dumps(dict(scope='Owned uncontained controller diagnostic from deployed N6 image; same8global4owner6budget limits; explicit test-only loopback grant; no live configuration change',results=rows),indent=2)+'\n')
