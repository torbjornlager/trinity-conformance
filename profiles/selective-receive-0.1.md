# Selective receive 0.1 — separate draft conformance pack

This draft selects documented public semantics from the shared
[receive/1-2 contract](https://github.com/torbjornlager/trinity-demonstrator/blob/main/web/manual.html#receive/1-2).
It is separately versioned and does not amend baseline 0.1 or add an advertised
node profile. Each assertion is required within the selected pack. Both native
ACTOR candidates execute the identical [goals](../cases/selective-receive-0.1.json).

| Case | Selected observation |
| --- | --- |
| SR-001 | A ground pattern cannot bind a variable in a message; a repeated-variable pattern cannot merge distinct message variables. General matching preserves shared/distinct variables and leaves sender variables independent. |
| SR-002 | Selecting a later target preserves the order of three earlier deferred messages and a following native-queue message. |
| SR-003 | Failing and ordinary throwing guards retain the candidate, roll back pattern/guard bindings and do not duplicate it. |
| SR-004 | A nondeterministic guard uses its first solution only, and the body sees that solution's bindings. |
| SR-005 | Body failure or an ordinary exception consumes the selected message; other messages remain available. |
| SR-006 | A body cut leaves both the caller's member/2 alternatives and its enclosing disjunction available. |

Pids remain opaque. All messages are sent by the caller to itself, making them
available before the zero-time polls. No sleeps, transport peers, private mailbox
inspection, runtime imports or destructive guard side effects are needed.
SR-003's tentative variable bindings and literal throw test the documented guard
rules; no observable external action occurs in those guards.

SR-004 intentionally enumerates any receive alternatives and asserts the exact
one-element result. SR-006 enumerates the caller alternatives to detect a cut
escaping its body scope. These are contract observations, not once/1 wrappers
that hide unexpected nondeterminism. Every case must finish as one final successful
query without a residual continuation, as checked by the existing runner.

Cases have fresh sessions and consume their expected data; linked-session and
disposable-node teardown bound failed fixtures. Scope excludes interruption and
handoff stress, abort/termination/resource-limit control exceptions, timeout
accuracy under traffic, clause-priority completeness, arbitrary mailbox load,
remote delivery, browser execution, GNU ACTOR, security and lifecycle certification.
Unknown differences stay required failures; no runtime repair is part of this batch.
