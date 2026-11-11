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


def reference_profile_case(case, name, root, args, env):
    quoted = baseline.actor.prolog_quote_atom
    fixture = quoted(str(ROOT / 'adapters/reference_profile_policy.pl'))
    profile, expected = quoted(case['profile']), quoted(case['expected'])
    if name == 'swi':
        goal = (f"use_module({quoted(str(root / 'prolog/web_prolog.pl'))}),"
                f"use_module({fixture}),"
                f"(reference_profile_policy:check(node_profile_policy,{profile},{expected})->halt;halt(1))")
        command = [args.swipl, '-q', '-g', goal]
    else:
        goal = (f"use_module(profile_policy),use_module({fixture}),"
                f"(reference_profile_policy:check(profile_policy,{profile},{expected})->halt;halt(1))")
        command = [args.tpl, '-g', goal]
    result = subprocess.run(command, cwd=root, env=env, capture_output=True,
                            text=True, timeout=10)
    baseline.actor.require(result.returncode == 0,
                           f'profile policy failed: {result.stdout} {result.stderr}')
    return dict(scope='native profile policy', profile=case['profile'],
                expected=case['expected'], exit_code=result.returncode)


def query_rejection_case(case, url):
    candidate = baseline.actor.Candidate(url, 'actor', 8, None, None, False, ())
    with baseline.actor.Harness(candidate) as harness:
        options = '[session(true)]'
        if case.get('source'):
            options = '[session(true),src_text(' + baseline.actor.prolog_quote_atom(case['source']) + ')]'
        harness.spawn_shell(options)
        harness.call(case['goal'], '[limit(1)]')
        rejected = harness.recv_type('error', limit=64)
        formal = baseline.variant_tokens(rejected.get('details') or rejected.get('data', ''))
        baseline.actor.require(len(formal) > 3 and formal[:2] == ['error', '(']
                               and formal[2] in case['expected_error_names'], repr(rejected))
        if case.get('expected_formal'):
            # Ignore the implementation-specific context, but require the exact
            # formal error, including its domain/type and original culprit.
            observed = []
            depth = 0
            for token in formal[2:]:
                if token == ',' and depth == 0:
                    break
                observed.append(token)
                if token in ['(', '[', '{']:
                    depth += 1
                elif token in [')', ']', '}']:
                    depth -= 1
            baseline.actor.require(observed == baseline.variant_tokens(case['expected_formal']),
                                   repr(rejected))
        harness.call('RejectionRecovery=ok', '[limit(1)]')
        recovered = harness.recv_type('success', limit=64)
        baseline.actor.require(baseline.actor.row_value(recovered, 'RejectionRecovery') == 'ok'
                               and recovered.get('more') is False, repr(recovered))
        harness.halt()
        return dict(rejection=rejected, recovery=recovered)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--swi-root', type=Path, required=True)
    parser.add_argument('--trealla-root', type=Path, required=True)
    parser.add_argument('--swipl', default='swipl')
    parser.add_argument('--tpl', required=True)
    parser.add_argument('--mode', choices=['blacklist', 'whitelist', 'off'], default='blacklist')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    pack = json.loads(args.manifest.read_text())
    args.output.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    library = Path(args.tpl).resolve().parent / 'library'
    if library.is_dir():
        env['TPL_LIBRARY_PATH'] = str(library)
    rows = []
    # Each case uses a fresh shell plus rejection/recovery commands. Size the
    # disposable SWI fixture budget to the pack, without changing node defaults.
    ws_budget = max(1000, len(pack['cases']) * 10)
    for name, root in [('swi', args.swi_root), ('trealla', args.trealla_root)]:
        port = free_port()
        url = f'http://127.0.0.1:{port}'
        if name == 'swi':
            goal = (f"use_module({baseline.actor.prolog_quote_atom(str(root / 'prolog/web_prolog.pl'))}),"
                    "use_module(library(socket)),tcp_socket(Socket),"
                    f"tcp_bind(Socket,ip(127,0,0,1):{port}),tcp_listen(Socket,128),"
                    f"node:node({port},[tcp_socket(Socket),profile(actor),sandbox({args.mode}),auth(open),max_ws_commands_per_window({ws_budget})]),"
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
                    if case.get('candidate_error_formals'):
                        case['expected_formal'] = case['candidate_error_formals'][name]
                        case['expected_error_names'] = [case['expected_formal'].split('(')[0]]
                    row = dict(candidate=name, mode=args.mode, id=case['id'])
                    if args.mode not in case.get('only_sandbox_modes', ['blacklist', 'whitelist', 'off']):
                        row.update(status='not_applicable', detail='policy check for other sandbox modes')
                        rows.append(row)
                        continue
                    if args.mode not in case.get('sandbox_modes', ['blacklist', 'whitelist', 'off']):
                        row.update(status='deferred', detail=case['deferred_reason'])
                        rows.append(row)
                        print(name, row['id'], row['status'], row['detail'], flush=True)
                        continue
                    try:
                        if case['transport'] == 'http':
                            observed = baseline.http_case(case, url, 8, None, False)
                        elif case['transport'] == 'query':
                            observed = baseline.query_case(case, url.replace('http:', 'ws:') + '/ws', 8, None)
                        elif case['transport'] == 'query_rejection':
                            observed = query_rejection_case(case, url.replace('http:', 'ws:') + '/ws')
                        elif case['transport'] == 'profile_policy':
                            observed = reference_profile_case(case, name, root, args, env)
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
                  swi_fixture_ws_command_budget=ws_budget,
                  manifest_sha256=hashlib.sha256(args.manifest.read_bytes()).hexdigest())
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    return int(any(row['status'] == 'fail' for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
