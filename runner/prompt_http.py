"""Run the prompt HTTP pack against explicit semi-stateful fixture endpoints."""
import argparse
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from contextlib import ExitStack, contextmanager
from functools import lru_cache
from http.cookiejar import CookieJar
import json
from itertools import permutations
from pathlib import Path
from threading import Barrier
from time import monotonic, sleep
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener

MANIFEST = Path(__file__).resolve().parents[1] / "cases/prompt-http-0.1.json"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


@lru_cache(maxsize=None)
def endpoint_client(base):
    # Each endpoint has its own visitor, even if two fixtures share a host.
    return build_opener(HTTPCookieProcessor(CookieJar()))


def post_response(base, command, fields, *, client=None):
    if command == "spawn":
        body = json.dumps(fields).encode()
        content_type = "application/json"
    else:
        body = urlencode(fields).encode()
        content_type = "application/x-www-form-urlencoded"
    request = Request(f"{base.rstrip('/')}/toplevel_{command}", body,
                      {"Content-Type": content_type})
    try:
        response = (client or endpoint_client(base)).open(request, timeout=8)
    except HTTPError as error:
        response = error
    except OSError as error:
        raise AssertionError(f"{command}: {error}") from error
    with response:
        body = response.read()
        try:
            event = json.loads(body)
        except ValueError as error:
            raise AssertionError(f"{command}: HTTP {response.code} returned {body[:300]!r}") from error
        return response.code, event


def post(base, command, fields, status=200):
    code, event = post_response(base, command, fields)
    require(code == status, f"{command}: expected HTTP {status}, got {code}: {event!r}")
    return event


def spawn_session(base, correlated):
    options = {"options": "[session(true)]"}
    if correlated is not None:
        options["prompt_correlation"] = correlated
    event = post(base, "spawn", options)
    require(event["type"] == "spawned", repr(event))
    return {"pid": event["pid"], "format": "json"}


@contextmanager
def session(base, correlated):
    fields = spawn_session(base, correlated)
    try:
        yield fields
    finally:
        expect_event(post(base, "halt", fields), fields, "halted")


def expect_event(event, fields, kind):
    require(event.get("type") == kind and event.get("pid") == fields["pid"],
            f"expected {kind} for PID {fields['pid']!r}: {event!r}")


def prompt_ref(event, fields, correlated=True):
    expect_event(event, fields, "prompt")
    if not correlated:
        require("prompt_ref" not in event, repr(event))
        return None
    ref = event.get("prompt_ref")
    require(isinstance(ref, str) and bool(ref), f"expected opaque string reference: {event!r}")
    return ref


def open_prompt(base, fields, correlated=True, goal="read(X)"):
    event = post(base, "call", {**fields, "goal": goal})
    return prompt_ref(event, fields, correlated)


def reject(base, fields, ref=None):
    response = {**fields, "input": "wrong."}
    if ref is not None:
        response["prompt_ref"] = ref
    event = post(base, "respond", response, 400)
    expect_invalid_ref(event)


def expect_invalid_ref(event):
    require(event.get("type") == "error" and event.get("code") == "invalid_prompt_ref",
            f"expected invalid_prompt_ref: {event!r}")


def respond(base, fields, value, ref=None):
    response = {**fields, "input": f"{value}."}
    if ref is not None:
        response["prompt_ref"] = ref
    expect_event(post(base, "respond", response), fields, "responded")


def answer(base, fields, value, ref=None):
    respond(base, fields, value, ref)
    if ref is not None:
        reject(base, fields, ref)
    event = post(base, "poll", fields)
    expect_event(event, fields, "success")
    require(event.get("data") == [{"X": value}] and event.get("more") is False,
            f"wrong prompt answer: {event!r}")


def check(base, require_by_default=False):
    with ExitStack() as stack:
        correlation = None if require_by_default else True
        main = stack.enter_context(session(base, correlation))
        other = stack.enter_context(session(base, correlation))
        old_ref = open_prompt(base, main)
        expect_event(post(base, "abort", main), main, "abort")
        new_ref = open_prompt(base, main)
        require(new_ref != old_ref, "Abort allowed reference reuse")
        other_ref = open_prompt(base, other)
        require(other_ref != new_ref, "sessions issued the same prompt reference")
        reject(base, main, old_ref)
        reject(base, main)
        reject(base, main, other_ref)
        reject(base, other, new_ref)
        invalid = post(base, "respond", {**main, "input": "broken(.", "prompt_ref": new_ref})
        require(invalid.get("type") == "error", repr(invalid))
        answer(base, main, "fresh", new_ref)
        reject(base, main, new_ref)
        answer(base, other, "independent", other_ref)
        old_client = stack.enter_context(session(base, False))
        if require_by_default:
            ref = open_prompt(base, old_client)
            reject(base, old_client)
            answer(base, old_client, "still_correlated", ref)
        else:
            open_prompt(base, old_client, correlated=False)
            answer(base, old_client, "legacy")


def interrupt_wait(base, fields, command, **params):
    with ThreadPoolExecutor(max_workers=1) as client:
        started = monotonic()
        running = client.submit(post, base, command, {**fields, **params})
        try:
            early = running.result(timeout=0.2)
        except FutureTimeout:
            pass
        else:
            raise AssertionError(f"{command} returned before Abort: {early!r}")
        expect_event(post(base, "abort", fields), fields, "abort")
        try:
            interrupted = running.result(timeout=2)
        except FutureTimeout as error:
            raise AssertionError(f"{command} did not return its Abort event") from error
        expect_event(interrupted, fields, "abort")
        require(monotonic() - started < 3, f"Abort did not beat the {command} wait")


def expect_answer(event, fields, bindings, more=False):
    expect_event(event, fields, "success")
    require(event.get("data") == [bindings] and event.get("more") is more,
            f"expected answer {bindings!r} with more={more}: {event!r}")


def check_running_abort(base):
    with session(base, True) as fields:
        interrupt_wait(base, fields, "call", goal="(assertz(pt005_started(written)), repeat, fail)")
        fresh = post(base, "call", {**fields, "goal": "once(pt005_started(X)), Y=fresh"})
        expect_answer(fresh, fields, {"X": "written", "Y": "fresh"})


def check_continuation_abort(base):
    with session(base, True) as fields:
        goal = "(X=first ; assertz(pt006_next(entered)), repeat, fail)"
        first = post(base, "call", {**fields, "goal": goal, "limit": 1})
        expect_answer(first, fields, {"X": "first"}, more=True)
        interrupt_wait(base, fields, "next")
        fresh = post(base, "call", {**fields, "goal": "once(pt006_next(X))"})
        expect_answer(fresh, fields, {"X": "entered"})

        ref = open_prompt(base, fields, goal="read(X), assertz(pt006_poll(X)), repeat, fail")
        respond(base, fields, "entered", ref)
        interrupt_wait(base, fields, "poll")
        fresh = post(base, "call", {**fields, "goal": "once(pt006_poll(X))"})
        expect_answer(fresh, fields, {"X": "entered"})
        new_ref = open_prompt(base, fields)
        require(new_ref != ref, "Abort allowed reference reuse after Poll")
        reject(base, fields, ref)
        answer(base, fields, "fresh", new_ref)


def check_buffered_abort(base):
    goal = "read(X), assertz(pt007_resumed(X)), read(Y)"
    with ExitStack() as stack:
        main = stack.enter_context(session(base, True))
        control = stack.enter_context(session(base, True))
        old_ref = open_prompt(base, main, goal=goal)
        control_first = open_prompt(base, control, goal=goal)
        respond(base, main, "aborted", old_ref)
        respond(base, control, "control", control_first)

        # Give the continuations time to enqueue their next prompts without
        # polling either session before Abort.
        sleep(0.2)
        expect_event(post(base, "abort", main), main, "abort")
        fresh = post(base, "call", {**main, "goal": "once(pt007_resumed(X))"})
        expect_answer(fresh, main, {"X": "aborted"})

        control_ref = prompt_ref(post(base, "poll", control), control)
        new_ref = open_prompt(base, main)
        reject(base, main, old_ref)
        reject(base, main, control_ref)
        answer(base, main, "fresh", new_ref)
        respond(base, control, "retained", control_ref)
        expect_answer(post(base, "poll", control), control, {"X": "control", "Y": "retained"})

        goal = "read(X), assertz(pt007_finished(X)), Y=old_answer"
        ref = open_prompt(base, main, goal=goal)
        respond(base, main, "completed", ref)
        sleep(0.2)
        expect_event(post(base, "abort", main), main, "abort")
        fresh = post(base, "call", {**main, "goal": "once(pt007_finished(X)), Y=new_answer"})
        expect_answer(fresh, main, {"X": "completed", "Y": "new_answer"})


def check_halted_prompt(base, lost_status):
    with session(base, True) as survivor:
        survivor_ref = open_prompt(base, survivor)
        with session(base, True) as halted:
            halted_ref = open_prompt(base, halted)
        require(halted_ref != survivor_ref, "sessions issued the same prompt reference")

        late = {**halted, "input": "late.", "prompt_ref": halted_ref}
        attempts = (("respond", late), ("call", {**halted, "goal": "X=unexpected"}))
        for command, fields in attempts:
            event = post(base, command, fields, lost_status)
            expect_session_lost(event)
        reject(base, survivor, halted_ref)
        answer(base, survivor, "survived", survivor_ref)


def expect_session_lost(event):
    require(event.get("type") == "error" and event.get("code") == "session_lost",
            f"expected session_lost after Halt: {event!r}")


def race_requests(base, clients, requests):
    start = Barrier(len(requests))

    def submit(command, fields):
        start.wait(timeout=2)
        return post_response(base, command, fields)

    return [clients.submit(submit, command, fields) for command, fields in requests]


def race_replies(base, fields, ref, clients, inputs):
    requests = [("respond", {**fields, "input": text, "prompt_ref": ref}) for text in inputs]
    return [request.result() for request in race_requests(base, clients, requests)]


def check_competing_replies(base):
    with session(base, True) as fields, ThreadPoolExecutor(max_workers=2) as clients:
        for _ in range(8):
            ref = open_prompt(base, fields, goal="read(X), read(Y)")
            values = ("left", "right")
            results = race_replies(base, fields, ref, clients, [f"{value}." for value in values])
            require(sorted(code for code, _ in results) == [200, 400],
                    f"expected one accepted and one rejected reply: {results!r}")
            for value, (code, event) in zip(values, results):
                if code == 200:
                    expect_event(event, fields, "responded")
                    winner = value
                else:
                    expect_invalid_ref(event)

            fresh_ref = prompt_ref(post(base, "poll", fields), fields)
            require(fresh_ref != ref, "the next prompt reused the consumed reference")
            reject(base, fields, ref)
            respond(base, fields, "second", fresh_ref)
            expect_answer(post(base, "poll", fields), fields, {"X": winner, "Y": "second"})

        ref = open_prompt(base, fields)
        malformed, valid = race_replies(base, fields, ref, clients, ("broken(.", "valid."))
        require(malformed[1].get("type") == "error", f"accepted malformed input: {malformed!r}")
        require(valid[0] == 200, f"malformed input blocked a valid reply: {valid!r}")
        expect_event(valid[1], fields, "responded")
        expect_answer(post(base, "poll", fields), fields, {"X": "valid"})


def check_reply_racing_abort(base):
    with session(base, True) as fields, ThreadPoolExecutor(max_workers=2) as clients:
        for round_index in range(8):
            old_ref = open_prompt(base, fields, goal="read(X), read(Y)")
            reply = {**fields, "input": "old.", "prompt_ref": old_ref}
            abort_request = ("abort", fields)
            reply_request = ("respond", reply)
            if round_index % 2:
                replying, aborting = race_requests(base, clients, (reply_request, abort_request))
            else:
                aborting, replying = race_requests(base, clients, (abort_request, reply_request))
            code, event = aborting.result()
            require(code == 200, f"Abort failed during a reply: HTTP {code}: {event!r}")
            expect_event(event, fields, "abort")

            fresh_ref = open_prompt(base, fields)
            require(fresh_ref != old_ref, "Abort allowed reference reuse after a racing reply")
            code, event = replying.result()
            if code == 200:
                expect_event(event, fields, "responded")
            else:
                require(code == 400, f"unexpected racing reply: HTTP {code}: {event!r}")
                expect_invalid_ref(event)
            reject(base, fields, old_ref)
            answer(base, fields, "fresh", fresh_ref)


def expect_racing_reply(response, fields, lost_status, reply_kind="valid"):
    code, event = response
    if code == 200 and event.get("type") == "responded":
        require(reply_kind == "valid", f"accepted {reply_kind} reply: {event!r}")
        expect_event(event, fields, "responded")
    elif reply_kind == "malformed" and code == 200 and event.get("type") == "error" and "code" not in event:
        data = event.get("data")
        # The ECLiPSe bridge reports parse failure as "Invalid request or goal".
        require(
            isinstance(data, str) and (data == "Invalid request or goal" or
                                       "syntax error" in data.lower() or "syntax_error(" in data),
            f"expected a parse error for malformed input: {event!r}",
        )
    elif code == 400:
        expect_invalid_ref(event)
    else:
        require(code == lost_status, f"unexpected racing reply: HTTP {code}: {event!r}")
        expect_session_lost(event)


def check_reply_racing_halt(base, lost_status):
    with session(base, True) as survivor, ThreadPoolExecutor(max_workers=2) as clients:
        survivor_ref = open_prompt(base, survivor)
        for round_index in range(8):
            fields = spawn_session(base, True)
            halted = False
            try:
                ref = open_prompt(base, fields, goal="read(X), read(Y)")
                reply = {**fields, "input": "old.", "prompt_ref": ref}
                halt_request = ("halt", fields)
                reply_request = ("respond", reply)
                if round_index % 2:
                    replying, halting = race_requests(base, clients, (reply_request, halt_request))
                else:
                    halting, replying = race_requests(base, clients, (halt_request, reply_request))
                code, event = halting.result()
                require(code == 200, f"Halt failed during a reply: HTTP {code}: {event!r}")
                expect_event(event, fields, "halted")
                halted = True
                expect_session_lost(post(base, "respond", reply, lost_status))
                expect_racing_reply(replying.result(), fields, lost_status)
                reject(base, survivor, ref)
            finally:
                if not halted:
                    post_response(base, "halt", fields)
        answer(base, survivor, "survived", survivor_ref)


def prepare_running_request(base, fields, command):
    if command == "call":
        return {**fields, "goal": "repeat, fail"}
    if command == "next":
        goal = "(X=first ; repeat, fail)"
        first = post(base, "call", {**fields, "goal": goal, "limit": 1})
        expect_answer(first, fields, {"X": "first"}, more=True)
    else:
        ref = open_prompt(base, fields, goal="read(X), repeat, fail")
        respond(base, fields, "entered", ref)
    return fields


def check_running_halt(base, lost_status):
    with session(base, True) as survivor, ThreadPoolExecutor(max_workers=1) as client:
        survivor_ref = open_prompt(base, survivor)
        for command in ("call", "next", "poll"):
            fields = spawn_session(base, True)
            halted = False
            try:
                request = prepare_running_request(base, fields, command)
                started = monotonic()
                running = client.submit(post, base, command, request, lost_status)
                try:
                    early = running.result(timeout=0.2)
                except FutureTimeout:
                    pass
                else:
                    raise AssertionError(f"{command} returned before Halt: {early!r}")

                expect_event(post(base, "halt", fields), fields, "halted")
                halted = True
                try:
                    event = running.result(timeout=2)
                except FutureTimeout as error:
                    raise AssertionError(f"{command} did not finish after Halt") from error
                if lost_status == 200 and event.get("type") == "down":
                    expect_event(event, fields, "down")
                else:
                    expect_session_lost(event)
                require(monotonic() - started < 3, f"Halt did not beat the {command} wait")
                expect_session_lost(post(base, "call", {**fields, "goal": "true"}, lost_status))
            finally:
                if not halted:
                    post_response(base, "halt", fields)
        answer(base, survivor, "survived", survivor_ref)


def race_abort_and_halt(base, clients, fields, round_index):
    abort_request = ("abort", fields)
    halt_request = ("halt", fields)
    if round_index % 2:
        halting, aborting = race_requests(base, clients, (halt_request, abort_request))
        return aborting, halting
    return race_requests(base, clients, (abort_request, halt_request))


def expect_interrupted(response, fields, lost_status, command):
    code, event = response
    if code == 200 and event.get("type") == "abort":
        expect_event(event, fields, "abort")
    elif lost_status == 200 and code == 200 and event.get("type") == "down":
        expect_event(event, fields, "down")
    else:
        require(code == lost_status, f"{command}: unexpected HTTP {code}: {event!r}")
        expect_session_lost(event)


def check_abort_racing_halt(base, lost_status, command="call"):
    with ThreadPoolExecutor(max_workers=3) as clients:
        for round_index in range(8):
            fields = spawn_session(base, True)
            halted = False
            try:
                request_fields = prepare_running_request(base, fields, command)
                running = clients.submit(post_response, base, command, request_fields)
                try:
                    early = running.result(timeout=0.2)
                except FutureTimeout:
                    pass
                else:
                    raise AssertionError(f"{command} returned before the race: {early!r}")

                started = monotonic()
                aborting, halting = race_abort_and_halt(base, clients, fields, round_index)
                code, event = halting.result(timeout=2.5)
                require(code == 200, f"Halt failed in the race: HTTP {code}: {event!r}")
                expect_event(event, fields, "halted")
                halted = True

                for pending_command, request in ((command, running), ("abort", aborting)):
                    response = request.result(timeout=max(0, started + 2.5 - monotonic()))
                    expect_interrupted(response, fields, lost_status, pending_command)
                require(monotonic() - started < 2.5, "Abort and Halt did not beat the ordinary wait")
                expect_session_lost(post(base, "call", {**fields, "goal": "true"}, lost_status))
                expect_session_lost(post(base, "abort", fields, lost_status))
                if command != "call":
                    expect_session_lost(post(base, command, fields, lost_status))
            except FutureTimeout as error:
                raise AssertionError(f"{command}, Abort and Halt did not all finish promptly") from error
            finally:
                if not halted:
                    post_response(base, "halt", fields)


def check_prompt_abort_racing_halt(base, lost_status):
    with ThreadPoolExecutor(max_workers=2) as clients:
        for round_index in range(8):
            fields = spawn_session(base, True)
            halted = False
            try:
                ref = open_prompt(base, fields)
                deadline = monotonic() + 2.5
                aborting, halting = race_abort_and_halt(base, clients, fields, round_index)
                code, event = halting.result(timeout=max(0, deadline - monotonic()))
                require(code == 200, f"Halt failed at a pending prompt: HTTP {code}: {event!r}")
                expect_event(event, fields, "halted")
                halted = True
                response = aborting.result(timeout=max(0, deadline - monotonic()))
                expect_interrupted(response, fields, lost_status, "abort")
                require(monotonic() < deadline, "Abort and Halt did not finish promptly")

                late = {**fields, "input": "late.", "prompt_ref": ref}
                expect_session_lost(post(base, "respond", late, lost_status))
            except FutureTimeout as error:
                raise AssertionError("Abort and Halt did not both finish at a pending prompt") from error
            finally:
                if not halted:
                    post_response(base, "halt", fields)


def check_reply_abort_halt_race(base, lost_status, reply_kind="valid"):
    orders = permutations(("respond", "abort", "halt"))
    reply_text = "broken(." if reply_kind == "malformed" else "valid."
    with ExitStack() as stack, ThreadPoolExecutor(max_workers=3) as clients:
        other = stack.enter_context(session(base, True)) if reply_kind == "wrong-session" else None
        for order in orders:
            fields = spawn_session(base, True)
            halted = False
            try:
                ref = open_prompt(base, fields, goal="read(X), read(Y)")
                if reply_kind == "stale":
                    respond(base, fields, "valid", ref)
                    fresh_ref = prompt_ref(post(base, "poll", fields), fields)
                    require(fresh_ref != ref, "the pending prompt reused the consumed reference")
                if other is not None:
                    require(fields["pid"] != other["pid"], "expected two distinct session PIDs")
                    other_ref = open_prompt(base, other)
                    require(other_ref != ref, "the sessions issued the same prompt reference")
                    ref = other_ref
                reply = {**fields, "input": reply_text}
                if reply_kind != "missing-reference":
                    reply["prompt_ref"] = ref
                requests = [(command, reply if command == "respond" else fields) for command in order]
                deadline = monotonic() + 2.5
                pending = dict(zip(order, race_requests(base, clients, requests)))
                code, event = pending["halt"].result(timeout=max(0, deadline - monotonic()))
                require(code == 200, f"Halt failed in the three-request race: HTTP {code}: {event!r}")
                expect_event(event, fields, "halted")
                halted = True

                response = pending["abort"].result(timeout=max(0, deadline - monotonic()))
                expect_interrupted(response, fields, lost_status, "abort")
                response = pending["respond"].result(timeout=max(0, deadline - monotonic()))
                expect_racing_reply(response, fields, lost_status, reply_kind)
                require(monotonic() < deadline, "Reply, Abort and Halt did not all finish promptly")
                expect_session_lost(post(base, "respond", reply, lost_status))
                if other is not None:
                    answer(base, other, "survived", other_ref)
            except FutureTimeout as error:
                raise AssertionError("Reply, Abort and Halt did not all finish promptly") from error
            finally:
                if not halted:
                    post_response(base, "halt", fields)



def check_visitor_ownership(base):
    owner_jar = CookieJar()
    owner = build_opener(HTTPCookieProcessor(owner_jar))
    stranger = build_opener(HTTPCookieProcessor(CookieJar()))
    code, spawned = post_response(base, "spawn", {"options": "[session(true)]"}, client=owner)
    require(code == 200 and spawned.get("type") == "spawned", repr(spawned))
    fields = {"pid": spawned["pid"], "format": "json"}
    try:
        code, prompt = post_response(base, "call", {**fields, "goal": "read(X)"}, client=owner)
        require(code == 200, repr(prompt))
        ref = prompt_ref(prompt, fields)
        cookie = next((item for item in owner_jar
                       if item.name in ("wp_visitor", "__Host-wp_visitor")), None)
        require(cookie is not None, "the server did not issue a visitor cookie")
        require("httponly" in {name.lower() for name in cookie._rest},
                "the visitor cookie is missing HttpOnly")
        if base.startswith("https://"):
            require(cookie.name.startswith("__Host-") and cookie.secure,
                    "HTTPS visitor identity requires a secure host-only cookie")
        forged = build_opener()
        changed = cookie.value[:-1] + ("0" if cookie.value[-1] != "0" else "1")
        forged.addheaders.append(("Cookie", f"{cookie.name}={changed}"))
        for client in (stranger, forged):
            for command, params in (
                ("respond", {**fields, "input": "wrong.", "prompt_ref": ref}),
                ("halt", fields),
            ):
                _, denied = post_response(base, command, params, client=client)
                require(denied.get("type") == "error",
                        f"another visitor could {command} on the owner's session")
        code, event = post_response(base, "respond",
                                    {**fields, "input": "owned.", "prompt_ref": ref},
                                    client=owner)
        require(code == 200, repr(event))
        expect_event(event, fields, "responded")
        code, answer = post_response(base, "poll", fields, client=owner)
        require(code == 200 and answer.get("data") == [{"X": "owned"}], repr(answer))
        expect_event(answer, fields, "success")
    finally:
        code, halted = post_response(base, "halt", fields, client=owner)
        require(code == 200, repr(halted))
        expect_event(halted, fields, "halted")


def check_session_database(base):
    with session(base, True) as first, session(base, True) as other:
        expect_answer(post(base, "call", {**first, "goal": "assertz(pt021_secret(retained))"}), first, {})
        expect_answer(post(base, "call", {**first, "goal": "pt021_secret(X)"}), first, {"X": "retained"})
        expect_event(post(base, "call", {**other, "goal": "catch(pt021_secret(_),_,fail)"}), other, "failure")
        expect_event(post(base, "abort", first), first, "abort")
        expect_answer(post(base, "call", {**first, "goal": "pt021_secret(X)"}), first, {"X": "retained"})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--swi")
    parser.add_argument("--eclipse")
    parser.add_argument("--trealla")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--visitor-ownership", action="store_true",
                        help="also check anonymous cookie isolation on endpoints configured for it")
    args = parser.parse_args()
    endpoints = [(engine, getattr(args, engine)) for engine in ("swi", "eclipse", "trealla")
                 if getattr(args, engine)]
    if not endpoints:
        parser.error("provide at least one engine endpoint")
    manifest = json.loads(MANIFEST.read_text())
    results = []
    for engine, endpoint in endpoints:
        for case in manifest["cases"]:
            result = {"id": case["id"], "engine": engine}
            try:
                if case["id"] == "PT-004":
                    check(endpoint, require_by_default=engine in ("swi", "trealla"))
                elif case["id"] == "PT-005":
                    check_running_abort(endpoint)
                elif case["id"] == "PT-006":
                    check_continuation_abort(endpoint)
                elif case["id"] == "PT-007":
                    check_buffered_abort(endpoint)
                elif case["id"] == "PT-008":
                    check_halted_prompt(endpoint, lost_status=200 if engine == "swi" else 404)
                elif case["id"] == "PT-009":
                    check_competing_replies(endpoint)
                elif case["id"] == "PT-010":
                    check_reply_racing_abort(endpoint)
                elif case["id"] == "PT-011":
                    check_reply_racing_halt(endpoint, lost_status=200 if engine == "swi" else 404)
                elif case["id"] == "PT-012":
                    check_running_halt(endpoint, lost_status=200 if engine == "swi" else 404)
                elif case["id"] == "PT-013":
                    check_abort_racing_halt(endpoint, lost_status=200 if engine == "swi" else 404)
                elif case["id"] == "PT-014":
                    for command in ("next", "poll"):
                        check_abort_racing_halt(endpoint, 200 if engine == "swi" else 404, command)
                elif case["id"] == "PT-015":
                    check_prompt_abort_racing_halt(endpoint, 200 if engine == "swi" else 404)
                elif case["id"] == "PT-016":
                    check_reply_abort_halt_race(endpoint, 200 if engine == "swi" else 404)
                elif case["id"] == "PT-017":
                    check_reply_abort_halt_race(endpoint, 200 if engine == "swi" else 404, reply_kind="malformed")
                elif case["id"] == "PT-018":
                    check_reply_abort_halt_race(endpoint, 200 if engine == "swi" else 404, reply_kind="stale")
                elif case["id"] == "PT-019":
                    check_reply_abort_halt_race(endpoint, 200 if engine == "swi" else 404,
                                                reply_kind="wrong-session")
                elif case["id"] == "PT-020":
                    check_reply_abort_halt_race(endpoint, 200 if engine == "swi" else 404,
                                                reply_kind="missing-reference")
                elif case["id"] == "PT-021":
                    check_session_database(endpoint)
                else:
                    raise ValueError(f"unknown case {case['id']}")
            except (AssertionError, KeyError, ValueError, OSError) as error:
                result.update(status="fail", detail=str(error))
            else:
                result["status"] = "pass"
            results.append(result)
        if args.visitor_ownership:
            result = {"id": "visitor-ownership", "engine": engine}
            try:
                check_visitor_ownership(endpoint)
            except (AssertionError, KeyError, ValueError, OSError) as error:
                result.update(status="fail", detail=str(error))
            else:
                result["status"] = "pass"
            results.append(result)
    passed = all(result["status"] == "pass" for result in results)
    report = {"suite": manifest["suite"], "status": "pass" if passed else "fail",
              "results": results}
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
