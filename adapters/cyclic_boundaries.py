#!/usr/bin/env python3
"""Bounded cyclic-term diagnostics; no normative cyclic-term contract is assumed."""
import hashlib, json, os, signal, socket, subprocess, sys, tempfile, time
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'runner'),str(ROOT/'adapters')]
import run as wire
from local_promises import quote,free_port,preservation,git,sha
BASE=Path('/Users/torbjorn.lager/Documents/GitHub')
NATIVE=BASE/'swi-prolog-node'; TREALLA=BASE/'trealla-port'
RUNTIME=Path('/Users/torbjorn.lager/.local/share/trinity-runtime-tests')
SWI=RUNTIME/'swi-default-startup-2026-10-24/runtime/bin/swipl'
TPL=RUNTIME/'trealla-v3.14.10-acceptance-2026-10-24/engine/tpl'
OUT=ROOT/'reports/2026-10-25-cyclic-term-boundaries/results'
# Reject pathological frame allocations before reading the payload.
class LimitedWS(wire.WebSocket):
    def _recv_exact(self,count):
        if count>16384:raise ValueError('diagnostic WebSocket read cap exceeded')
        return super()._recv_exact(count)
wire.WebSocket=LimitedWS
ENV=dict(os.environ,TPL_LIBRARY_PATH=str(TPL.parent/'library'))
for key in ['SWI_HOME_DIR','SWIPL_HOME_DIR','WP_CONFIG_FILE','WP_ASSET_ROOT','WP_WASM_SOURCE_DIR','WP_NATIVE_STATE','WP_NATIVE_MODE','WP_EXPERIMENTAL_TEXT']:
    ENV.pop(key,None)
# Keep error culprits (which may themselves be cyclic) out of the result.
SUMMARY="(E=error(type_error(K,_),_)->Outcome=rejected(type_error,K);E=error(resource_error(K),_)->Outcome=rejected(resource_error,K);E=error(representation_error(K),_)->Outcome=rejected(representation_error,K);E=error(F,_)->functor(F,N,A),Outcome=rejected(N,A);functor(E,N,A),Outcome=rejected(N,A))"
def guarded(goal):return 'catch(('+goal+'),E,'+SUMMARY+')'
def classify(var):
    return f"(acyclic_term({var})->functor({var},N,A),Outcome=received_acyclic(N,A);Outcome=received_cyclic)"
def child_limits():
    import resource
    resource.setrlimit(resource.RLIMIT_CPU,(20,20))
    resource.setrlimit(resource.RLIMIT_FSIZE,(1024*1024,1024*1024))
class Node:
    def __init__(self,kind,label,roots):
        self.kind=kind;self.port=free_port();self.url=f'http://127.0.0.1:{self.port}'
        if kind=='swi':
            goal=f"use_module(library(sgml)),use_module(library(option)),consult({quote(roots[kind]/'load.pl')}),set_setting(http:public_host,'127.0.0.1'),set_setting(http:public_port,{self.port}),set_setting(http:public_scheme,http),use_module(library(socket)),tcp_socket(S),tcp_bind(S,ip(127,0,0,1):{self.port}),tcp_listen(S,128),node:node({self.port},[tcp_socket(S),profile(actor),sandbox(blacklist),auth(open)]),thread_get_message(stop)"
            cmd=[str(SWI),'-f','none','-q','-g',goal]
        else:
            goal=f"use_module(web_prolog),use_module(distribution),web_prolog:web_prolog_node({self.port},[bind_address('127.0.0.1'),node_url({quote(self.url)}),profile(actor),sandbox(blacklist),auth(open),trusted_proxy_ranges(['127.0.0.1'])]),thread_get_message(stop)"
            cmd=[str(TPL),'-g',goal]
        self.log=(OUT/(label+'.log')).open('w')
        self.p=subprocess.Popen(cmd,cwd=roots[kind],env=ENV,stdout=self.log,stderr=self.log,start_new_session=True,preexec_fn=child_limits)
        self.record=dict(kind=kind,pid=self.p.pid,url=self.url,command=cmd,log=label+'.log')
        for _ in range(160):
            if self.p.poll() is not None:raise RuntimeError('startup exit '+str(self.p.returncode))
            try:
                with socket.create_connection(('127.0.0.1',self.port),.2) as ready:
                    ready.sendall(b'GET / HTTP/1.0\r\nHost: localhost\r\n\r\n')
                    if ready.recv(256):return
            except OSError:time.sleep(.05)
        raise TimeoutError('node startup')
    def stop(self):
        self.record['exit_before_stop']=self.p.poll()
        if self.p.poll() is None:
            os.killpg(self.p.pid,signal.SIGTERM)
            try:self.p.wait(timeout=1)
            except subprocess.TimeoutExpired:os.killpg(self.p.pid,signal.SIGKILL);self.p.wait()
        self.record['stopped']=self.p.poll() is not None;self.log.close()
def http(node,goal,template):
    url=node.url+'/call?'+urlencode(dict(goal='('+goal+')',template='('+template+')',format='prolog',limit='1'))
    try:
        with urlopen(url,timeout=4) as r:
            body=r.read(16385)
            return dict(status=r.status,body=body[:16384].decode('utf-8',errors='replace'),truncated=len(body)>16384)
    except Exception as e:return dict(exception=type(e).__name__,message=str(e))
def ws(node,goal):
    candidate=wire.Candidate(node.url.replace('http:','ws:')+'/ws','actor',4,None,None,False,())
    with wire.Harness(candidate) as h:
        h.spawn_shell()
        h.call(goal,'[template(Outcome),format(prolog),limit(1)]')
        events=[]
        for _ in range(8):
            event=h.recv();events.append(event)
            if event.get('type') in ['success','failure','error']:return dict(events=events)
        return dict(events=events,diagnostic='no terminal event within eight events')
def actor_goal(peer,cyclic):
    options='['+(f'node({quote(peer)}),' if peer else '')
    worker="probe :- receive({inspect(V,Parent) -> self(Me),Parent ! observed(Me,V)})."
    make='V=f(V)' if cyclic else 'V=pair(A,A)'
    check=classify('Received') if cyclic else '(Received=pair(U,W),var(U),U==W->Outcome=shared_ok;Outcome=sharing_lost)'
    options=options+'src_text('+quote(worker)+')]' 
    return guarded(f"self(Self),spawn(probe,Pid,{options}),{make},Pid ! inspect(V,Self),receive({{observed(Pid,Received)->({check})}},[timeout(1),on_timeout(Outcome=delivery_timeout)])")

def rpc_goal(peer,cyclic):
    goal='X=f(X)' if cyclic else 'X=pair(A,A)'
    check=classify('X') if cyclic else '(X=pair(U,V),var(U),U==V,Outcome=shared_ok)'
    return guarded(f"(rpc({quote(peer)},({goal}),[limit(1),once(true)]) -> {check}; Outcome=logical_failure)")
def promise_goal(peer,cyclic):
    goal='X=f(X)' if cyclic else 'X=pair(A,A)'
    check=classify('Value') if cyclic else '(Value=pair(U,V),var(U),U==V,Outcome=shared_ok)'
    return guarded(f"promise({quote(peer)},({goal}),Ref,[template(X),limit(1),once(true)]),yield(Ref,Answer,[timeout(3)]),(Answer=success([Value],_)->{check};Answer=error(E)->{SUMMARY};Answer=timeout->Outcome=yield_timeout;functor(Answer,N,A),Outcome=answer(N,A))")
def main():
    OUT.mkdir(parents=True,exist_ok=False)
    pin=BASE/'trinity-demonstrator/dependencies/swi-prolog-node.json'
    before=preservation(NATIVE,TREALLA,SWI,TPL);before['pin']=sha(pin)
    rows=[];nodes=[]
    provenance=dict(sources={k:dict(path=str(p),commit=git(p,'rev-parse','HEAD'),status=git(p,'status','--short')) for k,p in [('swi',NATIVE),('trealla',TREALLA),('conformance',ROOT)]},adapter_sha256=sha(Path(__file__)),engines=before['engines'],nodes=nodes)
    try:
        with tempfile.TemporaryDirectory(prefix='trinity-cycles-') as temp:
            roots={}
            for kind,repo in [('swi',NATIVE),('trealla',TREALLA)]:
                root=Path(temp)/kind;root.mkdir();roots[kind]=root
                archive=subprocess.Popen(['git','-C',str(repo),'archive','HEAD'],stdout=subprocess.PIPE)
                subprocess.run(['tar','-x','-C',str(root)],stdin=archive.stdout,check=True);archive.stdout.close();assert archive.wait()==0
            local=[('occurs_new','(unify_with_occurs_check(X,f(X))->write(accepted);write(rejected))'),('create','X=f(X),(acyclic_term(X)->write(acyclic);write(cyclic))'),('copy','X=f(X),copy_term(X,Y),(acyclic_term(Y)->write(acyclic_copy);write(cyclic_copy))'),('occurs_existing','X=f(X),(unify_with_occurs_check(X,X)->write(accepted);write(rejected))')]
            for kind,exe in [('swi',SWI),('trealla',TPL)]:
                for name,goal in local:
                    cmd=[str(exe)]+(['-f','none','-q'] if kind=='swi' else [])+['-g',goal+',nl,halt']
                    row=dict(case='engine_'+name,caller=kind,command=cmd)
                    try:
                        r=subprocess.run(cmd,env=ENV,capture_output=True,text=True,timeout=4,preexec_fn=child_limits,start_new_session=True)
                        row.update(exit_code=r.returncode,stdout=r.stdout[:16384],stderr=r.stderr[:16384])
                    except subprocess.TimeoutExpired:row['exception']='TimeoutExpired'
                    rows.append(row)
            cases=[]
            for caller in ['swi','trealla']:
                for name,goal,template in [('http_shared','X=pair(A,A),X=pair(U,V),var(U),U==V,Outcome=shared_ok','Outcome'),('http_cycle_summary','X=f(X),(acyclic_term(X)->Outcome=acyclic;Outcome=cyclic)','Outcome'),('http_cycle','X=f(X)','X'),('http_cyclic_exception','X=f(X),throw(error(cycle_probe(X),cycle_probe))','X')]:
                    cases.append((name,caller,None,goal,template))
                for cyclic in [False,True]:cases.append(('actor_cycle' if cyclic else 'actor_shared',caller,None,cyclic,None))
                for peer in ['swi','trealla']:
                    for family in ['remote_actor','rpc','promise']:
                        for cyclic in [False,True]:cases.append((family+('_cycle' if cyclic else '_shared'),caller,peer,cyclic,None))
            for index,(name,caller,peer,value,template) in enumerate(cases):
                label=f'{index:02}-{caller}-{name}'+(f'-{peer}' if peer else '')
                row=dict(case=name,caller=caller,peer=peer);active=[];start=time.monotonic()
                try:
                    c=Node(caller,label+'-caller',roots);active.append(c);nodes.append(c.record)
                    p=None
                    if peer:p=Node(peer,label+'-peer',roots);active.append(p);nodes.append(p.record)
                    if name.startswith('http_'):row['result']=http(c,value,template)
                    else:
                        if name.startswith(('actor_','remote_actor_')):goal=actor_goal(p.url if p else None,value)
                        elif name.startswith('rpc_'):goal=rpc_goal(p.url,value)
                        else:goal=promise_goal(p.url,value)
                        row['goal']=goal;row['result']=ws(c,goal)
                    row['health_after']=http(c,'Outcome=healthy','Outcome')
                except Exception as e:row.update(exception=type(e).__name__,message=str(e))
                finally:
                    for node in reversed(active):node.stop()
                    row['seconds']=round(time.monotonic()-start,3);rows.append(row)
                    (OUT/'observations.json').write_text(json.dumps(rows,indent=2)+'\n')
                    print(label,json.dumps(row.get('result',row.get('exception'))),flush=True)
    finally:
        after=preservation(NATIVE,TREALLA,SWI,TPL);after['pin']=sha(pin)
        (OUT/'preservation.json').write_text(json.dumps(dict(checks={k:before[k]==after[k] for k in before},before=before,after=after),indent=2)+'\n')
        (OUT/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
        (OUT/'observations.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
