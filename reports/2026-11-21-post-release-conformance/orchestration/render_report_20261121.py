"""Render the 21 Nov post-release report (replaces render_report.py, whose prose is specific to 20 Nov).
Data sources are this run's export plus comparison.json (orchestration/compare.py against the 20 Nov report).
The SUMMARY/RESULTS/files-sha256 tail is unchanged from render_report.py."""
from pathlib import Path
import json, collections, hashlib, re
R = Path('/private/tmp/claude-502/-Users-lager-trinity-demonstrator/58219eb7-1e68-4089-a2dd-25c3117837f6/scratchpad/tc')
P = Path(__file__).resolve().parents[1]; D = R / 'reports/2026-11-21-post-release-conformance'; OLD = R / 'reports/2026-11-20-post-uri-full-conformance'
def read(p): return json.loads(p.read_text())
def rs(p): return read(p).get('results', []) if p.exists() else []
def count(rows): return dict(collections.Counter(r['status'] for r in rows))
def fmt(c): return ', '.join(str(c[s]) + ' ' + s for s in ['pass', 'fail', 'error', 'blocked', 'not_applicable', 'unsupported', 'deferred', 'observed', 'diagnostic_error'] if c.get(s)) or 'none'
s = read(D / 'SUMMARY.json'); v = read(D / 'verification.json'); revs = read(P / 'release.json')['revisions']; completion = read(P / 'completion-verification.json')
cmp = read(P / 'comparison.json'); ch = read(P / 'orchestration-changes.json')
primary = {n: count([r for p in (P / 'observations' / n).glob('*.json') for r in rs(p)]) for n in ['n0', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7']}

# Classification of remaining failed rows (brief: STATUS-2026-11-20 categories); unmatched rows stay unclassified.
def classify(x):
    sid, node, suite, cl = x['id'], x['node'], x['suite'], x['classification']
    if cl.startswith('out_of_scope'): return 'Out-of-scope rows (profile or environment exclusion)'
    if suite == 'receive-control-0.1': return 'Real defect: regression in Trealla 7a8e8ce (N5 rolled back after the sweep)'
    if suite in ('node-uri-io-0.1', 'monitor-contracts-0.1', 'monitor-preflight-0.1'): return 'Superseded 0.1 assertions (the 0.2 pack passes on the same node/fixture)'
    if node == 'n7' and re.fullmatch(r'SL-01[4-7]', sid): return 'Sandbox-only rows on N7 (should be not applicable with sandbox off)'
    if re.fullmatch(r'LOCAL-00[67]', sid): return 'Live prerequisite missing: needs a peer serving local_node_loaded/1'
    if node == 'n7' and sid in ('NU-020', 'NU-021'): return 'N7 design gap: one peer connection per spawn'
    if node == 'n7' and sid == 'PE-008': return 'N7 defect: explicit limit plus timeout returns a truncated page'
    if (node == 'n6' and (sid == 'ER-007' or sid.startswith('HTTP-CTL'))) or (node == 'fixture:gnu-direct-api' and sid.startswith('HTTP-CTL')): return 'GNU classification and NUL representation (expected to remain)'
    return 'Unclassified: unchanged since 20 November, needs triage'
remaining = cmp['still_failing'] + cmp['regressed']
classes = collections.defaultdict(list)
for x in remaining: classes[classify(x)].append(x)

L = ['# Full live conformance after the 21 November release — 21 November 2026', '',
     f"Fresh execution of **{s['manifest_count']} manifests / {s['main_case_rows']:,} input rows** at suite `{s['suite_revision']}`, against the live nodes after the 21 November conformance release. Every result was executed for this run; nothing was copied from earlier runs. Repeated cases, versions, transports and nodes are separate observations, not independent defects or a conformance percentage.", '',
     '[Per-file outcomes](SUMMARY.json) · [case inventory](verification.json) · [comparison with 20 November](COMPARISON.json) · [frozen inputs](suite-inputs.json) · [provenance](execution/provenance.json) · [preservation](preservation.json) · [orchestration changes](execution/orchestration-changes.json)', '',
     '## Runtime selection and conditions', '',
     f"N0–N4 and admin: native SWI `{revs['native'][:7]}` / SWI-Prolog 11.0.0, demonstrator `{revs['shared'][:7]}`, browser `{revs['browser'][:7]}`. N5: Trealla `{revs['trealla'][:7]}` / 3.14.20. N6: gprolog-port `{revs['gprolog'][:7]}`. N7: eclipse-node `{revs['eclipse_runtime'][:7]}` worker and adapter. Owned native fixtures use snapshots of these deployed images.", '',
     'The orchestration is the 20 November sweep\'s, with only paths, dates and pins changed; every other change is listed in [orchestration-changes.json](execution/orchestration-changes.json). Admission budgets and pacing are unchanged: one sequential controller per endpoint, HTTP calls 0.8 s apart, retained sessions 2.1 s, prompt sessions 4 s, N6 waits 303 s before its library phase. No runtime, setting or quota changed during the run, and no persistent service restarted (in contrast to 20 November, when N5 restarted on its own).', '',
     f"Suite changes since 20 November (`6dd7809` → `a7a4a7b`): six files, no added or removed manifests ([input-comparison.json](execution/input-comparison.json)). Runner self-tests: {completion['runner_self_tests']} pass.", '',
     '**After the sweep, N5 was rolled back** to its pre-release behaviour because of the receive-guard regression below. N5 results in this report describe Trealla `49377b5` as it ran during the sweep.', '',
     '## Primary public selections', '', '| Node | Profile | Fresh result |', '|---|---|---|']
for n, c in primary.items(): L.append('| ' + n.upper() + ' | ' + ('RELATION' if n == 'n0' else 'ISOBASE' if n in ['n1', 'n6'] else 'ISOTOPE' if n == 'n2' else 'ACTOR') + ' | ' + fmt(c) + ' |')
t = cmp['transitions']
L += ['', '## Comparison with 20 November', '',
      f"Rows are matched by file, case, candidate and occurrence ([COMPARISON.json](COMPARISON.json)). **{len(cmp['fixed'])} rows changed from fail to pass, {len(cmp['regressed'])} from pass to fail, and {len(cmp['still_failing'])} still fail.** Failed rows fell from {sum(v for k, v in t.items() if k.startswith('fail->'))} to {sum(v for k, v in t.items() if k.endswith('->fail'))}.", '',
      f"{t.get('pass->absent', 0) + t.get('fail->absent', 0) + t.get('observed->absent', 0)} rows exist only on 20 November: the N6 capacity-refusal replays (none were needed this time: zero N6 capacity refusals) and native promise outputs that this run records under the provenance reruns instead (`procps-rerun/`), as 20 November also did.", '',
      '| Node / fixture | Failed 20 Nov | Failed 21 Nov | Fixed | New failures |', '|---|---|---|---|---|']
bynode = collections.defaultdict(collections.Counter)
for row in cmp['by_suite_and_node']: bynode[row['node']]['old'] += row['old_fail']; bynode[row['node']]['new'] += row['new_fail']
for x in cmp['fixed']: bynode[x['node']]['fixed'] += 1
for x in cmp['regressed']: bynode[x['node']]['reg'] += 1
for n in sorted(bynode, key=lambda k: (k.startswith('fixture'), k)): c = bynode[n]; L.append(f"| {n} | {c['old']} | {c['new']} | {c['fixed']} | {c['reg']} |")
L += ['', '### By pack and node', '', 'Only packs with a failure on either day.', '', '| Pack | Node / fixture | Failed 20 Nov | Failed 21 Nov |', '|---|---|---|---|']
for row in cmp['by_suite_and_node']: L.append(f"| {row['suite'] if row['suite'] != '?' else '(aggregate adapter)'} | {row['node']} | {row['old_fail']} | {row['new_fail']} |")

# Brief expectations
src = (P / 'orchestration/compare.py').read_text().split('old, oldm = load')[0]; ns = {}; exec(src, ns)
old, om = ns['load'](OLD); new, nm = ns['load'](D)
def q(pat, nodes, d, m):
    r = re.compile(pat); return dict(collections.Counter(st for k, st in d.items() if r.fullmatch(k[1]) and m[k]['node'] in nodes))
ALL = ['n0', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7']; SWI = ['n1', 'n2', 'n3', 'n4']
fixed_checks = [('PE-008', r'PE-008', ALL), ('SR-015 on N5', r'SR-015', ['n5']), ('PE-014..018 on N6 and N7', r'PE-01[4-8]', ['n6', 'n7']), ('SU-HTTP-016 on N6 and N7', r'SU-HTTP-016', ['n6', 'n7']),
                ('URI-001..006, URI-010 on N6', r'URI-0(0[1-6]|10)', ['n6']), ('TXT-019/023/024/026', r'TXT-0(19|23|24|26)', ALL + ['fixture:swi', 'fixture:trealla']),
                ('OPT-004, URI-007, URI-011 on SWI and Trealla (live and fixtures)', r'(OPT-004|URI-007|URI-011)', SWI + ['n5', 'fixture:swi', 'fixture:trealla']),
                ('HTTP-FIELD-024..026, 051..053 on N5', r'HTTP-FIELD-0(2[4-6]|5[1-3])', ['n5']), ('CA-002, CA-013/014 on N7', r'CA-0(02|13|14)', ['n7']), ('LC-082/083/087/088 on N7', r'LC-08[2378]', ['n7'])]
remain_checks = [('NU-020/021 on N7', r'NU-02[01]', ['n7']), ('ER-007 on N6', r'ER-007', ['n6']), ('HTTP-CTL on N6', r'HTTP-CTL-.*', ['n6']), ('SL-014..017 on N7', r'SL-01[4-7]', ['n7']), ('LOCAL-006/007 live', r'LOCAL-00[67]', ALL)]
L += ['', '## Brief expectations', '', 'Expected to stop failing:', '', '| Rows | 20 Nov | 21 Nov |', '|---|---|---|']
for name, pat, nodes in fixed_checks: L.append(f'| {name} | {fmt(q(pat, nodes, old, om))} | {fmt(q(pat, nodes, new, nm))} |')
def inv(report):
    n = 0
    for f in read(report / 'SUMMARY.json')['files']:
        if '/n7/' not in f['file'] and 'n7' not in Path(f['file']).name: continue
        try: data = read(report / f['file'])
        except Exception: continue
        n += sum(1 for r in ns['rows'](data) if r['status'] == 'fail' and 'Invalid request or goal' in json.dumps(r))
    return n
L.append(f'| N7 failed rows reporting "Invalid request or goal" | {inv(OLD)} | {inv(D)} |')
L += ['', 'Remaining PE-008 failure: N7 with `limit=5&timeout=1` returns `success([a],true)`; `timeout` alone gives `resource_error(time)`. URI-007 still fails in the owned Trealla fixture (standalone boundaries); it passes on live N5 and the SWI fixture.', '',
      'Expected to remain:', '', '| Rows | 20 Nov | 21 Nov |', '|---|---|---|']
for name, pat, nodes in remain_checks: L.append(f'| {name} | {fmt(q(pat, nodes, old, om))} | {fmt(q(pat, nodes, new, nm))} |')
L += ['', 'SL-014..017 on sandbox-off N7 are still recorded as failures; marking them not applicable is a harness change that has not been made.']

L += ['', '## Regression: receive guards on Trealla', '',
      'Receive-control RG-001, RG-002, RG-003, RG-005, RG-006 and RG-007 pass on 20 November and fail in this run in the owned Trealla fixture (`timed out`, `missing_time_error`, `missing_termination`). They check that abort, the configured execution limit and actor termination propagate while an entered receive guard waits in `rpc/2`.', '',
      'Controls in the same lab image: predecessor Trealla `d451596` passes all eight cases; `7a8e8ce`, `a4739ed` and `49377b5` each fail the same six. The regression is introduced by `7a8e8ce` ("Keep receive body cuts local and align rpc timeouts and options with the manual"): `rpc.pl` now maps every `time_limit_exceeded` raised during the HTTP read to `rpc_error(http_timeout)`, including the owner\'s execution limit, and inside a guard an rpc error is a non-match. Live N5 was rolled back after this sweep; the fix belongs in trealla-port.']

L += ['', '## Remaining failures by category', '', 'Categories follow the 20 November status classification. Rows that do not match a recorded category are left unclassified rather than guessed.', '', '| Category | Rows | Packs |', '|---|---|---|']
for name, xs in sorted(classes.items(), key=lambda kv: -len(kv[1])):
    L.append(f"| {name} | {len(xs)} | {', '.join(sorted({x['suite'] if x['suite'] != '?' else '(aggregate adapter)' for x in xs}))} |")
L += ['', 'N6 capacity refusals: none in this run (62 replayed rows on 20 November).', '',
      'Unclassified rows include N7 NU-015/016/017/019 (URI 0.2), N7 PE-001, ER-010 on N1 and N7, and owned-fixture rows in isobase-diagnostics, retained-context (CTX-016/017 b), statechart-document and the browser B-SV-006 case. Every one of them also failed on 20 November.']

L += ['', '## Live standard library', '', '842 rows per transport, original source and assertions.', '', '| Node | Stateless HTTP | Retained WSS |', '|---|---|---|']
for n in ['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7']:
    rows = [r for p in (P / 'live-library' / n).glob('*.json') for r in rs(p)]
    L.append('| ' + n.upper() + ' | ' + fmt(count([r for r in rows if r.get('candidate', '').endswith('-http')])) + ' | ' + (fmt(count([r for r in rows if r.get('candidate', '').endswith('-wss')])) if n in ['n3', 'n4', 'n5', 'n7'] else 'not exposed') + ' |')
a = read(P / 'admission-summary.json')
L += ['', '## Finite admission', '', f"{a['finite_observations']} fresh finite HTTP probes, 140 per node on N1–N7, 0.6 s apart after all other endpoint work; outside manifest row counts. Overall: {a['status']}.", '', '| Node | Probe result | Admission policy unchanged |', '|---|---|---|']
for x in a['nodes']: L.append('| ' + x['node'].upper() + ' | ' + x['status'] + ' | ' + str(x.get('admission_policy_matches_before')) + ' |')
L += ['', 'Blocked, unsupported and inapplicable rows are accounted for without being called passes; every unexecuted row keeps its reason in verification.json. Persistent service container and image IDs match the pre-run snapshot, and all owned fixture containers were removed.', '',
      '[Completion checks](execution/completion-verification.json) · [artifact hashes](files-sha256.json)']
(D / 'REPORT.md').write_text('\n'.join(L) + '\n')
for name in ['orchestration-changes.json', 'completion-verification.json']:
    (D / 'execution' / name).write_text(json.dumps(read(P / name), indent=2) + '\n')
(D / 'COMPARISON.json').write_text(json.dumps(dict(cmp, classification={k: len(x) for k, x in classes.items()}, rows_by_category={k: [dict(file=r['file'], id=r['id'], node=r['node'], suite=r['suite']) for r in x] for k, x in classes.items()}), indent=2) + '\n')
# Unchanged tail from render_report.py
byclass = collections.defaultdict(collections.Counter)
for f in s['files']: byclass[f['classification']].update(f['counts'])
s.update(status='completed_with_failures_retained' if any(f['counts'].get('fail', 0) or f['counts'].get('error', 0) for f in s['files']) else 'completed', counts_by_classification={k: dict(x) for k, x in byclass.items()}, completion=completion)
(D / 'SUMMARY.json').write_text(json.dumps(s, indent=2) + '\n')
(D / 'RESULTS.json').write_text(json.dumps({'status': s['status'], 'manifest_count': s['manifest_count'], 'main_case_rows': s['main_case_rows'], 'primary_public': primary, 'counts_by_classification': s['counts_by_classification'], 'completion': completion}, indent=2) + '\n')
(D / 'files-sha256.json').write_text(json.dumps({str(p.relative_to(D)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(D.rglob('*')) if p.is_file() and p.name != 'files-sha256.json'}, indent=2) + '\n')
print('Rendered report', {k: len(x) for k, x in classes.items()})
