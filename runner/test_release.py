import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import release

class ReleaseGate(unittest.TestCase):
    def test_skips_and_partial_results_cannot_pass(self):
        self.assertTrue(release.complete_pass({'results':[{'id':'a','status':'pass'}]}, ['a']))
        for report in [{}, {'results':[]}, {'results':[{'id':'a','status':'unsupported'}]},
                       {'results':[{'id':'a','status':'pass'},{'id':'a','status':'pass'}]}]:
            self.assertFalse(release.complete_pass(report,['a']))
    def test_gate_requires_both_risky_boundary_packs(self):
        suites={p['suite'] for p in json.loads(release.PROFILE.read_text())['packs']}
        self.assertTrue({'source-copying-0.1','ownership-lifecycle-0.1'} <= suites)
    def test_missing_credentials_stop_before_connection(self):
        with tempfile.TemporaryDirectory() as d:
            p=subprocess.run([sys.executable,str(Path(release.__file__)), '--ws-url','ws://127.0.0.1:1/ws',
                '--candidate','test','--token-env','ABSENT_RELEASE_OWNER_TOKEN',
                '--observer-token-env','ABSENT_RELEASE_OBSERVER_TOKEN','--disposable-fixture',
                '--output',str(Path(d)/'out')],capture_output=True,text=True,env={})
            self.assertEqual(p.returncode,2)
            self.assertIn('two distinct execution-only',p.stderr)
            self.assertFalse((Path(d)/'out').exists())

if __name__=='__main__': unittest.main()
