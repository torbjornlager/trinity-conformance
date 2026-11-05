import unittest

from promise_self_route_analysis import analyze


class SelfRouteAnalysisTests(unittest.TestCase):
    def test_recovered_retry_does_not_erase_timeout(self):
        report = dict(results=[dict(id='SELF-001', status='fail', stamped=True, trace=[
            dict(phase='created', event=dict(data=[dict(PromiseStart='1', PromiseReturned='1.001')])),
            dict(phase='owner_collection', event=dict(data=[dict(Outcome='timeout', WaitStart='2', WaitEnd='4')])),
            dict(phase='diagnostic_retry_after_timeout', event=dict(data=[dict(Outcome='success([mark(1.1)],false)', WaitStart='4', WaitEnd='4.1')]))])])
        result = analyze(report)
        self.assertEqual(result['counts'], {'pass': 0, 'fail': 1, 'error': 0})
        self.assertEqual(result['results'][0]['owner_yield_ms'], 2000)
        self.assertNotIn('producer_execution_to_collection_ms', result['results'][0])

    def test_error_without_timing_is_retained(self):
        result = analyze(dict(results=[dict(id='SELF-002', status='error', stamped=False, trace=[])]))
        self.assertEqual(result['counts']['error'], 1)
        self.assertEqual(result['results'][0]['timing_unavailable'], 'KeyError')


if __name__ == '__main__':
    unittest.main()
