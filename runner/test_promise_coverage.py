"""A successful diagnostic must not erase a required promise-pack failure."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]

class PromiseCoverage(unittest.TestCase):
 def test_failure_is_visible_even_when_all_diagnostics_succeed(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'diagnostics').mkdir()
   for caller in ['swi','trealla']:
    for peer in ['swi','trealla']:
     failed=caller=='trealla' and peer=='swi'
     row=dict(id='PY-TEST',status='fail' if failed else 'pass',detail='sentinel required failure')
     data=dict(counts={'pass':int(not failed),'fail':int(failed)},results=[row])
     (root/f'{caller}-promise-yield-to-{peer}.json').write_text(json.dumps(data))
     (root/f'{caller}-interop-http-to-{peer}.json').write_text(json.dumps(dict(counts={'pass':1,'fail':0},results=[{'status':'pass'}])))
     (root/'diagnostics'/f'{caller}-promise-diagnostics-to-{peer}.json').write_text(json.dumps(dict(counts={'observed':3,'diagnostic_error':0})))
   subprocess.run([sys.executable,str(ROOT/'runner/promise_coverage.py'),str(root)],check=True)
   text=(root/'COVERAGE.md').read_text()
   self.assertIn('3/4 assertions pass; 1 failures remain',text)
   self.assertIn('PY-TEST — trealla → swi',text)
   self.assertIn('sentinel required failure',text)
   self.assertIn('4/4 selections pass',text)

if __name__=='__main__':unittest.main()
