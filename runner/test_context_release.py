import copy
import json
import unittest

from context_release import MANIFEST, validate


class ContextReleaseTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(MANIFEST.read_text())
        self.expected = self.manifest['cases'] + self.manifest['controlled_promise_cases']
        self.report = dict(routes=self.manifest['routes'], results=[
            dict(row, status='pass') for row in self.expected])

    def check_report(self, report):
        validate(report, self.expected, self.manifest['routes'])

    def test_exact_inventory_passes(self):
        self.assertEqual(len(self.report['results']), 57)
        self.check_report(self.report)

    def test_missing_duplicate_or_unknown_case_cannot_pass(self):
        variants = [self.report['results'][1:],
                    self.report['results'] + [self.report['results'][0]],
                    self.report['results'][1:] + [dict(candidate='swi', id='unknown', status='pass')]]
        for rows in variants:
            with self.subTest(rows=len(rows)), self.assertRaises(ValueError):
                self.check_report(dict(self.report, results=rows))

    def test_nonpassing_or_policy_excluded_case_cannot_pass(self):
        for mutation in [dict(status=s) for s in ['fail', 'blocked', 'error', 'unsupported']] + [dict(policy_exclusion=True)]:
            report = copy.deepcopy(self.report)
            report['results'][0].update(mutation)
            # A forged aggregate count must not override observed rows.
            report['counts'] = dict(pass_count=57, fail=0)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.check_report(report)

    def test_missing_or_repeated_route_cannot_pass(self):
        for routes in [self.manifest['routes'][:-1], self.manifest['routes'] + self.manifest['routes'][:1]]:
            with self.assertRaises(ValueError):
                self.check_report(dict(self.report, routes=routes))

    def test_controlled_promises_cannot_be_omitted(self):
        report = dict(self.report, results=self.report['results'][:51])
        with self.assertRaises(ValueError):
            self.check_report(report)

    def test_negative_control_is_required_and_identified(self):
        expected = self.manifest['attachment_cases']
        report = dict(results=[dict(r, status='pass') for r in expected])
        validate(report, expected)
        report['results'][-1]['negative_control'] = False
        with self.assertRaises(ValueError):
            validate(report, expected)


if __name__ == '__main__':
    unittest.main()
