#!/usr/bin/env python3
"""Real receive-guard controls on disposable native ACTOR sessions."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runner'))
from run import Candidate, Harness, prolog_quote_atom, row_value
from receive_control_peer import GuardPeer


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def answer(harness, goal):
    harness.call('(' + goal + '),ControlCheck=passed', '[limit(1)]')
    event = harness.recv_type('success', limit=32)
    if event.get('more') is not False or row_value(event, 'ControlCheck') != 'passed':
        raise AssertionError(event)
    return event


def observe(case, pack, url, peer):
    result = dict(control=case['control'], guard_target='primary-session' if case['control'] in ('abort', 'ordinary_error') else 'child-toplevel' if case['control'] == 'time_limit' else 'child-actor')
    with Harness(Candidate(url, 'actor', 5, None, None, False, ())) as h:
        source = case.get('source', '')
        extra = ',src_text(' + prolog_quote_atom(source) + ')' if source else ''
        h.spawn_shell('[session(true)' + extra + ']')
        raw_probe = pack['probe_goal']
        raw_ordinary = pack['ordinary_goal']
        recovery = pack['recovery_goal']
        if source:
            raw_probe = raw_probe.replace('GuardBinding=dirty,', 'GuardBinding=dirty,guard_private_marker(ok),')
            raw_ordinary = raw_ordinary.replace('GuardBinding=dirty,', 'GuardBinding=dirty,guard_private_marker(ok),').replace('GuardRecovered=passed', 'guard_private_body(ok),GuardRecovered=passed')
            recovery = 'guard_private_body(ok),(' + recovery + ')'
        probe = 'LibraryEntryURI=' + prolog_quote_atom(peer.url) + ',(' + raw_probe + ')'
        if case['control'] in ('abort', 'ordinary_error'):
            goal = probe if case['control'] == 'abort' else 'LibraryEntryURI=' + prolog_quote_atom(peer.url) + ',(' + raw_ordinary + '),ControlCheck=passed'
            h.call(goal, '[limit(1)]')
        elif case['control'] == 'time_limit':
            result['setup'] = answer(h, f'toplevel_spawn(Target,[session(true),time_limit({case["time_limit"]}){extra}]),toplevel_call(Target,({probe}),[template(true)])')
            target = row_value(result['setup'], 'Target')
        else:
            result['setup'] = answer(h, 'spawn((' + probe + '),Target,[monitor(true)' + extra + '])')
            target = row_value(result['setup'], 'Target')
        peer.require_held_entry()
        result['entry_count'] = len(peer.requests)
        result['peer_held_at_control'] = not peer.release.is_set()
        if case['control'] == 'abort':
            h.send(dict(command='toplevel_abort', pid=h.shell))
            event = h.recv()
            if event.get('type') != 'abort':
                raise AssertionError(event)
            result['control_response'] = event
            result['recovery'] = answer(h, recovery)
        elif case['control'] == 'time_limit':
            result['control_and_recovery'] = answer(h,
                f'receive({{error({target},error(resource_error(time),_))->true}},[timeout(3),on_timeout(throw(missing_time_error))]),'
                f'toplevel_call({target},({recovery}),[template(recovered)]),'
                f'receive({{success({target},[recovered],false)->true}},[timeout(3),on_timeout(throw(missing_recovery))]),'
                f'toplevel_halt({target},true)')
            result['formal_error_checked'] = 'error(resource_error(time),_)'
        elif case['control'] == 'terminate':
            result['control_response'] = answer(h,
                f'exit({target},guard_terminated),receive({{down({target},{target},guard_terminated)->true}},'
                '[timeout(3),on_timeout(throw(missing_termination))])')
        else:
            peer.body = b'error(guard_ordinary).\n'
            peer.release.set()
            event = h.recv_type('success', limit=32)
            if event.get('more') is not False or row_value(event, 'ControlCheck') != 'passed':
                raise AssertionError(event)
            result['ordinary_response'] = event
        if case['control'] != 'ordinary_error' and peer.release.is_set():
            raise AssertionError('RPC released before control and recovery')
        result['health'] = answer(h, 'true')
        h.halt()
        result['halt_confirmed'] = True
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ('swipl', 'tpl'):
        p.add_argument('--' + arg, required=True)
    for arg in ('swi-root', 'trealla-root', 'output'):
        p.add_argument('--' + arg, type=Path, required=True)
    p.add_argument('--manifest', type=Path, default=ROOT / 'cases/receive-control-0.1.json')
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=False)
    pack = json.loads(a.manifest.read_text())
    rows, sources = [], {}
    for name in ('swi', 'trealla'):
        root = a.swi_root if name == 'swi' else a.trealla_root
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
        env = os.environ.copy()
        env['TPL_LIBRARY_PATH'] = str(Path(a.tpl).parent / 'library')
        if name == 'swi':
            cmd = [a.swipl, '-f', 'none', '-q', '-g', f'use_module({prolog_quote_atom(str(root / "prolog/web_prolog.pl"))}),node({port},[profile(actor),auth(open)]),thread_get_message(stop)']
        else:
            cmd = [a.tpl, '-g', f'use_module(distribution),web_prolog:web_prolog_node({port},[])']
        scope = root / 'prolog' if name == 'swi' else root
        files = scope.rglob('*.pl') if name == 'swi' else scope.glob('*.pl')
        sources[name] = dict(revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
            executable_sha256=sha(cmd[0]), files_sha256={str(f.relative_to(root)): sha(f) for f in sorted(files)})
        with (a.output / (name + '.log')).open('w') as log:
            node = subprocess.Popen(cmd, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT)
            try:
                for _ in range(150):
                    if node.poll() is not None:
                        raise RuntimeError(name + ' startup')
                    try:
                        with socket.create_connection(('127.0.0.1', port), timeout=.1):
                            break
                    except OSError:
                        time.sleep(.03)
                else:
                    raise TimeoutError('startup')
                for case in pack['cases']:
                    row = dict(candidate=name, id=case['id'], title=case['title'])
                    with GuardPeer() as peer:
                        try:
                            row.update(status='pass', observation=observe(case, pack, f'ws://127.0.0.1:{port}/ws', peer))
                        except Exception as error:
                            row.update(status='fail', detail=str(error))
                        row['peer_requests'] = peer.requests
                    rows.append(row)
                    print(name, case['id'], row['status'], flush=True)
            finally:
                node.terminate()
                try:
                    node.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    node.kill()
                    node.wait(timeout=2)
    report = dict(suite=pack['suite'], manifest_sha256=sha(a.manifest), adapter_sha256=sha(__file__), peer_sha256=sha(Path(__file__).with_name('receive_control_peer.py')),
                  sources=sources, results=rows, counts={s: sum(r['status'] == s for r in rows) for s in ('pass', 'fail')})
    (a.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    return int(report['counts']['fail'] > 0)


if __name__ == '__main__':
    raise SystemExit(main())
