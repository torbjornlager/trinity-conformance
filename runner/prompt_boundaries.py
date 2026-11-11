"""Check respond/3 profile boundaries through public native HTTP and WS routes."""
import argparse
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

from prompt_http import session, post
from run import Candidate, Harness, require


def check_stateless(base, goal):
    url = base.rstrip('/') + '/call?' + urlencode({'goal': goal, 'format': 'json'})
    try:
        response = urlopen(url, timeout=8)
    except HTTPError as error:
        response = error
    with response:
        result = json.loads(response.read())
    require(result.get('type') == 'error' and 'profile_violation' in json.dumps(result),
            f'ISOBASE admitted respond/3: {result!r}')


def check_isotope(base, goal):
    with session(base, True) as fields:
        result = post(base, 'call', {**fields, 'goal': goal})
        require(result.get('type') == 'error' and 'profile_violation' in json.dumps(result),
                f'ISOTOPE admitted respond/3: {result!r}')


def check_actor(base):
    ws = base.replace('http://', 'ws://').replace('https://', 'wss://').rstrip('/') + '/ws'
    candidate = Candidate(ws, 'actor', 5, None, None, False, ())
    with Harness(candidate) as harness:
        harness.spawn_shell()
        harness.call("self(P),respond(P,boundary_ref,ok),"
                     "receive({'$input'(_,boundary_ref,ok)->true})", '[limit(1)]')
        result = harness.recv('success')
        require(result.get('more') is False, f'ACTOR respond/3 failed: {result!r}')
        harness.halt()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for engine in ('swi', 'trealla'):
        parser.add_argument('--' + engine + '-actor')
        parser.add_argument('--' + engine + '-isotope')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    results = []
    for engine in ('swi', 'trealla'):
        actor = getattr(args, engine + '_actor')
        isotope = getattr(args, engine + '_isotope')
        if not (actor or isotope):
            continue
        if not (actor and isotope):
            parser.error('provide both actor and isotope endpoints for ' + engine)
        cases = [('PB-001', lambda: check_stateless(actor, 'respond(1234567890,ref,answer)')),
                 ('PB-002', lambda: check_stateless(actor, 'G=respond(1234567890,ref,answer),call(G)')),
                 ('PB-003', lambda: check_isotope(isotope, 'respond(1234567890,ref,answer)')),
                 ('PB-004', lambda: check_isotope(isotope, 'G=respond(1234567890,ref,answer),call(G)')),
                 ('PB-005', lambda: check_actor(actor))]
        for case_id, check in cases:
            try:
                check()
                results.append(dict(engine=engine, id=case_id, status='pass'))
            except Exception as error:
                results.append(dict(engine=engine, id=case_id, status='fail', detail=str(error)))
    if not results:
        parser.error('provide at least one pair of native endpoints')
    report = dict(suite='prompt-boundaries-0.1', results=results)
    rendered = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end='')
    return int(any(x['status'] != 'pass' for x in results))


if __name__ == '__main__':
    raise SystemExit(main())
