#!/usr/bin/env python3
"""Bounded sustained admission probe; admission refusals are never passes.

Use owned fixtures for boundary/exhaustion tests. This finite read-only probe
can qualify an operator-selected live budget without changing node settings.
"""
from __future__ import annotations
import argparse
import json
import math
import os
from pathlib import Path
import statistics
import time
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def request(url, headers):
    started = time.monotonic()
    try:
        response = urlopen(Request(url, headers=headers), timeout=10)
    except HTTPError as error:
        response = error
    with response:
        return dict(http_status=response.status, body=response.read().decode(),
                    retry_after=response.headers.get('Retry-After'),
                    seconds=round(time.monotonic() - started, 6))


def probe(url, count, interval, headers, metadata=True):
    info = request(url.rstrip('/') + '/node_info', headers) if metadata else None
    if info is not None:
        if info['http_status'] != 200:
            raise RuntimeError('node_info unavailable: ' + str(info['http_status']))
        info = json.loads(info['body'])
    query = urlencode(dict(goal='(AdmissionProbe=passed)', template='(AdmissionProbe)',
                           format='prolog', limit=1))
    rows = []
    started = time.monotonic()
    for index in range(count):
        # Pace starts; slow responses never produce a catch-up burst.
        next_start = time.monotonic() + interval
        try:
            row = request(url.rstrip('/') + '/call?' + query, headers)
            row['status'] = ('pass' if row['http_status'] == 200 and
                             ''.join(row['body'].split()) == 'success([passed],false).'
                             else 'fail')
        except Exception as error:
            row = dict(status='error', detail=type(error).__name__ + ': ' + str(error))
        row['index'] = index + 1
        rows.append(row)
        if index + 1 < count:
            time.sleep(max(0, next_start - time.monotonic()))
    elapsed = time.monotonic() - started
    timings = sorted(r['seconds'] for r in rows if 'seconds' in r)
    return dict(url=url, status='pass' if all(r['status']=='pass' for r in rows) else 'fail',
                node_info=info, count=count, interval_seconds=interval,
                elapsed_seconds=round(elapsed, 3),
                completed_requests_per_minute=round(count * 60 / elapsed, 2),
                median_response_seconds=statistics.median(timings) if timings else None,
                p95_response_seconds=timings[math.ceil(.95*len(timings))-1] if timings else None,
                observations=rows,
                scope='Finite HTTP equality checks. No concurrency, session-creation, '
                      'isolation or resource-reclamation claim.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',required=True)
    parser.add_argument('--count',type=int,default=140)
    parser.add_argument('--interval',type=float,default=.6)
    parser.add_argument('--headers-env',help='environment variable containing a JSON header object; never exported')
    parser.add_argument('--no-metadata',action='store_true',help='owned transport fixture without node_info')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not 1 <= args.count <= 1000 or not math.isfinite(args.interval) or args.interval < 0:
        parser.error('count must be 1..1000 and interval finite and nonnegative')
    headers=json.loads(os.environ[args.headers_env]) if args.headers_env else {}
    result=probe(args.url,args.count,args.interval,headers,not args.no_metadata)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('observations','node_info')}))
    return 0 if result['status']=='pass' else 1


if __name__=='__main__':
    raise SystemExit(main())
