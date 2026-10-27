"""Regression tests for terminal answers hidden by asynchronous down events."""
import unittest
from run import Harness, ConformanceFailure

class AnswerWaitTests(unittest.TestCase):
    def harness(self, events):
        harness = Harness(None)
        pending = iter(events)
        harness.recv = lambda: next(pending)
        return harness

    def test_down_before_success(self):
        answer = {'type': 'success', 'data': [{}], 'more': False}
        harness = self.harness([{'type': 'down', 'pid': 1}, answer])
        self.assertEqual(harness.recv_type('success'), answer)

    def test_admission_error_reported_before_another_read(self):
        harness = self.harness([{'type': 'error', 'details': 'error(instantiation_error,_)'}])
        with self.assertRaisesRegex(ConformanceFailure, 'instantiation_error'):
            harness.recv_type('success')

    def test_failure_after_child_notification(self):
        harness = self.harness([{'type': 'down'}, {'type': 'failure'}])
        with self.assertRaisesRegex(ConformanceFailure, 'failure'):
            harness.recv_type('success')

    def test_input_request_is_not_acknowledged_as_output(self):
        harness = self.harness([{'type': 'io_request', 'request_id': 'input-1',
                                 'event': {'type': 'prompt', 'data': 'Name?'}}])
        with self.assertRaisesRegex(ConformanceFailure, 'non-output I/O'):
            harness.recv_type('success')

    def test_halt_wait_can_skip_previous_error(self):
        # Other wait types retain their original selective behaviour.
        harness = self.harness([{'type': 'error'}, {'type': 'halted'}])
        self.assertEqual(harness.recv_type('halted'), {'type': 'halted'})

if __name__ == '__main__':
    unittest.main()
