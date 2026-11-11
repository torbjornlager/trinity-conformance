% Trusted fixture control stays on stdin; no test control endpoint is exposed.
:- module(discovery_control,[start/4]).
start(Host,Port,Ack,Updated) :-
    owner_spawn(Host,discovery_control:run(Host,Port,Ack,Updated),_,[]).
% Trusted fixture machinery uses Trealla's framework entry, never public spawn.
owner_spawn(trealla,Goal,Pid,Options) :- !,
    actors:spawn_runtime(Goal,Pid,['$entry_context'(caller)|Options]).
owner_spawn(swi,Goal,Pid,Options) :- actors:spawn(Goal,Pid,Options).

run(Host,Port,Ack,Updated) :-
    owner_spawn(Host,discovery_control:service_loop,Service,[monitor(true)]),
    actors:register(discovery_private,Service),
    actors:register_service(discovery_public,Service),
    acknowledge(Ack,0),loop(Host,Port,Ack,Updated,Service).
service_loop :- actors:receive({stop->true},[]).
loop(Host,Port,Ack,Updated,Service) :-
    read_term(user_input,Command,[]),
    (Command==end_of_file -> true
    ; Command=command(Token,Action),
      catch(perform_context(Action,Host,Port,Updated,Service),Error,
            (setup_call_cleanup(open(Ack,write,Out),
               (format(Out,'~d error ',[Token]),writeq(Out,Error)),close(Out)),
             throw(Error))),
      acknowledge(Ack,Token),loop(Host,Port,Ack,Updated,Service)).
% The trusted SWI controller selects its listener explicitly; it was created
% before startup and therefore has no inherited request/serving-node context.
perform_context(Action,swi,Port,Updated,Service) :- !,
    node_runtime_state:with_node_port_context(Port,discovery_control:perform(Action,swi,Port,Updated,Service)).
perform_context(Action,Host,Port,Updated,Service) :- perform(Action,Host,Port,Updated,Service).
perform(inspect,_,_,_,_).
% Shared source is replayed into each Trealla actor. Initializer behavior is
% outside this metadata fixture, so use the identical declarations without the
% initializer before the private-shadow stage. The preceding stage checks that
% metadata reads never rerun initialization; native parser tests cover scan-time
% rejection of executing initializers.
perform(prepare_private,swi,_,_,_).
perform(prepare_private,trealla,_,Updated,_) :-
    atom_concat(Directory,'updated.pl',Updated),
    atom_concat(Directory,'shared-runtime.pl',Runtime),
    isolation:configure_shared_db([Runtime]).
perform(unregister,_,_,_,_) :- actors:unregister_service(discovery_public).
perform(publish,_,_,_,Service) :- actors:register_service(discovery_public,Service).
perform(stop,_,_,_,Service) :-
    actors:send(Service,stop),
    actors:receive({down(Service,Service,true)->true},
                   [timeout(3),on_timeout(throw(discovery_service_down_missing))]).
perform(reconfigure,swi,Port,Updated,_) :-
    setup_call_cleanup(open(Updated,read,S),read_string(S,_,Text),close(S)),
    node_runtime_state:with_node_port_context(Port,node:set_node_shared_db(Text)),
    retire_fixture_declarations.
perform(reconfigure,trealla,_,Updated,_) :- isolation:configure_shared_db([Updated]).
perform(clear,swi,Port,_,_) :-
    node_runtime_state:with_node_port_context(Port,node:set_node_shared_db('')).
perform(clear,trealla,_,_,_) :- isolation:clear_shared_db.
% SWI reload replaces clauses but retains imports and empty dynamic declarations.
% Explicitly retire this fixture's two declarations to establish the same
% owner-controlled database state as Trealla's complete source replacement.
retire_fixture_declarations :-
    node:current_shared_db_module(Module),
    abolish(Module:last/2),abolish(Module:review_empty/1).
acknowledge(File,Token) :-
    flag(review_metadata_initializations,Count,Count),
    setup_call_cleanup(open(File,write,S),format(S,'~d ~d~n',[Token,Count]),close(S)).
