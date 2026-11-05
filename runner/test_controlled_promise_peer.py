from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import unittest
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'adapters'))
from controlled_promise_peer import ControlledPromisePeer


class ControlledPromisePeerTests(unittest.TestCase):
    def test_response_requires_explicit_release(self):
        with ControlledPromisePeer() as peer, ThreadPoolExecutor(max_workers=1) as pool:
            def request():
                with urllib.request.urlopen(peer.url + '/call', timeout=3) as response:
                    return response.read()

            future = pool.submit(request)
            try:
                self.assertTrue(peer.arrived.wait(2))
                self.assertFalse(peer.sent.is_set())
                self.assertFalse(future.done())
            finally:
                peer.release.set()
            self.assertEqual(future.result(timeout=2), b'success([mark],false).\n')
            self.assertTrue(peer.sent.wait(2))
            self.assertEqual(len(peer.requests), 1)
            self.assertEqual(peer.errors, [])


if __name__ == '__main__':
    unittest.main()
