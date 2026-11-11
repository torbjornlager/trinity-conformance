% Identical policy assertions; the adapter supplies only the host module name.
:- module(reference_profile_policy,[check/3]).

check(Module, Profile, Expected) :-
    catch((call(Module:profile_check_goal(Profile,make_ref(Ref))),Outcome=admitted),
          Error, (denial(Profile,Error),Outcome=denied)),
    nonvar(Outcome),Outcome==Expected,var(Ref).

denial(Profile,error(profile_violation(Profile,goal(make_ref(_))),_)).
% Trealla does not serve RELATION; reject only the exact unsupported primitive.
denial(relation,error(existence_error(procedure,make_ref/1),_)).
