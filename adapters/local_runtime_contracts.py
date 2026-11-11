#!/usr/bin/env python3
"""Run a shared baseline selection on disposable native loopback nodes."""
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--swi-root', type=Path, required=True)
    parser.add_argument('--trealla-root', type=Path, required=True)
    parser.add_argument('--swipl', default='swipl')
    parser.add_argument('--tpl', required=True)
    parser.add_argument('--mode', choices=['blacklist', 'whitelist'], default='blacklist')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    pack = json.loads(args.manifest.read_text())
    args.output.mkdir(parents=True, exist_ok=True)
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
                    f"node:node({port},[tcp_socket(Socket),profile(actor),sandbox({args.mode}),auth(open)]),"
                    'thread_get_message(stop)')
            command = [args.swipl, '-q', '-g', goal]
        else:
            goal = (f"use_module(distribution),web_prolog:web_prolog_node({port},"
                    f"[bind_address('127.0.0.1'),profile(actor),sandbox({args.mode}),auth(open)])")
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
                for original in pack['cases']:
                    case = dict(original)
                    if pack.get('source'):
                        case['source'] = pack['source']
                    row = dict(candidate=name, mode=args.mode, id=case['id'])
                    try:
                        if case['transport'] == 'http':
                            observed = baseline.http_case(case, url, 8, None, False)
                        elif case['transport'] == 'query':
                            observed = baseline.query_case(case, url.replace('http:', 'ws:') + '/ws', 8, None)
                        else:
                            raise ValueError(f"unsupported transport: {case['transport']}")
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
    report = dict(suite=pack['suite'], mode=args.mode, results=rows,
                  manifest_sha256=hashlib.sha256(args.manifest.read_bytes()).hexdigest())
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    return int(any(row['status'] != 'pass' for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
