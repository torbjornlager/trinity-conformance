% Trusted owner source: metadata requests must not rerun initialization.
:- use_module(library(lists),[last/2]).
:- dynamic review_empty/1.
review_fact(a).
review_rule(X):-review_fact(X).
review_grammar(X) --> [X].
provides(ignored/99).
relation_filter(review_fact(_)).
'$review_private'(hidden).
