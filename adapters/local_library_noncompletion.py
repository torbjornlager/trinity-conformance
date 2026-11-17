#!/usr/bin/env python3
"""Isolated native countall probes with an external callback entry peer."""
import argparse
import hashlib
import http.server
import json
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runner'))
from library_noncompletion import bounds, validate_observation


def atom(value):
    return "'" + str(value).replace('\\', '\\\\').replace("'", "''") + "'"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def terminate(process):
    started = time.monotonic()
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            # The child can exit between poll and killpg. If it is still
            # alive, target our owned child directly rather than its group.
            if process.poll() is None:
                process.terminate()
        try:
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=1)
    return dict(confirmed=process.poll() is not None, returncode=process.returncode,
                duration_ms=round((time.monotonic() - started) * 1000))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('swi', 'trealla', 'gnu'):
        parser.add_argument('--' + name + '-root', type=Path, required=True)
    parser.add_argument('--swipl', required=True)
    parser.add_argument('--tpl', required=True)
    parser.add_argument('--manifest', type=Path, default=ROOT / 'cases/library-noncompletion-0.1.json')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    pack = json.loads(args.manifest.read_text())
    entries, lock = {}, threading.Lock()

    class Peer(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            parsed = urllib.parse.urlsplit(self.path)
            key = parsed.path.removesuffix('/call').strip('/')
            with lock:
                item = entries.setdefault(key, dict(count=0, finished=False, requests=[]))
                item['count'] += 1
                item['requests'].append(urllib.parse.parse_qs(parsed.query))
            body = b'success([v],false).\n'
            self.send_response(200)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            self.wfile.flush()
            with lock:
                item['finished'] = True

    peer = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Peer)
    thread = threading.Thread(target=peer.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{peer.server_port}'
    rows, sources = [], {}
    try:
        with tempfile.TemporaryDirectory(prefix='countall-noncompletion-') as tmp:
            policy = Path(tmp) / 'outbound-policy'
            policy.write_text(f'http 127.0.0.1 {peer.server_port} 127.0.0.1\n')
            policy.chmod(0o600)
            env = dict(os.environ, TPL_LIBRARY_PATH=str(Path(args.tpl).parent / 'library'), ISO_OUTBOUND_POLICY=str(policy))
            for name in ('swi', 'trealla', 'gnu'):
                root = getattr(args, name + '_root')
                executable = args.swipl if name == 'swi' else args.tpl if name == 'trealla' else str(root / 'isobase/query-worker')
                sources[name] = dict(revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
                                     tracked_diff_sha256=hashlib.sha256(subprocess.check_output(['git', 'diff', 'HEAD', '--'], cwd=root)).hexdigest(),
                                     executable=executable, executable_sha256=sha(executable))
                scope = root / 'prolog' if name == 'swi' else root / 'isobase' if name == 'gnu' else root
                sources[name]['prolog_sha256'] = {str(p.relative_to(root)): sha(p) for p in sorted(scope.rglob('*.pl') if name == 'swi' else scope.glob('*.pl')) if p.is_file()}

                def command(goal):
                    if name == 'swi':
                        return [executable, '-f', 'none', '-q', '-g', f'use_module({atom(root / "prolog/web_prolog.pl")}),use_module({atom(root / "prolog/web_prolog/standard_library.pl")}),(catch(({goal}),E,(writeq(E),nl,fail))->write(control_passed),nl,halt;halt(1))']
                    if name == 'trealla':
                        return [executable, '-g', f'use_module(actors),use_module(rpc),source_policy:configure_source_policy([load_uri_allowed_origins([{atom(base)}]),load_uri_allowed_ip_ranges([\'127.0.0.0/8\'])],_),(catch(({goal}),E,(writeq(E),nl,fail))->write(control_passed),nl,halt;halt(1))']
                    return [executable, 'query((' + goal + '),control_passed)', '1']

                def entry(key):
                    with lock:
                        return json.loads(json.dumps(entries.get(key, dict(count=0, finished=False, requests=[]))))

                def control(case, phase):
                    key = name + '-' + case['id'] + '-' + phase
                    goal = 'LibraryEntryURI=' + atom(base + '/' + key) + ',(' + case['warmup_goal'] + ')'
                    result = subprocess.run(command(goal), cwd=root, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=8)
                    correct = result.stdout.strip() == 'control_passed' if name != 'gnu' else json.loads(result.stdout) == dict(type='success', answers=['control_passed'], more=False)
                    marker = entry(key)
                    observed = dict(passed=result.returncode == 0 and correct and not result.stderr,
                                    entry_count=marker['count'], stdout=result.stdout, stderr=result.stderr, requests=marker['requests'])
                    if not observed['passed'] or marker['count'] != 1:
                        raise AssertionError(observed)
                    return observed

                for case in pack['cases']:
                    row = dict(candidate=name, id=case['id'], title=case['title'])
                    observed = {}
                    process = None
                    try:
                        window, entry_timeout, _ = bounds(case)
                        observed['warmup'] = control(case, 'warmup')
                        key = name + '-' + case['id'] + '-probe'
                        goal = 'LibraryEntryURI=' + atom(base + '/' + key) + ',(' + case['goal'] + ')'
                        process = subprocess.Popen(command(goal), cwd=root, env=env, stdin=subprocess.DEVNULL,
                                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
                        entry_deadline = time.monotonic() + entry_timeout / 1000
                        while not entry(key)['finished']:
                            if process.poll() is not None:
                                raise AssertionError('query exited before callback entry: ' + repr(process.communicate()))
                            if time.monotonic() >= entry_deadline:
                                raise TimeoutError('callback entry deadline')
                            time.sleep(.005)
                        started = time.monotonic()
                        readable, _, _ = select.select([process.stdout, process.stderr], [], [], window / 1000)
                        elapsed = (time.monotonic() - started) * 1000
                        marker = entry(key)
                        observed['probe'] = dict(entry_count=marker['count'], entry_response_finished=marker['finished'],
                                                 requests=marker['requests'], elapsed_ms=elapsed,
                                                 terminal='query output before termination' if readable else None,
                                                 alive_before_termination=process.poll() is None)
                        observed['termination'] = terminate(process)
                        stdout, stderr = process.communicate(timeout=1)
                        observed['termination'].update(stdout=stdout.decode(), stderr=stderr.decode())
                        observed['recovery'] = control(case, 'recovery')
                        validate_observation(case, observed)
                        row.update(status='pass', observation=observed)
                    except Exception as error:
                        row.update(status='fail', detail=str(error), observation=observed)
                    finally:
                        if process is not None:
                            observed['cleanup'] = terminate(process)
                    rows.append(row)
                    print(name, case['id'], row['status'], flush=True)
    finally:
        peer.shutdown()
        peer.server_close()
        thread.join(timeout=1)
    report = dict(suite=pack['suite'], scope='Standalone native APIs/private GNU worker; externally terminated processes, not public-node transport',
                  manifest_sha256=sha(args.manifest), adapter_sha256=sha(__file__), validator_sha256=sha(ROOT / 'runner/library_noncompletion.py'),
                  sources=sources, results=rows, counts={s: sum(r['status'] == s for r in rows) for s in ('pass', 'fail')})
    (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    return int(report['counts']['fail'] > 0)


if __name__ == '__main__':
    raise SystemExit(main())
