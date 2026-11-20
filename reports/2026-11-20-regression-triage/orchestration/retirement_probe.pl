:- module(retirement_probe,[main/0]).
:- use_module('/opt/swi-prolog-node/prolog/web_prolog/actors.pl').
:- dynamic held/6.
:- multifile actors:hook_send/2,actors:hook_pid_retired/1.
actors:hook_send(To,down(P,Ref,Why)) :-
    retirement_probe:held(To,P,Ref,Main,Gate,_),!,
    thread_send_message(Main,down(P,Ref,Why)),
    thread_get_message(Gate,release).
actors:hook_pid_retired(P) :-
    retirement_probe:held(_,P,_,_,_,Events),
    thread_send_message(Events,retired(P)).
main :-
    self(Self),thread_self(Main),message_queue_create(Gate),message_queue_create(Events),
    setup_call_cleanup(
      (spawn(receive({finish->true}),P),monitor(P,Ref),assertz(held(Self,P,Ref,Main,Gate,Events))),
      setup_call_cleanup(true,
        (send(P,finish),receive({down(P,Ref,true)->true},[timeout(3),on_timeout(throw(missing_down))]),
         actors(Visible),(memberchk(P,Visible)->Result=still_visible;Result=retired),
         format('monitor_delivery_actor_state(~q).~n',[Result])),
        (thread_send_message(Gate,release),thread_get_message(Events,retired(P),[timeout(3)]))),
      (retractall(held(_,_,_,_,_,_)),message_queue_destroy(Gate),message_queue_destroy(Events))),
    halt.
