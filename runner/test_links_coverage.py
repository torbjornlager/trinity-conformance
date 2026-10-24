"""Required failures and missing cases remain visible in the local matrix."""
import json
from pathlib import Path
import tempfile
import unittest
import links_coverage

class LinksCoverage(unittest.TestCase):
 def test_failure_and_absent_case_are_not_reported_as_passes(self):
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp)
   swi=dict(counts={'pass':1,'fail':1},results=[dict(id='LM-A',status='pass'),dict(id='LM-B',status='fail',detail='sentinel failure')])
   trealla=dict(counts={'pass':1,'fail':0},results=[dict(id='LM-A',status='pass')])
   for name,d in [('swi',swi),('trealla',trealla)]:(out/(name+'-links-monitors.json')).write_text(json.dumps(d))
   links_coverage.render(out);text=(out/'COVERAGE.md').read_text()
   self.assertIn('2/3 selected assertions pass; 1 failures',text)
   self.assertIn('| LM-B | [fail](swi-links-monitors.json) | not measured |',text)
   self.assertIn('sentinel failure',text)

class ServerWaitCoverage(unittest.TestCase):
 def test_server_waits_use_their_own_reports_and_preserve_failure(self):
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp)
   for name in ['swi','trealla']:
    fail=name=='trealla'
    data=dict(counts={'pass':int(not fail),'fail':int(fail)},results=[dict(id='SW-TEST',status='fail' if fail else 'pass',detail='wait sentinel')])
    (out/(name+'-server-waits.json')).write_text(json.dumps(data))
   links_coverage.render(out,'server-waits');text=(out/'COVERAGE.md').read_text()
   self.assertIn('1/2 selected assertions pass; 1 failures',text)
   self.assertIn('[fail](trealla-server-waits.json)',text)
   self.assertIn('wait sentinel',text)
   self.assertNotIn('LM-006',text)

if __name__=='__main__':unittest.main()
