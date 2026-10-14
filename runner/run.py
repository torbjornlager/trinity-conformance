#!/usr/bin/env python3
"""Dependency-free black-box runner for Trinity Web Prolog nodes."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import socket
import ssl
import struct
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "cases" / "actor-core-0.1.json"
PROFILE_ORDER = {"relation": 0, "isobase": 1, "isotope": 2, "actor": 3}
CLASSIFICATIONS = {
    "protocol_implementation_defect",
    "runtime_defect",
    "deliberately_unsupported",
    "specification_ambiguity",
}


class ConformanceFailure(AssertionError):
    pass


class ProtocolError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ConformanceFailure(message)


class WebSocket:
    """Small RFC 6455 client sufficient for the text-only node protocol."""

    def __init__(
        self,
        url: str,
        timeout: float,
        token: str | None = None,
        origin: str | None = None,
        insecure_tls: bool = False,
        extra_headers: tuple[str, ...] = (),
    ) -> None:
        parsed = urlsplit(url)
        if parsed.scheme not in {"ws", "wss"} or not parsed.hostname:
            raise ValueError(f"invalid WebSocket URL: {url}")
        self.timeout = timeout
        self.sock = socket.create_connection(
            (parsed.hostname, parsed.port or (443 if parsed.scheme == "wss" else 80)),
            timeout=timeout,
        )
        if parsed.scheme == "wss":
            context = ssl.create_default_context()
            if insecure_tls:
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
            self.sock = context.wrap_socket(self.sock, server_hostname=parsed.hostname)
        self.sock.settimeout(timeout)
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query
        host = parsed.hostname
        port = parsed.port
        if port and port not in {80, 443}:
            host = f"{host}:{port}"
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        request_headers = [
            f"GET {path} HTTP/1.1",
            f"Host: {host}",
            "Upgrade: websocket",
            "Connection: Upgrade",
            f"Sec-WebSocket-Key: {key}",
            "Sec-WebSocket-Version: 13",
        ]
        if token:
            request_headers.append(f"Authorization: Bearer {token}")
        if origin:
            request_headers.append(f"Origin: {origin}")
        request_headers.extend(extra_headers)
        request = "\r\n".join(request_headers) + "\r\n\r\n"
        self.sock.sendall(request.encode("ascii"))
        response = self._read_headers()
        status = response.split("\r\n", 1)[0]
        if " 101 " not in status:
            self.sock.close()
            raise ProtocolError(f"WebSocket upgrade failed: {status}")
        header_map: dict[str, str] = {}
        for line in response.split("\r\n")[1:]:
            if ":" in line:
                name, value = line.split(":", 1)
                header_map[name.strip().lower()] = value.strip()
        expected = base64.b64encode(
            hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()
        ).decode("ascii")
        if header_map.get("sec-websocket-accept") != expected:
            self.sock.close()
            raise ProtocolError("invalid Sec-WebSocket-Accept")

    def _read_headers(self) -> str:
        data = bytearray()
        while b"\r\n\r\n" not in data:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ProtocolError("connection closed during WebSocket upgrade")
            data.extend(chunk)
            if len(data) > 65536:
                raise ProtocolError("oversized WebSocket upgrade response")
        head, extra = bytes(data).split(b"\r\n\r\n", 1)
        if extra:
            raise ProtocolError("unexpected framed data in upgrade response")
        return head.decode("iso-8859-1")

    def _recv_exact(self, count: int) -> bytes:
        chunks = bytearray()
        while len(chunks) < count:
            chunk = self.sock.recv(count - len(chunks))
            if not chunk:
                raise ProtocolError("WebSocket closed unexpectedly")
            chunks.extend(chunk)
        return bytes(chunks)

    def _send_frame(self, opcode: int, payload: bytes) -> None:
        first = 0x80 | opcode
        length = len(payload)
        if length < 126:
            header = bytes([first, 0x80 | length])
        elif length <= 0xFFFF:
            header = bytes([first, 0x80 | 126]) + struct.pack("!H", length)
        else:
            header = bytes([first, 0x80 | 127]) + struct.pack("!Q", length)
        mask = os.urandom(4)
        masked = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
        self.sock.sendall(header + mask + masked)

    def send_json(self, value: dict[str, Any]) -> None:
        self._send_frame(0x1, json.dumps(value, separators=(",", ":")).encode("utf-8"))

    def recv_json(self) -> dict[str, Any]:
        payload_parts: list[bytes] = []
        text_started = False
        while True:
            first, second = self._recv_exact(2)
            fin = bool(first & 0x80)
            opcode = first & 0x0F
            masked = bool(second & 0x80)
            length = second & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._recv_exact(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._recv_exact(8))[0]
            mask = self._recv_exact(4) if masked else b""
            payload = self._recv_exact(length)
            if masked:
                payload = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
            if opcode == 0x8:
                raise ProtocolError("server closed the WebSocket")
            if opcode == 0x9:
                self._send_frame(0xA, payload)
                continue
            if opcode == 0xA:
                continue
            if opcode == 0x1:
                text_started = True
                payload_parts = [payload]
            elif opcode == 0x0 and text_started:
                payload_parts.append(payload)
            else:
                raise ProtocolError(f"unexpected WebSocket opcode {opcode}")
            if fin:
                value = json.loads(b"".join(payload_parts).decode("utf-8"))
                if not isinstance(value, dict):
                    raise ProtocolError("node event is not a JSON object")
                return value

    def close(self) -> None:
        try:
            self._send_frame(0x8, struct.pack("!H", 1000))
        except OSError:
            pass
        finally:
            self.sock.close()


@dataclass
class Candidate:
    ws_url: str
    advertised_profile: str
    timeout: float
    token: str | None
    origin: str | None
    insecure_tls: bool
    headers: tuple[str, ...]


class Harness:
    def __init__(self, candidate: Candidate) -> None:
        self.candidate = candidate
        self.ws: WebSocket | None = None
        self.shell: int | None = None
        self.welcome: dict[str, Any] | None = None

    def __enter__(self) -> "Harness":
        self.ws = WebSocket(
            self.candidate.ws_url,
            self.candidate.timeout,
            self.candidate.token,
            self.candidate.origin,
            self.candidate.insecure_tls,
            self.candidate.headers,
        )
        self.send({"command": "transport_hello", "version": 1,
                   "browser_pids": True, "io_ack": True})
        welcome = self.recv()
        require(welcome.get("type") == "transport_welcome",
                f"expected transport_welcome, got {welcome!r}")
        self.welcome = welcome
        return self

    def __exit__(self, _kind: Any, _value: Any, _traceback: Any) -> None:
        if self.ws:
            self.ws.close()

    def send(self, command: dict[str, Any]) -> None:
        assert self.ws
        self.ws.send_json(command)

    def recv(self, expected_type: str | None = None) -> dict[str, Any]:
        assert self.ws
        event = self.ws.recv_json()
        if expected_type:
            require(event.get("type") == expected_type,
                    f"expected {expected_type}, got {event!r}")
        return event

    def recv_type(self, expected_type: str, limit: int = 4) -> dict[str, Any]:
        seen: list[dict[str, Any]] = []
        for _ in range(limit):
            event = self.recv()
            if event.get("type") == expected_type:
                return event
            seen.append(event)
        raise ConformanceFailure(
            f"expected {expected_type}; preceding events were {seen!r}"
        )

    def spawn_shell(self, options: str = "[session(true)]") -> int:
        self.send({"command": "toplevel_spawn", "options": options})
        event = self.recv("spawned")
        pid = event.get("pid")
        require(isinstance(pid, int) and 1_000_000_000 <= pid <= 9_999_999_999,
                f"invalid public PID: {pid!r}")
        self.shell = pid
        return pid

    def call(self, goal: str, options: str = "[]") -> None:
        assert self.shell is not None
        self.send({"command": "toplevel_call", "pid": self.shell,
                   "goal": goal, "options": options})

    def next(self) -> None:
        assert self.shell is not None
        self.send({"command": "toplevel_next", "pid": self.shell})

    def halt(self) -> None:
        if self.shell is None:
            return
        self.send({"command": "toplevel_halt", "pid": self.shell})
        self.recv_type("halted", limit=32)
        self.shell = None


def row_value(event: dict[str, Any], name: str) -> str:
    rows = event.get("data")
    require(isinstance(rows, list) and len(rows) == 1 and isinstance(rows[0], dict),
            f"expected one binding row, got {rows!r}")
    value = rows[0].get(name)
    require(isinstance(value, str), f"missing string binding {name}: {rows[0]!r}")
    return value


def prolog_quote_atom(value: str) -> str:
    """Render source text as a portable single-quoted Prolog atom."""
    return "'" + value.replace("'", "''") + "'"


def case_ac_001(candidate: Candidate) -> None:
    with Harness(candidate) as harness:
        welcome = harness.welcome or {}
        require(welcome.get("version") == 1,
                f"unexpected protocol version: {welcome!r}")
        if "profile" in welcome:
            require(welcome.get("profile") == "actor",
                    f"unexpected negotiated profile: {welcome!r}")
        require(welcome.get("browser_pids") is True and welcome.get("io_ack") is True,
                f"browser capability negotiation failed: {welcome!r}")


def case_ac_002(candidate: Candidate) -> None:
    with Harness(candidate) as harness:
        pid = harness.spawn_shell()
        harness.call("self(Self)", "[limit(1)]")
        event = harness.recv("success")
        require(event.get("more") is False, "self/1 exposed another solution")
        value = row_value(event, "Self")
        match = re.match(r"^(\d{10})(?:@.+)?$", value)
        require(match is not None, f"invalid displayed self PID: {value!r}")
        require(int(match.group(1)) == pid,
                f"self PID {value!r} differs from spawned PID {pid}")
        harness.halt()


def case_ac_003(candidate: Candidate) -> None:
    with Harness(candidate) as harness:
        harness.spawn_shell()
        harness.call("member(X,[a,b,c])", "[limit(2)]")
        first = harness.recv("success")
        require(first.get("more") is True, "first page did not advertise more results")
        rows = first.get("data")
        require(isinstance(rows, list) and [row.get("X") for row in rows] == ["a", "b"],
                f"unexpected first page: {rows!r}")
        harness.next()
        final = harness.recv("success")
        require(final.get("more") is False, "final page advertised more results")
        require(row_value(final, "X") == "c", f"unexpected final page: {final!r}")
        harness.halt()


def case_ac_004(candidate: Candidate) -> None:
    goal = (
        'self(Self), Self ! number(-2), receive({ '
        'number(N) if N > 0 -> format("Positive number: ~p~n", [N]) ; '
        'number(N) if N =< 0 -> format("Non-positive number: ~p~n", [N]) })'
    )
    with Harness(candidate) as harness:
        harness.spawn_shell()
        harness.call(goal)
        output = harness.recv("io_request")
        nested = output.get("event")
        require(isinstance(nested, dict) and nested.get("type") == "output",
                f"expected output event, got {output!r}")
        require(nested.get("data") == "Non-positive number: -2",
                f"unexpected guarded receive output: {nested.get('data')!r}")
        request_id = output.get("request_id")
        require(isinstance(request_id, str), "io_request omitted request_id")
        harness.send({"command": "browser_io_reply", "request_id": request_id,
                      "status": "ok"})
        success = harness.recv("success")
        require(success.get("more") is False, "guarded receive was not deterministic")
        require(row_value(success, "N") == "-2", f"wrong receive binding: {success!r}")
        harness.halt()


def case_ac_005(candidate: Candidate) -> None:
    goal = (
        "self(Self), Self ! goodbye, Self ! hello, "
        "receive({hello -> true}), receive({goodbye -> true})"
    )
    with Harness(candidate) as harness:
        harness.spawn_shell()
        harness.call(goal, "[limit(1)]")
        success = harness.recv("success")
        require(success.get("more") is False,
                f"deferred receive was not deterministic: {success!r}")
        harness.halt()


def case_ac_006(candidate: Candidate) -> None:
    with Harness(candidate) as harness:
        pid = harness.spawn_shell()
        harness.call("input('Input',X)", "[limit(1)]")
        prompt = harness.recv("prompt")
        require(prompt.get("pid") == pid and prompt.get("data") == "Input",
                f"unexpected browser prompt: {prompt!r}")
        harness.send({"command": "toplevel_respond", "pid": pid, "input": "hello"})
        responded = False
        success: dict[str, Any] | None = None
        for _ in range(2):
            event = harness.recv()
            if event.get("type") == "responded":
                responded = True
            elif event.get("type") == "success":
                success = event
            else:
                raise ConformanceFailure(f"unexpected input event: {event!r}")
        require(responded and success is not None,
                "input did not produce both responded and success events")
        require(row_value(success, "X") == "hello", f"wrong input binding: {success!r}")
        harness.halt()


def case_ac_007(candidate: Candidate) -> None:
    with Harness(candidate) as harness:
        harness.spawn_shell("[session(true),src_list([shell_marker])]")
        harness.call("toplevel_spawn(Pid,[session(true),monitor(true)])", "[limit(1)]")
        spawned = harness.recv("success")
        child = row_value(spawned, "Pid")
        harness.call(
            f"toplevel_call({child},input('Input',X)),receive({{Answer->true}})",
            "[limit(1)]",
        )
        prompt_answer = harness.recv("success")
        prompt_text = row_value(prompt_answer, "Answer")
        require(prompt_text.startswith("prompt("),
                f"nested input bypassed its protocol caller: {prompt_text!r}")
        harness.call(
            f"respond({child},hello),receive({{Answer->true}})", "[limit(1)]"
        )
        completed = harness.recv("success")
        answer = row_value(completed, "Answer")
        require(answer.startswith("success(") and "input('Input',hello)" in answer,
                f"unexpected nested input completion: {answer!r}")
        harness.halt()


def require_source_goal_success(candidate: Candidate, source: str, goal: str) -> None:
    options = f"[session(true),src_text({prolog_quote_atom(source)})]"
    with Harness(candidate) as harness:
        harness.spawn_shell(options)
        harness.call(goal, "[limit(1)]")
        # Supervisor operations legitimately surface child down events on the
        # owning browser connection before the enclosing goal completes.
        success = harness.recv_type("success", limit=32)
        require(success.get("more") is False,
                f"behaviour goal was not deterministic: {success!r}")
        harness.halt()


SERVER_SOURCE = (
    "counter(inc,N,ok,N1):-N1 is N+1. "
    "counter(get,N,val(N),N). "
    "counter2(get,N,seen(N),N). "
    "counter2(inc,N,added(N1),N1):-N1 is N+1."
)

SUPERVISOR_SOURCE = (
    "forever:-receive({stop->true}). "
    "crasher(Delay):-sleep(Delay),exit(crash). "
    "finisher(Delay):-sleep(Delay). "
    "fridge(store(F),Foods,ok,[F|Foods]). "
    "fridge(take(F),Foods,ok(F),Rest):-select(F,Foods,Rest),!. "
    "fridge(take(_),Foods,not_found,Foods)."
)


def case_bh_001(candidate: Candidate) -> None:
    require_source_goal_success(
        candidate,
        SERVER_SOURCE,
        "server_spawn(counter,0,Pid),"
        "server_request(Pid,inc,ok),server_request(Pid,inc,ok),"
        "server_request(Pid,get,val(2)),server_halt(Pid,true)",
    )


def case_bh_002(candidate: Candidate) -> None:
    require_source_goal_success(
        candidate,
        SERVER_SOURCE,
        "server_spawn(counter,0,Pid),"
        "server_promise(Pid,inc,R1),server_promise(Pid,inc,R2),"
        "R1\\=R2,server_yield(R1,ok),server_yield(R2,ok),"
        "server_request(Pid,get,val(2)),server_halt(Pid,true)",
    )


def case_bh_003(candidate: Candidate) -> None:
    require_source_goal_success(
        candidate,
        SERVER_SOURCE,
        "server_spawn(counter,0,Pid),server_request(Pid,inc,ok),"
        "server_upgrade(Pid,counter2,[src_predicates([counter2/4])]),"
        "server_request(Pid,get,seen(1)),server_request(Pid,inc,added(2)),"
        "server_halt(Pid,true)",
    )


def case_bh_004(candidate: Candidate) -> None:
    require_source_goal_success(
        candidate,
        SUPERVISOR_SOURCE,
        "supervisor_spawn([child(a,[start(forever)]),"
        "child(b,[start(forever)])],Sup,[src_predicates([forever/0])]),"
        "supervisor_which_children(Sup,[info(a,A,worker,permanent),"
        "info(b,B,worker,permanent)]),A\\=B,A\\=undefined,B\\=undefined,"
        "supervisor_count_children(Sup,[specs-2,active-2,supervisors-0,workers-2]),"
        "supervisor_halt(Sup)",
    )


def case_bh_005(candidate: Candidate) -> None:
    require_source_goal_success(
        candidate,
        SUPERVISOR_SOURCE,
        "supervisor_spawn([],Sup,[src_predicates([forever/0])]),"
        "supervisor_spawn_child(Sup,child(dynamic,[start(forever)]),ok),"
        "supervisor_which_children(Sup,[info(dynamic,P1,worker,permanent)]),"
        "supervisor_terminate_child(Sup,dynamic,ok),"
        "supervisor_respawn_child(Sup,dynamic,ok(P2)),P1\\=P2,"
        "supervisor_terminate_child(Sup,dynamic,ok),"
        "supervisor_delete_child(Sup,dynamic,ok),"
        "supervisor_which_children(Sup,[]),supervisor_halt(Sup)",
    )


def case_bh_006(candidate: Candidate) -> None:
    require_source_goal_success(
        candidate,
        SUPERVISOR_SOURCE,
        "supervisor_spawn([child(stable,[start(forever)]),"
        "child(flaky,[start(crasher(0.1)),restart(permanent)])],Sup,"
        "[strategy(one_for_one),intensity(5),period(10),"
        "src_predicates([forever/0,crasher/1])]),"
        "supervisor_which_children(Sup,[info(stable,S1,_,_),info(flaky,F1,_,_)]),"
        "sleep(0.3),supervisor_which_children(Sup,"
        "[info(stable,S2,_,_),info(flaky,F2,_,_)]),S1==S2,F1\\=F2,"
        "supervisor_halt(Sup)",
    )


def case_bh_007(candidate: Candidate) -> None:
    require_source_goal_success(
        candidate,
        SUPERVISOR_SOURCE,
        "supervisor_spawn([child(a,[start(forever)]),"
        "child(b,[start(forever)]),"
        "child(c,[start(crasher(0.1)),restart(permanent)])],Sup,"
        "[strategy(one_for_all),intensity(5),period(10),"
        "src_predicates([forever/0,crasher/1])]),"
        "supervisor_which_children(Sup,[info(a,A1,_,_),info(b,B1,_,_),info(c,C1,_,_)]),"
        "sleep(0.3),supervisor_which_children(Sup,"
        "[info(a,A2,_,_),info(b,B2,_,_),info(c,C2,_,_)]),"
        "A1\\=A2,B1\\=B2,C1\\=C2,supervisor_halt(Sup)",
    )


def case_bh_008(candidate: Candidate) -> None:
    require_source_goal_success(
        candidate,
        SUPERVISOR_SOURCE,
        "supervisor_spawn([child(keeper,[start(forever)]),"
        "child(temp,[start(crasher(0.05)),restart(temporary)]),"
        "child(trans,[start(finisher(0.05)),restart(transient)])],Sup,"
        "[intensity(5),period(10),"
        "src_predicates([forever/0,crasher/1,finisher/1])]),"
        "sleep(0.2),supervisor_which_children(Sup,Children),"
        "Children=[info(keeper,K,worker,permanent),"
        "info(trans,undefined,worker,transient)],K\\=undefined,supervisor_halt(Sup)",
    )


def case_bh_009(candidate: Candidate) -> None:
    require_source_goal_success(
        candidate,
        SUPERVISOR_SOURCE,
        "Inner=[child(i1,[start(forever)]),child(i2,[start(forever)])],"
        "supervisor_spawn([child(inner,[start(start_sub_supervisor(Inner,"
        "[strategy(one_for_one),intensity(3),period(10)])),"
        "type(supervisor),restart(permanent),shutdown(infinity)]),"
        "child(outer,[start(forever)])],Sup,"
        "[intensity(5),period(10),src_predicates([forever/0])]),"
        "supervisor_which_children(Sup,[info(inner,I1,_,_),info(outer,O1,_,_)]),"
        "exit(I1,kill),sleep(0.25),supervisor_which_children(Sup,"
        "[info(inner,I2,_,_),info(outer,O2,_,_)]),I1\\=I2,O1==O2,"
        "supervisor_halt(Sup)",
    )


def case_bh_010(candidate: Candidate) -> None:
    require_source_goal_success(
        candidate,
        SUPERVISOR_SOURCE,
        "supervisor_spawn([child(fridge_service,[start(server(fridge,"
        "[initial_state([])])),restart(permanent),shutdown(1)])],Sup,"
        "[src_predicates([fridge/4])]),"
        "supervisor_which_children(Sup,[info(fridge_service,Pid,_,_)]),"
        "server_request(fridge_service,store(milk),ok),"
        "server_request(fridge_service,take(milk),ok(milk)),"
        "monitor(Pid,Ref),supervisor_terminate_child(Sup,fridge_service,ok),"
        "receive({down(Pid,Ref,true)->true},[timeout(2),on_timeout(fail)]),"
        "supervisor_halt(Sup)",
    )


def require_goal_success(candidate: Candidate, goal: str) -> None:
    with Harness(candidate) as harness:
        harness.spawn_shell()
        harness.call(goal, "[limit(1)]")
        success = harness.recv("success")
        require(success.get("more") is False,
                f"portable text goal was not deterministic: {success!r}")
        harness.halt()


def case_txt_001(candidate: Candidate) -> None:
    require_goal_success(candidate, 'member("abc",[[a,b,c]])')


def case_txt_002(candidate: Candidate) -> None:
    require_goal_success(candidate, 'member("",[[]])')


def case_txt_003(candidate: Candidate) -> None:
    require_goal_success(candidate, 'member("å",[[\'å\']])')


def case_txt_004(candidate: Candidate) -> None:
    require_goal_success(candidate, 'phrase(("ab","cd"),"abcd")')


def case_txt_005(candidate: Candidate) -> None:
    source = 'portable_literal :- append("ab",[],[a,b]).'
    options = f"[session(true),src_text({prolog_quote_atom(source)})]"
    with Harness(candidate) as harness:
        harness.spawn_shell(options)
        harness.call("portable_literal", "[limit(1)]")
        success = harness.recv("success")
        require(success.get("more") is False,
                f"loaded text predicate was not deterministic: {success!r}")
        harness.halt()


def case_txt_006(candidate: Candidate) -> None:
    with Harness(candidate) as harness:
        harness.spawn_shell()
        harness.call('member(Text,["ab"])', "[limit(1)]")
        first = harness.recv("success")
        rendered = row_value(first, "Text")
        require(re.fullmatch(r'[\[\]a-zA-Z,"\' ]+', rendered) is not None,
                f"unsafe serialized text term: {rendered!r}")
        harness.call(f"append({rendered},[],[a,b])", "[limit(1)]")
        second = harness.recv("success")
        require(second.get("more") is False,
                f"round-tripped text goal was not deterministic: {second!r}")
        harness.halt()


def case_txt_007(candidate: Candidate) -> None:
    require_goal_success(
        candidate, 'append("ab",[c,d],"abcd")'
    )


TUTORIAL_019_SOURCE = """
asynch_test_4(Answer1, Answer2) :-
    promise('https://n3.elfenbenstornet.se', (p(X),sleep(0.2)), Ref1, [
        template(X),
        offset(1),
        src_text("p(a). p(b).")
    ]),
    promise('https://n4.elfenbenstornet.se', (p(Y),sleep(0.1)), Ref2, [
        template(Y),
        limit(1),
        src_list([p(c), p(d)])
    ]),
    yield(Ref1, Answer1),
    yield(Ref2, Answer2).
""".strip()


def case_demo_019(candidate: Candidate) -> None:
    options = (
        "[session(true),src_text("
        + prolog_quote_atom(TUTORIAL_019_SOURCE)
        + ")]"
    )
    with Harness(candidate) as harness:
        harness.spawn_shell(options)
        harness.call("asynch_test_4(Answer1,Answer2)", "[limit(1)]")
        success = harness.recv_type("success", limit=32)
        require(success.get("more") is False,
                f"tutorial 19 returned another solution: {success!r}")
        require(row_value(success, "Answer1") == "success([b],false)",
                f"unexpected N3 promise answer: {success!r}")
        require(row_value(success, "Answer2") == "success([c],true)",
                f"unexpected N4 promise answer: {success!r}")
        harness.halt()


CASE_FUNCTIONS: dict[str, Callable[[Candidate], None]] = {
    "AC-001": case_ac_001,
    "AC-002": case_ac_002,
    "AC-003": case_ac_003,
    "AC-004": case_ac_004,
    "AC-005": case_ac_005,
    "AC-006": case_ac_006,
    "AC-007": case_ac_007,
    "BH-001": case_bh_001,
    "BH-002": case_bh_002,
    "BH-003": case_bh_003,
    "BH-004": case_bh_004,
    "BH-005": case_bh_005,
    "BH-006": case_bh_006,
    "BH-007": case_bh_007,
    "BH-008": case_bh_008,
    "BH-009": case_bh_009,
    "BH-010": case_bh_010,
    "TXT-001": case_txt_001,
    "TXT-002": case_txt_002,
    "TXT-003": case_txt_003,
    "TXT-004": case_txt_004,
    "TXT-005": case_txt_005,
    "TXT-006": case_txt_006,
    "TXT-007": case_txt_007,
    "DEMO-019": case_demo_019,
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ws-url", required=True, help="candidate WebSocket URL")
    parser.add_argument("--advertised-profile", default="actor",
                        choices=tuple(PROFILE_ORDER))
    parser.add_argument("--token", help="bearer token; prefer --token-env")
    parser.add_argument("--token-env", help="environment variable containing a bearer token")
    parser.add_argument("--origin")
    parser.add_argument(
        "--header", action="append", default=[],
        help="additional WebSocket upgrade header (repeatable; NAME: VALUE)",
    )
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--insecure-tls", action="store_true")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--case", action="append", dest="case_ids",
                        help="run only this case ID; repeatable")
    parser.add_argument("--classifications", type=Path)
    parser.add_argument("--report", type=Path, help="write a JSON result report")
    parser.add_argument("--candidate", default="external")
    args = parser.parse_args()

    token = args.token
    if args.token_env:
        token = os.environ.get(args.token_env)
        if token is None:
            parser.error(f"environment variable {args.token_env!r} is not set")
    manifest = load_json(args.manifest)
    classifications = load_json(args.classifications) if args.classifications else {}
    if not isinstance(classifications, dict):
        parser.error("classification file must contain a JSON object")
    selected = set(args.case_ids or [])
    known = {case["id"] for case in manifest["cases"]}
    unknown = selected - known
    if unknown:
        parser.error("unknown case ID(s): " + ", ".join(sorted(unknown)))

    for header in args.header:
        if ":" not in header or "\r" in header or "\n" in header:
            parser.error("--header must be a single NAME: VALUE header line")
    candidate = Candidate(args.ws_url, args.advertised_profile, args.timeout,
                          token, args.origin, args.insecure_tls,
                          tuple(args.header))
    required_profile = manifest["required_advertised_profile"]
    results: list[dict[str, Any]] = []
    started_at = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    for metadata in manifest["cases"]:
        case_id = metadata["id"]
        if selected and case_id not in selected:
            continue
        before = time.monotonic()
        result = {"id": case_id, "title": metadata["title"]}
        if PROFILE_ORDER[args.advertised_profile] < PROFILE_ORDER[required_profile]:
            result.update(status="unsupported", duration_ms=0,
                          detail=f"requires advertised profile {required_profile}")
        else:
            try:
                function = CASE_FUNCTIONS[case_id]
                function(candidate)
                result.update(status="pass",
                              duration_ms=round((time.monotonic() - before) * 1000))
            except Exception as error:  # each case must produce a report row
                diagnostic = classifications.get(case_id, {})
                classification = diagnostic.get("classification", "unclassified")
                if classification != "unclassified" and classification not in CLASSIFICATIONS:
                    classification = "unclassified"
                result.update(
                    status="fail",
                    duration_ms=round((time.monotonic() - before) * 1000),
                    detail=f"{type(error).__name__}: {error}",
                    classification=classification,
                )
                for key in ("issue", "note"):
                    if key in diagnostic:
                        result[key] = diagnostic[key]
        results.append(result)
        marker = {"pass": "PASS", "fail": "FAIL", "unsupported": "UNSUPPORTED"}[result["status"]]
        detail = f" — {result['detail']}" if "detail" in result else ""
        print(f"{marker:11} {case_id}  {metadata['title']}{detail}")

    counts = {status: sum(row["status"] == status for row in results)
              for status in ("pass", "fail", "unsupported")}
    report = {
        "suite": manifest["suite"],
        "schema_version": 1,
        "candidate": args.candidate,
        "ws_url": args.ws_url,
        "advertised_profile": args.advertised_profile,
        "started_at": started_at,
        "duration_ms": round((time.monotonic() - started) * 1000),
        "counts": counts,
        "results": results,
    }
    print(f"\n{counts['pass']} passed, {counts['fail']} failed, "
          f"{counts['unsupported']} unsupported")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with args.report.open("w", encoding="utf-8") as stream:
            json.dump(report, stream, indent=2, sort_keys=True)
            stream.write("\n")
        print(f"Report: {args.report}")
    return 1 if counts["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
