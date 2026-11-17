#!/usr/bin/env python3
"""Deterministic last-attachment races on disposable native source copies.

A test-only barrier pauses immediately after the last-attachment decision.
The negative control moves retirement outside the decision's mutex; it must
reproduce an attached caller whose namespace is subsequently closed.
"""
import argparse, hashlib, json, os, shutil, subprocess, tempfile
from pathlib import Path

SWI_SETUP = """
setup_case(NS) :-
    node_execution_context:open_client_connection(q1,ws_client(race_one)),
    node_execution_context:open_client_connection(q2,ws_client(race_two)),
    node_execution_context:resolve_client_lineage(global,'http://local','http://foreign',token,q1,open,NS),
    with_mutex(actors_registry,retractall(node_execution_context:lineage_attachment(_,q1,_,_,_))).
attach(NS) :- node_execution_context:resolve_client_lineage(global,'http://local','http://foreign',token,q2,open,NS).
close_unattached(NS) :- node_execution_context:close_unattached_namespace(NS).
status(NS,S) :- node_execution_context:client_namespace_status(NS,S).
registry(actors_registry).
"""
TPL_SETUP = """
setup_case(NS) :-
    receiver_lineage_tests:new_relay(Base,A),receiver_lineage_tests:new_relay(Other,B),
    assertz(relays(Base,A,Other,B)),
    receiver_lineage_tests:token(a,T),receiver_lineage_tests:token(b,Account),
    receiver_lineage_tests:context_wire('http://foreign',T,Account,false,JSON),assertz(wire(JSON)),
    receiver_lineage_tests:context_call(A,JSON,spawn,actors:current_actor_namespace(NS)),
    with_mutex('$actor_registry',retractall(receiver_lineage:connection_lineage(A,NS))).
attach(NS) :- relays(_,_,_,B),wire(JSON),
    receiver_lineage_tests:context_call(B,JSON,spawn,actors:current_actor_namespace(NS)).
close_unattached(NS) :- receiver_lineage:close_unattached_namespace(NS).
status(NS,S) :- (actors:closed_registry_namespace(NS) -> S=closed ; S=open).
registry('$actor_registry').
:- dynamic relays/4,wire/1.
"""
COMMON = """
:- dynamic barrier/2.
before_retire(NS) :-
    (barrier(NS,Parent) ->
        thread_send_message(Parent,boundary),thread_get_message(continue)
    ;true).
joined(Parent) :-
    catch((attach(NS),Outcome=attached(NS)),E,Outcome=rejected(E)),
    thread_send_message(Parent,joined(Outcome)).
reattach_first :-
    setup_case(NS),attach(Joined),NS==Joined,
    close_unattached(NS),status(NS,open),
    writeln(reattach_first_passed).
run :-
    setup_case(NS),thread_self(Parent),assertz(barrier(NS,Parent)),
    thread_create(attachment_race:close_unattached(NS),Closer,[]),
    thread_get_message(boundary),registry(Mutex),
    (mutex_trylock(Mutex) -> mutex_unlock(Mutex),Lock=free ; Lock=busy),
    (Lock==free -> joined(Parent),Join=none
    ;thread_create(attachment_race:joined(Parent),Join,[])),
    thread_send_message(Closer,continue),thread_join(Closer,true),
    thread_get_message(joined(Outcome)),
    (Join==none -> true ; thread_join(Join,true)),
    retractall(barrier(_,_)),status(NS,Original),
    writeq(race_result(Lock,Outcome,Original)),nl,
    (Outcome=attached(Joined) -> status(Joined,open) ; Outcome=rejected(_)),
    Lock==busy,Original==closed,
    writeln(attachment_race_passed).
"""

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--swipl',required=True);p.add_argument('--tpl',required=True)
    p.add_argument('--swi-root',type=Path,required=True);p.add_argument('--trealla-root',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=False);results=[]
    with tempfile.TemporaryDirectory(prefix='attachment-race-') as tmp:
        for mode,root,exe,setup in [('swi',a.swi_root,a.swipl,SWI_SETUP),('trealla',a.trealla_root,a.tpl,TPL_SETUP)]:
            for negative in [False,True]:
                label=mode+('-negative' if negative else '-fixed');work=Path(tmp)/label;work.mkdir()
                if mode=='swi':
                    shutil.copytree(root/'prolog',work/'prolog')
                    module=work/'prolog/web_prolog/node_execution_context.pl'
                    import_line=":- use_module('prolog/web_prolog.pl').\n"
                    needle='''    with_mutex(actors_registry,
        (NS=delegated_context(_), \\+ lineage_attachment(_,_,_,_,NS)
        -> close_namespace_locked(NS,WasOpen),Retired=true
        ;Retired=false)),'''
                    test='NS=delegated_context(_), \\+ lineage_attachment(_,_,_,_,NS)'
                    retire='close_namespace_locked(NS,WasOpen)';mutex='actors_registry'
                else:
                    for f in root.glob('*.pl'):shutil.copy2(f,work/f.name)
                    module=work/'receiver_lineage.pl'
                    import_line=":- use_module(receiver_lineage_tests,[]).\n"
                    needle='''    with_mutex('$actor_registry',
        ((NS=ws_lineage(_,_);NS=delegated_context(_)),
         \\+ connection_lineage(_,NS)
        -> retire_namespace_locked(NS),Retired=true
        ;Retired=false)),'''
                    test='(NS=ws_lineage(_,_);NS=delegated_context(_)), \\+ connection_lineage(_,NS)'
                    retire='retire_namespace_locked(NS)';mutex="'$actor_registry'"
                source=module.read_text();assert source.count(needle)==1,(label,'instrumentation boundary changed')
                if negative:
                    replacement=f'''    with_mutex({mutex},(({test}) -> Decided=true ; Decided=false)),
    (Decided==true -> attachment_race:before_retire(NS),{retire},Retired=true ; Retired=false),'''
                else:
                    replacement=needle.replace('-> '+retire,'-> attachment_race:before_retire(NS),'+retire)
                module.write_text(source.replace(needle,replacement))
                fixture=work/'attachment_race.pl';fixture.write_text(':- module(attachment_race,[run/0,reattach_first/0,before_retire/1]).\n'+import_line+setup+COMMON)
                goal='(catch(attachment_race:run,E,(writeq(E),nl,fail))->halt;halt(1))'
                cmd=[exe,'-q','-s',str(fixture),'-g',goal] if mode=='swi' else [exe,'-g',"consult('attachment_race.pl'),"+goal]
                env=dict(os.environ)
                if mode=='trealla':env['TPL_LIBRARY_PATH']=str(Path(exe).parent/'library')
                if not negative:
                    first_cmd=[part.replace('attachment_race:run','attachment_race:reattach_first') for part in cmd]
                    first=subprocess.run(first_cmd,cwd=work,env=env,capture_output=True,text=True,timeout=20)
                    first_ok=first.returncode==0 and 'reattach_first_passed' in first.stdout
                    (a.output/(mode+'-reattach-first.log')).write_text(first.stdout+first.stderr)
                    results.append(dict(candidate=mode,id='ATTACH-REJOIN-FIRST',status='pass' if first_ok else 'fail',returncode=first.returncode,observation=first.stdout.strip()))
                    print(mode+'-reattach-first','pass' if first_ok else 'FAIL',flush=True)
                r=subprocess.run(cmd,cwd=work,env=env,capture_output=True,text=True,timeout=20)
                (a.output/(label+'.log')).write_text(r.stdout+r.stderr)
                ok=(r.returncode==1 and 'race_result(free,attached(' in r.stdout and ',closed)' in r.stdout) if negative else (r.returncode==0 and 'attachment_race_passed' in r.stdout)
                results.append(dict(candidate=mode,id='ATTACH-NEGATIVE' if negative else 'ATTACH-ATOMIC',status='pass' if ok else 'fail',negative_control=negative,returncode=r.returncode,source_sha256=hashlib.sha256(source.encode()).hexdigest(),instrumented_sha256=hashlib.sha256(module.read_bytes()).hexdigest(),observation=r.stdout.strip()))
                print(label,'pass' if ok else 'FAIL',flush=True)
    sources={mode:dict(root=str(root),revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),clean=not subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip()) for mode,root in [('swi',a.swi_root),('trealla',a.trealla_root)]}
    (a.output/'results.json').write_text(json.dumps(dict(suite='last-attachment-race-0.1',sources=sources,results=results),indent=2)+'\n')
    if any(r['status']!='pass' for r in results):raise SystemExit(1)
if __name__=='__main__':main()
