"""Process isolation and runner exit status are part of WASM evidence."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
@unittest.skipUnless(shutil.which('node'),'Node.js is required')
class WasmAdapterTests(unittest.TestCase):
    def run_adapter(self,exit_after_report=False):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);module=root/'tests/wasm/swi_wasm_contracts.js';module.parent.mkdir(parents=True)
            module.write_text("let calls=0;"+("process.on('exit',()=>{process.exitCode=7});" if exit_after_report else '')+"exports.runExternalContractCases=async(mode,cases)=>{calls++;return cases.map(c=>({id:c.id,title:c.title,status:calls===1&&cases.length===1&&c.source==='fixture.'?'pass':'fail',duration_ms:1}))};")
            manifest=root/'manifest.json';manifest.write_text(json.dumps(dict(suite='fixture',scope='required',cases=[dict(id=str(i),title='fixture',goal='true',source='fixture.') for i in range(2)])))
            report=root/'report.json'
            result=subprocess.run(['node',str(ROOT/'adapters/wasm.cjs'),str(root),'worker',str(manifest),str(report)],capture_output=True,text=True,timeout=10)
            return result,json.loads(report.read_text())
    def test_cases_run_in_fresh_processes_and_retain_source(self):
        result,report=self.run_adapter();self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(report['counts']['pass'],2)
    def test_nonzero_process_cannot_supply_a_pass(self):
        result,report=self.run_adapter(True);self.assertEqual(result.returncode,1)
        self.assertEqual(report['counts']['fail'],2)
        self.assertTrue(all('7' in row['detail'] for row in report['results']))
if __name__=='__main__':unittest.main()
