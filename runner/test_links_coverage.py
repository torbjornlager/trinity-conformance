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

class SelectiveReceiveCoverage(unittest.TestCase):
 def test_receive_suite_preserves_failure_and_scope(self):
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp)
   for name in ['swi','trealla']:
    failed=name=='swi'
    data=dict(counts={'pass':int(not failed),'fail':int(failed)},results=[dict(id='SR-TEST',status='fail' if failed else 'pass',detail='receive sentinel')])
    (out/(name+'-selective-receive.json')).write_text(json.dumps(data))
   links_coverage.render(out,'selective-receive');text=(out/'COVERAGE.md').read_text()
   self.assertIn('1/2 selected assertions pass; 1 failures',text)
   self.assertIn('[fail](swi-selective-receive.json)',text)
   self.assertIn('receive sentinel',text)
   self.assertNotIn('Server callbacks',text)
   self.assertNotIn('LM-006',text)

class ToplevelWaitCoverage(unittest.TestCase):
 def test_toplevel_failure_remains_visible(self):
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp)
   for name in ['swi','trealla']:
    failed=name=='trealla'
    data=dict(counts={'pass':int(not failed),'fail':int(failed)},results=[dict(id='TW-TEST',status='fail' if failed else 'pass',detail='toplevel sentinel')])
    (out/(name+'-toplevel-waits.json')).write_text(json.dumps(data))
   links_coverage.render(out,'toplevel-waits');text=(out/'COVERAGE.md').read_text()
   self.assertIn('1/2 selected assertions pass; 1 failures',text)
   self.assertIn('[fail](trealla-toplevel-waits.json)',text)
   self.assertIn('toplevel sentinel',text)
   self.assertNotIn('Server callbacks',text)

class LocalNamingCoverage(unittest.TestCase):
 def test_naming_failure_and_missing_cell_remain_visible(self):
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp)
   a=dict(counts={'pass':0,'fail':1},results=[dict(id='LN-TEST',status='fail',detail='naming sentinel')])
   b=dict(counts={'pass':0,'fail':0},results=[])
   for name,data in [('swi',a),('trealla',b)]:
    (out/(name+'-local-naming.json')).write_text(json.dumps(data))
   links_coverage.render(out,'local-naming');text=(out/'COVERAGE.md').read_text()
   self.assertIn('0/1 selected assertions pass; 1 failures',text)
   self.assertIn('| LN-TEST | [fail](swi-local-naming.json) | not measured |',text)
   self.assertIn('naming sentinel',text)
   self.assertNotIn('Server callbacks',text)

if __name__=='__main__':unittest.main()
