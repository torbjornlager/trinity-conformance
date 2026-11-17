#!/usr/bin/env python3
"""Run the maintained retained-context selection on disposable native nodes."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'cases/retained-context-0.1.json'


def validate(report, expected, routes=None):
    """Reject missing, duplicate, unexpected, excluded and nonpassing cases."""
    key = lambda row: (row['candidate'], row['id'])
    wanted = Counter(map(key, expected))
    actual = Counter(map(key, report['results']))
    if any(n != 1 for n in wanted.values()) or actual != wanted:
        raise ValueError(f'case inventory mismatch: missing={wanted-actual}, extra={actual-wanted}')
    if routes is not None and Counter(report['routes']) != Counter(routes):
        raise ValueError('route inventory mismatch')
    for row in report['results']:
        if row['status'] != 'pass' or row.get('policy_exclusion'):
            raise ValueError(f"nonpassing case: {key(row)} ({row['status']})")
        reference = next(r for r in expected if key(r) == key(row))
        if row.get('negative_control', False) != reference.get('negative_control', False):
            raise ValueError(f'negative-control identity mismatch: {key(row)}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ['swipl', 'tpl', 'swi-root', 'trealla-root']:
        parser.add_argument('--' + flag, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    args.output.mkdir(parents=True, exist_ok=False)
    common = ['--swipl', args.swipl, '--tpl', args.tpl,
              '--swi-root', args.swi_root, '--trealla-root', args.trealla_root]
    groups = []
    # Run each group once, even if another group fails. Never retry to qualify.
    for label, adapter, expected in [
        ('contexts', 'local_retained_context.py', manifest['cases'] + manifest['controlled_promise_cases']),
        ('attachments', 'local_attachment_race.py', manifest['attachment_cases']),
        ('closure', 'local_context_closure.py', manifest['closure_cases']),
    ]:
        target = args.output / label
        command = [sys.executable, str(ROOT / 'adapters' / adapter), *common, '--output', str(target)]
        if label == 'contexts':
            command += ['--controlled-promises', '--routes', *manifest['routes']]
        with (args.output / (label + '.log')).open('w') as log:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
        group = dict(group=label, command=command, exit_code=result.returncode, status='fail')
        try:
            report = json.loads((target / 'results.json').read_text())
            validate(report, expected, manifest['routes'] if label == 'contexts' else None)
            if result.returncode:
                raise ValueError(f'adapter exit {result.returncode}')
            group['status'] = 'pass'
        except (OSError, ValueError, KeyError, TypeError) as error:
            group['detail'] = str(error)
        groups.append(group)
        print(label, group['status'], flush=True)
    summary = dict(suite=manifest['suite'], manifest_sha256=hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
                   groups=groups, status='pass' if all(g['status'] == 'pass' for g in groups) else 'fail')
    (args.output / 'results.json').write_text(json.dumps(summary, indent=2) + '\n')
    return int(summary['status'] != 'pass')


if __name__ == '__main__':
    raise SystemExit(main())
