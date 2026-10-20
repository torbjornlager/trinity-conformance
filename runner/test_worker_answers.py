"""Guard against weakening the public worker-answer assertions."""
import unittest
from unittest.mock import patch
from run import worker_goal, ConformanceFailure

class ScriptedHarness:
    def __init__(self, events):
        self.events = iter(events)
        self.calls = []
        self.options = None
        self.halted = False
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass
    def spawn_shell(self, options):
        self.options = options
    def call(self, goal, options):
        self.calls.append((goal, options))
    def recv(self):
        return next(self.events)
    def halt(self):
        self.halted = True

class WorkerAnswerTests(unittest.TestCase):
    def test_child_down_before_final_bound_answer(self):
        harness = ScriptedHarness([{'type': 'down'},
            {'type': 'success', 'data': [{'X': 'ok'}], 'more': False}])
        with patch('run.Harness', return_value=harness):
            worker_goal(None, 'first_solution(X,[X=ok])', bindings={'X': 'ok'})
        self.assertEqual(harness.calls, [('first_solution(X,[X=ok])', '[limit(1)]')])
        self.assertTrue(harness.halted)

    def test_empty_continuation_is_a_failure_of_the_assertion(self):
        harness = ScriptedHarness([{'type': 'success', 'data': [{}], 'more': True}])
        with patch('run.Harness', return_value=harness):
            with self.assertRaisesRegex(ConformanceFailure, 'continuation'):
                worker_goal(None, 'first_solution(ok,[true])')

    def test_query_error_is_not_waited_past(self):
        harness = ScriptedHarness([{'type': 'error', 'data': 'ownership_error'}])
        with patch('run.Harness', return_value=harness):
            with self.assertRaisesRegex(ConformanceFailure, 'ownership_error'):
                worker_goal(None, 'first_solution(X,[X=ok])')

    def test_expected_failure_is_observed_without_an_extra_read(self):
        harness = ScriptedHarness([{'type': 'down'}, {'type': 'failure'}])
        with patch('run.Harness', return_value=harness):
            worker_goal(None, 'parallel([fail])', expected='failure')
        self.assertTrue(harness.halted)

if __name__ == '__main__':
    unittest.main()
