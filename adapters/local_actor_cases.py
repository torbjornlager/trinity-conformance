#!/usr/bin/env python3
"""Run a shared finite actor selection in fresh disposable native sessions."""
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
from baseline import query_case
from run import prolog_quote_atom


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ('swipl', 'tpl'):
        p.add_argument('--' + arg, required=True)
    for arg in ('swi-root', 'trealla-root', 'manifest', 'output'):
        p.add_argument('--' + arg, type=Path, required=True)
    p.add_argument('--sandbox', choices=['blacklist', 'whitelist', 'off'])
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=False)
    pack = json.loads(a.manifest.read_text())
    rows, sources = [], {}
    for name in ('swi', 'trealla'):
        root = a.swi_root if name == 'swi' else a.trealla_root
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        env = os.environ.copy()
        for key in ('WP_CONFIG_FILE', 'SWI_HOME_DIR', 'SWIPL_HOME_DIR', 'WP_NATIVE_STATE', 'WP_NATIVE_MODE'):
            env.pop(key, None)
        if name == 'swi':
            policy = ',sandbox('+a.sandbox+')' if a.sandbox else ''
            command = [a.swipl, '-f', 'none', '-q', '-g', f'use_module({prolog_quote_atom(str(root / "prolog/web_prolog.pl"))}),node({port},[profile(actor),auth(open),max_session_spawns_per_window(1000){policy}]),thread_get_message(stop)']
        else:
            env['TPL_LIBRARY_PATH'] = str(Path(a.tpl).parent / 'library')
            policy = ',sandbox('+a.sandbox+')' if a.sandbox else ''
            command = [a.tpl, '-g', f'use_module(distribution),web_prolog:web_prolog_node({port},[max_session_spawns_per_window(1000){policy}])']
        scope = root / 'prolog' if name == 'swi' else root
        files = scope.rglob('*.pl') if name == 'swi' else scope.glob('*.pl')
        sources[name] = dict(revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
                             tracked_diff_sha256=hashlib.sha256(subprocess.check_output(['git', 'diff', 'HEAD', '--'], cwd=root)).hexdigest(),
                             executable_sha256=sha(command[0]), files_sha256={str(f.relative_to(root)): sha(f) for f in sorted(files)})
        with (a.output / (name + '.log')).open('w') as log:
            node = subprocess.Popen(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT)
            try:
                for _ in range(150):
                    if node.poll() is not None:
                        raise RuntimeError(name + ' startup failed; see log')
                    try:
                        with socket.create_connection(('127.0.0.1', port), timeout=.1):
                            break
                    except OSError:
                        time.sleep(.03)
                else:
                    raise TimeoutError(name + ' startup')
                for case in pack['cases']:
                    row = dict(candidate=name, id=case['id'], title=case['title'])
                    try:
                        selected = dict(case, source=pack.get('source', '') + '\n' + case.get('source', ''))
                        row.update(status='pass', observation=query_case(selected, f'ws://127.0.0.1:{port}/ws', 8, None))
                    except Exception as error:
                        row.update(status='fail', detail=str(error))
                    rows.append(row)
                    print(name, case['id'], row['status'], flush=True)
            finally:
                node.terminate()
                try:
                    node.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    node.kill()
                    node.wait(timeout=2)
    report = dict(suite=pack['suite'], manifest_sha256=sha(a.manifest), adapter_sha256=sha(__file__),
                  sources=sources, sandbox=a.sandbox or 'runtime default', scope='Disposable native ACTOR WebSocket sessions; fresh session per case', results=rows,
                  counts={s: sum(r['status'] == s for r in rows) for s in ('pass', 'fail')})
    (a.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    return int(report['counts']['fail'] > 0)


if __name__ == '__main__':
    raise SystemExit(main())
