"""Validate complete held-guard control matrices and their barrier evidence."""
import argparse
import hashlib
import json
from pathlib import Path


def successful(answer):
    return (answer.get('type') == 'success' and answer.get('more') is False and
            len(answer.get('data', [])) == 1 and answer['data'][0].get('ControlCheck') == 'passed')


def validate_observation(case, observed):
    if observed.get('entry_count') != 1 or observed.get('peer_held_at_control') is not True:
        raise ValueError('missing unique held guard entry')
    kind = case['control']
    if kind == 'abort':
        if observed.get('control_response', {}).get('type') != 'abort' or not successful(observed.get('recovery', {})):
            raise ValueError('missing actual abort or same-actor mailbox recovery')
        if 'primary-session' not in observed.get('guard_target', ''):
            raise ValueError('abort must exercise the primary session')
    elif kind == 'time_limit':
        if observed.get('formal_error_checked') != 'error(resource_error(time),_)' or not successful(observed.get('control_and_recovery', {})):
            raise ValueError('missing formal time error or retained-actor recovery')
        if 'child-toplevel' not in observed.get('guard_target', ''):
            raise ValueError('configured limit must exercise the public toplevel lifecycle')
    elif kind == 'terminate':
        if not successful(observed.get('control_response', {})) or 'child-actor' not in observed.get('guard_target', ''):
            raise ValueError('missing monitored actor termination')
    elif kind == 'ordinary_error':
        if not successful(observed.get('ordinary_response', {})):
            raise ValueError('ordinary guard exception was not a non-match')
    else:
        raise ValueError('unknown guard control')
    if not successful(observed.get('health', {})):
        raise ValueError('missing session health control')
    if observed.get('halt_confirmed') is not True and observed.get('close_confirmed') is not True:
        raise ValueError('missing confirmed cleanup')


def validate_report(manifest_path, report, candidates):
    raw = manifest_path.read_bytes()
    pack = json.loads(raw)
    if report['manifest_sha256'] != hashlib.sha256(raw).hexdigest():
        raise ValueError('different guard-control manifest')
    definitions = {c['id']: c for c in pack['cases']}
    if len(definitions) != len(pack['cases']):
        raise ValueError('duplicate guard-control definition')
    expected = {(candidate, case) for candidate in candidates for case in definitions}
    rows = report['results']
    if len(rows) != len(expected) or {(r['candidate'], r['id']) for r in rows} != expected:
        raise ValueError('missing, duplicate or unexpected guard-control case')
    for row in rows:
        if row['status'] != 'pass':
            raise ValueError('guard-control matrix contains a failure')
        validate_observation(definitions[row['id']], row.get('observation', {}))
    if report['counts'] != {'pass': len(rows), 'fail': 0}:
        raise ValueError('guard-control counts disagree')
    return len(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--native', type=Path, required=True)
    p.add_argument('--browser', type=Path, required=True)
    a = p.parse_args()
    try:
        native = validate_report(a.manifest, json.loads(a.native.read_text()), ['swi', 'trealla'])
        browser = validate_report(a.manifest, json.loads(a.browser.read_text()), ['swi-wasm-worker', 'swi-wasm-main'])
        print(json.dumps(dict(native_pass=native, browser_pass=browser)))
    except (KeyError, OSError, ValueError) as error:
        p.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
