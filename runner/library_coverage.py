#!/usr/bin/env python3
"""Validate and render the clause-level library test inventory."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from appendix_coverage import ALIASES, ROOT
from library_noncompletion import validate_observation


def load_manifest(audit, root):
    manifest_path = root / audit['manifest']
    if not manifest_path.resolve().is_relative_to(root.resolve()):
        raise ValueError('escaping library manifest')
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != audit['manifest_sha256']:
        raise ValueError('library manifest changed; reassess clause coverage')
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('extends'):
        parent_path = root / manifest['extends']['manifest']
        if not parent_path.resolve().is_relative_to(root.resolve()):
            raise ValueError('escaping parent library manifest')
        parent_raw = parent_path.read_bytes()
        if hashlib.sha256(parent_raw).hexdigest() != manifest['extends']['sha256']:
            raise ValueError('parent library manifest changed')
        parent = json.loads(parent_raw)
        if manifest['cases'][:len(parent['cases'])] != parent['cases']:
            raise ValueError('extended library cases changed their parent assertions')
        if not manifest.get('source', '').startswith(parent.get('source', '')):
            raise ValueError('extended library source changed its parent prefix')
    cases = {r['id'] for r in manifest['cases']}
    if audit.get('case_count', len(cases)) != len(cases):
        raise ValueError('library case count mismatch')
    if len(cases) != len(manifest['cases']):
        raise ValueError('duplicate library case')
    return manifest


def load_reports(audit, targets, root):
    if set(audit['evidence']) != set(targets):
        raise ValueError('incomplete library target accounting')
    reports = {}
    for mode, evidence in audit['evidence'].items():
        if evidence['candidate'] != ALIASES[mode]:
            raise ValueError('wrong library evidence target')
        path = root / evidence['report']
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError('escaping library report')
        reports[mode] = json.loads(path.read_text())
        if reports[mode]['manifest_sha256'] != audit['manifest_sha256']:
            raise ValueError('evidence used a different library manifest')
    return reports


def validate(audit, ledger, root=ROOT):
    if audit['source'] != ledger['source']:
        raise ValueError('library audit manuscript does not match ledger')
    manifest = load_manifest(audit, root)
    reports = load_reports(audit, ledger['targets'], root)
    definitions = {r['id']: r for r in manifest['cases']}
    case_reports = {case: reports for case in definitions}
    for extra in audit.get('supplemental_suites', []):
        added = load_manifest(extra, root)
        extra_reports = load_reports(extra, ledger['targets'], root)
        for case in added['cases']:
            if case['id'] in definitions:
                raise ValueError('duplicate supplemental library case')
            definitions[case['id']] = case
            case_reports[case['id']] = extra_reports
    cases = set(definitions)
    units = {r['id'] for r in ledger['requirements']}
    seen = set()
    for row in audit['obligations']:
        if row['id'] in seen:
            raise ValueError('duplicate library obligation')
        seen.add(row['id'])
        if not row['requirements'] or not set(row['requirements']) <= units:
            raise ValueError('missing library source unit')
        if row['status'] not in ['covered', 'needs_tests', 'failing']:
            raise ValueError('unknown library status')
        if row['status'] == 'covered' and (not row['existing_cases'] or row['tests_needed']):
            raise ValueError('covered obligation requires evidence and no open tests')
        if row['status'] == 'needs_tests' and not row['tests_needed']:
            raise ValueError('open obligation requires a concrete test gap')
        failed = {mode: [] for mode in reports}
        for case in row['existing_cases']:
            if case not in cases:
                raise ValueError('unknown library case')
            for mode, report in case_reports[case].items():
                candidate = ALIASES[mode]
                observed = [r for r in report['results'] if r['id'] == case and r['candidate'] == candidate]
                if len(observed) != 1 or observed[0]['status'] not in ['pass', 'fail']:
                    raise ValueError('missing, duplicate or nonpassing library evidence')
                if observed[0]['status'] == 'pass' and definitions[case].get('bounded_noncompletion'):
                    validate_observation(definitions[case], observed[0].get('observation', {}))
                if observed[0]['status'] == 'fail':
                    failed[mode].append(case)
        if row.get('per_target'):
            if set(row['per_target']) != set(reports):
                raise ValueError('incomplete obligation target accounting')
            for mode, target in row['per_target'].items():
                expected = 'failing' if failed[mode] else 'needs_tests' if row['tests_needed'] else 'covered'
                if target['status'] != expected or sorted(target['failing_cases']) != sorted(failed[mode]):
                    raise ValueError('nonpassing library evidence target mismatch')
        expected = 'failing' if any(failed.values()) else 'needs_tests' if row['tests_needed'] else 'covered'
        if row['status'] != expected:
            raise ValueError('nonpassing library evidence cannot be relabelled')
    return dict(Counter(r['status'] for r in audit['obligations']))


def render(audit, counts):
    out = ['# Library requirement test gaps', '',
           f"Pinned Appendix B: `{audit['source']['revision']}`. The expanded prose is mapped into **{sum(counts.values())} testable obligations**: **{counts.get('covered', 0)} covered** within existing evidence and **{counts.get('needs_tests', 0)} needing additional tests**, and **{counts.get('failing', 0)} with an observed failure**. These are clause counts, not a conformance percentage.", '',
           f"The {audit.get('case_count', 112)}-case shared manifest and {sum(s.get('case_count', 0) for s in audit.get('supplemental_suites', []))} supplemental case(s) supply recorded native SWI, Trealla, GNU and both browser-mode observations. Each case is checked against its own pinned manifest and all five recorded targets. This does not certify current public deployments. A partial row can contain passing cases while still needing tests; a known failure is recorded separately.", '',
           '[Source-unit matrix](APPENDIX_B_COVERAGE.md) · [Machine-readable clause inventory](../requirements/library-obligations-0.1.json) · [Shared test goals](../' + audit['manifest'] + ')', '',
           '## Observed failures', '',
           '| ID / source unit | Assertion | Failing target and cases |', '|---|---|---|']
    for r in audit['obligations']:
        if r['status'] == 'failing':
            failures = '; '.join(mode + ': ' + ', '.join(t['failing_cases']) for mode, t in r['per_target'].items() if t['status'] == 'failing')
            out.append('| ' + r['id'] + ' / ' + ', '.join(r['requirements']) + ' | ' + r['statement'] + ' | ' + failures + ' |')
    if counts.get('failing'):
        out += ['', *audit.get('failure_notes', []), '']
    else:
        out += ['', 'No failures in the current selected development evidence. The [earlier Trealla failures](../reports/2026-11-05-library-finite-cases/README.md) and [repair qualification](../reports/2026-11-05-trealla-succ-repair/README.md) remain separate records; this is not a public deployment claim.', '']
    out += ['', '## Additional tests', '',
           '| ID / source unit | Family | Existing cases | Tests still needed |',
           '|---|---|---|---|']
    for r in audit['obligations']:
        if r['status'] != 'needs_tests':
            continue
        cases = ', '.join(r['existing_cases']) or 'None for this clause'
        out.append('| ' + r['id'] + ' / ' + ', '.join(r['requirements']) + ' | `' + r['family'] + '` | ' + cases + ' | ' + ' '.join(r['tests_needed']).replace('|', '\\|') + ' |')
    if not counts.get('needs_tests'):
        out += ['', 'No additional test gaps in this selected obligation inventory. The scope limits below still apply.', '']
    out += ['', '## Covered clauses within the recorded selection', '',
            '| ID / source unit | Assertion | Cases passing on all five recorded targets |', '|---|---|---|']
    for r in audit['obligations']:
        if r['status'] == 'covered':
            out.append('| ' + r['id'] + ' / ' + ', '.join(r['requirements']) + ' | `' + r['family'] + '` — ' + r['statement'] + ' | ' + ', '.join(r['existing_cases']) + ' |')
    out += ['', '## Separate decisions and limits', '']
    out += ['- ' + note for note in audit['deferred_semantic_decisions']]
    out += ['', 'The nineteen manuscript examples checked on native SWI do not supply five-target evidence. Shared nested forall controls and externally bounded member/length generation pass in all five recorded modes. Generation evidence checks six-answer prefixes, followed by continuation stop and recovery on retained sessions; it is not a proof of every infinite enumeration. The [countall fixture](../reports/2026-11-05-library-noncompletion/README.md) confirms callback entry, no completed count or error during 500 ms, external termination and fresh-execution recovery on every mode. It is not a mathematical nontermination proof, same-session abort guarantee or public transport certificate.', '',
            'New source-unit signatures remain unverified pending full supported-mode mapping. Finite callback assertions pass, but the common paragraph incorporates the broader ISO call/N contract, which remains unexpanded; it is not promoted wholesale. Unverified does not mean an implementation has failed.', '']
    return '\n'.join(out)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    audit = json.loads((ROOT / 'requirements/library-obligations-0.1.json').read_text())
    ledger = json.loads((ROOT / 'requirements/appendix-b-0.1.json').read_text())
    try:
        counts = validate(audit, ledger)
        text = render(audit, counts)
        output = ROOT / 'docs/LIBRARY_TEST_GAPS.md'
        if args.check:
            if output.read_text() != text:
                raise ValueError('library gap document is stale')
        else:
            output.write_text(text)
        print(json.dumps(counts))
    except (OSError, KeyError, ValueError) as error:
        p.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
