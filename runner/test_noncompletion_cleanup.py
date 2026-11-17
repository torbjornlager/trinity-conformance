import importlib.util
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location('native_noncompletion',
    Path(__file__).resolve().parents[1] / 'adapters/local_library_noncompletion.py')
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)


class CleanupRaceTests(unittest.TestCase):
    def test_child_exiting_between_poll_and_group_signal_is_reaped(self):
        child = Mock(pid=123456, returncode=0)
        child.poll.side_effect = [None, 0, 0]
        with patch.object(native.os, 'killpg', side_effect=PermissionError):
            observed = native.terminate(child)
        self.assertTrue(observed['confirmed'])
        child.terminate.assert_not_called()
        child.wait.assert_called_once()

    def test_live_owned_child_can_be_terminated_directly(self):
        child = Mock(pid=123456, returncode=-15)
        child.poll.side_effect = [None, None, -15]
        with patch.object(native.os, 'killpg', side_effect=PermissionError):
            observed = native.terminate(child)
        self.assertTrue(observed['confirmed'])
        child.terminate.assert_called_once()
        child.wait.assert_called_once()


if __name__ == '__main__':
    unittest.main()
