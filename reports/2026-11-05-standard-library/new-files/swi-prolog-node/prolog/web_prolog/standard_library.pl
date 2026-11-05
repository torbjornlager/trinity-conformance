:- module(standard_library, [maplist/6, maplist/7, maplist/8, countall/2]).

/** <module> Required library forms beyond the host's implicit imports

Closures keep the calling actor's module. These are ordinary meta-predicates,
so the node's existing goal and sandbox walkers inspect their callbacks.
*/
:- use_module(library(aggregate), [aggregate_all/3]).
:- meta_predicate maplist(5,?,?,?,?,?), maplist(6,?,?,?,?,?,?),
                  maplist(7,?,?,?,?,?,?,?), countall(0,?).

maplist(_, [], [], [], [], []).
maplist(G, [A|As], [B|Bs], [C|Cs], [D|Ds], [E|Es]) :-
    call(G,A,B,C,D,E), maplist(G,As,Bs,Cs,Ds,Es).
maplist(_, [], [], [], [], [], []).
maplist(G, [A|As], [B|Bs], [C|Cs], [D|Ds], [E|Es], [F|Fs]) :-
    call(G,A,B,C,D,E,F), maplist(G,As,Bs,Cs,Ds,Es,Fs).
maplist(_, [], [], [], [], [], [], []).
maplist(G, [A|As], [B|Bs], [C|Cs], [D|Ds], [E|Es], [F|Fs], [H|Hs]) :-
    call(G,A,B,C,D,E,F,H), maplist(G,As,Bs,Cs,Ds,Es,Fs,Hs).

countall(Goal, Count) :-
    aggregate_all(count, Goal, Actual), Count = Actual.
