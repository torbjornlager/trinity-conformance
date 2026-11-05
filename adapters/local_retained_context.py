#!/usr/bin/env python3
"""Test native client-context boundaries on disposable localhost nodes.

No live nodes, installed engines, release pins or runtime implementations change.
Every failed, blocked or errored observation causes a nonzero exit.
"""
import argparse,contextlib,hashlib,json,os,re,secrets,socket,subprocess,sys,tempfile,time,urllib.parse,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runner'))
from run import Candidate,Harness,prolog_quote_atom,row_value
from controlled_promise_peer import ControlledPromisePeer

SOURCE = """audit_create(Parent,URL):-promise(URL,true,R,[template(mark)]),send(Parent,created(R)),receive({finish->true}).
audit_collect(Parent,Ref):-catch(yield(Ref,A,[timeout(2)]),E,A=error(E)),send(Parent,collected(A)).
audit_lookup(Parent,Name):-whereis(Name,P),send(Parent,found(P)).
"""
def port():
 with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def literal(s):return prolog_quote_atom(str(s))
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--swipl',required=True);p.add_argument('--tpl',required=True)
 p.add_argument('--swi-root',type=Path,required=True);p.add_argument('--trealla-root',type=Path,required=True)
 p.add_argument('--controlled-promises',action='store_true',help='add six barrier-controlled timeout/ownership checks, including public-style self routes')
 p.add_argument('--output',type=Path,required=True);p.add_argument('--routes',nargs='*',default=['swi-a:swi-b','swi-a:trealla-b','trealla-a:swi-b','trealla-a:trealla-b'],choices=['swi-a:swi-b','swi-a:trealla-b','trealla-a:swi-b','trealla-a:trealla-b']);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 ports={name:port() for name in ['swi-a','swi-b','swi-c','trealla-a','trealla-b']}
 urls={name:('http://localhost:' if name.startswith('swi-') else 'http://127.0.0.1:')+str(n) for name,n in ports.items()};rows=[];processes=[];logs=[]
 sources={}
 for name,root in [('swi',a.swi_root),('trealla',a.trealla_root)]:
  files=(root/'prolog').rglob('*.pl') if name=='swi' else root.glob('*.pl')
  sources[name]=dict(root=str(root),revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff'],cwd=root)).hexdigest(),files_sha256={str(f.relative_to(root)):sha(f) for f in sorted(files)})
 def save():
  report=dict(suite='native-retained-context-audit-0.1',scope='Scoped audit: retained WSS and fresh HTTP on SWI/Trealla; explicitly selected remote routes; no live services changed',routes=a.routes,adapter_sha256=sha(__file__),sources=sources,results=rows,counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail','blocked','error']})
  (a.output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
 def record(candidate,id,title,fn,requirements):
  row=dict(candidate=candidate,id=id,title=title,requirements=requirements)
  try:
   observation,ok=fn();row.update(observation=observation,status='pass' if ok else 'fail')
   detail=json.dumps(observation)
   if not ok and not id.startswith('CTX-018') and any(x in detail for x in ['sandbox_policy:', 'roundtrip_promise_missing', 'roundtrip_name_missing', 'no_collector_reply']):
    row['status']='blocked';row['blocker']='remote source/goal export failed before a context result could be observed'
  except Exception as e:row.update(status='error',detail=str(e))
  rows.append(row);save();print(candidate,id,row['status'],flush=True)
 def start(label,cmd,cwd,env):
  f=(a.output/(label+'.log')).open('w+');logs.append(f);proc=subprocess.Popen(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT);processes.append(proc);return proc
 def wait(name,proc):
  for _ in range(200):
   if proc.poll() is not None:raise RuntimeError(name+' fixture exited; inspect fixture log')
   try:
    with socket.create_connection(('127.0.0.1',ports[name]),timeout=.1):return
   except OSError:time.sleep(.04)
  raise TimeoutError(name+' fixture readiness')
 def harness(name,token):return Harness(Candidate(urls[name].replace('http:','ws:')+'/ws','actor',8,token,urls[name],False,()))
 def run(h,goal):
  h.call('('+goal+'),AuditCheck=passed','[limit(1)]')
  for _ in range(32):
   event=h.recv()
   if event.get('type') in ['success','failure','error'] and event.get('pid',h.shell)==h.shell:return event
   h.acknowledge_output(event)
  raise RuntimeError('missing terminal query answer')
 def good(event):return event.get('type')=='success'
 def paired(h1,g1,h2,g2):
  first=run(h1,g1);second=run(h2,g2)
  return dict(first=first,second=second),good(first) and good(second)
 def unregister_boundary(other,owner,name):
  first=run(other,f'unregister({name})');second=run(owner,f'self(S),whereis({name},Found)')
  return dict(foreign=first,owner=second),good(first) and good(second) and row_value(second,'Found')==row_value(second,'S')
 def run_check(h,goal):
  e=run(h,goal);return e,good(e)
 def missing(ref):return f'catch(yield({ref},_,[timeout(0)]),error(existence_error(promise,{ref}),_),Missing=true),Missing==true'
 def create(h,url):
  e=run(h,f'promise({literal(url)},true,Ref,[template(mark)])')
  if not good(e):raise RuntimeError('promise setup: '+json.dumps(e))
  return row_value(e,'Ref')
 def collector(h,remote,ref):
  source=SOURCE.splitlines()[1]+'\n'
  return run(h,f'self(S),spawn(audit_collect(S,{ref}),_,[node({literal(remote)}),src_text({literal(source)})]),receive({{collected(Outcome)->true}},[timeout(4),on_timeout(throw(no_collector_reply))])')
 def remote_create(h,remote,promise_url=None):
  source=SOURCE.splitlines()[0]+'\n'
  e=run(h,f'self(S),spawn(audit_create(S,{literal(promise_url or remote)}),Creator,[node({literal(remote)}),src_text({literal(source)})]),receive({{created(Ref)->true}},[timeout(4),on_timeout(throw(no_creator_reply))])')
  if not good(e):raise RuntimeError('remote creator setup: '+json.dumps(e))
  ref=row_value(e,'Ref')
  if not ref.isdigit():raise RuntimeError('unbound remote promise reference: '+json.dumps(e))
  return ref,row_value(e,'Creator')
 def collected(e):return good(e) and row_value(e,'Outcome')=='success([mark],false)'
 env=dict(os.environ)
 for key in ['WP_CONFIG_FILE','SWI_HOME_DIR','SWIPL_HOME_DIR','WP_NATIVE_STATE','WP_NATIVE_MODE']:env.pop(key,None)
 try:
  with tempfile.TemporaryDirectory(prefix='retained-context-audit-') as tmp:
   tmp=Path(tmp);creds=tmp/'credentials.json';boot=tmp/'swi.pl'
   peers=','.join(literal(u)+'-Peer' for u in urls.values())
   node_goals=[f'node({ports[n]},[profile(actor),auth(open),max_call_requests_per_window(1000),max_ws_actors_per_principal(256),max_principal_actors(256),peer_transport_tokens([{peers}])])' for n in ['swi-a','swi-b','swi-c']]
   boot.write_text(':- use_module('+literal(a.swi_root/'prolog/web_prolog.pl')+').\n:- use_module(library(http/json)).\n:- initialization(main,main).\nmain :- node_tokens:issue_token("node:context-audit",[execute,internal_transport],[],PeerString),atom_string(Peer,PeerString),node_tokens:issue_token("audit-client",[execute],[],Client),open('+literal(creds)+',write,S),json_write_dict(S,_{peer:Peer,client:Client}),close(S),'+','.join(node_goals)+',thread_get_message(stop).\n')
   swi=start('swi-fixture',[a.swipl,'-f','none','-q',str(boot)],a.swi_root,env)
   for name in ['swi-a','swi-b','swi-c']:wait(name,swi)
   credentials=json.loads(creds.read_text());client=credentials['client'];peer=credentials['peer']
   for name in ['trealla-a','trealla-b']:
    launcher=tmp/(name+'.pl');launcher.write_text(':- use_module(distribution).\naudit_main :- web_prolog:web_prolog_node('+str(ports[name])+',[max_call_requests_per_window(1000),peer_transport_tokens(['+','.join(literal(u)+'-'+literal(peer) for u in urls.values())+']),bearer_token(audit_client,'+literal(client)+',[execute]),bearer_token(\'node:context-audit\','+literal(peer)+',[execute,internal_transport])]).\n')
    te=dict(env,TPL_LIBRARY_PATH=str(Path(a.tpl).parent/'library'))
    proc=start(name+'-fixture',[a.tpl,'-g',f'consult({literal(launcher)}),audit_main'],a.trealla_root,te);wait(name,proc)
   for name in ['swi-a','trealla-a']:
    candidate=name.split('-')[0];url=urls[name]
    with contextlib.ExitStack() as stack:
     h=stack.enter_context(harness(name,client));h.spawn_shell()
     other=stack.enter_context(harness(name,client));other.spawn_shell()
     record(candidate,'CTX-001','retained local parent/child promise sharing',lambda h=h:run_check(h,f'promise({literal(url)},true,R,[template(mark)]),self(S),spawn((yield(R,A),send(S,answer(A))),_,[]),receive({{answer(success([mark],false))->true}},[timeout(4),on_timeout(throw(no_local_child_reply))])'),['B-004','B-296'])
     ref=create(h,url)
     record(candidate,'CTX-002','separate WSS contexts with equal credentials cannot collect',lambda h=other,ref=ref:run_check(h,missing(ref)),['B-004','B-296'])
     record(candidate,'CTX-003','foreign cleanup cannot dispose owner promise',lambda h=h,o=other,ref=ref:paired(o,f'promise_cleanup({ref})',h,f'yield({ref},success([mark],false))'),['B-305','B-306'])
     ref=create(h,url);first=h.shell;second=h.spawn_shell()
     record(candidate,'CTX-004','a second toplevel on one retained WSS context shares promises',lambda h=h,ref=ref:run_check(h,f'yield({ref},success([mark],false))'),['B-004','B-296'])
     ref=create(h,url);h.halt();h.spawn_shell()
     record(candidate,'CTX-005','toplevel replacement retains its WSS context promises',lambda h=h,ref=ref:run_check(h,f'yield({ref},success([mark],false))'),['B-304'])
     name1='context_audit_'+secrets.token_hex(6)
     e=run(h,f'self(S),register({name1},S)')
     if not good(e):raise RuntimeError('name setup failed: '+str(e))
     record(candidate,'CTX-006','ordinary name hidden from another WSS context',lambda o=other,n=name1:((e:=run(o,f'whereis({n},Found)')),good(e) and row_value(e,'Found')=='undefined'),['B-004','B-058','B-062'])
     record(candidate,'CTX-007','equal names can be registered in separate WSS contexts',lambda o=other,n=name1:run_check(o,f'self(S),register({n},S)'),['B-058'])
     record(candidate,'CTX-009','ordinary names propagate to local descendants',lambda h=h,n=name1:run_check(h,f'self(S),spawn((whereis({n},P),send(S,found(P))),_,[]),receive({{found(S)->true}},[timeout(4),on_timeout(throw(local_name_missing))])'),['B-004','B-058'])
     name2='context_audit_'+secrets.token_hex(6)
     setup=run(h,f'unregister({name1}),self(S),register({name2},S)')
     if not good(setup):raise RuntimeError('second name setup failed: '+str(setup))
     record(candidate,'CTX-008','foreign unregister does not remove owner name',lambda h=h,o=other,n=name2:unregister_boundary(o,h,n),['B-064'])
    for authenticated,id in [(True,'CTX-010'),(False,'CTX-011')]:
     def http_boundary(authenticated=authenticated,url=url):
      def request(goal,template='AuditCheck'):
       params=dict(goal='('+goal+')',template=template,limit=1,format='prolog');request=urllib.request.Request(url+'/call?'+urllib.parse.urlencode(params))
       if authenticated:request.add_header('Authorization','Bearer '+client)
       with urllib.request.urlopen(request,timeout=8) as response:return response.read().decode()
      created=request(f'promise({literal(url)},true,R,[template(mark)])','R');match=re.fullmatch(r'success\(\[(\d+)\],false\)\.', ''.join(created.split()))
      if not match:raise RuntimeError('HTTP promise setup: '+created)
      ref=match[1];observed=request(f'catch(yield({ref},A,[timeout(1)]),E,A=error(E))','A');return dict(created=created,separate_request=observed),'existence_error(promise,'+ref+')' in ''.join(observed.split())
     record(candidate,id,('authenticated' if authenticated else 'anonymous')+' fresh HTTP requests do not retain a client context through credentials',http_boundary,['B-004','B-296'])
   def retained_http_session():
    url=urls['swi-a'];sessions=[];observed={}
    def post(route,params):
     request=urllib.request.Request(url+'/'+route,data=urllib.parse.urlencode(dict(params,format='json')).encode(),headers={'Authorization':'Bearer '+client,'Content-Type':'application/x-www-form-urlencoded'})
     with urllib.request.urlopen(request,timeout=8) as response:return json.load(response)
    def call(pid,goal,template='AuditCheck'):
     return post('toplevel_call',dict(pid=pid,goal='('+goal+'),AuditCheck=passed',template=template,limit=1))
    try:
     for _ in range(2):
      spawned=post('toplevel_spawn',dict(options='[session(true)]'));sessions.append(spawned['pid'])
     created=call(sessions[0],f'promise({literal(url)},true,R,[template(mark)])','R');observed['create']=created
     value=created['data'][0];ref=value['R'] if isinstance(value,dict) else value
     if not str(ref).isdigit():raise RuntimeError('HTTP session reference missing: '+str(created))
     observed['separate_session']=call(sessions[1],missing(ref))
     observed['same_session_later_request']=call(sessions[0],f'yield({ref},success([mark],false))')
     return observed,all(e.get('type')=='success' for e in observed.values())
    finally:
     for pid in sessions:post('toplevel_halt',dict(pid=pid))
   record('swi','CTX-020','retained HTTP session preserves promises across requests and isolates another session with equal credentials',retained_http_session,['B-004','B-296','B-304'])
   for home in ['swi-a','trealla-a']:
    for dest in ['swi-b','trealla-b']:
     if home+':'+dest not in a.routes:continue
     candidate=home.split('-')[0];pair=home+' -> '+dest;remote=urls[dest]
     home_source=SOURCE.splitlines()[2]+'\n'+f'audit_back_name(Parent,Name):-spawn(audit_lookup(Parent,Name),_,[node({literal(urls[home])}),src_predicates([audit_lookup/2])]),receive({{finish->true}}).\naudit_back_promise(Parent,Ref):-spawn(audit_collect(Parent,Ref),_,[node({literal(urls[home])}),src_predicates([audit_collect/2])]),receive({{finish->true}}).\n'
     with contextlib.ExitStack() as stack:
      options='[session(true),src_text('+literal(home_source)+')]'
      h=stack.enter_context(harness(home,client));h.spawn_shell(options)
      other=stack.enter_context(harness(home,client));other.spawn_shell(options)
      record(candidate,'CTX-012-'+dest,'remote transport control: '+pair,lambda h=h:run_check(h,f'self(S),spawn(send(S,remote_ready),_,[node({literal(remote)})]),receive({{remote_ready->true}},[timeout(4),on_timeout(throw(remote_control_missing))])'),['B-004'])
      record(candidate,'CTX-018-'+dest,'inline catch exports only language terms: '+pair,lambda h=h:run_check(h,f'self(S),spawn((catch(true,E,true),send(S,inline_ready)),_,[node({literal(remote)})]),receive({{inline_ready->true}},[timeout(4),on_timeout(throw(inline_control_missing))])'),[])
      try:
       ref,creator=remote_create(h,remote)
       record(candidate,'CTX-013-'+dest,'remote descendants share a context at destination: '+pair,lambda h=h,ref=ref:((e:=collector(h,remote,ref)),collected(e)),['B-004','B-296'])
       run(h,f'send({creator},finish)')
       ref,creator=remote_create(h,remote)
       record(candidate,'CTX-014-'+dest,'remote descendants of different clients remain isolated: '+pair,lambda h=other,ref=ref:((e:=collector(h,remote,ref)),good(e) and 'existence_error(promise,'+ref+')' in row_value(e,'Outcome')),['B-004','B-296'])
       record(candidate,'CTX-015-'+dest,'owner retains remote promise after foreign collection attempt: '+pair,lambda h=h,ref=ref:((e:=collector(h,remote,ref)),collected(e)),['B-296'])
       run(h,f'send({creator},finish)')
      except Exception as e:
       for number in ['013','014','015']:
        if not any(r['candidate']==candidate and r['id']=='CTX-'+number+'-'+dest for r in rows):
         rows.append(dict(candidate=candidate,id='CTX-'+number+'-'+dest,title='remote promise prerequisite: '+pair,status='blocked',requirements=[],detail=str(e)))
       save()
      name='loop_context_'+secrets.token_hex(6);run(h,f'self(S),register({name},S)')
      def roundtrip_name(h=h,name=name,remote=remote,home=home):
       source=SOURCE.splitlines()[2]+'\n'+f'audit_back_name(Parent,Name):-spawn(audit_lookup(Parent,Name),_,[node({literal(urls[home])}),src_predicates([audit_lookup/2])]),receive({{finish->true}}).\n'
       goal=f'self(S),spawn(audit_back_name(S,{name}),Bridge,[node({literal(remote)}),src_text({literal(source)})]),receive({{found(Found)->true}},[timeout(4),on_timeout(throw(roundtrip_name_missing))]),send(Bridge,finish),Expected=S'
       e=run(h,goal);return e,good(e) and row_value(e,'Found')==row_value(e,'Expected')
      record(candidate,'CTX-016-'+dest,'round-trip descendant rejoins origin ordinary namespace: '+pair,roundtrip_name,['B-004','B-058','B-062'])
      def roundtrip_promise(h=h,remote=remote,home=home):
       source=SOURCE.splitlines()[1]+'\n'+f'audit_back_promise(Parent,Ref):-spawn(audit_collect(Parent,Ref),_,[node({literal(urls[home])}),src_predicates([audit_collect/2])]),receive({{finish->true}}).\n'
       ref=create(h,urls[home]);goal=f'self(S),spawn(audit_back_promise(S,{ref}),Bridge,[node({literal(remote)}),src_text({literal(source)})]),receive({{collected(Outcome)->true}},[timeout(4),on_timeout(throw(roundtrip_promise_missing))]),send(Bridge,finish)'
       e=run(h,goal);return e,collected(e)
      record(candidate,'CTX-017-'+dest,'round-trip descendant rejoins origin promise context: '+pair,roundtrip_promise,['B-004','B-296'])
   if a.controlled_promises:
    for home,dest in [('swi-a','swi-a'),('swi-a','swi-b'),('swi-a','trealla-b'),('trealla-a','trealla-a'),('trealla-a','swi-b'),('trealla-a','trealla-b')]:
     def controlled(home=home,dest=dest):
      trace=[];peer=None;creator=None
      def observe(phase,event):
       trace.append(dict(phase=phase,elapsed_ms=peer.elapsed(),event=event))
       return event
      try:
       with ControlledPromisePeer() as peer,contextlib.ExitStack() as stack:
        h=stack.enter_context(harness(home,client));h.spawn_shell('[session(true)]')
        other=stack.enter_context(harness(home,client));other.spawn_shell('[session(true)]')
        ref,creator=remote_create(h,urls[dest],peer.url)
        observe('created',dict(reference=ref,creator=creator))
        if not peer.arrived.wait(4):raise RuntimeError('producer did not receive HTTP request')
        observe('producer_arrived',dict(released=peer.release.is_set()))
        foreign=observe('foreign_pending',collector(other,urls[dest],ref))
        early=observe('owner_pending',collector(h,urls[dest],ref))
        held=not peer.release.is_set() and not peer.sent.is_set()
        peer.release.set()
        if not peer.sent.wait(4):raise RuntimeError('producer did not send released answer')
        observe('producer_sent',dict(request_count=len(peer.requests)))
        foreign_ready=observe('foreign_released',collector(other,urls[dest],ref))
        answer=observe('owner_retry',collector(h,urls[dest],ref))
        consumed=observe('owner_after_collection',collector(h,urls[dest],ref))
        finish=observe('creator_finish',run(h,f'send({creator},finish)'))
        missing_answer=lambda e: good(e) and 'existence_error(promise,'+ref+')' in row_value(e,'Outcome')
        ok=(held and good(early) and row_value(early,'Outcome')=='timeout' and
            missing_answer(foreign) and missing_answer(foreign_ready) and collected(answer) and
            missing_answer(consumed) and good(finish) and len(peer.requests)==1 and not peer.errors)
        return dict(trace=trace,requests=peer.requests,producer_errors=peer.errors),ok
      except Exception as e:
       return dict(trace=trace,requests=peer.requests if peer else [],detail=str(e)),False
     record(home.split('-')[0],'CP-001-'+dest,'controlled pending timeout, foreign denial, release and owner retry: '+home+' -> '+dest,controlled,['B-296','B-304'])
 except Exception as e:
  rows.append(dict(candidate='fixture',id='CTX-FIXTURE',title='audit fixture setup',status='error',detail=str(e)));save();print('fixture error',str(e),flush=True)
 finally:
  for proc in reversed(processes):
   proc.terminate()
   try:proc.wait(timeout=5)
   except subprocess.TimeoutExpired:proc.kill();proc.wait()
  for f in logs:f.close()
  save()
 print('counts',json.loads((a.output/'results.json').read_text())['counts'],flush=True)
 return int(any(r['status']!='pass' for r in rows))
if __name__=='__main__':raise SystemExit(main())
