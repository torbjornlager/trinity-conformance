#!/usr/bin/env python3
"""Diagnose an explicitly selected public actor/HTTP self-route without retries to qualify."""
import argparse
import contextlib
import hashlib
import json
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runner'))
from run import Candidate, Harness, prolog_quote_atom, row_value

SOURCE = """probe_create(Parent,URL,Stamped):-get_time(Start),(Stamped==true->promise(URL,get_time(T),R,[template(mark(T))]);promise(URL,true,R,[template(mark)])),get_time(Returned),send(Parent,created(R,Start,Returned)),receive({finish->true}).
probe_collect(Parent,R):-get_time(Start),catch(yield(R,A,[timeout(2)]),E,A=error(E)),get_time(End),send(Parent,collected(A,Start,End)).
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True)
    parser.add_argument('--credentials-file', type=Path, required=True,
                        help='JSON with a token field; never included in the report')
    parser.add_argument('--attempts', type=int, default=20)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.attempts < 2:
        parser.error('--attempts must be at least 2 (original and timestamped controls)')
    token = json.loads(args.credentials_file.read_text())['token']
    args.output.mkdir(parents=True, exist_ok=False)
    candidate = Candidate(args.url.replace('https:', 'wss:').replace('http:', 'ws:') + '/ws',
                          'actor', 10, token, args.url, False, ())
    rows = []
    started = time.monotonic()

    def save():
        report = dict(suite='public-promise-self-route-diagnostic-0.1', url=args.url,
                      adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      source=SOURCE, deadline_seconds=2, results=rows,
                      counts={s: sum(r['status'] == s for r in rows) for s in ['pass', 'fail', 'error']},
                      scope='Public actor and HTTP self-route; producer execution timestamps do not measure client-side answer installation')
        (args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')

    def run(h, goal):
        h.call('(' + goal + '),ProbeCheck=passed', '[limit(1)]')
        for _ in range(32):
            event = h.recv()
            if event.get('type') in ['success', 'failure', 'error'] and event.get('pid', h.shell) == h.shell:
                return event
            h.acknowledge_output(event)
        raise RuntimeError('missing terminal query result')

    def collect(h, ref):
        goal = f'self(S),spawn(probe_collect(S,{ref}),_,[node({prolog_quote_atom(args.url)}),src_text({prolog_quote_atom(SOURCE)})]),receive({{collected(Outcome,WaitStart,WaitEnd)->true}},[timeout(4),on_timeout(throw(no_collector_reply))])'
        return run(h, goal)

    def missing(event, ref):
        return event.get('type') == 'success' and 'existence_error(promise,' + ref + ')' in row_value(event, 'Outcome')

    for index in range(args.attempts):
        stamped = index % 2 == 1
        row = dict(id=f'SELF-{index+1:03}', stamped=stamped, trace=[], status='error')
        rows.append(row)

        def observe(phase, event):
            row['trace'].append(dict(phase=phase, elapsed_ms=round((time.monotonic()-started)*1000, 3), event=event))
            return event

        try:
            with contextlib.ExitStack() as stack:
                h = stack.enter_context(Harness(candidate))
                h.spawn_shell('[session(true)]')
                other = stack.enter_context(Harness(candidate))
                other.spawn_shell('[session(true)]')
                try:
                    goal = f'self(S),spawn(probe_create(S,{prolog_quote_atom(args.url)},{str(stamped).lower()}),Creator,[node({prolog_quote_atom(args.url)}),src_text({prolog_quote_atom(SOURCE)})]),receive({{created(Ref,PromiseStart,PromiseReturned)->true}},[timeout(4),on_timeout(throw(no_creator_reply))])'
                    created = observe('created', run(h, goal))
                    ref, creator = row_value(created, 'Ref'), row_value(created, 'Creator')
                    foreign = observe('foreign_collection', collect(other, ref))
                    owner = observe('owner_collection', collect(h, ref))
                    outcome = row_value(owner, 'Outcome') if owner.get('type') == 'success' else ''
                    expected = bool(re.fullmatch(r'success\(\[mark\([-+0-9.eE]+\)\],false\)', outcome)) if stamped else outcome == 'success([mark],false)'
                    row['status'] = 'pass' if missing(foreign, ref) and expected else 'fail'
                    if outcome == 'timeout':
                        # Diagnostic retry cannot change the original failed status.
                        observe('diagnostic_retry_after_timeout', collect(h, ref))
                    observe('creator_finish', run(h, f'send({creator},finish)'))
                finally:
                    for label, client in [('foreign', other), ('owner', h)]:
                        try:
                            client.halt()
                        except Exception as error:
                            observe(label + '_halt_error', dict(detail=str(error)))
                            row['status'] = 'error'
        except Exception as error:
            row.update(status='error', detail=str(error))
        save()
        print(row['id'], 'timestamped' if stamped else 'original', row['status'], flush=True)
    return int(any(r['status'] != 'pass' for r in rows))


if __name__ == '__main__':
    raise SystemExit(main())
