#!/usr/bin/env python3
"""Run shared Boolean cases with resource inventories and a loopback source counter."""
import argparse
import http.server
import json
import os
from pathlib import Path
import subprocess
import threading

ROOT = Path(__file__).resolve().parents[1]


def quote(value):
    return "'" + str(value).replace('\\', '\\\\').replace("'", "''") + "'"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['swi-root', 'trealla-root', 'tpl', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    requests = []

    class Peer(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            requests.append(self.path.split('?')[0])
            body = b'should_not_be_fetched(ok).\n'
            self.send_response(200)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    peer = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Peer)
    threading.Thread(target=peer.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{peer.server_port}'
    pack = json.loads((ROOT / 'cases/boolean-options-0.1.json').read_text())
    fixture = ROOT / 'adapters/native_boolean_checks.pl'
    env = dict(os.environ, TPL_LIBRARY_PATH=str(args.tpl.parent / 'library'))
    results = []
    try:
        for host, root in [('swi', args.swi_root), ('trealla', args.trealla_root)]:
            modules = ['actors', 'toplevel_actors', 'rpc', 'statechart_actor',
                       'server_actor', 'supervisor_actor']
            folder = root / 'prolog/web_prolog' if host == 'swi' else root
            imports = ''.join(':- use_module(' + quote(folder / (m + '.pl')) + ').\n'
                              for m in modules)
            imports = ':- style_check(-singleton).\n' + imports
            imports += ':- use_module(' + quote(fixture) + ').\n'
            lines = []
            for case in pack['cases']:
                goal = case['native_goal']
                if case['id'].startswith(('BOOL-spawn-', 'BOOL-server-', 'BOOL-supervisor-',
                                           'BOOL-toplevel-', 'BOOL-rpc-', 'BOOL-promise-')):
                    # Add a source occurrence before the invalid scalar. Validation
                    # must finish before either fetching it or dispatching the call.
                    goal = goal.replace('Options=[', 'Options=[src_uri(' + quote(base + '/source.pl') + '),', 1)
                if case['id'].startswith('BOOL-chart-'):
                    goal = goal.replace("src_text('<invalid/>')",
                                        'src_uri(' + quote(base + '/source.xml') + ')')
                goal = goal.replace("'http://127.0.0.1:1'", quote(base))
                lines.append('check(' + quote(case['id']) + ',(' + goal + ')).\n')
            program = args.output / (host + '-negative.pl')
            program.write_text(imports + ''.join(lines) + '''
run :- forall(check(Id,Goal),
    (native_boolean_checks:negative(Goal) -> format('PASS ~w~n',[Id])
    ; throw(boolean_case_failed(Id)))).
''')
            for kind, load, goal in [('negative', program, 'run'),
                                     ('positive', program, 'native_boolean_checks:positive')]:
                command = (["swipl", '-f', 'none', '-q', '-g'] if host == 'swi'
                           else [str(args.tpl), '-g'])
                query = 'consult(' + quote(load) + '),(catch((' + goal + "),E,(write_canonical(E),nl,fail))->halt;halt(1))"
                start = len(requests)
                run = subprocess.run(command + [query], cwd=root, env=env,
                                     capture_output=True, text=True, timeout=45)
                seen = requests[start:]
                ok = run.returncode == 0 and not seen
                if kind == 'negative':
                    ok = ok and len([s for s in run.stdout.splitlines() if s.startswith('PASS ')]) == len(pack['cases'])
                results.append(dict(host=host, kind=kind, status='pass' if ok else 'fail',
                                    exit_code=run.returncode, requests=seen,
                                    stdout=run.stdout, stderr=run.stderr))
                print(host, kind, results[-1]['status'], flush=True)
    finally:
        peer.shutdown()
        peer.server_close()
    (args.output / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    return int(any(r['status'] != 'pass' for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
