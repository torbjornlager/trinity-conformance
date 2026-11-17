#!/usr/bin/env python3
"""Run draft manual-boundary assertions against explicitly selected local runtimes.

This adapter exercises standalone APIs, not public-node admission or transport.
It accepts development checkouts and records their exact source changes.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
SUITES = ('uri-atoms-0.1', 'manual-option-sources-0.1')


def atom(value):
    return "'" + str(value).replace('\\', '\\\\').replace("'", "''") + "'"


def provenance(root):
    revision = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    changed = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-m', '-o', '--exclude-standard', '-z']).split(b'\0')
    hashes = {os.fsdecode(name): hashlib.sha256((root / os.fsdecode(name)).read_bytes()).hexdigest()
              for name in changed if name and (root / os.fsdecode(name)).is_file()}
    return dict(root=str(root), revision=revision, dirty=bool(changed[:-1]), changed_files=hashes)


def execute(command, cwd, env, timeout, gnu=False):
    start = time.monotonic()
    try:
        result = subprocess.run(command, cwd=cwd, env=env, input='', text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        passed = result.returncode == 0
        if gnu:
            try:
                passed = passed and [json.loads(line) for line in result.stdout.splitlines()] == [
                    {'type': 'success', 'answers': ['ok'], 'more': False}]
            except ValueError:
                passed = False
        return dict(status='pass' if passed else 'fail', exit_code=result.returncode,
                    stdout=result.stdout, stderr=result.stderr,
                    duration_ms=round((time.monotonic() - start) * 1000))
    except subprocess.TimeoutExpired:
        return dict(status='fail', detail=f'case exceeded {timeout} seconds',
                    duration_ms=round((time.monotonic() - start) * 1000))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--swi-root', required=True, type=Path)
    parser.add_argument('--trealla-root', required=True, type=Path)
    parser.add_argument('--swipl', default='swipl')
    parser.add_argument('--tpl', required=True, type=Path)
    parser.add_argument('--gnu-worker', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--timeout', type=float, default=30)
    parser.add_argument('--suite', action='append', choices=SUITES + ('supervisor-common-0.1','statechart-document-0.1','rpc-timeout-0.1','http-transport-options-0.1','runtime-introspection-0.1','appendix-library-probes-0.1'),
                        help='select a draft pack; default retains the original boundary packs')
    args = parser.parse_args()
    suites = args.suite or SUITES
    if args.timeout <= 0 or not args.timeout < float('inf'):
        parser.error('--timeout must be positive and finite')
    if args.output.exists():
        parser.error('--output must be a new file')
    swi, trealla = args.swi_root.resolve(), args.trealla_root.resolve()
    swipl = shutil.which(args.swipl)
    if swipl is None:
        parser.error('SWI executable not found')
    tpl = args.tpl.resolve()
    env = os.environ.copy()
    env['TPL_LIBRARY_PATH'] = str(tpl.parent / 'library')
    candidates = [
        ('swi', swi, [swipl, '-f', 'none', '-q'],
         'use_module(' + atom(swi / 'prolog/web_prolog.pl') + '),'),
        ('trealla', trealla, [str(tpl)], 'use_module(actor_api),use_module(actors),use_module(distribution),')]
    if args.gnu_worker:
        worker = args.gnu_worker.resolve()
        candidates.append(('gnu', worker.parent.parent, [str(worker)], ''))
    results, sources = [], {}
    for name, checkout, command, imports in candidates:
        sources[name] = provenance(checkout)
        sources[name]['executable'] = command[0]
        sources[name]['executable_sha256'] = hashlib.sha256(Path(command[0]).read_bytes()).hexdigest()
        for suite in suites:
            pack = json.loads((ROOT / 'cases' / (suite + '.json')).read_text())
            if name == 'gnu' and pack['minimum_profile'] != 'isobase':
                continue
            for case in pack['cases']:
                if case['transport'] != 'query' or case.get('source'):
                    raise ValueError('this adapter only supports source-free local query cases')
                goal = case['goal']
                if name == 'gnu':
                    invocation = command + ['query((' + goal + '),ok)', '100']
                    cwd = Path(command[0]).parent
                else:
                    invocation = command + ['-g', imports + '(catch((' + goal +
                        '),E,(writeq(E),nl,fail))->halt(0);halt(1))']
                    cwd = checkout
                row = dict(candidate=name, suite=suite, id=case['id'], title=case['title'])
                row.update(execute(invocation, cwd, env, args.timeout, name == 'gnu'))
                results.append(row)
    counts = {status: sum(row['status'] == status for row in results) for status in ('pass', 'fail')}
    report = dict(scope='supporting', execution='standalone local APIs; no public-node certification',
                  contracts={suite: hashlib.sha256((ROOT / 'cases' / (suite + '.json')).read_bytes()).hexdigest() for suite in suites},
                  adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  sources=sources, counts=counts, results=results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(counts))
    return int(counts['fail'] != 0)


if __name__ == '__main__':
    raise SystemExit(main())
