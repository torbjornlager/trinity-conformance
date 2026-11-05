#!/usr/bin/env python3
"""Check configured SWI settings on three simultaneous nodes, without deployment."""
import argparse
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runner'))
from baseline import http_case, variant_tokens
from run import Candidate, Harness, row_value
from local_standard_library import atom, port, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--swipl', required=True)
    parser.add_argument('--swi-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    fixtures = []
    commands = [f'use_module({atom(args.swi_root / "prolog/web_prolog.pl")})']
    for i, profile in enumerate(['isobase', 'isotope', 'actor']):
        n = port()
        while any(f['port'] == n for f in fixtures):
            n = port()
        values = dict(profile=profile, sandbox='blacklist', auth='dev' if i == 1 else 'open',
                      timeout=7+i, rate_window_seconds=73+i, max_inflight_calls=11+i,
                      max_term_text_bytes=65536+i, max_call_requests_per_window=1000+i,
                      max_load_text_bytes=131072+i, load_uri_allowed_origins=[],
                      max_sessions_per_principal=19+i, max_session_spawns_per_window=211+i,
                      max_ws_actors_per_principal=23+i, max_ws_frame_bytes=262144+i,
                      max_ws_commands_per_window=307+i)
        def term(v):
            return '[]' if v == [] else str(v) if isinstance(v, int) else atom(v)
        options = [f'{k}({term(v)})' for k, v in values.items()]
        options.append('dev_principal(ns_private_principal)')
        commands.append(f'node({n},[' + ','.join(options) + '])')
        expected = dict(values, url=f'http://localhost:{n}')
        if profile != 'actor':
            for key in ['max_ws_actors_per_principal', 'max_ws_frame_bytes', 'max_ws_commands_per_window']:
                del expected[key]
        if profile == 'isobase':
            for key in ['max_sessions_per_principal', 'max_session_spawns_per_window']:
                del expected[key]
        pairs = '[' + ','.join(atom(k)+'-'+term(v) for k, v in sorted(expected.items())) + ']'
        comparison = f'Sorted=={pairs}'
        goal = 'findall(K-V,node_setting(K,V),Pairs),sort(Pairs,Sorted),'+comparison
        fixtures.append(dict(profile=profile, port=n, url=f'http://127.0.0.1:{n}', expected=expected, goal=goal, comparison=comparison))
    commands.append('thread_get_message(stop)')
    env = os.environ.copy()
    for key in ['WP_CONFIG_FILE', 'SWI_HOME_DIR', 'SWIPL_HOME_DIR', 'WP_NATIVE_STATE', 'WP_NATIVE_MODE']:
        env.pop(key, None)
    rows = []
    with (args.output / 'swi.log').open('w+') as log:
        process = subprocess.Popen([args.swipl, '-f', 'none', '-q', '-g', ','.join(commands)],
                                   cwd=args.swi_root, env=env, stdout=log, stderr=subprocess.STDOUT)
        try:
            for fixture in fixtures:
                for _ in range(200):
                    if process.poll() is not None:
                        log.seek(0)
                        raise RuntimeError(log.read())
                    try:
                        with socket.create_connection(('127.0.0.1', fixture['port']), timeout=.1):
                            break
                    except OSError:
                        time.sleep(.03)
                else:
                    raise TimeoutError('node startup')
            for index, fixture in enumerate(fixtures):
                for spoof in [False, True]:
                    row = dict(candidate='swi', id='NS-CONFIG-'+fixture['profile']+('-host' if spoof else ''),
                               title='Exact configured settings of servicing node', expected=fixture['expected'])
                    params = dict(goal='('+fixture['goal']+'),NodeCheck=passed', template='NodeCheck', format='prolog', limit=1)
                    try:
                        if spoof:
                            other = fixtures[(index+1) % len(fixtures)]
                            request = Request(fixture['url']+'/call?'+urlencode(params),
                                              headers={'Host': 'localhost:'+str(other['port'])})
                            with urlopen(request, timeout=8) as response:
                                body = response.read().decode()
                            if variant_tokens(body) != variant_tokens('success([passed],false).'):
                                raise AssertionError(body)
                            observation = dict(body=body, host_header=request.get_header('Host'))
                        else:
                            observation = http_case(dict(requests=[dict(params=params, expect_prolog='success([passed],false).')]), fixture['url'], 8, None, False)
                        row.update(status='pass', observation=observation)
                    except Exception as error:
                        row.update(status='fail', detail=str(error))
                    rows.append(row)
                    print(row['id'], row['status'], flush=True)
            fixture = fixtures[-1]
            with Harness(Candidate('ws://127.0.0.1:'+str(fixture['port'])+'/ws', 'actor', 8, None, fixture['url'], False, ())) as harness:
                harness.spawn_shell('[session(true)]')
                for case_id, goal in [
                    ('NS-CONFIG-retained', fixture['goal']),
                    ('NS-CONFIG-child', 'self(Me),spawn((findall(K-V,node_setting(K,V),Pairs),Me!ns_settings(Pairs)),_,[]),receive({ns_settings(Pairs)->sort(Pairs,Sorted)},[timeout(3)]),'+fixture['comparison']),
                ]:
                    row = dict(candidate='swi', id=case_id, title='Configured settings survive actor context propagation')
                    try:
                        harness.call('('+goal+'),NodeCheck=passed', '[limit(1)]')
                        event = harness.recv()
                        if event.get('type') != 'success' or event.get('more') is not False or row_value(event, 'NodeCheck') != 'passed':
                            raise AssertionError(event)
                        row.update(status='pass', observation=event)
                    except Exception as error:
                        row.update(status='fail', detail=str(error))
                    rows.append(row)
                    print(case_id, row['status'], flush=True)
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
    report = dict(suite='node-settings-configuration-0.1', adapter_sha256=sha(__file__),
                  helpers_sha256={f: sha(ROOT/f) for f in ['adapters/local_standard_library.py', 'runner/baseline.py', 'runner/run.py']},
                  sources=dict(revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.swi_root, text=True).strip(),
                               executable_sha256=sha(args.swipl), files_sha256={str(p.relative_to(args.swi_root)): sha(p) for p in sorted((args.swi_root/'prolog').rglob('*.pl'))}),
                  results=rows, counts={s: sum(r['status'] == s for r in rows) for s in ['pass', 'fail']})
    (args.output / 'results.json').write_text(json.dumps(report, indent=2)+'\n')
    return int(report['counts']['fail'] > 0)


if __name__ == '__main__':
    raise SystemExit(main())
