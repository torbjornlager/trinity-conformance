#!/usr/bin/env python3
"""Run identical page/error assertions on disposable native loopback nodes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runner'))
import baseline


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def toplevel_case(case, url):
    candidate = baseline.actor.Candidate(url.replace('http:', 'ws:') + '/ws',
                                        'actor', 6, None, None, False, ())
    observed = []
    with baseline.actor.Harness(candidate) as harness:
        harness.spawn_shell()
        for step in case['steps']:
            if step['command'] == 'call':
                harness.call(step['goal'], step.get('options', '[]'))
            elif step['command'] == 'next':
                harness.next()
            else:
                harness.send(dict(command='toplevel_stop', pid=harness.shell))
            event = harness.recv_type(step['expect_type'], limit=16)
            baseline.actor.require(event.get('pid') == harness.shell, repr(event))
            if 'values' in step:
                rows = event.get('data')
                baseline.actor.require(isinstance(rows, list), repr(event))
                values = [row.get('X') if isinstance(row, dict) else row for row in rows]
                baseline.actor.require(values == step['values'], repr(event))
                baseline.actor.require(event.get('more') is step['more'], repr(event))
            if 'error' in step:
                # SWI provides a human display in data and the public term in
                # details; Trealla's legacy envelope places that term in data.
                error = event.get('details', event.get('data', ''))
                baseline.actor.require(str(error).strip() == step['error'], repr(event))
            observed.append(event)
        harness.halt()
    return observed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--swi-root', type=Path, required=True)
    parser.add_argument('--trealla-root', type=Path, required=True)
    parser.add_argument('--swipl', default='swipl')
    parser.add_argument('--tpl', required=True)
    parser.add_argument('--mode', choices=['blacklist', 'whitelist'], default='blacklist')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = ROOT / 'cases/partial-page-errors-0.1.json'
    packs = [json.loads(manifest.read_text()),
             json.loads((ROOT / 'cases/error-contract-0.1.json').read_text())]
    env = os.environ.copy()
    library = Path(args.tpl).resolve().parent / 'library'
    if library.is_dir():
        env['TPL_LIBRARY_PATH'] = str(library)
    rows = []
    for name, root in [('swi', args.swi_root), ('trealla', args.trealla_root)]:
        port = free_port()
        url = f'http://127.0.0.1:{port}'
        if name == 'swi':
            goal = (f"use_module({baseline.actor.prolog_quote_atom(str(root / 'prolog/web_prolog.pl'))}),"
                    "use_module(library(socket)),tcp_socket(Socket),"
                    f"tcp_bind(Socket,ip(127,0,0,1):{port}),tcp_listen(Socket,128),"
                    f"node:node({port},[tcp_socket(Socket),profile(actor),sandbox({args.mode}),auth(open),timeout(1)]),"
                    'thread_get_message(stop)')
            command = [args.swipl, '-q', '-g', goal]
        else:
            goal = (f"use_module(distribution),web_prolog:web_prolog_node({port},"
                    f"[bind_address('127.0.0.1'),profile(actor),sandbox({args.mode}),auth(open),time_limit(1)])")
            command = [args.tpl, '-g', goal]
        with (args.output / f'{name}-node.log').open('w') as log:
            process = subprocess.Popen(command, cwd=root, env=env, stdout=log, stderr=log)
            try:
                deadline = time.monotonic() + 10
                while True:
                    if process.poll() is not None:
                        raise RuntimeError(f'{name} exited during startup: {process.returncode}')
                    try:
                        with urlopen(url + '/node_info', timeout=.3):
                            break
                    except OSError:
                        if time.monotonic() >= deadline:
                            raise TimeoutError(f'{name} readiness timed out')
                        time.sleep(.05)
                for pack in packs:
                    for case in pack['cases']:
                        # This gate covers paging plus existing and strengthened
                        # integer zero-divisor cases, not unrelated admission policy.
                        if pack['suite'] == 'error-contract-0.1' and case['id'] not in {
                                'ER-011', 'ER-012', 'ER-013', 'ER-014', 'ER-015', 'ER-016'}:
                            continue
                        row = dict(candidate=name, mode=args.mode, id=case['id'])
                        try:
                            if case['transport'] == 'http':
                                observed = baseline.http_case(case, url, 6, None, False)
                            else:
                                observed = toplevel_case(case, url)
                            row.update(status='pass', observation=observed)
                        except Exception as error:
                            row.update(status='fail', detail=f'{type(error).__name__}: {error}')
                        rows.append(row)
                        print(name, row['id'], row['status'], row.get('detail', ''), flush=True)
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
    report = dict(mode=args.mode, results=rows,
                  manifests={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in [manifest, ROOT / 'cases/error-contract-0.1.json']})
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    return int(any(row['status'] != 'pass' for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
