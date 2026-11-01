#!/usr/bin/env python3
"""Run the scoped ACTOR release gate on an explicitly disposable private node."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit
import ownership_lifecycle

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / 'profiles/actor-release-0.1.json'

def complete_pass(report, expected):
    rows = report.get('results', [])
    return (len(rows) == len(expected) and
            {r.get('id') for r in rows} == set(expected) and
            all(r.get('status') == 'pass' for r in rows))

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ws-url', required=True)
    p.add_argument('--candidate', required=True)
    p.add_argument('--token-env', required=True)
    p.add_argument('--observer-token-env', required=True)
    p.add_argument('--disposable-fixture', action='store_true')
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if not a.disposable_fixture:
        p.error('requires --disposable-fixture: never run the release gate on a live service')
    if urlsplit(a.ws_url).hostname not in ('127.0.0.1', 'localhost', '::1'):
        p.error('use a disposable loopback fixture (or an explicit tunnel to one)')
    try:
        ownership_lifecycle.validate(os.environ.get(a.token_env), os.environ.get(a.observer_token_env))
    except ValueError as e:
        p.error(str(e))
    a.output.mkdir(parents=True, exist_ok=False)
    profile = json.loads(PROFILE.read_text())
    summary = dict(profile=profile['profile'], candidate=a.candidate, packs=[], passed=False)
    for pack in profile['packs']:
        manifest = ROOT / 'cases' / (pack['suite']+'.json')
        path = a.output / (pack['suite']+'.json')
        args = [sys.executable, str(ROOT/'runner'/pack['runner']), '--manifest', str(manifest),
                '--candidate', a.candidate, '--token-env', a.token_env, '--report', str(path)]
        if pack['runner'] == 'baseline.py':
            args += ['--url', a.ws_url, '--profile', 'actor']
        else:
            args += ['--ws-url', a.ws_url]
            if pack['suite'] == 'ownership-lifecycle-0.1':
                args += ['--observer-token-env', a.observer_token_env]
        result = subprocess.run(args)
        expected = [c['id'] for c in json.loads(manifest.read_text())['cases']]
        report = json.loads(path.read_text()) if path.exists() else {}
        passed = result.returncode == 0 and complete_pass(report, expected)
        summary['packs'].append(dict(suite=pack['suite'], passed=passed,
                                    returncode=result.returncode, expected_cases=len(expected),
                                    report=path.name))
        (a.output/'release-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    summary['passed'] = all(x['passed'] for x in summary['packs'])
    (a.output/'release-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    return 0 if summary['passed'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
