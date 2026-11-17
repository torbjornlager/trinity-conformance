# Semi-stateful HTTP prompt correlation 0.1

This opt-in draft covers the JSON semi-stateful HTTP binding. It has a separate
[manifest](../cases/prompt-http-0.1.json) and result set from the actor interop
pack.

## Contract

1. Create a session with JSON `{"options":"[session(true)]","prompt_correlation":true}`
   on `POST /toplevel_spawn`. The session's prompts include an opaque, nonempty
   JSON string `prompt_ref`. Clients echo the string unchanged.
2. Reply with form fields `pid`, `format=json`, `input` and `prompt_ref` on
   `POST /toplevel_respond`. Send a period-terminated term for `read/1`.
   Only the current reference for that session can route input. Existing
   session ownership checks apply first.
3. Missing, stale, duplicate and wrong-session references return HTTP 400
   with `type: "error"` and `code: "invalid_prompt_ref"`. A rejection leaves the
   current prompt intact. A parse error also leaves its reference available
   for a corrected input.
4. A successfully routed reply consumes the reference. `responded` confirms
   routing. The next session event establishes whether the goal accepted
   the value. If the goal's input pattern rejects a routed value, the client
   can use Abort to recover.
5. After `/toplevel_abort` acknowledges Abort, a prompt from the aborted goal
   cannot accept a reply. The session PID remains usable and the next prompt
   has a fresh reference. Session termination also revokes the reference.
6. Explicit `prompt_correlation: false` selects PID-only replies and omits
   `prompt_ref` from prompt events. Omitting the option preserves each
   adapter's existing default. SWI-Prolog and Trealla use PID-only replies by default.
   The ECLiPSe adapter retains its existing numeric reference by default.
7. A client may send `/toplevel_abort` from another HTTP connection while
   `/toplevel_call`, `/toplevel_next` or `/toplevel_poll` is waiting for a
   goal that is still executing. When Abort interrupts the goal before the
   waiting request receives its event, both requests receive an `abort`
   event for that session PID. A new call can then run on the same session.
   The session's private database survives the interrupted query.
8. Abort also discards unread prompts and answers from the previous query,
   including an answer buffered before the client polled. Other sessions
   keep their own queued events and prompt references.
9. `/toplevel_halt` retires the session and its pending reference before
   returning `halted`. A fresh call or reply addressed to the retired PID
   returns an error with `code: "session_lost"` for the former owner.
   SWI-Prolog uses HTTP 200 for this event. ECLiPSe and Trealla use HTTP 404.
10. If two fresh requests send well-formed replies to the same current
    reference, exactly one receives `responded`. The other receives HTTP
    400 with `invalid_prompt_ref`. A malformed reply leaves a concurrent
    valid reply eligible to consume that reference.
11. If a valid reply races Abort, Abort returns `abort`. The reply can
    return `responded` if it claimed the reference first, or HTTP 400
    with `invalid_prompt_ref` if Abort revoked the reference first. After the
    Abort acknowledgement, the session can run a fresh call even while
    the earlier reply request is still returning. Any new prompt requires
    its own reference.
12. If a valid reply races Halt, Halt returns `halted`. The reply can
    return `responded` if it claimed the reference first. An overlapping
    request can see `invalid_prompt_ref` if the prompt has been revoked
    during teardown, or `session_lost` if the session has been retired.
    Fresh replies after the Halt acknowledgement return `session_lost`
    with the status in rule 9. The halted session's reference cannot
    answer a prompt in another session.
13. Halt can interrupt a running goal while Call, Next or Poll is waiting
    for an event. Halt returns `halted`, and the waiting request finishes
    without waiting for its ordinary timeout. Trealla and ECLiPSe return
    HTTP 404 with `session_lost`. SWI-Prolog returns HTTP 200 with its
    `down` event or `session_lost` if teardown removed the event queue
    first. The halted PID stays retired and other sessions keep their
    own prompts.
14. Abort and Halt may race while Call, Next or Poll is waiting for a
    running goal. Halt acknowledges with `halted` and retires the PID.
    The waiting request and Abort finish with `abort` if interruption
    is acknowledged first, or with the termination outcome in rule 13
    if retirement wins. Subsequent requests to that PID return
    `session_lost` as in rule 9.
15. Abort and Halt can also race with a correlated prompt pending. Both
    requests finish, and Halt retires the PID. A fresh reply carrying the
    old prompt reference returns `session_lost` after Halt acknowledges.
16. A valid correlated reply, Abort and Halt can race on separate
    connections. All three requests finish. Halt returns `halted`, and
    the overlapping reply can return `responded`, `invalid_prompt_ref`
    or `session_lost` according to when the prompt is revoked and the
    session retired. Replaying the same reply after Halt returns
    `session_lost`.
17. A malformed correlated reply racing Abort and Halt receives a parse
    error if it reaches parsing first, or `invalid_prompt_ref` or
    `session_lost` if the prompt or session has already been retired.
    Both control requests finish. After Halt, replay returns `session_lost`
    even when the reply contains malformed input.
18. A reply carrying a consumed reference is rejected when it races Abort
    and Halt with a newer prompt pending. It returns `invalid_prompt_ref`
    while the PID is live or `session_lost` once it is retired. Both control
    requests finish, and replay after Halt returns `session_lost`.
19. A reply carrying another session's prompt reference is rejected when
    it races Abort and Halt. All three requests finish. The reply returns
    `invalid_prompt_ref` while its destination PID is live or `session_lost`
    after retirement. Replaying it to the halted PID returns `session_lost`,
    and the other session still accepts the correct reply to its prompt.
20. In a correlated session, a reply with no `prompt_ref` is rejected
    when it races Abort and Halt. All three requests finish. The reply
    returns `invalid_prompt_ref` while the destination PID is live or
    `session_lost` after retirement. Replaying it after Halt returns
    `session_lost`.

The status rules above describe fresh requests. SWI's optional
`Web-Prolog-Ack` retry facility can return a cached event without executing
a command again. This pack sends fresh requests.

## Local verification

Start an ECLiPSe adapter with an extracted Linux ARM64 runtime and Docker.

```sh
python3 /path/to/trinity-demonstrator/experiments/eclipse-clp/isotope_http.py \
  /path/to/extracted-eclipse-runtime --port 18088
```

In another terminal, start a disposable native SWI-Prolog node.

```sh
swipl -q -s /path/to/swi-prolog-node/load.pl \
  -g 'node(18089,[profile(isotope),auth(dev)]),thread_get_message(stop)'
```

Start Trealla's native node with its HTTP session routes enabled.

```sh
cd /path/to/trealla-port
tpl -g "use_module(web_prolog),web_prolog_node(18090,[profile(isotope),auth(dev),bind_address('127.0.0.1'),http_sessions(true)])"
```

From the conformance checkout, run the same cases on all three endpoints.

```sh
python3 runner/prompt_http.py --swi http://127.0.0.1:18089 \
  --eclipse http://127.0.0.1:18088 --trealla http://127.0.0.1:18090
```

PT-004 checks a stale reply across Abort on the same PID, an omitted
reference, cross-session references in both directions, a malformed input
followed by a valid retry, duplicate replies before and after polling, and
explicit PID-only mode. The successful bindings demonstrate which reply
actually reached each goal.

The runner also verifies omitted-option PID-only mode on SWI-Prolog and Trealla.

PT-005 starts a call on one connection and aborts it from another. It
expects both Abort events before the ordinary call wait could expire. The
fresh call reads a private fact written by the interrupted goal and adds a
new binding. The result proves that the first goal ran and the same session
handled the new call.

PT-006 covers two continuation paths on one session. Next resumes a
nondeterministic goal after its first answer. Poll waits for a goal that
resumed after a correlated prompt reply. After each Abort, a fresh call
reads the private fact written by the interrupted continuation. A final
prompt rejects the old reference and accepts its own reply.

PT-007 lets two sessions resume after prompt replies without polling.
Abort clears the unread prompt on one session, and the other session's
unread prompt still accepts its reply. The case also lets a resumed goal
finish before Abort and checks that its unread answer cannot appear as
the result of the next call. Private facts confirm the aborted session
ran both continuations.

PT-008 halts one of two sessions while both have prompts pending. A late
reply and a new call on the retired PID return `session_lost`. The survivor
rejects the retired session's reference and accepts its own reply.

PT-009 sends competing replies from two HTTP connections. It checks that
the goal binds the value acknowledged by `responded` and waits for the
correct reply to its next prompt. It also races a malformed reply against
a valid one and checks that the valid value reaches the goal.

PT-010 races a valid reply to the first of two reads against Abort. On
receiving the Abort acknowledgement, it starts a fresh call on the same
PID before collecting the reply's result. It then verifies that the
fresh call's prompt rejects the old reference and accepts the new one.

PT-011 races Halt against a valid prompt reply. It checks a late reply
immediately after the Halt acknowledgement and verifies that a separate
session rejects the retired reference while keeping its own prompt usable.

PT-012 interrupts a nonterminating goal during Call, during Next after its
first answer, and during Poll after a prompt reply. It checks that both
requests finish, that a new call to the retired PID fails, and that a
separate session still accepts its own prompt reply.

PT-013 races Abort and Halt from separate connections during a
nonterminating Call. It requires all three requests to finish before
the ordinary wait expires, then sends a fresh Call and Abort to confirm
that the halted PID stays retired.

PT-014 repeats the race during Next after the first answer and during
Poll after a correlated prompt reply. In each scenario, a fresh Call,
Abort and the original continuation route all reject the retired PID.

PT-015 leaves a correlated prompt unanswered while racing Abort and Halt
from separate connections. After both finish, it sends the original
reference to the halted PID and requires `session_lost`.

PT-016 starts a valid reply, Abort and Halt together while a correlated
prompt is pending. It varies the submission order and checks that all
three requests finish, then resends the identical reply to the halted PID.

PT-017 repeats that race with a malformed term and the current reference.
It checks that the reply is rejected during the race and that replaying
the same malformed request after Halt returns `session_lost`.

PT-018 answers the first of two prompts, then races a replay of that reply
against Abort and Halt while the second prompt is pending. All three
requests finish, the stale reply is rejected, and replay after Halt
returns `session_lost`.

PT-019 opens prompts in two sessions and sends one session's reference to
the other while racing Abort and Halt there. It replays the wrong-session
reply to the halted PID, then checks the surviving prompt's answer binding.
PT-020 leaves a correlated prompt pending and sends a well-formed term
without a reference while Abort and Halt race. It checks that the reply
is rejected and that replaying the identical request after Halt returns
`session_lost`.

PT-016 through PT-020 each try all six submission orders once in a full
run so the suite fits within the default session spawn quota.
