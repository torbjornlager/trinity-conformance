#!/usr/bin/env python3
"""Disposable, public-interface experiments for the paper's transition core.

Run inside an isolated container with frozen runtime sources mounted read-only.
No production endpoints or credentials are used. Every outcome is retained.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import secrets
import signal
import socket
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--sources', type=Path, default=Path('/sources'))
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--repetitions', type=int, default=1)
parser.add_argument('--only', nargs='*', help='Explicit case subset; recorded in provenance')
args = parser.parse_args()
assert args.repetitions > 0
args.output.mkdir(parents=True, exist_ok=False)
spec = importlib.util.spec_from_file_location('paper_actor_client', args.sources/'conformance/runner/run.py')
actor = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = actor
spec.loader.exec_module(actor)
sys.modules['run'] = actor
sys.path.insert(0, '/work/conformance/runner')
import ownership_lifecycle
LIFECYCLE_CASES = json.loads(Path('/work/conformance/cases/ownership-lifecycle-0.1.json').read_text())['cases']

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def atom(text):
    return "'" + str(text).replace('\\', '\\\\').replace("'", "''") + "'"

def require(condition, detail):
    if not condition:
        raise AssertionError(detail)

TRACE = []

class Session(actor.Harness):
    def send(self, command):
        TRACE.append(dict(direction='send', command=command))
        super().send(command)

    def recv(self, expected_type=None):
        event = super().recv(expected_type)
        TRACE.append(dict(direction='receive', event=event))
        return event

    def spawn_shell(self, options='[session(true)]'):
        self.send(dict(command='toplevel_spawn', options=options))
        event = self.recv('spawned')
        require('pid' in event, event)
        self.shell = event['pid']  # opaque; no decimal-width assumption
        return self.shell

actor.Harness = Session

def connect(node, principal='alice'):
    return Session(actor.Candidate(node['url'].replace('http:', 'ws:')+'/ws',
                                   'actor', 5, node['tokens'][principal], None, False, ()))

def call(session, goal, options='[limit(1)]'):
    session.call(goal, options)
    return session.recv_type('success', limit=64)

def assertion(node, goal):
    with connect(node) as session:
        session.spawn_shell()
        answer = call(session, '('+goal+'),PaperResult=passed')
        require(actor.row_value(answer, 'PaperResult') == 'passed', answer)
        require(answer.get('more') is False, ('unexpected residual choice', answer))
        session.halt()
        return answer

CASES = [
    ('K1', 'First guard witness; body alternatives; one consumed message',
     "self(S),S!offer(a),S!offer(b),findall(W-B,receive({offer(a) if member(W,[first,second])->member(B,[one,two])},[timeout(0),on_timeout(throw(missing_offer))]),Pairs),Pairs==[first-one,first-two],receive({offer(Second)->Second==b},[timeout(0),on_timeout(throw(missing_second))])"),
    ('K2', 'Rejected guard bindings and consumed-message failure do not roll back effects',
     "self(S),S!offer(0),receive({offer(X) if (Tentative=wrong,fail)->fail},[timeout(0)]),var(X),var(Tentative),\\+receive({offer(Y)->Y==0,fail},[timeout(0),on_timeout(throw(missing_offer))]),var(Y),receive({offer(_)->throw(restored_message)},[timeout(0)])"),
    ('K3', 'One-sided matching preserves unbound message variables',
     "self(S),S!offer(V),receive({offer(report)->throw(bound_message_variable)},[timeout(0)]),var(V),receive({offer(W)->var(W),W=accepted},[timeout(0),on_timeout(throw(missing_variable_offer))]),var(V)"),
    ('K4', 'Timeout does not cancel a gated query or miscorrelate its late answer',
     "self(S),toplevel_spawn(P,[session(true)]),toplevel_call_synch(P,(self(Me),S!query_ready(Me),receive({release->true})),Early,[template(old),timeout(0)]),var(Early),receive({query_ready(P)->true},[timeout(2),on_timeout(throw(no_ready))]),P!release,toplevel_call_synch(P,true,Fresh,[template(fresh),timeout(2),on_timeout(throw(no_fresh))]),Fresh==success(P,[fresh],false),toplevel_halt(P,true)"),
    ('K5', 'A query error preserves a persistent session and does not deliver death',
     "toplevel_spawn(P,[session(true),monitor(true)]),toplevel_call_synch(P,throw(paper_error),E,[timeout(2),on_timeout(throw(no_error))]),E==error(P,paper_error),receive({down(P,P,_)->throw(premature_death)},[timeout(0)]),toplevel_call_synch(P,true,A,[template(recovered),timeout(2),on_timeout(throw(no_recovery))]),A==success(P,[recovered],false),toplevel_halt(P,true),receive({down(P,P,_)->true},[timeout(2),on_timeout(throw(no_death))])"),
    ('K6', 'Abort of a computing guard retains its unselected message',
     "self(S),toplevel_spawn(P,[session(true)]),toplevel_call(P,(self(Me),Me!candidate(saved),receive({candidate(X) if (S!guard_ready(Me),repeat,fail)->true}))),receive({guard_ready(P)->true},[timeout(2),on_timeout(throw(no_guard_ready))]),toplevel_abort(P),toplevel_call_synch(P,receive({candidate(V)->true}),A,[template(V),timeout(2),on_timeout(throw(no_retained_candidate))]),A==success(P,[saved],false),toplevel_halt(P,true)"),
]

def ownership(node):
    with connect(node, 'alice') as alice, connect(node, 'bob') as bob:
        alice.spawn_shell()
        bob.spawn_shell()
        result = call(alice, "self(Parent),spawn((self(Me),Parent!target_ready(Me),repeat,receive({probe(Who)->Who!alive,fail;stop->true}),!),Target,[monitor(true)]),receive({target_ready(Target)->true},[timeout(2),on_timeout(throw(target_not_ready))]),Target!probe(Parent),receive({alive->true},[timeout(2),on_timeout(throw(owner_probe_failed))])")
        target = actor.row_value(result, 'Target')
        denial_goal = (f"monitor({target},R),catch((exit({target},forbidden),ExitOutcome=returned),E,ExitOutcome=thrown),"
                       "(nonvar(E),E=error(permission_error(exit,actor,_),_)->Classification=denied;Classification=other)")
        denial = call(bob, denial_goal)
        try:
            require(actor.row_value(denial, 'ExitOutcome') == 'thrown', ('exit did not throw',denial))
            require(actor.row_value(denial, 'Classification') == 'denied', ('wrong exception',denial))
            ref = actor.row_value(denial, 'R')
            goal = (f"self(S),{target}!probe(S),"
                    "receive({alive->true},[timeout(2),on_timeout(throw(target_not_alive))]),"
                    f"{target}!stop,receive({{down({target},{ref},true)->true}},"
                    "[timeout(2),on_timeout(throw(no_observation))]),PaperResult=passed")
            answer = call(bob, goal)
            require(actor.row_value(answer, 'PaperResult') == 'passed', answer)
            require(answer.get('more') is False, answer)
        except Exception as original:
            diagnostic = call(alice, 'receive({down(Observed,ObservedRef,Why)->State=terminated},[timeout(0),on_timeout(State=no_notification)])')
            raise AssertionError(str(original)+'; owner diagnostic: '+json.dumps(diagnostic)) from original
        alice.halt()
        bob.halt()
        return dict(target=target, denial=denial, observation=answer,
                    scope='Two authenticated client contexts on one loopback node; application send/monitor permitted, exit denied.')

def disconnect(node):
    with connect(node, 'alice') as alice, connect(node, 'bob') as bob:
        alice.spawn_shell()
        bob.spawn_shell()
        answer = call(alice, "self(S),spawn((self(Me),S!worker_ready(Me),repeat,fail),Target,[monitor(true)]),receive({worker_ready(Target)->true},[timeout(2),on_timeout(throw(no_worker_ready))])")
        target = actor.row_value(answer, 'Target')
        watching = call(bob, f'monitor({target},Ref)')
        ref = actor.row_value(watching, 'Ref')
        # Transport EOF, not application halt or a simulated undetected partition.
        alice.ws.sock.shutdown(socket.SHUT_RDWR)
        alice.ws.sock.close()
        alice.ws = None
        before = time.monotonic()
        goal = (f"receive({{down({target},{ref},Reason)->true}},"
                "[timeout(3),on_timeout(throw(no_reclamation_notification))]),"
                f"Reason==kill,monitor({target},Again),receive({{down({target},Again,no_process)->true}},"
                "[timeout(2),on_timeout(throw(target_still_present))]),PaperResult=passed")
        try:
            result = call(bob, goal)
        except Exception as original:
            diagnostic = call(bob, f"findall(M,(repeat,(receive({{M->true}},[timeout(0),on_timeout(fail)])->true;!,fail)),Messages),monitor({target},Again),receive({{down(Seen,Again,Status)->true}},[timeout(0),on_timeout(Status=unresolved)])")
            raise AssertionError(str(original)+'; observer diagnostic: '+json.dumps(diagnostic)) from original
        require(actor.row_value(result, 'PaperResult') == 'passed', result)
        require(result.get('more') is False, result)
        bob.halt()
        return dict(target=target, reason='kill', later_monitor='no_process',
                    observation_seconds=round(time.monotonic()-before, 6),
                    scope='Observed local socket EOF and linked worker computing in Prolog; no packet-loss/lease or foreign-call experiment.')

def paging(node):
    observations = []
    for offset in (0, 2):
        params=dict(goal='(member(X,[a,b,c]))', template='(X)', offset=offset, limit=2, format='prolog')
        request=Request(node['url']+'/call?'+urlencode(params),
                        headers={'Authorization':'Bearer '+node['tokens']['alice']})
        with urlopen(request, timeout=5) as response:
            text=response.read().decode()
            require(response.status == 200, text)
        compact=''.join(text.split())
        expected='success([a,b],true).' if offset == 0 else 'success([c],false).'
        require(compact == expected, dict(offset=offset, expected=expected, observed=text))
        observations.append(dict(offset=offset, body=text))
    with connect(node) as session:
        session.spawn_shell()
        first=call(session,'member(X,[a,b,c])','[template(X),limit(2)]')
        require(first.get('data') == [{'X':'a'},{'X':'b'}] and first.get('more') is True,first)
        session.next()
        last=session.recv_type('success',limit=32)
        require(last.get('data') == [{'X':'c'}] and last.get('more') is False,last)
        session.halt()
    return dict(http=observations,ptcp=[first,last],
                scope='Fixed pure goal; answer sequence only. No cache eviction, mutation, snapshot or effect-equivalence claim.')

def launch(engine, temp):
    number=port()
    node=dict(url=f'http://127.0.0.1:{number}', tokens={})
    script=temp/(engine+'-fixture.pl')
    if engine == 'swi':
        executable=os.environ.get('SWIPL','/usr/bin/swipl')
        credentials=temp/'swi-credentials.json'
        text=(f":- consult({atom(args.sources/'swi/load.pl')}).\n"
              ":- use_module(library(http/json)).\n"
              f"main :- set_setting(http:public_host,'127.0.0.1'),set_setting(http:public_port,{number}),set_setting(http:public_scheme,http),"
              "use_module(library(socket)),tcp_socket(S),"
              f"tcp_bind(S,ip(127,0,0,1):{number}),tcp_listen(S,128),"
              f"node:node({number},[tcp_socket(S),profile(actor),sandbox(blacklist),auth(private)]),"
              "node_tokens:issue_token(paper_alice,[execute],[],A),node_tokens:issue_token(paper_bob,[execute],[],B),node_tokens:issue_token(paper_admin,[execute,admin],[],C),"
              f"open({atom(credentials)},write,O),json_write_dict(O,_{{alice:A,bob:B,admin:C}}),close(O),thread_get_message(stop).\n")
        command=[executable,'-f','none','-q','-s',str(script),'-g','main','-t','halt']
    else:
        executable=os.environ.get('TPL','/opt/trealla/tpl')
        node['tokens']={key:secrets.token_hex(24) for key in ('alice','bob','admin')}
        text=(f":- asserta(user:file_search_path(library,{atom(args.sources/'trealla')})).\n"
              f":- use_module({atom(args.sources/'trealla/web_prolog.pl')}).\n"
              f"main :- web_prolog:web_prolog_node({number},[bind_address('127.0.0.1'),node_url({atom(node['url'])}),"
              "profile(actor),sandbox(blacklist),auth(private),"
              f"bearer_token(paper_alice,{atom(node['tokens']['alice'])},[execute]),"
              f"bearer_token(paper_bob,{atom(node['tokens']['bob'])},[execute]),"
              f"bearer_token(paper_admin,{atom(node['tokens']['admin'])},[execute,admin])]),thread_get_message(stop).\n")
        command=[executable,'-q','-f',str(script),'-g','main']
    script.write_text(text)
    log=(args.output/(engine+'-node.log')).open('w')
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TPL_LIBRARY_PATH='/opt/trealla/library')
    proc=subprocess.Popen(command,cwd=args.sources/engine,env=env,stdout=log,stderr=log,start_new_session=True)
    for _ in range(160):
        if proc.poll() is not None:
            raise RuntimeError(f'{engine} fixture exited {proc.returncode}; see node log')
        try:
            if engine == 'swi': node['tokens']=json.loads(credentials.read_text())
            with socket.create_connection(('127.0.0.1',number),timeout=.1): pass
            break
        except (OSError,json.JSONDecodeError): time.sleep(.05)
    else:
        proc.terminate()
        raise TimeoutError(engine+' startup')
    version_command=[executable,'--version'] if engine=='swi' else [executable,'-g','current_prolog_flag(version_data,V),writeq(V),nl,halt']
    version=subprocess.run(version_command,env=env,text=True,capture_output=True,timeout=10)
    node['provenance']=dict(version=(version.stdout+version.stderr).strip(),executable=executable,
                            executable_sha256=sha(executable),fixture='generated disposable fixture; bearer secrets excluded')
    return node,proc,log

def admin_control(node):
    with connect(node,'alice') as owner, connect(node,'admin') as admin:
        owner.spawn_shell();admin.spawn_shell()
        target=ownership_lifecycle.worker(owner)
        result=call(admin,f'exit({target},admin_stop),AdminResult=passed')
        observed=call(owner,f'receive({{down({target},{target},admin_stop)->true}},[timeout(2),on_timeout(throw(no_admin_exit))])')
        owner.halt();admin.halt()
        return dict(result=result,observed=observed)

def http_control(node):
    with connect(node,'alice') as owner:
        owner.spawn_shell();target=ownership_lifecycle.worker(owner)
        def http(principal,goal):
            req=Request(node['url']+'/call?'+urlencode(dict(goal='('+goal+')',template='(Outcome-Denial)' if principal=='bob' else '(AdminResult)',format='prolog')),
                        headers={'Authorization':'Bearer '+node['tokens'][principal]})
            with urlopen(req,timeout=5) as response:return response.read().decode()
        denial=http('bob',f'catch((exit({target},forbidden),Outcome=returned),E,Outcome=thrown),(nonvar(E),E=error(permission_error(exit,actor,_),_)->Denial=yes;Denial=no)')
        require(''.join(denial.split())=='success([thrown-yes],false).',denial)
        call(owner,f'self(S),send({target},probe(S)),receive({{alive->true}},[timeout(2),on_timeout(throw(http_exit_affected_target))])')
        allowed=http('admin',f'exit({target},admin_http_stop),AdminResult=passed')
        require(''.join(allowed.split())=='success([passed],false).',allowed)
        call(owner,f'receive({{down({target},{target},admin_http_stop)->true}},[timeout(2),on_timeout(throw(no_admin_http_exit))])')
        owner.halt()
        return dict(denial=denial,allowed=allowed)

rows=[]
provenance=dict(date=time.strftime('%Y-%m-%d'),platform=platform.platform(),
                harness_sha256=sha(__file__),cases_sha256=None,engines={},repetitions=args.repetitions,
                method='New ownership/lifecycle conformance cases on disposable loopback nodes; explicit owner-exit controls and no runtime introspection.',selected_cases=args.only or 'all')
(args.output/'case-inputs.json').write_text(json.dumps(CASES,indent=2)+'\n')
provenance['cases_sha256']=sha(args.output/'case-inputs.json')
report_path=args.output/'results.json'

def save():
    report_path.write_text(json.dumps(dict(provenance=provenance,results=rows),indent=2)+'\n')

with tempfile.TemporaryDirectory(prefix='paper-fixtures-') as folder:
    temp=Path(folder)
    for engine in ('swi','trealla'):
        proc=None;log=None
        try:
            node,proc,log=launch(engine,temp)
            provenance['engines'][engine]=node['provenance']
            for repetition in range(1,args.repetitions+1):
                functions=[('D1','Same principal across separate connections remains isolated',lambda:ownership_lifecycle.execute(actor.Candidate(node['url'].replace('http:','ws:')+'/ws','actor',5,node['tokens']['alice'],None,False,()),{'id':'OL-001'},node['tokens']['alice'])),
                           ('D2','Sibling actors inherit owner termination authority',lambda:assertion(node,'self(S),spawn(receive({never->true}),V,[monitor(true)]),spawn(exit(V,sibling_done),K,[monitor(true)]),receive({down(V,V,sibling_done)->true},[timeout(2),on_timeout(throw(no_sibling_exit))]),receive({down(K,K,true)->true},[timeout(2),on_timeout(throw(no_killer_finish))])')),
                           ('D3','Node-owner submitted goal retains cross-client termination authority',lambda:admin_control(node)),
                           ('D4','HTTP submitted goals enforce client authority and retain node-owner authority',lambda:http_control(node))]
                for ident,title,function in functions:
                    if args.only and ident not in args.only: continue
                    TRACE.clear()
                    started=time.monotonic()
                    row=dict(engine=engine,id=ident,title=title,repetition=repetition)
                    try: row.update(status='pass',observation=function())
                    except Exception as error: row.update(status='fail',error=f'{type(error).__name__}: {error}')
                    row.update(seconds=round(time.monotonic()-started,6),events=list(TRACE))
                    rows.append(row);save()
                    print(engine,ident,repetition,row['status'],row.get('error',''),flush=True)
        except Exception as error:
            rows.append(dict(engine=engine,id='FIXTURE',status='fail',error=f'{type(error).__name__}: {error}'));save()
            print(engine,'FIXTURE fail',error,flush=True)
        finally:
            if proc and proc.poll() is None:
                os.killpg(proc.pid,signal.SIGTERM)
                try:proc.wait(timeout=3)
                except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
            if log:log.close()
            save()
print('Report:',report_path,flush=True)
sys.exit(any(row['status']!='pass' for row in rows))
