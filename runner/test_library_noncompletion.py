import copy
import unittest

from library_noncompletion import bounds, validate_observation


class NoncompletionTests(unittest.TestCase):
    def setUp(self):
        self.case = dict(bounded_noncompletion=dict(observation_ms=500, entry_timeout_ms=5000, termination_timeout_ms=3000))
        self.observed = dict(warmup=dict(passed=True, entry_count=1), recovery=dict(passed=True, entry_count=1),
                             probe=dict(entry_count=1, entry_response_finished=True, elapsed_ms=501,
                                        terminal=None, alive_before_termination=True),
                             termination=dict(confirmed=True, duration_ms=25))

    def test_complete_bounded_observation(self):
        self.assertTrue(validate_observation(self.case, self.observed))

    def test_absent_or_duplicate_entry_cannot_pass(self):
        for count in (0, 2):
            bad = copy.deepcopy(self.observed)
            bad['probe']['entry_count'] = count
            with self.assertRaisesRegex(ValueError, 'entry signal'):
                validate_observation(self.case, bad)

    def test_completed_count_error_or_dead_execution_cannot_pass(self):
        for changes in (dict(terminal={'count': 0}), dict(terminal={'error': 'admission denied'}),
                        dict(alive_before_termination=False)):
            bad = copy.deepcopy(self.observed)
            bad['probe'].update(changes)
            with self.assertRaisesRegex(ValueError, 'completed or failed'):
                validate_observation(self.case, bad)

    def test_shortened_window_or_unfinished_response_cannot_pass(self):
        for changes in (dict(elapsed_ms=499), dict(entry_response_finished=False)):
            bad = copy.deepcopy(self.observed)
            bad['probe'].update(changes)
            with self.assertRaises(ValueError):
                validate_observation(self.case, bad)

    def test_missing_controls_or_unconfirmed_cleanup_cannot_pass(self):
        for phase, changes in [('warmup', dict(passed=False)), ('recovery', dict(entry_count=0)),
                               ('termination', dict(confirmed=False)), ('termination', dict(duration_ms=3001))]:
            bad = copy.deepcopy(self.observed)
            bad[phase].update(changes)
            with self.assertRaises(ValueError):
                validate_observation(self.case, bad)

    def test_unbounded_or_boolean_deadlines_are_rejected(self):
        for key, value in [('observation_ms', 0), ('observation_ms', 1000000),
                           ('entry_timeout_ms', True), ('termination_timeout_ms', 0)]:
            case = copy.deepcopy(self.case)
            case['bounded_noncompletion'][key] = value
            with self.assertRaises(ValueError):
                bounds(case)


if __name__ == '__main__':
    unittest.main()
