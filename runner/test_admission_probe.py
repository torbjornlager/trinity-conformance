import unittest
from unittest.mock import patch
import admission_probe

class FakeSocket:
    def __init__(self,*args):
        self.events=iter([
            {'type':'transport_welcome'}, {'type':'spawned','pid':1234567890},
            {'type':'error','details':'error(instantiation_error,_)'},
            {'type':'success','data':[{'ProbeEntry':'no'}],'more':False},
            {'type':'halted'}])
    def send_json(self,command): pass
    def recv_json(self): return next(self.events)
    def close(self): pass

class AdmissionCapture(unittest.TestCase):
    @patch.object(admission_probe.actor,'WebSocket',FakeSocket)
    def test_outer_error_is_observed_with_complete_transcript_not_pass(self):
        result=admission_probe.observe({'goal':'supervisor_spawn(Specs,P)'},'ws://fixture/ws',1,None)
        self.assertTrue(result['complete'])
        self.assertFalse(result['execution_entered'])
        self.assertEqual(result['terminal']['type'],'error')
        calls=[x['message'] for x in result['transcript'] if x['direction']=='send' and x['message']['command']=='toplevel_call']
        self.assertIn('supervisor_spawn(Specs,P)',calls[0]['goal'])
        self.assertIn('ProbeEntry',calls[1]['goal'])
        self.assertNotIn('writeln',calls[0]['goal'])
        self.assertEqual(len(result['transcript']),10)
    @patch.object(admission_probe.actor,'WebSocket',side_effect=TimeoutError('sentinel'))
    def test_transport_failure_remains_incomplete(self,mock):
        result=admission_probe.observe({'goal':'true'},'ws://fixture/ws',1,None)
        self.assertFalse(result['complete'])
        self.assertIn('sentinel',result['probe_error'])

class DiagnosticScope(unittest.TestCase):
    def test_required_pack_cannot_use_observation_transport(self):
        import baseline,json,tempfile,sys,contextlib,io
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);manifest=p/'case.json';report=p/'report.json'
            manifest.write_text(json.dumps(dict(suite='probe',scope='required',cases=[dict(id='probe',title='probe',transport='admission',goal='true')])))
            argv=['baseline','--manifest',str(manifest),'--url','ws://fixture/ws','--candidate','fixture','--profile','actor','--report',str(report)]
            with patch.object(sys,'argv',argv),patch.object(admission_probe,'observe') as observe,contextlib.redirect_stdout(io.StringIO()):
                self.assertTrue(baseline.main())
                observe.assert_not_called()
            row=json.loads(report.read_text())['results'][0]
            self.assertEqual(row['status'],'fail')
            self.assertIn('diagnostic scope',row['detail'])

if __name__=='__main__':unittest.main()

