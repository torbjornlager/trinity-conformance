import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from receive_controls import validate_observation, validate_report


def answer():
    return dict(type='success', more=False, data=[dict(ControlCheck='passed')])


class GuardControlTests(unittest.TestCase):
    def setUp(self):
        self.case = dict(id='RG-001', control='abort')
        self.observed = dict(entry_count=1, peer_held_at_control=True, guard_target='primary-session',
                             control_response=dict(type='abort'), recovery=answer(), health=answer(), halt_confirmed=True)

    def test_complete_abort_control(self):
        validate_observation(self.case, self.observed)

    def test_admission_failure_missing_entry_or_released_peer_cannot_pass(self):
        for update in (dict(entry_count=0), dict(entry_count=2), dict(peer_held_at_control=False), dict(control_response=dict(type='error'))):
            observed = copy.deepcopy(self.observed)
            observed.update(update)
            with self.assertRaises(ValueError):
                validate_observation(self.case, observed)

    def test_recovery_continuation_or_missing_cleanup_cannot_pass(self):
        for key, value in [('halt_confirmed', False), ('recovery', dict(type='success', more=True, data=[dict(ControlCheck='passed')])), ('health', {})]:
            observed = copy.deepcopy(self.observed)
            observed[key] = value
            with self.assertRaises(ValueError):
                validate_observation(self.case, observed)

    def test_time_control_requires_formal_error_and_retained_recovery(self):
        case = dict(control='time_limit')
        observed = dict(self.observed, guard_target='worker-child-toplevel', control_and_recovery=answer(), formal_error_checked='error(resource_error(time),_)')
        validate_observation(case, observed)
        observed['formal_error_checked'] = 'display diagnostic'
        with self.assertRaises(ValueError):
            validate_observation(case, observed)

    def test_termination_and_ordinary_controls_are_distinct(self):
        validate_observation(dict(control='terminate'), dict(self.observed, guard_target='worker-child-actor', control_response=answer()))
        validate_observation(dict(control='ordinary_error'), dict(self.observed, ordinary_response=answer()))
        with self.assertRaises(ValueError):
            validate_observation(dict(control='terminate'), self.observed)

    def test_manifest_hash_and_complete_unique_accounting(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'manifest.json'
            path.write_text(json.dumps(dict(cases=[self.case])))
            report = dict(manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), counts={'pass': 1, 'fail': 0}, results=[dict(candidate='swi', id='RG-001', status='pass', observation=self.observed)])
            self.assertEqual(validate_report(path, report, ['swi']), 1)
            for update in (dict(results=[]), dict(results=report['results'] * 2), dict(manifest_sha256='wrong')):
                bad = dict(report, **update)
                with self.assertRaises(ValueError):
                    validate_report(path, bad, ['swi'])
