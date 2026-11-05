#!/usr/bin/env python3
"""Run maintained native context-scope and closure regressions, without listeners."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for flag in ['swipl', 'tpl', 'swi-root', 'trealla-root']:
        p.add_argument('--' + flag, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=False)
    rows = []
    sources = {}
    plans = {
        'swi': [('NAMES', 'namespace_teardown'), ('OWNERSHIP', 'promise_ownership'),
                ('LIFECYCLE', 'promise_lifecycle')],
        'trealla': [('NAMES', 'namespace_tests'), ('OWNERSHIP', 'rpc_ownership_tests'),
                    ('LIFECYCLE', 'rpc_namespace_tests')],
    }
    for mode, root, exe in [('swi', Path(a.swi_root), a.swipl),
                             ('trealla', Path(a.trealla_root), a.tpl)]:
        files = {}
        for label, suite in plans[mode]:
            if mode == 'swi':
                file = f'tests/tiers/node/{suite}_tests.pl'
                goal = f'(run_tests({suite})->halt;halt(1))'
                command = [exe, '-q', '-s', 'load.pl', '-s', file, '-g', goal]
            else:
                file = suite + '.pl'
                goal = (f"(catch((consult('{file}'),{suite}:{suite}),"
                        'E,(writeq(E),nl,fail))->halt;halt(1))')
                # Ownership tests intentionally live in user, unlike the two modules.
                if suite == 'rpc_ownership_tests':
                    goal = goal.replace(f'{suite}:{suite}', suite)
                command = [exe, '-g', goal]
            env = dict(os.environ)
            if mode == 'trealla':
                env['TPL_LIBRARY_PATH'] = str(Path(exe).resolve().parent / 'library')
            r = subprocess.run(command, cwd=root, env=env, capture_output=True,
                               text=True, timeout=90)
            output = r.stdout + r.stderr
            (a.output / f'{mode}-{label.lower()}.txt').write_text(output)
            # SWI can exit zero after a load error: reject those as well.
            passed = r.returncode == 0 and 'ERROR:' not in output
            rows.append(dict(candidate=mode, id='LIFE-' + label,
                             status='pass' if passed else 'fail', exit_code=r.returncode,
                             command=command, source=file,
                             source_sha256=hashlib.sha256((root / file).read_bytes()).hexdigest()))
            files[file] = rows[-1]['source_sha256']
            print(mode, label, rows[-1]['status'], flush=True)
        sources[mode] = dict(revision=subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(), files_sha256=files)
    (a.output / 'results.json').write_text(json.dumps(dict(
        suite='native-context-closure-0.1', sources=sources, results=rows), indent=2) + '\n')
    return int(any(r['status'] != 'pass' for r in rows))


if __name__ == '__main__':
    raise SystemExit(main())
