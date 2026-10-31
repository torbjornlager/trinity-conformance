"""Public ACTOR contracts across two authenticated client connections.

No runtime introspection. Timeouts bound test observations, not the semantics
of all hosts. The two execution-only tokens must name distinct principals.
"""
from dataclasses import replace
import socket
import run as actor


def validate(token, observer_token):
    if not token or not observer_token or token == observer_token:
        raise ValueError('ownership-lifecycle-0.1 requires two distinct execution-only principal tokens')


def shell(session):
    session.send(dict(command='toplevel_spawn', options='[session(true)]'))
    event = session.recv('spawned')
    actor.require('pid' in event, f'missing opaque pid: {event!r}')
    session.shell = event['pid']


def call(session, goal):
    session.call(goal, '[limit(1)]')
    answer = session.recv_type('success', limit=64)
    actor.require(answer.get('more') is False, f'unexpected alternatives: {answer!r}')
    return answer


def value(answer, key):
    return actor.row_value(answer, key)


def worker(owner):
    reply = call(owner, 'self(S),spawn((self(Me),send(S,ready(Me)),repeat,receive({probe(Who)->send(Who,alive),fail;stop->true}),!),Target,[monitor(true)]),receive({ready(Target)->true},[timeout(2),on_timeout(throw(no_readiness))])')
    return value(reply, 'Target')


def watch(observer, target):
    return value(call(observer, f'monitor({target},Ref)'), 'Ref')


def take_down(observer, target, ref, reason):
    reply = call(observer, f'receive({{down({target},{ref},Reason)->true}},[timeout(3),on_timeout(throw(no_original_notification))]),Reason=={reason},monitor({target},Again),receive({{down({target},Again,no_process)->true}},[timeout(2),on_timeout(throw(no_missing_notification))])')
    # A second immediate receive cannot find a duplicate original notification.
    call(observer, f'receive({{down({target},{ref},_)->throw(duplicate_notification)}},[timeout(0)])')
    return reply


def denied_exit(owner, observer):
    target = worker(owner)
    # Capture return vs throw before classification; never manufacture an error
    # by unifying an unbound exception variable with the expected error term.
    result = call(observer, f'monitor({target},Ref),catch((exit({target},forbidden),Outcome=returned),E,Outcome=thrown),(nonvar(E),E=error(permission_error(exit,actor,_),_)->Denial=yes;Denial=no)')
    ref = value(result, 'Ref')
    # Observe survival independently, even when the denial assertion will fail.
    survival = call(owner, f'self(S),send({target},probe(S)),receive({{alive->Survived=yes}},[timeout(2),on_timeout(Survived=no)])')
    diagnostics = dict(exit=result, survival=survival)
    actor.require(value(result, 'Outcome') == 'thrown' and value(result, 'Denial') == 'yes', f'foreign exit was not denied; observations={diagnostics!r}')
    actor.require(value(survival, 'Survived') == 'yes', f'foreign exit affected target; observations={diagnostics!r}')
    call(owner, f'exit({target},owner_stop)')
    take_down(observer, target, ref, 'owner_stop')
    return diagnostics


def computing_tree(owner, observer, generations):
    # Both levels announce readiness before entering pure Prolog computation.
    if generations == 1:
        goal = 'self(S),spawn((self(Me),send(S,ready(Me)),repeat,fail),Target,[monitor(true)]),receive({ready(Target)->true},[timeout(2),on_timeout(throw(no_readiness))])'
    else:
        goal = 'self(S),spawn((self(Me),spawn((self(G),send(S,grand_ready(G)),repeat,fail),Grand),send(S,ready(Me,Grand)),repeat,fail),Target,[monitor(true)]),receive({ready(Target,Grand)->true},[timeout(2),on_timeout(throw(no_child_readiness))]),receive({grand_ready(Grand)->true},[timeout(2),on_timeout(throw(no_grand_readiness))])'
    result = call(owner, goal)
    targets = [value(result, 'Target')]
    if generations == 2:
        targets.append(value(result, 'Grand'))
    return [(target, watch(observer, target)) for target in targets]


def lifecycle(owner, observer, disconnect=False, generations=1):
    targets = computing_tree(owner, observer, generations)
    if disconnect:
        assert owner.ws
        owner.ws.sock.shutdown(socket.SHUT_RDWR)
        owner.ws.sock.close()
        owner.ws = None
    else:
        call(owner, f'exit({targets[0][0]},kill)')
    observed = []
    for target, ref in targets:
        observed.append(take_down(observer, target, ref, 'kill'))
    # Observer survives the original connection's teardown and remains usable.
    call(observer, 'ObserverStillUsable=yes')
    return dict(targets=targets, observations=observed)


def execute(candidate, metadata, observer_token):
    with actor.Harness(candidate) as owner, actor.Harness(replace(candidate, token=observer_token)) as observer:
        shell(owner)
        shell(observer)
        case = metadata['id']
        if case == 'OL-001':
            result = denied_exit(owner, observer)
        elif case == 'OL-002':
            result = lifecycle(owner, observer)
        elif case == 'OL-003':
            result = lifecycle(owner, observer, disconnect=True)
        elif case == 'OL-004':
            result = lifecycle(owner, observer, disconnect=True, generations=2)
        else:
            raise ValueError('unknown ownership/lifecycle case: '+case)
        if owner.ws:
            owner.halt()
        observer.halt()
        return result
