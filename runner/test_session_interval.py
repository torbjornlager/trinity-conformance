"""WebSocket session starts can be paced for nodes with engine-start limits."""
import unittest
from unittest import mock
import run


class SessionInterval(unittest.TestCase):
    def tearDown(self):
        run.set_session_interval(0.0)
        run._last_session_start = 0.0

    def test_default_never_sleeps(self):
        with mock.patch.object(run.time, 'sleep') as sleep:
            run._pace_session_start();run._pace_session_start()
        sleep.assert_not_called()

    def test_consecutive_starts_are_spaced(self):
        run.set_session_interval(4.0)
        clock = iter([100.0, 100.0, 101.0, 104.0])
        with mock.patch.object(run.time, 'monotonic', lambda: next(clock)), \
             mock.patch.object(run.time, 'sleep') as sleep:
            run._last_session_start = 0.0
            run._pace_session_start()   # long after the previous start: no wait
            run._pace_session_start()   # 1 s after: waits the remaining 3 s
        sleep.assert_called_once_with(3.0)

    def test_negative_interval_is_rejected(self):
        with self.assertRaises(ValueError):
            run.set_session_interval(-1)


if __name__ == '__main__':
    unittest.main()
