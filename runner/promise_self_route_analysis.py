#!/usr/bin/env python3
"""Summarize public self-route phase timings without converting failed attempts to passes."""
import argparse
import json
from pathlib import Path
import re
import statistics


def analyze(report):
    rows = []
    for row in report['results']:
        phases = {t['phase']: t['event'] for t in row['trace']}
        metrics = dict(id=row['id'], status=row['status'], stamped=row['stamped'])
        try:
            created = phases['created']['data'][0]
            owner = phases['owner_collection']['data'][0]
            metrics['promise_setup_ms'] = (float(created['PromiseReturned']) - float(created['PromiseStart'])) * 1000
            metrics['owner_yield_ms'] = (float(owner['WaitEnd']) - float(owner['WaitStart'])) * 1000
            match = re.fullmatch(r'success\(\[mark\(([-+0-9.eE]+)\)\],false\)', owner['Outcome'])
            if match:
                produced = float(match[1])
                metrics['promise_start_to_producer_execution_ms'] = (produced - float(created['PromiseStart'])) * 1000
                metrics['producer_execution_to_collection_ms'] = (float(owner['WaitEnd']) - produced) * 1000
        except (KeyError, IndexError, TypeError, ValueError) as error:
            metrics['timing_unavailable'] = type(error).__name__
        rows.append(metrics)
    summary = {}
    for key in ['promise_setup_ms', 'owner_yield_ms', 'promise_start_to_producer_execution_ms', 'producer_execution_to_collection_ms']:
        values = [r[key] for r in rows if key in r]
        if values:
            summary[key] = dict(samples=len(values), min=min(values), median=statistics.median(values), max=max(values))
    return dict(attempts=len(rows), counts={s: sum(r['status'] == s for r in rows) for s in ['pass', 'fail', 'error']},
                timings=summary, results=rows,
                limitation='Same-node wall timestamps measure producer execution and yield, not HTTP response arrival or promise installation. Diagnostic retry never replaces the original status.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(analyze(json.loads(args.report.read_text())), indent=2) + '\n')
