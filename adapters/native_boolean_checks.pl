:- module(native_boolean_checks,[negative/1,positive/0]).
:- meta_predicate negative(0).

% Trusted test process only. No guards or private resource access are sent to
% public nodes or installed in user source. Both hosts expose these inventories.
negative(Goal) :-
    actors:self(Self),actors:send(Self,boolean_probe_unrelated),
    resources(Before),
    call(Goal),
    resources(After),
    (Before==After -> true ; throw(boolean_resource_change(Before,After))),
    actors:receive({boolean_probe_unrelated -> true},
        [timeout(1),on_timeout(throw(unrelated_message_lost))]),
    actors:receive({'$call'(_,_) -> throw(invalid_call_was_sent)},[timeout(0)]).

resources(state(Pids,Monitors,Links,Promises,Queues)) :-
    actors:actors(Pids),
    findall(A-B-R,actors:monitor(A,B,R),Monitors),
    findall(A-B,actors:link(A,B),Links),
    findall(R,rpc:promise_state(R,_,_,_,_,_,_),Promises),
    findall(Q,message_queue_property(Q,size(_)),Queues).

positive :-
    forall(member(First-Second,[false-true,true-false]),
        (spawn_settings(First,Second),chart_settings(First,Second))),
    once_settings(false,true),once_settings(true,false).

% Keep the child alive while observing the actual link/monitor setting.
spawn_settings(First,Second) :-
    actors:self(Self),
    setup_call_cleanup(
      actors:spawn(actors:receive({stop -> true}),Pid,
        [link(First),link(Second),monitor(First),monitor(Second)]),
      ((First==true -> actors:link(Self,Pid),actors:monitor(Self,Pid,Pid)
       ; \+actors:link(Self,Pid),\+actors:monitor(Self,Pid,_))),
      actors:send(Pid,stop)),
    (First==true -> actors:receive({down(Pid,Pid,_)->true},
        [timeout(2),on_timeout(throw(missing_child_down))]);true).

chart_settings(First,Second) :-
    actors:self(Self),
    Text='<statechart version="0.2" initial="a"><state id="a"/></statechart>',
    setup_call_cleanup(
      statechart_actor:statechart_spawn(Pid,
        [src_text(Text),trace(First),trace(Second),io_target(Self),link(false)]),
      true,
      statechart_actor:statechart_halt(Pid,_,2)),
    collect_trace(Pid,0,Count),
    (First==true -> Count>0 ; Count=:=0).
collect_trace(Pid,N,Count) :-
    actors:receive({terminal_output(Pid,statechart_trace(_)) -> Next is N+1,
                     native_boolean_checks:collect_trace(Pid,Next,Count)},
      [timeout(0.05),on_timeout(Count=N)]).

once_settings(First,Second) :-
    setup_call_cleanup(
      toplevel_actors:toplevel_spawn(Pid,[session(true)]),
      (toplevel_actors:toplevel_call_synch(Pid,member(X,[a,b]),Answer,
         [template(X),limit(1),once(First),once(Second),timeout(2)]),
       (First==true -> Answer=success(Pid,[a],false)
                    ; Answer=success(Pid,[a],true))),
      toplevel_actors:toplevel_halt(Pid)).
