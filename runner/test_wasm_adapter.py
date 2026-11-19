"""Process isolation and runner exit status are part of WASM evidence."""
import json
import os
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
            module.write_text("let calls=0;"+("process.on('exit',()=>{process.exitCode=7});" if exit_after_report else '')+"exports.runExternalContractCases=async(mode,cases)=>{calls++;return cases.map(c=>({id:c.id,title:c.title,status:calls===1&&cases.length===1&&c.goal==='true'?'pass':'fail',duration_ms:1}))};")
            manifest=root/'manifest.json';manifest.write_text(json.dumps(dict(suite='fixture',scope='required',cases=[dict(id=str(i),title='fixture',goal='true') for i in range(2)])))
            report=root/'report.json'
            result=subprocess.run(['node',str(ROOT/'adapters/wasm.cjs'),str(root),'worker',str(manifest),str(report)],capture_output=True,text=True,timeout=10)
            self.assertTrue(report.exists(),result.stderr)
            return result,json.loads(report.read_text())
    def run_source_adapter(self, exit_after_report=False, one_failure=False):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            for file in ['web/vendor/swi-wasm-node.js','web/swi_wasm_actor_worker.js','web/swipl-bundle.js']:
                target=root/file;target.parent.mkdir(parents=True,exist_ok=True);target.write_text('// fixture')
            module=root/'modules/playwright/index.js';module.parent.mkdir(parents=True)
            stub="""
exports.chromium={launch:async()=>({
 newPage:async()=>({goto:async()=>{},close:async()=>{},evaluate:async(fn,arg)=>{
  if(typeof arg==='object'){
   if(arg.mode!=='worker'||arg.source!=='common.\\nprivate.')throw Error('missing source or wrong mode');
   return;
  }
  if(arg.includes('private_failure'))return {type:'failure',more:false};
  return {type:'success',more:false,data:[{LibraryCheck:'passed'}]};
 }}),close:async()=>{}
})};
"""
            if exit_after_report:stub+="process.on('exit',()=>{process.exitCode=7});"
            module.write_text(stub)
            cases=[dict(id='source',title='helper source',goal='private',source='private.')]
            if one_failure:cases.append(dict(id='failed',title='failed assertion',goal='private_failure',source='private.'))
            manifest=root/'manifest.json';manifest.write_text(json.dumps(dict(suite='fixture',source='common.',cases=cases)))
            report=root/'report.json'
            result=subprocess.run(['node',str(ROOT/'adapters/wasm.cjs'),str(root),'worker',str(manifest),str(report)],env=dict(os.environ,NODE_PATH=str(root/'modules')),capture_output=True,text=True,timeout=10)
            self.assertTrue(report.exists(),result.stderr)
            return result,json.loads(report.read_text())

    def test_source_cases_load_common_and_private_source_in_selected_session_mode(self):
        result,report=self.run_source_adapter();self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(report['counts']['pass'],1)
        self.assertEqual(report['results'][0]['candidate'],'swi-wasm-worker')

    def test_source_adapter_nonzero_exit_invalidates_passing_rows(self):
        result,report=self.run_source_adapter(True);self.assertNotEqual(result.returncode,0)
        self.assertEqual(report['counts']['fail'],1)
        self.assertIn('7',report['results'][0]['detail'])

    def test_assertion_failure_does_not_invalidate_other_source_case_passes(self):
        result,report=self.run_source_adapter(one_failure=True);self.assertEqual(result.returncode,1)
        self.assertEqual(report['counts']['pass'],1)
        self.assertEqual(report['counts']['fail'],1)

    def test_source_free_cases_run_in_fresh_processes(self):
        result,report=self.run_adapter();self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(report['counts']['pass'],2)
    def test_nonzero_process_cannot_supply_a_pass(self):
        result,report=self.run_adapter(True);self.assertEqual(result.returncode,1)
        self.assertEqual(report['counts']['fail'],2)
        self.assertTrue(all('7' in row['detail'] for row in report['results']))
if __name__=='__main__':unittest.main()
