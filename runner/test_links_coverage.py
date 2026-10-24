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

if __name__=='__main__':unittest.main()
