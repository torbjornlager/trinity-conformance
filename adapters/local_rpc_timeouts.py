#!/usr/bin/env python3
"""Supporting RPC timeout checks with disposable HTTP peers and execution nodes."""
import argparse,hashlib,http.server,json,os,select,socket,subprocess,tempfile,threading,time,urllib.parse
from pathlib import Path
import sys
from local_manual_boundaries import provenance
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--swi-root',type=Path,required=True);parser.add_argument('--trealla-root',type=Path,required=True);parser.add_argument('--gnu-root',type=Path,required=True)
parser.add_argument('--swipl',required=True);parser.add_argument('--tpl',required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--port-base',type=int,default=29460)
a=parser.parse_args()
if a.output.exists():parser.error('--output must be a new file')
a.output.parent.mkdir(parents=True,exist_ok=True)
roots={'swi':a.swi_root.resolve(),'trealla':a.trealla_root.resolve(),'gnu':a.gnu_root.resolve()};swi=str(Path(a.swipl).resolve());tpl=str(Path(a.tpl).resolve());gnu=str(roots['gnu']/'isobase/query-worker');node=roots['swi']/'prolog/web_prolog.pl'
requests=[];results=[];processes=[]
class Peer(http.server.BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  path=urllib.parse.urlsplit(self.path);fields=urllib.parse.parse_qs(path.query)
  requests.append({'path':path.path,'query':fields})
  mode=path.path
  for tag in ['headers','body','drip','pages','resource']:
   if 'fixture_'+tag in fields.get('goal',[''])[0]:mode='/'+tag+'/call'
  if path.path=='/source.pl':time.sleep(.25);body=b'helper(ok).\n'
  elif mode.startswith('/resource/'):body=b'error(error(resource_error(time),fixture)).\n'
  elif mode.startswith('/pages/'):
   time.sleep(.06);body=b'success([v(a)],true).\n' if fields.get('offset')==['0'] else b'success([v(b)],false).\n'
  else:body=b'success([v(ok)],false).\n'
  try:
   if mode.startswith('/headers/'):time.sleep(.6)
   self.send_response(200);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.flush()
   if mode.startswith('/body/'):time.sleep(.6)
   if mode.startswith('/drip/'):
    for byte in body:self.wfile.write(bytes([byte]));self.wfile.flush();time.sleep(.025)
   else:self.wfile.write(body)
  except (BrokenPipeError,ConnectionResetError):pass
peer=http.server.ThreadingHTTPServer(('127.0.0.1',0),Peer);threading.Thread(target=peer.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{peer.server_port}'
def atom(value):return "'"+str(value).replace("'","''")+"'"
def cmd(kind,goal):
 if kind=='swi':return [swi,'-f','none','-q','-g',f'use_module({atom(node)}),(catch(({goal}),E,(writeq(E),nl,fail))->halt;halt(1))']
 if kind=='trealla':return [tpl,'-g',f"use_module(actors),use_module(rpc),source_policy:configure_source_policy([load_uri_allowed_origins([{atom(base)}]),load_uri_allowed_ip_ranges(['127.0.0.0/8'])],_),(catch(({goal}),E,(writeq(E),nl,fail))->halt;halt(1))"]
 return [gnu,'query(('+goal+'),ok)','100']
def run(kind,title,goal,check=None):
 start=time.monotonic();first=len(requests)
 if kind!='gnu' and 'whole-request deadline:' in title:
  goal='findall(S,stream_property(S,mode(_)),StreamsBefore),('+goal+'),findall(S,stream_property(S,mode(_)),StreamsAfter),sort(StreamsBefore,Sorted),sort(StreamsAfter,Sorted)'
 try:
  p=subprocess.run(cmd(kind,goal),cwd=roots[kind] if kind!='gnu' else roots[kind]/'isobase',env=env,capture_output=True,text=True,input='',timeout=8)
  ok=p.returncode==0
  if kind=='gnu':ok=ok and [json.loads(x) for x in p.stdout.splitlines()]==[{'type':'success','answers':['ok'],'more':False}]
  observed=requests[first:];ok=ok and (check(observed) if check else True)
  if 'whole-request deadline:' in title:ok=ok and time.monotonic()-start<.5
  row=dict(candidate=kind,title=title,status='pass' if ok else 'fail',stdout=p.stdout,stderr=p.stderr,requests=observed,duration_ms=round((time.monotonic()-start)*1000))
 except subprocess.TimeoutExpired as e:row=dict(candidate=kind,title=title,status='fail',detail='client exceeded 8 seconds',requests=requests[first:])
 results.append(row);print(kind,title,row['status'],flush=True)
def wait(p,port):
 for _ in range(100):
  if p.poll() is not None:raise RuntimeError('fixture terminated')
  try:
   with socket.create_connection(('127.0.0.1',port),timeout=.1):return
  except OSError:time.sleep(.05)
 raise RuntimeError('fixture startup deadline')
def stop(p):
 p.terminate()
 try:p.wait(timeout=3)
 except subprocess.TimeoutExpired:p.kill();p.wait()
with tempfile.TemporaryDirectory(prefix='rpc-timeout-policy-') as td:
 policy=Path(td)/'policy';policy.touch(mode=0o600)
 env=dict(os.environ,TPL_LIBRARY_PATH=str(Path(tpl).parent/'library'),ISO_OUTBOUND_POLICY=str(policy))
 def allow(url):
  u=urllib.parse.urlsplit(url)
  rule=f'{u.scheme} {u.hostname} {u.port} 127.0.0.1\n'
  if rule not in policy.read_text().splitlines(keepends=True):
   with policy.open('a') as out:out.write(rule)
 allow(base)
 try:
  for kind in roots:
   fast=atom(base+'/fast')
   run(kind,'execution/HTTP limits are independent and first wins',f'rpc({fast},X=ok,[timeout(0.7),timeout(0.9),http_timeout(1),http_timeout(0)]),X==ok',lambda rs:len(rs)==1 and float(rs[0]['query'].get('timeout',['nan'])[0])==0.7 and 'http_timeout' not in rs[0]['query'])
   run(kind,'promise execution timeout is normalized and forwarded',f'promise({fast},X=ok,R,[template(v(X)),timeout(-3),timeout(4),http_timeout(1),http_timeout(0)]),yield(R,success([v(ok)],false)),var(X)',lambda rs:len(rs)==1 and rs[0]['query'].get('timeout')==['0'])
   run(kind,'node URI path prefix is retained',f'rpc({atom(base+"/prefix/")},X=ok,[http_timeout(1)]),X==ok',lambda rs:len(rs)==1 and rs[0]['path']=='/prefix/call')
   run(kind,'omission leaves execution timeout unspecified',f'rpc({fast},X=ok),X==ok',lambda rs:len(rs)==1 and 'timeout' not in rs[0]['query'])
   run(kind,'values above 300 seconds are accepted',f'rpc({fast},X=ok,[timeout(301),http_timeout(301)]),X==ok',lambda rs:len(rs)==1 and rs[0]['query'].get('timeout')==['301'])
   run(kind,'negative HTTP limit is immediate transport timeout',f'catch((rpc({fast},true,[http_timeout(-2)]),fail),error(rpc_error(http_timeout),_),Caught=true),Caught==true',lambda rs:not rs)
   run(kind,'zero HTTP promise yields transport error answer',f'promise({fast},X=ok,R,[template(v(X)),http_timeout(0)]),yield(R,error(error(rpc_error(http_timeout),_))),var(X)',lambda rs:not rs)
   for phase in ['headers','body','drip']:
    url=atom(base+'/'+phase)
    run(kind,'RPC whole-request deadline: '+phase,f'catch((rpc({url},fixture_{phase}(X),[http_timeout(0.1)]),fail),error(rpc_error(http_timeout),_),Caught=true),Caught==true,var(X),rpc({fast},Y=ok),Y==ok')
    run(kind,'promise whole-request deadline: '+phase,f'promise({url},fixture_{phase}(X),R,[template(v(X)),http_timeout(0.1)]),yield(R,error(error(rpc_error(http_timeout),_)),[timeout(2)]),var(X),rpc({fast},Y=ok),Y==ok')
   run(kind,'each page gets its own HTTP deadline',f'findall(X,rpc({atom(base+"/pages")},fixture_pages(X),[limit(1),http_timeout(0.1)]),[a,b])',lambda rs:len(rs)==2)
   run(kind,'source fetching is independent of HTTP request deadline',f'rpc({fast},helper(X),[src_uri({atom(base+"/source.pl")}),http_timeout(0.08)]),X==ok',lambda rs:len(rs)==2 and rs[0]['path']=='/source.pl' and rs[1]['path'].endswith('/call'))
   resource=atom(base+'/resource')
   run(kind,'remote execution errors are propagated unchanged',f'catch((rpc({resource},fixture_resource,[timeout(0.2),http_timeout(1)]),fail),error(resource_error(time),fixture),Caught=true),Caught==true')
   run(kind,'promises preserve remote execution error answers',f'promise({resource},fixture_resource,R,[timeout(0.2),http_timeout(1)]),yield(R,error(error(resource_error(time),fixture)))')
  for dest in roots:
   port=a.port_base;out=(a.output.parent/('node-'+dest+'.log')).open('w')
   if dest=='swi':argv=[swi,'-f','none','-q','-g',f'use_module({atom(node)}),node:node({port},[profile(isobase),auth(open),timeout(0.3)]),thread_get_message(stop)']
   elif dest=='trealla':argv=[tpl,'-g',f"consult('distribution.pl'),web_prolog:web_prolog_node({port},[profile(isobase),auth(open),time_limit(0.3)]),thread_get_message(stop)"]
   else:argv=[str(roots['gnu']/'isobase/isobase-node'),'--port',str(port),'--auth','open','--time-ms','300']
   p=subprocess.Popen(argv,cwd=roots[dest] if dest!='gnu' else roots[dest]/'isobase',env=env,stdout=out,stderr=out);processes.append(p);wait(p,port);url=f'http://127.0.0.1:{port}';allow(url)
   for kind in roots:
    for seconds in [.03,1]:
     run(kind,f'execution limit {seconds}s and owner clamp -> '+dest,f'catch((rpc({atom(url)},(repeat,fail),[timeout({seconds}),http_timeout(2)]),fail),error(resource_error(time),_),Caught=true),Caught==true')
    run(kind,'promise execution limit -> '+dest,f'promise({atom(url)},(repeat,fail),R,[timeout(0.03),http_timeout(2)]),yield(R,error(error(resource_error(time),_)))')
   if dest=='gnu':
    for kind in roots:
     run(kind,'application exception resembling old deadline marker stays unchanged -> gnu',f'catch((rpc({atom(url)},throw(time_limit_exceeded),[http_timeout(2)]),fail),time_limit_exceeded,Caught=true),Caught==true')
   stop(p);out.close()
 finally:
  for p in processes:
   if p.poll() is None:stop(p)
  peer.shutdown()
report=dict(scope='supporting HTTP deadline and execution-timeout checks; disposable fixtures, no profile certification',sources={k:provenance(v) for k,v in roots.items()},executables={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in [swi,tpl,gnu]},runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),counts={s:sum(r['status']==s for r in results) for s in ['pass','fail']},results=results)
a.output.write_text(json.dumps(report,indent=2)+'\n');print(report['counts']);sys.exit(bool(report['counts']['fail']))
