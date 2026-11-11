:- module(http_field_order,[check/0]).
:- dynamic(rpc:resolve_rpc_uri/2).

% Trusted fixture only: replace URI resolution with a sentinel in this fresh
% process. No source guard or test hook is installed in the runtime or nodes.
check :-
    retractall(rpc:resolve_rpc_uri(_,_)),
    assertz((rpc:resolve_rpc_uri(_,_) :- throw(resolver_entered))),
    check_kind(rpc),
    check_kind(promise).

check_kind(Kind) :-
    findall(R,rpc:promise_state(R,_,_,_,_,_,_),Before),
    atom_codes(Bad,[98,97,100,10,118,97,108,117,101]),
    Options=[request_header('X-Probe'=first),request_header('x-probe'=Bad)],
    catch(invoke(Kind,X,Ref,Options),error(domain_error(http_header_value,Bad),_),Caught=true),
    Caught==true,var(X),var(Ref),
    findall(R,rpc:promise_state(R,_,_,_,_,_,_),After),Before==After,
    % Positive control proves the sentinel is installed on this public path.
    catch(invoke(Kind,Y,ValidRef,[request_header('X-Probe'=ok)]),resolver_entered,Reached=true),
    Reached==true,var(Y),var(ValidRef).

invoke(rpc,X,_,Options) :- rpc:rpc('http://example.invalid',X=ok,Options).
invoke(promise,X,Ref,Options) :- rpc:promise('http://example.invalid',X=ok,Ref,Options).
