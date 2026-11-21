"""Compare this sweep with the 20 Nov full sweep, row by row, pack by pack and node by node.

New in this run (not part of the 20 Nov orchestration). Rows are keyed by (file, case id, candidate, occurrence);
row extraction is build_report.rows(). Usage: compare.py OLD_REPORT_DIR NEW_REPORT_DIR OUTPUT.json
"""
import json, re, sys, collections
from pathlib import Path
STATUS = {'pass', 'fail', 'blocked', 'error', 'observed', 'unsupported', 'diagnostic_error', 'not_applicable', 'deferred'}
def rows(x):
    if isinstance(x, dict):
        if x.get('status') in STATUS and any(k in x for k in ['id', 'case_id', 'case', 'label', 'title']): yield x; return
        for k, v in x.items():
            if k not in ['observation', 'transcript', 'sources', 'source', 'inputs', 'requests', 'events', 'trace']: yield from rows(v)
    elif isinstance(x, list):
        for v in x: yield from rows(v)
NODES = ['n0', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7']
def node_of(path, row):
    for part in Path(path).parts:
        if part in NODES: return part
    m = re.search(r'(?<![a-z0-9])(n[0-7])(?![0-9])', Path(path).name)
    if m: return m.group(1)
    c = str(row.get('candidate') or '')
    m = re.match(r'(n[0-7])\b', c)
    return m.group(1) if m else ('fixture:' + c if c else 'fixture')
def load(report):
    report = Path(report); summary = json.loads((report / 'SUMMARY.json').read_text())
    out = {}; meta = {}
    for f in summary['files']:
        p = report / f['file']
        try: data = json.loads(p.read_text())
        except Exception: continue
        seen = collections.Counter()
        for r in rows(data):
            cid = str(r.get('id') or r.get('case_id') or r.get('case') or r.get('label') or r.get('title'))
            cand = str(r.get('candidate') or ''); k0 = (f['file'], cid, cand); seen[k0] += 1
            key = k0 + (seen[k0],); out[key] = r['status']
            meta[key] = dict(node=node_of(f['file'], r), suite=(f.get('suites') or ['?'])[0] if len(f.get('suites') or []) == 1 else '+'.join(f.get('suites') or ['?']), classification=f['classification'])
    return out, meta
old, oldm = load(sys.argv[1]); new, newm = load(sys.argv[2])
def norm(path):  # report directory layouts are the same; normalise the report-name component only
    return path
trans = collections.Counter(); fixed = []; regressed = []; still = []
table = collections.defaultdict(lambda: collections.Counter())
for k in sorted(set(old) | set(new)):
    a, b = old.get(k, 'absent'), new.get(k, 'absent'); m = newm.get(k) or oldm.get(k)
    trans[(a, b)] += 1
    cell = table[(m['suite'], m['node'])]
    cell['old_fail'] += a == 'fail'; cell['new_fail'] += b == 'fail'; cell['new_pass'] += b == 'pass'; cell['old_pass'] += a == 'pass'
    rec = dict(file=k[0], id=k[1], candidate=k[2], occurrence=k[3], node=m['node'], suite=m['suite'], classification=m['classification'], old=a, new=b)
    if a == 'fail' and b == 'pass': fixed.append(rec)
    elif a == 'pass' and b == 'fail': regressed.append(rec)
    elif b == 'fail': still.append(rec)
result = dict(old=sys.argv[1], new=sys.argv[2], old_rows=len(old), new_rows=len(new),
              transitions={f'{a}->{b}': n for (a, b), n in sorted(trans.items())},
              fixed=fixed, regressed=regressed, still_failing=still,
              by_suite_and_node=[dict(suite=s, node=n, **c) for (s, n), c in sorted(table.items()) if c['old_fail'] or c['new_fail']])
Path(sys.argv[3]).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(dict(old_rows=len(old), new_rows=len(new), fixed=len(fixed), regressed=len(regressed), still_failing=len(still))))
