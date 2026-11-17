import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from library_coverage import validate


class LibraryCoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'cases.json').write_text(json.dumps(dict(cases=[dict(id='STDLIB-001')])))
        sha = hashlib.sha256((self.root / 'cases.json').read_bytes()).hexdigest()
        self.ledger = dict(source=dict(revision='pinned'), targets=dict(swi='native'), requirements=[dict(id='B-359')])
        self.audit = dict(source=self.ledger['source'], manifest='cases.json', manifest_sha256=sha,
                          evidence=dict(swi=dict(report='run.json', candidate='swi')),
                          obligations=[dict(id='LIB-001', requirements=['B-359'], status='covered',
                                            existing_cases=['STDLIB-001'], tests_needed=[])])
        self.report = dict(manifest_sha256=sha, results=[dict(id='STDLIB-001', candidate='swi', status='pass')])
        self.save()

    def save(self):
        (self.root / 'run.json').write_text(json.dumps(self.report))

    def test_covered_and_partial_are_distinct(self):
        self.assertEqual(validate(self.audit, self.ledger, self.root), dict(covered=1))
        self.audit['obligations'][0].update(status='needs_tests', tests_needed=['Bounded fresh-list generation'])
        self.assertEqual(validate(self.audit, self.ledger, self.root), dict(needs_tests=1))

    def test_covered_cannot_hide_a_gap_or_lack_evidence(self):
        for update in [dict(existing_cases=[]), dict(tests_needed=['More tests'])]:
            audit = copy.deepcopy(self.audit)
            audit['obligations'][0].update(update)
            with self.assertRaisesRegex(ValueError, 'covered obligation'):
                validate(audit, self.ledger, self.root)

    def test_missing_duplicate_or_failed_observation_cannot_cover(self):
        for rows in [[], self.report['results'] * 2, [dict(self.report['results'][0], status='fail')]]:
            self.report['results'] = rows
            self.save()
            with self.assertRaisesRegex(ValueError, 'nonpassing library evidence'):
                validate(self.audit, self.ledger, self.root)

    def test_manuscript_and_executed_manifest_must_match(self):
        changed = copy.deepcopy(self.audit)
        changed['source'] = dict(revision='other')
        with self.assertRaisesRegex(ValueError, 'manuscript'):
            validate(changed, self.ledger, self.root)
        self.report['manifest_sha256'] = 'other'
        self.save()
        with self.assertRaisesRegex(ValueError, 'different library manifest'):
            validate(self.audit, self.ledger, self.root)

    def test_observed_failure_can_be_recorded_but_not_hidden(self):
        self.report['results'][0]['status'] = 'fail'
        self.save()
        row = self.audit['obligations'][0]
        row.update(status='failing', per_target=dict(swi=dict(status='failing', failing_cases=['STDLIB-001'])))
        self.assertEqual(validate(self.audit, self.ledger, self.root), dict(failing=1))
        row['per_target']['swi']['status'] = 'covered'
        with self.assertRaisesRegex(ValueError, 'target mismatch'):
            validate(self.audit, self.ledger, self.root)

    def test_passing_observations_cannot_be_labelled_failing(self):
        self.audit['obligations'][0]['status'] = 'failing'
        with self.assertRaisesRegex(ValueError, 'cannot be relabelled'):
            validate(self.audit, self.ledger, self.root)

    def test_unknown_source_case_or_target_is_rejected(self):
        for mutate in [lambda a: a['obligations'][0].update(requirements=['B-missing']),
                       lambda a: a['obligations'][0].update(existing_cases=['missing']),
                       lambda a: a.update(evidence={}),
                       lambda a: a['evidence']['swi'].update(candidate='gnu')]:
            audit = copy.deepcopy(self.audit)
            mutate(audit)
            with self.assertRaises(ValueError):
                validate(audit, self.ledger, self.root)

    def extension(self):
        parent = dict(cases=[dict(id='EARLIER', goal='true')], source='earlier_source.\n')
        raw = json.dumps(parent).encode()
        (self.root / 'parent.json').write_bytes(raw)
        child = dict(cases=parent['cases'] + [dict(id='STDLIB-001')],
                     source=parent['source'] + 'added_source.\n',
                     extends=dict(manifest='parent.json', sha256=hashlib.sha256(raw).hexdigest()))
        return child

    def save_manifest(self, manifest):
        raw = json.dumps(manifest).encode()
        (self.root / 'cases.json').write_bytes(raw)
        self.audit['manifest_sha256'] = hashlib.sha256(raw).hexdigest()
        self.report['manifest_sha256'] = self.audit['manifest_sha256']
        self.save()

    def test_parent_case_or_source_rewrite_cannot_qualify(self):
        child = self.extension()
        self.save_manifest(child)
        self.assertEqual(validate(self.audit, self.ledger, self.root), dict(covered=1))
        for mutation in ['case', 'source']:
            changed = copy.deepcopy(child)
            if mutation == 'case':
                changed['cases'][0]['goal'] = 'fail'
            else:
                changed['source'] = 'replaced_source.\n'
            self.save_manifest(changed)
            with self.assertRaisesRegex(ValueError, 'changed.*parent'):
                validate(self.audit, self.ledger, self.root)

    def test_parent_hash_drift_cannot_qualify(self):
        self.save_manifest(self.extension())
        (self.root / 'parent.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'parent library manifest changed'):
            validate(self.audit, self.ledger, self.root)

    def supplemental(self):
        manifest = dict(cases=[dict(id='EXTERNAL-001')])
        raw = json.dumps(manifest).encode()
        (self.root / 'extra.json').write_bytes(raw)
        sha = hashlib.sha256(raw).hexdigest()
        report = dict(manifest_sha256=sha, results=[dict(id='EXTERNAL-001', candidate='swi', status='pass')])
        (self.root / 'extra-report.json').write_text(json.dumps(report))
        self.audit['supplemental_suites'] = [dict(manifest='extra.json', manifest_sha256=sha,
            case_count=1, evidence=dict(swi=dict(report='extra-report.json', candidate='swi')))]
        self.audit['obligations'][0]['existing_cases'].append('EXTERNAL-001')
        return manifest, report

    def test_supplemental_cases_use_their_own_manifest_and_report(self):
        self.supplemental()
        self.assertEqual(validate(self.audit, self.ledger, self.root), dict(covered=1))
        self.audit['supplemental_suites'][0]['evidence']['swi']['report'] = 'run.json'
        with self.assertRaisesRegex(ValueError, 'different library manifest'):
            validate(self.audit, self.ledger, self.root)

    def test_supplement_cannot_shadow_an_existing_case(self):
        manifest, report = self.supplemental()
        manifest['cases'][0]['id'] = 'STDLIB-001'
        raw = json.dumps(manifest).encode()
        (self.root / 'extra.json').write_bytes(raw)
        sha = hashlib.sha256(raw).hexdigest()
        self.audit['supplemental_suites'][0]['manifest_sha256'] = sha
        report.update(manifest_sha256=sha)
        (self.root / 'extra-report.json').write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError, 'duplicate supplemental'):
            validate(self.audit, self.ledger, self.root)

    def test_passing_supplement_requires_its_bounded_observation(self):
        manifest, report = self.supplemental()
        manifest['cases'][0]['bounded_noncompletion'] = dict(observation_ms=500, entry_timeout_ms=5000, termination_timeout_ms=3000)
        raw = json.dumps(manifest).encode()
        (self.root / 'extra.json').write_bytes(raw)
        sha = hashlib.sha256(raw).hexdigest()
        self.audit['supplemental_suites'][0]['manifest_sha256'] = sha
        report.update(manifest_sha256=sha)
        (self.root / 'extra-report.json').write_text(json.dumps(report))
        with self.assertRaises((KeyError, ValueError)):
            validate(self.audit, self.ledger, self.root)


if __name__ == '__main__':
    unittest.main()
