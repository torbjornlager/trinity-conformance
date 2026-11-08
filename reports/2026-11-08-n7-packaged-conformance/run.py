#!/usr/bin/env python3
"""Run the existing HTTP packs against a disposable private N7 adapter."""
import argparse
from contextlib import ExitStack
from hashlib import sha256
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from secrets import token_hex
import signal
import socket
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Thread
from time import monotonic, sleep
from unittest.mock import patch
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "runner"))
import baseline
import prompt_http

ORIGIN = "https://n7.example.test"
OWNER = "owner@example.test"


class SourceFixture(SimpleHTTPRequestHandler):
    def do_GET(self):
        if any(header in self.headers for header in (
            "Cookie", "Authorization", "X-Web-Prolog-User", "X-Web-Prolog-Proxy-Token",
        )):
            self.send_error(403)
        elif self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/index.html")
            self.end_headers()
        else:
            super().do_GET()


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def stop(process):
    if process.poll() is not None:
        return
    process.send_signal(signal.SIGTERM)
    try:
        process.wait(timeout=12)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def read(url):
    with urlopen(url, timeout=2) as response:
        return response.read()


def wait_for(url, process, log):
    deadline = monotonic() + 20
    while process.poll() is None and monotonic() < deadline:
        try:
            return read(url)
        except OSError:
            sleep(0.1)
    raise RuntimeError(f"Fixture failed to start at {url}\n{log.read_text()[-3000:]}")


def start(stack, args, log):
    output = stack.enter_context(log.open("wb"))
    process = subprocess.Popen(args, stdout=output, stderr=subprocess.STDOUT)
    stack.callback(stop, process)
    return process


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demonstrator", required=True, type=Path)
    parser.add_argument("--swi-load", required=True, type=Path)
    parser.add_argument("--image", default="trinity-eclipse-n7:local")
    parser.add_argument("--allow-fixture-peers", action="store_true")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    adapter = args.demonstrator / "experiments/eclipse-clp/isotope_http.py"
    suites = ("isobase-http", "interop-http", "local-node-rpc", "isobase-diagnostics",
              "prompt-http", "actor-core")
    manifests = {suite: ROOT / "cases" / f"{suite}-0.1.json" for suite in suites}

    with ExitStack() as stack:
        scratch = Path(stack.enter_context(TemporaryDirectory(prefix="n7-conformance-")))
        token_file = scratch / "proxy-token"
        token_file.touch(mode=0o600)
        token = token_hex(32)
        token_file.write_text(token + "\n")
        port = free_port()
        endpoint = f"http://127.0.0.1:{port}"
        adapter_log = scratch / "adapter.log"
        def owner_request(url, *request_args, **kwargs):
            request = Request(url, *request_args, **kwargs)
            if url.startswith(endpoint + "/"):
                for key, value in {
                    "Host": "n7.example.test", "Origin": ORIGIN, "X-Web-Prolog-User": OWNER,
                    "X-Web-Prolog-Proxy-Token": token,
                }.items():
                    request.add_unredirected_header(key, value)
            return request

        peer_port = free_port()
        peer = f"http://127.0.0.1:{peer_port}"
        peer_log = scratch / "peer.log"
        swi = start(stack, ["swipl", "-q", "-s", str(args.swi_load), "-g",
                            f"node({peer_port},[profile(isotope),auth(dev)]),thread_get_message(stop)"], peer_log)
        query = urlencode({"goal": "member(X,[a,b,c])", "template": "X", "limit": 2, "format": "prolog"})
        if wait_for(peer + "/call?" + query, swi, peer_log).replace(b" ", b"").strip() != b"success([a,b],true).":
            raise RuntimeError("Expected the disposable peer to serve the first page")
        source = scratch / "source"
        source.mkdir()
        (source / "index.html").write_text("local_node_loaded(one).\nlocal_node_loaded(two).\n")
        server = stack.enter_context(ThreadingHTTPServer(
            ("127.0.0.1", 0),
            lambda *a, **kw: SourceFixture(*a, directory=str(source), **kw),
        ))
        Thread(target=server.serve_forever, daemon=True).start()
        stack.callback(server.shutdown)
        source_url = f"http://127.0.0.1:{server.server_port}"
        if read(source_url) != (source / "index.html").read_bytes():
            raise RuntimeError("Source fixture preflight failed")

        peer_args = ["--allow-peer", peer, "--allow-peer", source_url] if args.allow_fixture_peers else []
        process = start(stack, [sys.executable, str(adapter), "--pilot-image", args.image,
                                "--port", str(port), "--private-origin", ORIGIN,
                                "--owner", OWNER, "--proxy-token-file", str(token_file),
                                *peer_args], adapter_log)
        metadata = json.loads(wait_for(owner_request(endpoint + "/node_info"), process, adapter_log))
        if (metadata["profile"], metadata["auth"]) != ("isotope", "private"):
            raise RuntimeError("Expected a private ISOTOPE pilot")
        if args.allow_fixture_peers:
            # The alias reaches the same fixture from the host, but is not allowlisted.
            alias = peer.replace("127.0.0.1", "localhost")
            if read(alias + "/call?" + query) != read(peer + "/call?" + query):
                raise RuntimeError("Peer alias preflight failed")
            checks = {
                "unlisted_origin": f"rpc('{alias}',true)",
                "redirect": f"rpc(localhost,local_node_loaded(one),[src_uri('{source_url}/redirect')])",
            }
            for label, goal in checks.items():
                query_string = urlencode({"goal": goal, "format": "json"})
                event = json.loads(read(owner_request(endpoint + "/call?" + query_string)))
                if event["type"] != "error" or "peer_request_failed" not in event["data"]:
                    raise RuntimeError(f"Egress policy check failed for {label}: {event}")
            print("N7 denied an unlisted peer origin and refused a source redirect", flush=True)

        provenance = {
            "image": args.image,
            "image_id": subprocess.check_output(
                ["docker", "image", "inspect", "--format", "{{.Id}}", args.image], text=True
            ).strip(),
            "metadata": metadata,
            "fixture_peers_allowed": args.allow_fixture_peers,
            # The shared validator handles required/diagnostic v2 reports and
            # ACTOR v1 reports. Supporting and prompt evidence retains its format.
            "runs": [{"label": suite, "report": f"{suite}.json"} for suite in suites
                     if suite not in ("local-node-rpc", "prompt-http")],
            "sha256": {p.name: sha256(p.read_bytes()).hexdigest() for p in (
                adapter, Path(baseline.__file__), Path(baseline.actor.__file__),
                Path(prompt_http.__file__), *manifests.values(),
            )},
        }
        (args.output / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
        results = {}
        for suite, manifest in manifests.items():
            report = args.output / f"{suite}.json"
            if suite == "prompt-http":
                runner = prompt_http
                argv = ["--eclipse", endpoint, "--output", str(report)]
            elif suite == "actor-core":
                # The runner reports these cases as unsupported before opening a socket.
                with patch.object(sys, "argv", [suite, "--manifest", str(manifest),
                        "--ws-url", endpoint.replace("http:", "ws:", 1) + "/ws",
                        "--advertised-profile", "isotope", "--candidate", "n7-packaged",
                        "--report", str(report)]):
                    results[suite] = baseline.actor.main()
                continue
            else:
                runner = baseline
                argv = ["--manifest", str(manifest), "--url", endpoint, "--candidate", "n7-packaged",
                        "--profile", "isotope", "--report", str(report)]
                if suite == "interop-http":
                    argv += ["--peer", peer]
                elif suite == "local-node-rpc":
                    argv += ["--peer", source_url]
            with patch.object(runner, "Request", owner_request), patch.object(sys, "argv", [suite, *argv]):
                results[suite] = runner.main()
        return int(any(results.values()))


if __name__ == "__main__":
    raise SystemExit(main())
