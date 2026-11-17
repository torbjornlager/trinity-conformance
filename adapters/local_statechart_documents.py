#!/usr/bin/env python3
import subprocess,os,time,socket,threading,json,http.server,hashlib,sys
from pathlib import Path
from local_manual_boundaries import provenance
import argparse
parser=argparse.ArgumentParser(description='Check caller-fetched statechart documents against disposable native nodes.')
parser.add_argument('--swi-root',required=True,type=Path)
parser.add_argument('--trealla-root',required=True,type=Path)
parser.add_argument('--swipl',required=True)
parser.add_argument('--tpl',required=True)
parser.add_argument('--output',required=True,type=Path)
parser.add_argument('--port-base',type=int,default=29260)
args=parser.parse_args()
if args.output.exists():parser.error('--output must be a new file')
args.output.parent.mkdir(parents=True,exist_ok=True)
swi=str(Path(args.swipl).resolve());tpl=str(Path(args.tpl).resolve());native=args.swi_root.resolve();trealla=args.trealla_root.resolve();node=str(native/'prolog/web_prolog.pl')
env=dict(os.environ,TPL_LIBRARY_PATH=str(Path(tpl).parent/'library'))
rows=[];hits=[];processes=[];baseport=args.port_base
root='<statechart version="0.2" initial="s"><state id="s"><go on="probe(To)">send(To,loaded)</go></state></statechart>'
parent='''<statechart version="0.2" initial="s"><state id="s"><go on="probe(To)">statechart_spawn(C,[src_uri('child.xml'),trace(false),link(true)]),send(C,probe(To))</go></state></statechart>'''
child='<statechart version="0.2" initial="s"><state id="s"><go on="probe(To)">send(To,child_loaded)</go></state></statechart>'

class Handler(http.server.BaseHTTPRequestHandler):
 def do_GET(self):
  hits.append(self.path);body={'/docs/root.xml':root,'/docs/parent.xml':parent,'/docs/child.xml':child}.get(self.path)
  if body is None:self.send_error(404);return
  self.send_response(200);self.end_headers();self.wfile.write(body.encode())
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();origin='http://127.0.0.1:'+str(server.server_port)
def atom(v):return "'"+str(v).replace("'","''")+"'"
policy=f"[load_uri_allowed_origins([{atom(origin)}]),load_uri_allowed_ip_ranges(['127.0.0.0/8'])]"
def prefix(kind,home):
 if kind=='swi':return f"use_module({atom(node)}),node:node({home},[profile(actor),auth(open),load_uri_allowed_origins([{atom(origin)}]),load_uri_allowed_ip_ranges(['127.0.0.0/8'])]),"
 return f"use_module(actors),use_module(distribution),use_module(statechart_actor),source_policy:configure_source_policy({policy},_),"
def command(kind,goal):return [swi,'-f','none','-q','-g',goal] if kind=='swi' else [tpl,'-g',goal]
def wait(p,port):
 for i in range(100):
  if p.poll() is not None:raise RuntimeError('node failed')
  try:
   with socket.create_connection(('127.0.0.1',port),timeout=.1):return
  except OSError:time.sleep(.1)
 raise RuntimeError('node readiness timeout')
def stop(p):
 p.terminate()
 try:p.wait(timeout=4)
 except subprocess.TimeoutExpired:p.kill();p.wait()
def run(kind,title,options,want,home):
 start=len(hits);t=time.monotonic();goal=prefix(kind,home)+f"(catch((statechart_spawn(P,[{options},trace(false),link(false),monitor(true)]),self(Self),{want},statechart_halt(P,true,3),receive({{down(P,P,_) -> true}},[timeout(3),on_timeout(fail)])),E,(writeq(E),nl,fail))->halt;halt(1))"
 try:
  p=subprocess.run(command(kind,goal),cwd=native if kind=='swi' else trealla,env=env,capture_output=True,text=True,timeout=25)
  ok=p.returncode==0;out=p.stdout;err=p.stderr
 except subprocess.TimeoutExpired as e:ok=False;out=str(e);err=''
 observed=hits[start:];expected=['/docs/parent.xml','/docs/child.xml'] if 'parent.xml' in options else ['/docs/root.xml']
 ok=ok and observed==expected
 rows.append(dict(candidate=kind,title=title,status='pass' if ok else 'fail',fetches=observed,expected_fetches=expected,stdout=out,stderr=err,duration_ms=round((time.monotonic()-t)*1000)))
 print(title,kind,rows[-1]['status'],observed,flush=True)
try:
 for kind in ['swi','trealla']:
  run(kind,'local document base',f"src_uri('{origin}/docs/parent.xml')","send(P,probe(Self)),receive({child_loaded->true},[timeout(5),on_timeout(throw(missing_relative_document))])",baseport+1)
 for dest in ['swi','trealla']:
  for allow in [False,True]:
   port=baseport+2;settings="[profile(actor),auth(open)"+(f",load_uri_allowed_origins([{atom(origin)}]),load_uri_allowed_ip_ranges(['127.0.0.0/8'])" if allow else '')+"]"
   goal=(f"use_module({atom(node)}),node:node({port},{settings}),thread_get_message(stop)" if dest=='swi' else f"consult('distribution.pl'),web_prolog:web_prolog_node({port},{settings}),thread_get_message(stop)")
   log=open(args.output.parent/('fixture-'+dest+'-'+str(allow)+'.log'),'w');p=subprocess.Popen(command(dest,goal),cwd=native if dest=='swi' else trealla,env=env,stdout=log,stderr=log);processes.append(p);wait(p,port)
   for kind in ['swi','trealla']:
    src='parent' if allow else 'root';want="send(P,probe(Self)),receive({child_loaded->true},[timeout(5),on_timeout(throw(missing_relative_document))])" if allow else 'send(P,probe(Self)),receive({loaded->true},[timeout(5),on_timeout(throw(missing_loaded))])'
    run(kind,('remote document base' if allow else 'caller fetch with destination source disabled')+' -> '+dest,f"node('http://localhost:{port}'),src_uri('{origin}/docs/{src}.xml')",want,baseport+3)
   stop(p);log.close()
finally:
 for p in processes:
  if p.poll() is None:stop(p)
 server.shutdown()
result=dict(scope='supporting disposable-node statechart document checks; no release certification',origin=origin,counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']},sources={'swi':provenance(native),'trealla':provenance(trealla)},executables={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in [swi,tpl]},runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),results=rows)
args.output.write_text(json.dumps(result,indent=2)+'\n');print(result['counts']);sys.exit(bool(result['counts']['fail']))
