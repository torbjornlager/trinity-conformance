#!/usr/bin/env python3
"""Observe experimental text semantics on disposable, committed native sources.

Reader defaults are deliberately unchanged. Experimental failures are results,
not reasons to modify runtime sources or deployed configurations.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time

from local_promises import ROOT, free_port, git, preservation, quote, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['swipl', 'tpl', 'swi-root', 'trealla-root', 'demonstrator-root', 'output']:
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    for key in ['swipl', 'tpl', 'swi_root', 'trealla_root', 'demonstrator_root']:
        # Retain launcher paths: resolving the SWI symlink can change home lookup.
        path = getattr(args, key).absolute()
        if not path.exists(): parser.error('missing input: '+str(path))
        setattr(args, key, path)
    output = args.output.absolute()
    output.mkdir(parents=True, exist_ok=False)
    pin = args.demonstrator_root/'dependencies/swi-prolog-node.json'
    def snapshot():
        value = preservation(args.swi_root, args.trealla_root, args.swipl, args.tpl)
        value['dependency_pin'] = sha(pin)
        return value
    before = snapshot()
    inputs = [ROOT/'cases/portable-text-0.2.json', ROOT/'profiles/portable-text-0.2.md',
              ROOT/'runner/run.py', ROOT/'runner/portable_text.py',
              ROOT/'fixtures/portable-text/portable-text.pl', Path(__file__),
              ROOT/'adapters/local_promises.py']
    provenance = {'runs': [], 'sources': {}, 'nodes': {},
                  'inputs': {str(p.relative_to(ROOT)): sha(p) for p in inputs},
                  'configuration': 'ACTOR/blacklist, unchanged reader defaults; experimental observation',
                  'engine_hashes': before['engines']}
    requests = []
    class Handler(SimpleHTTPRequestHandler):
        def log_message(self, fmt, *values): requests.append(fmt % values)
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(
        Handler, directory=str(ROOT/'fixtures/portable-text')))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    source_base = 'http://127.0.0.1:'+str(server.server_port)
    provenance['source_fixture'] = source_base
    processes = []
    logs = []
    env = dict(os.environ, TPL_LIBRARY_PATH=str(args.tpl.parent/'library'))
    for key in ['SWI_HOME_DIR', 'SWIPL_HOME_DIR', 'WP_CONFIG_FILE', 'WP_ASSET_ROOT',
                'WP_WASM_SOURCE_DIR', 'WP_NATIVE_STATE', 'WP_NATIVE_MODE']:
        env.pop(key, None)
    try:
        with tempfile.TemporaryDirectory(prefix='portable-text-') as temporary:
            for name, root in [('swi', args.swi_root), ('trealla', args.trealla_root)]:
                revision = git(root, 'rev-parse', 'HEAD')
                archive = Path(temporary)/(name+'.tar')
                subprocess.run(['git', '-C', str(root), 'archive', '--format=tar',
                                '--output='+str(archive), revision], check=True)
                checkout = Path(temporary)/name
                checkout.mkdir()
                subprocess.run(['tar', '-xf', str(archive), '-C', str(checkout)], check=True)
                provenance['sources'][name] = dict(revision=revision,
                    archive_sha256=sha(archive), checkout=str(checkout),
                    excluded_working_tree_status=git(root, 'status', '--short'))
                port = free_port()
                url = 'http://127.0.0.1:'+str(port)
                policy = 'load_uri_allowed_origins(['+quote(source_base)+'])'
                if name == 'swi':
                    goal = (f"use_module(library(sgml)),use_module(library(option)),consult({quote(checkout/'load.pl')}),"
                        f"set_setting(http:public_host,'127.0.0.1'),set_setting(http:public_port,{port}),"
                        "set_setting(http:public_scheme,http),use_module(library(socket)),tcp_socket(S),"
                        f"tcp_bind(S,ip(127,0,0,1):{port}),tcp_listen(S,128),"
                        f"node:node({port},[tcp_socket(S),profile(actor),sandbox(blacklist),auth(open),{policy}]),"
                        'thread_get_message(stop)')
                    command = [str(args.swipl), '-f', 'none', '-q', '-g', goal]
                else:
                    goal = ("use_module(web_prolog),use_module(distribution),"
                        f"web_prolog:web_prolog_node({port},[bind_address('127.0.0.1'),node_url({quote(url)}),"
                        f"profile(actor),sandbox(blacklist),auth(open),{policy},"
                        "load_uri_allowed_ip_ranges(['127.0.0.1'])]),thread_get_message(stop)")
                    command = [str(args.tpl), '-g', goal]
                log = (output/(name+'-node.log')).open('w')
                logs.append(log)
                proc = subprocess.Popen(command, cwd=checkout, env=env,
                    stdout=log, stderr=log, start_new_session=True)
                processes.append(proc)
                provenance['nodes'][name] = dict(url=url, pid=proc.pid, command=command)
                for _ in range(150):
                    if proc.poll() is not None: raise RuntimeError(name+' startup failed')
                    try:
                        with socket.create_connection(('127.0.0.1', port), timeout=.1): break
                    except OSError: time.sleep(.05)
                else: raise TimeoutError(name+' startup')
            for caller, peer in [('swi', 'trealla'), ('trealla', 'swi')]:
                label = caller+'-portable-text'
                command = [sys.executable, 'runner/run.py', '--manifest', 'cases/portable-text-0.2.json',
                    '--candidate', caller, '--ws-url', provenance['nodes'][caller]['url'].replace('http:', 'ws:')+'/ws',
                    '--advertised-profile', 'actor', '--timeout', '5',
                    '--peer', provenance['nodes'][peer]['url'], '--source-base', source_base,
                    '--report', str(output/(label+'.json'))]
                with (output/(label+'.log')).open('w') as log:
                    result = subprocess.run(command, cwd=ROOT, env=env, stdout=log,
                                            stderr=subprocess.STDOUT, timeout=180)
                provenance['runs'].append(dict(label=label, report=label+'.json',
                    exit_code=result.returncode, command=command, peer=peer))
                print(label, result.returncode, flush=True)
    finally:
        for proc in reversed(processes):
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGTERM)
                try: proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
        for log in logs: log.close()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        provenance['source_requests'] = requests
        after = snapshot()
        checks = {key: before[key] == after[key] for key in before}
        (output/'preservation.json').write_text(json.dumps(dict(
            checks=checks, before=before, after=after), indent=2)+'\n')
        (output/'provenance.json').write_text(json.dumps(provenance, indent=2)+'\n')
        if not all(checks.values()): raise RuntimeError('preservation check failed')


if __name__ == '__main__': main()
