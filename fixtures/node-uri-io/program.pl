nu_done(P) :-
    receive({down(P,_,Why) -> (Why==true -> true ; throw(unexpected_exit(P,Why)))},
            [timeout(4),on_timeout(throw(missing_down(P)))]).
nu_baseline(Before) :- actors(After),sort(Before,B),sort(After,A),
    (A==B -> true ; throw(actor_baseline_changed(B,A))).
nu_canonical(P,URI) :- (integer(P) -> true ; P=_@Node,Node==URI).
nu_id(P,Id) :- (integer(P) -> Id=P ; P=Id@_).
nu_visible(P,Actors) :- nu_id(P,Id),member(Q,Actors),nu_id(Q,Id),!.
nu_emit(X) :- writeln(X).
nu_write(X) :- write(X).
nu_format :- format('format probe.~n').
nu_parent(Owner,Home) :-
    Options=[node(Home),src_predicates([nu_emit/1]),monitor(true)],
    spawn(nu_emit(nested),C,Options),
    nu_done(C),send(Owner,nested_done).
nu_ping(0,Pong) :- send(Pong,finished),format('Ping finished.~n').
nu_ping(N,Pong) :- self(Me),writeln(Me),send(Pong,ping(Me)),
    receive({pong -> format('Ping received pong.~n')},[timeout(4),on_timeout(throw(missing_pong))]),
    N1 is N-1,nu_ping(N1,Pong).
nu_pong :- receive({finished -> format('Pong finished.~n') ;
    ping(Ping) -> format('Pong received ping.~n'),send(Ping,pong),nu_pong}).
