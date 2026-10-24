import json
import tempfile
from pathlib import Path
import unittest
import admission_coverage

class AdmissionMatrix(unittest.TestCase):
    def test_observed_error_is_not_called_pass_and_missing_stays_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);manifest=p/'manifest.json'
            manifest.write_text(json.dumps({'cases':[{'id':'AP-X','pair':'control','variant':'runtime'}]}))
            a={'results':[{'id':'AP-X','status':'observed','observation':{'complete':True,'execution_entered':False,'terminal':{'type':'error'}}}]}
            for name,data in [('swi',a),('trealla',{'results':[]})]:
                (p/(name+'-admission-paths.json')).write_text(json.dumps(data))
            admission_coverage.render(p,manifest);text=(p/'DIAGNOSTICS.md').read_text()
            self.assertIn('No conformance passes are assigned',text)
            self.assertIn('error; before entry',text)
            self.assertIn('not measured',text)
    def test_incomplete_and_bound_pattern_are_not_normalized_away(self):
        row={'status':'diagnostic_error','detail':'sentinel timeout'}
        self.assertIn('INCOMPLETE: sentinel timeout',admission_coverage.summary(row))
        row={'status':'observed','observation':{'complete':True,'execution_entered':True,'terminal':{'type':'success','data':[{'PatternState':'bound(child(_,_))','Reply':'not_dispatched'}]}}}
        text=admission_coverage.summary(row)
        self.assertIn('pattern already bound',text)
        self.assertIn('not_dispatched',text)

    def test_outer_option_error_is_distinguished_from_source_failure(self):
        def row(details):
            return {'status':'observed','observation':{'complete':True,'execution_entered':False,'terminal':{'type':'error','details':details}}}
        self.assertIn('spawn_option error',admission_coverage.summary(row('error(domain_error(spawn_option,unknown(x)),_)')))
        self.assertIn('source socket error',admission_coverage.summary(row('error(socket_error(eai_noname,x),_)')))
        self.assertIn('before entry',admission_coverage.summary(row('error(domain_error(spawn_option,x),_)')))

if __name__=='__main__':unittest.main()
