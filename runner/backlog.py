"""Build the current issue inventory without changing historical observations.

Families are work queues, not counts of independent implementation defects.
Every included row retains its JSON pointer and original classification.
Reviewed decisions apply only to matching observations and require evidence.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ISSUE_STATUSES = {'fail', 'error', 'blocked', 'diagnostic_error'}
SKIP_FIELDS = {'observation', 'transcript', 'sources', 'source', 'inputs',
               'requests', 'events', 'trace'}


def rows(value, pointer='', inherited=None):
    context = dict(inherited or {})
    if isinstance(value, dict):
        for key in ['candidate', 'engine', 'suite', 'route', 'peer']:
            if value.get(key) is not None:
                context[key] = value[key]
        if value.get('status') and any(k in value for k in ['id', 'case_id', 'case', 'label']):
            yield pointer, {**context, **value}
            return
        for key, child in value.items():
            if key not in SKIP_FIELDS:
                escaped = key.replace('~', '~0').replace('/', '~1')
                yield from rows(child, pointer+'/'+escaped, context)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from rows(child, pointer+'/'+str(index), context)


def case_id(row):
    return str(next(row[k] for k in ['id', 'case_id', 'case', 'label'] if k in row))


def matches(record, selector):
    for key, expected in selector.items():
        if key.endswith('_contains'):
            if expected not in str(record.get(key[:-9], '')):
                return False
        elif key.endswith('_in'):
            if record.get(key[:-3]) not in expected:
                return False
        elif record.get(key) != expected:
            return False
    return True


def read(root, name, inputs):
    path = root/name
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    parts = Path(name).parts
    if len(parts)>2 and parts[0]=='reports':
        report = root/parts[0]/parts[1]
        manifest = report/'files-sha256.json'
        if manifest.exists() and path != manifest:
            hashes = json.loads(manifest.read_text())
            relative = path.relative_to(report).as_posix()
            if hashes.get(relative) != digest:
                raise ValueError('Report artifact hash mismatch: '+name)
    inputs[name] = digest
    return json.loads(raw)


def verify_proof(root, proof, inputs):
    data = read(root, proof['file'], inputs)
    selected = [r for _, r in rows(data)
                if matches({**r, 'case_id': case_id(r)}, proof.get('selector', {}))]
    if len(selected) < proof.get('minimum_matches', 1):
        raise ValueError('Missing proof observations: '+str(proof))
    if any(r['status'] != proof.get('status', 'pass') for r in selected):
        raise ValueError('Non-passing or conflicting proof: '+str(proof))


def family(record, config):
    for group in config['families']:
        if any(record['case_id'].startswith(p) for p in group.get('case_prefixes', [])):
            return group['id']
        if any(token in s for token in group.get('suite_tokens', []) for s in record['suites']):
            return group['id']
    return 'UNCLASSIFIED'


def build(root, config):
    inputs = {}
    summary = read(root, config['source_report']+'/SUMMARY.json', inputs)
    verification = read(root, config['source_report']+'/verification.json', inputs)
    unexecuted = [dict(suite=s['suite'], case_id=c['id']) for s in verification['coverage'] for c in s['cases'] if not c['has_execution_observation']]
    for decision in config['decisions']:
        if not decision.get('proofs'):
            raise ValueError('A decision requires evidence: '+decision['id'])
        for proof in decision['proofs']:
            verify_proof(root, proof, inputs)
    for finding in config.get('additional_findings', []):
        for proof in finding['proofs']:
            verify_proof(root, proof, inputs)
    observations, excluded = [], []
    hits = Counter()
    for entry in summary['files']:
        if not any(entry.get('counts', {}).get(s, 0) for s in ISSUE_STATUSES):
            continue
        name = config['source_report']+'/'+entry['file']
        data = read(root, name, inputs)
        for pointer, row in rows(data):
            if row['status'] not in ISSUE_STATUSES:
                continue
            record = dict(file=name, pointer=pointer, case_id=case_id(row),
                          candidate=row.get('candidate', row.get('engine')),
                          route=row.get('route'), peer=row.get('peer'),
                          title=row.get('title'), status=row['status'],
                          detail=row.get('detail', row.get('blocker', '')),
                          suites=[row['suite']] if row.get('suite') else entry['suites'],
                          original_classification=entry['classification'])
            reason = next((p for p in config['exclude_classification_prefixes']
                           if entry['classification'].startswith(p)), None)
            if 'invalid WebSocket URL' in record['detail']:
                reason = 'invalid_harness_toplevel_url'
            if reason:
                excluded.append(dict(record, exclusion=reason))
                continue
            record.update(family=family(record, config),
                          production_disposition=('blocked_precondition' if row['status']=='blocked' else 'diagnostic_only' if row['status']=='diagnostic_error' else 'open'), diagnosis='unclassified')
            for decision in config['decisions']:
                if any(matches(record, s) for s in decision['selectors']):
                    for key, value in decision['set'].items():
                        record[key] = value
                    record.setdefault('decisions', []).append(decision['id'])
                    hits[decision['id']] += 1
            observations.append(record)
    for decision in config['decisions']:
        if not hits[decision['id']]:
            raise ValueError('Decision matches no original observation: '+decision['id'])
    groups = []
    by_family = defaultdict(list)
    for row in observations:
        by_family[row['family']].append(row)
    descriptions = {f['id']: f for f in config['families']}
    for key, items in sorted(by_family.items()):
        groups.append(dict(id=key, title=descriptions.get(key, {}).get('title', key),
                           next_action=descriptions.get(key, {}).get('next_action', 'Classify individually.'),
                           original_statuses=dict(Counter(r['status'] for r in items)),
                           production_dispositions=dict(Counter(r['production_disposition'] for r in items)),
                           case_ids=sorted({r['case_id'] for r in items}),
                           observation_count=len(items)))
    return dict(format=1, source_report=config['source_report'],
                configuration_sha256=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest(),
                accounting='Families are work queues, not independently proven root causes. Case IDs and observations are not feature/defect counts. Candidate repairs do not close deployed findings.',
                inputs_sha256=inputs, families=groups, observations=observations,
                excluded_observations=excluded, decisions=config['decisions'],
                input_rows_without_execution=unexecuted,
                additional_findings=config.get('additional_findings', []),
                counts=dict(original_statuses=dict(Counter(r['status'] for r in observations)),
                            production_dispositions=dict(Counter(r['production_disposition'] for r in observations)),
                            excluded=len(excluded)))


def render(data, output):
    lines = ['# Current conformance issues', '',
             'The primary deployment checks pass. The broader contract backlog remains open.', '',
             '**This is the current triage view.** [Historical full sweep]('+data['source_report']+'/REPORT.md) · [Machine inventory](backlog/current.json) · [Reviewed decisions](backlog/decisions.json).', '',
             data['accounting'], '',
             'Original failures are retained. Later passing controls are linked to exact observations; neither unrelated passes nor candidate-only repairs turn production green. `open` means unresolved evidence, not a proven runtime defect.', '',
             'The reviewed baseline has '+str(data['counts']['original_statuses'].get('fail',0))+' applicable failed observations. '+str(data['counts']['production_dispositions'].get('open',0))+' remain unresolved failed observations. These figures count repeated runs and projections, not independent defects. Blocked selections are counted separately.', '',
             'There are '+str(len(data['input_rows_without_execution']))+' full-sweep input rows without a completed execution anywhere. Repeated blocked projections onto live endpoints are listed separately; they are not additional demonstrated defects.', '',
             '## Work queues', '',
             '| Queue | Original observations | Current disposition | Next action |',
             '|---|---:|---|---|']
    for group in data['families']:
        states=', '.join(str(n)+' '+s.replace('_',' ') for s,n in group['production_dispositions'].items())
        lines.append('| '+group['title']+' | '+str(group['observation_count'])+' | '+states+' | '+group['next_action']+' |')
    lines += ['', '## Contract correction', '',
              'The recorded author-directed decision of 17 November supersedes the earlier atom-only URI proposal. The old manual text and MC-028/029 rejection expectations were stale. Monitor packs 0.2 test accepted text forms against the same actor and actual monitor delivery; 0.1 remains immutable. The stale manual wording is corrected against that decision.', '',
              '## Evidence by queue', '']
    for group in data['families']:
        lines += ['### '+group['title'], '', 'Cases: '+', '.join('`'+i+'`' for i in group['case_ids'])+'.', '']
        files=sorted({r['file'] for r in data['observations'] if r['family']==group['id']})
        lines += ['- ['+f.split('/observations/')[-1]+']('+f+')' for f in files]
        lines += ['']
    lines += ['## Reviewed decisions', '']
    for decision in data['decisions']:
        lines += ['- **'+decision['id']+'**: '+decision['note']+' '+
                  ' '.join('[Evidence]('+p['file']+')' for p in decision['proofs'])]
    lines += ['', '## Additional qualification findings', '']
    for finding in data['additional_findings']:
        lines += ['- **'+finding['id']+'**: '+finding['note']+' '+
                  ' '.join('[Evidence]('+p['file']+')' for p in finding['proofs'])]
    lines += ['', 'Regenerate: `python3 runner/backlog.py`. Historical report directories are never edited.', '']
    output.write_text('\n'.join(lines))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', type=Path, default=ROOT/'backlog/decisions.json')
    a=p.parse_args()
    data=build(ROOT,json.loads(a.config.read_text()))
    (ROOT/'backlog/current.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    render(data, ROOT/'CURRENT_ISSUES.md')
    print(json.dumps(data['counts']))


if __name__=='__main__':
    main()
