#!/usr/bin/env python3
"""Supporting HTTP field checks with a disposable echo peer."""
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
  requests.append({'path':path.path,'query':fields,'headers':list(self.headers.items())})
  if path.path=='/source.pl':body=b'helper(ok).\n'
  elif 'fixture_pages' in fields.get('goal',[''])[0]:body=b'success([v(a)],true).\n' if fields.get('offset')==['0'] else b'success([v(b)],false).\n'
  else:body=b'success([v(ok)],false).\n'
  self.send_response(200);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
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

def header(rs,name,value):
 return bool(rs) and all([v for k,v in r['headers'] if k.lower()==name]==[value] for r in rs)
with tempfile.TemporaryDirectory(prefix='http-options-policy-') as td:
 policy=Path(td)/'policy';policy.write_text(f'http 127.0.0.1 {peer.server_port} 127.0.0.1\n');policy.chmod(0o600)
 env=dict(os.environ,TPL_LIBRARY_PATH=str(Path(tpl).parent/'library'),ISO_OUTBOUND_POLICY=str(policy))
 try:
  for kind in roots:
   uri=atom(base)
   for value,expected in [('value','value'),('[v,a,l,u,e]','value'),('[]',''),("['狐','狸']",'狐狸'.encode('utf-8').decode('latin1')),('"value"','value'),("'räv'",'rÃ¤v'),("'狐狸'",'狐狸'.encode('utf-8').decode('latin1'))]:
    run(kind,'text header representation '+value,f'rpc({uri},X=ok,[request_header(\'X-Test\'={value})]),X==ok',lambda rs,e=expected:header(rs,'x-test',e))
   for auth,expected in [('basic(user,password)','Basic dXNlcjpwYXNzd29yZA=='),('basic([u,s,e,r],"password")','Basic dXNlcjpwYXNzd29yZA=='),("basic('räv','päss')",'Basic csOkdjpww6Rzcw=='),('bearer(token)','Bearer token')]:
    run(kind,'RPC authorization '+auth,f'rpc({uri},X=ok,[authorization({auth})]),X==ok',lambda rs,e=expected:header(rs,'authorization',e))
    run(kind,'promise authorization '+auth,f'promise({uri},X=ok,R,[template(v(X)),authorization({auth})]),yield(R,success([v(ok)],false)),var(X)',lambda rs,e=expected:header(rs,'authorization',e))
   run(kind,'case-insensitive first-field precedence on every RPC page',f"findall(X,rpc({uri},fixture_pages(X),[limit(1),request_header('X-Test'=first),request_header('x-test'=later),user_agent(agent),request_header('User-Agent'=later),authorization(bearer(first)),request_header('Authorization'=later)]),[a,b])",lambda rs:len(rs)==2 and header(rs,'x-test','first') and header(rs,'authorization','Bearer first') and header(rs,'user-agent','agent'))
   run(kind,'explicit fields precede aliases in promise',f"promise({uri},X=ok,R,[template(v(X)),request_header('Authorization'='Custom first'),authorization(bearer(later)),request_header('User-Agent'=first),user_agent(later)]),yield(R,success([v(ok)],false))",lambda rs:header(rs,'authorization','Custom first') and header(rs,'user-agent','first'))
   run(kind,'explicit empty field',f"rpc({uri},X=ok,[request_header('X-Empty'='')]),X==ok",lambda rs:header(rs,'x-empty',''))
   run(kind,'caller retains explicit opaque query owner',f"rpc({uri},X=ok,[request_header('X-Web-Prolog-Query-Owner'='{('a'*64)}')]),X==ok",lambda rs:header(rs,'x-web-prolog-query-owner','a'*64))
   run(kind,'RPC fields never reach source fetching',f"rpc({uri},helper(X),[src_uri({atom(base+'/source.pl')}),request_header('X-Test'=rpc_only),authorization(bearer(secret)),user_agent(rpc_agent)]),X==ok",lambda rs:len(rs)==2 and rs[0]['path']=='/source.pl' and not any(k.lower() in ['x-test','authorization'] for k,v in rs[0]['headers']) and not header(rs[:1],'user-agent','rpc_agent') and header(rs[1:],'authorization','Bearer secret'))
   for kindcall in ['rpc','promise']:
    call=f'rpc({uri},true,Options)' if kindcall=='rpc' else f'promise({uri},true,R,Options)'
    run(kind,kindcall+' validates later duplicate before source fetch',f"Options=[src_uri({atom(base+'/source.pl')}),request_header(x=first),request_header(x=42)],catch(({call},fail),error(type_error(atom_or_string,42),_),Caught=true),Caught==true,var(R)",lambda rs:not rs)
 finally:peer.shutdown()
report=dict(scope='supporting HTTP field checks; disposable peer, no profile certification',sources={k:provenance(v) for k,v in roots.items()},executables={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in [swi,tpl,gnu]},runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),counts={s:sum(r['status']==s for r in results) for s in ['pass','fail']},results=results)
a.output.write_text(json.dumps(report,indent=2)+'\n');print(report['counts']);sys.exit(bool(report['counts']['fail']))
