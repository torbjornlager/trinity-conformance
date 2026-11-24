#!/usr/bin/env python3
"""Cross-node ACTOR cases (cross-node-actor-0.1) over a set of public nodes.

Pair cases run from every caller node over every ordered pair (A, B) of
distinct nodes, reusing one shell per caller and case. A case passes only when
every combination passes; each combination is kept in the observation.

  python3 runner/cross_node.py --node https://n3.example --node https://n5.example \
      --report reports/cross-node.json
"""
import argparse
from datetime import datetime, timezone
from itertools import count, permutations
import json
from pathlib import Path
import re
import time

import run as actor

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / 'cases/cross-node-actor-0.1.json'
TAGS = count(int(time.time()) % 100000 * 1000)


def ws_url(node):
    return re.sub(r'^http', 'ws', node.rstrip('/')) + '/ws'


def candidate(node, timeout):
    return actor.Candidate(ws_url(node), 'actor', timeout, None, node, False, ())


def answer(harness, goal, limit):
    """Run one goal in the shell; return its terminal event, acknowledging output."""
    harness.call(goal, '[limit(1)]')
    deadline = time.monotonic() + limit
    while time.monotonic() < deadline:
        event = harness.recv()
        if event.get('type') == 'io_request':
            harness.acknowledge_output(event)
        elif event.get('type') in ('success', 'failure', 'error') and event.get('pid') == harness.shell:
            return event
    raise actor.ConformanceFailure('no answer within %.0f s' % limit)


def expand(text, a, b, tag):
    return text.replace('__A__', a).replace('__B__', b).replace('__TAG__', str(tag))


def check_combination(case, event, caller, a):
    if event.get('type') != 'success':
        raise actor.ConformanceFailure('%s: %s' % (event.get('type'), str(event.get('data'))[:300]))
    if case['id'] == 'XN-002' and a.rstrip('/') != caller.rstrip('/'):
        pid = actor.row_value(event, 'XnPid')
        expected = re.compile(r"[1-9][0-9]*@'" + re.escape(a.rstrip('/')) + "'")
        actor.require(expected.fullmatch(pid) is not None, 'unqualified pid %r, expected Id@%r' % (pid, a))


def pair_case(case, nodes, callers, timeout):
    results = []
    for caller in callers:
        options = '[session(true)]'
        if case.get('source'):
            options = '[session(true),src_text(%s)]' % actor.prolog_quote_atom(case['source'])
        try:
            with actor.Harness(candidate(caller, timeout)) as harness:
                harness.spawn_shell(options)
                for a, b in permutations(nodes, 2):
                    row = dict(caller=caller, a=a, b=b)
                    try:
                        event = answer(harness, expand(case['goal'], a, b, next(TAGS)), 40)
                        check_combination(case, event, caller, a)
                        row['status'] = 'pass'
                    except actor.ConformanceFailure as error:
                        row.update(status='fail', detail=str(error))
                    results.append(row)
                try:
                    harness.halt()
                except Exception:
                    pass
        except Exception as error:
            # The caller itself was unusable; record every combination it owed.
            for a, b in permutations(nodes, 2):
                results.append(dict(caller=caller, a=a, b=b, status='fail',
                                    detail='caller session: %s: %s' % (type(error).__name__, error)))
    return results


def refused(harness, command):
    """Send a foreign command and return the error event it must produce."""
    harness.send(command)
    deadline = time.monotonic() + 8
    while time.monotonic() < deadline:
        event = harness.recv()
        if event.get('type') == 'error':
            return event
        harness.acknowledge_output(event)
    raise actor.ConformanceFailure('foreign %s was not refused' % command['command'])


def node_case(case, nodes, timeout):
    results = []
    for node in nodes:
        row = dict(node=node)
        try:
            with actor.Harness(candidate(node, timeout)) as owner, actor.Harness(candidate(node, timeout)) as foreign:
                owner.spawn_shell()
                send = refused(foreign, dict(command='send', pid=owner.shell, message='xn_foreign',
                                             request_id='xn-send'))
                exit_ = refused(foreign, dict(command='exit', pid=owner.shell, reason='kill',
                                              request_id='xn-exit'))
                event = answer(owner, 'receive({xn_foreign->throw(xn_foreign_delivered)},[timeout(0),on_timeout(true)])', 10)
                actor.require(event.get('type') == 'success', 'owner after foreign commands: %r' % (event,))
                owner.halt()
                row.update(status='pass', send=str(send.get('data'))[:200], exit=str(exit_.get('data'))[:200])
        except Exception as error:
            row.update(status='fail', detail='%s: %s' % (type(error).__name__, error))
        results.append(row)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--node', action='append', required=True, help='public ACTOR node origin (repeat)')
    parser.add_argument('--caller', action='append', help='caller node origin (repeat); default: every --node')
    parser.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument('--case', action='append', dest='case_ids')
    parser.add_argument('--candidate', default='external')
    parser.add_argument('--timeout', type=float, default=30)
    parser.add_argument('--session-interval', type=float, default=0.0, metavar='SECONDS')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    for origin in args.node + (args.caller or []):
        if not re.fullmatch(r'https?://[A-Za-z0-9.:-]+', origin):
            parser.error('nodes must be simple HTTP(S) origins')
    if len(set(args.node)) < 2:
        parser.error('at least two distinct nodes are required')
    actor.set_session_interval(args.session_interval)
    callers = args.caller or args.node
    pack = json.loads(args.manifest.read_text())
    started = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    rows = []
    for case in pack['cases']:
        if args.case_ids and case['id'] not in args.case_ids:
            continue
        before = time.monotonic()
        if case['topology'] == 'pair':
            combos = pair_case(case, args.node, callers, args.timeout)
        else:
            combos = node_case(case, args.node, args.timeout)
        failed = [c for c in combos if c['status'] != 'pass']
        row = dict(id=case['id'], title=case['title'], status='fail' if failed else 'pass',
                   observation=dict(combinations=combos),
                   duration_ms=round((time.monotonic() - before) * 1000))
        if failed:
            row['detail'] = '%d of %d combinations failed' % (len(failed), len(combos))
        rows.append(row)
        print('%-5s %s %s' % (row['status'].upper(), row['id'], row.get('detail', '')), flush=True)
        for combo in failed:
            where = combo.get('node') or '%s: %s -> %s' % (combo['caller'], combo['a'], combo['b'])
            print('      %s  %s' % (where, combo.get('detail', '')[:160]), flush=True)
    counts = {s: sum(r['status'] == s for r in rows) for s in ['pass', 'fail', 'unsupported', 'observed', 'diagnostic_error']}
    if args.report:
        report = dict(schema_version=2, baseline='0.1', suite=pack['suite'], scope=pack['scope'],
                      candidate=args.candidate, advertised_profile='actor', endpoint=','.join(args.node),
                      peer=None, started_at=started, duration_ms=round((time.monotonic() - clock) * 1000),
                      counts=counts, results=rows)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(counts))
    return bool(counts['fail'])


if __name__ == '__main__':
    raise SystemExit(main())
