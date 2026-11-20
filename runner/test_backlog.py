"""Evidence decisions must be scoped and cannot turn incomplete work green."""
import json
import hashlib
from pathlib import Path
import tempfile
import unittest
from backlog import build, rows


class BacklogEvidence(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.write('reports/full/SUMMARY.json',dict(files=[dict(file='run.json',classification='public_live_observation',suites=['pack'],counts={'fail':2,'blocked':1})]))
        self.write('reports/full/verification.json',dict(coverage=[dict(suite='pack',cases=[dict(id='A',has_execution_observation=True),dict(id='B',has_execution_observation=False)])]))
        self.write('reports/full/run.json',dict(results=[dict(id='A',candidate='swi',status='fail'),dict(id='A',candidate='trealla',status='fail'),dict(id='B',candidate='swi',status='blocked')]))
        self.write('proof.json',dict(results=[dict(id='A',candidate='swi',status='pass')]))
        self.config=dict(source_report='reports/full',families=[],exclude_classification_prefixes=['out_of_scope'],decisions=[])

    def write(self,name,value):
        p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value))

    def decision(self):
        return dict(id='repair',selectors=[dict(case_id='A',candidate='swi')],set=dict(candidate_disposition='verified_not_deployed'),proofs=[dict(file='proof.json',selector=dict(case_id='A',candidate='swi'))])

    def test_candidate_repair_keeps_production_open_and_other_candidate_unchanged(self):
        self.config['decisions']=[self.decision()]
        data=build(self.root,self.config);a,b,c=data['observations']
        self.assertEqual(a['production_disposition'],'open')
        self.assertEqual(a['candidate_disposition'],'verified_not_deployed')
        self.assertNotIn('candidate_disposition',b)
        self.assertEqual(c['production_disposition'],'blocked_precondition')
        self.assertEqual(len(data['input_rows_without_execution']),1)

    def test_unrelated_or_failed_evidence_cannot_prove_a_repair(self):
        self.config['decisions']=[self.decision()]
        for value in [dict(id='other',status='pass'),dict(id='A',candidate='swi',status='fail')]:
            self.write('proof.json',dict(results=[value]))
            with self.assertRaises(ValueError):build(self.root,self.config)

    def test_review_rule_must_match_an_original_observation(self):
        d=self.decision();d['selectors']=[dict(case_id='missing')];self.config['decisions']=[d]
        with self.assertRaisesRegex(ValueError,'matches no original'):build(self.root,self.config)

    def test_exclusions_remain_auditable(self):
        p=self.root/'reports/full/SUMMARY.json';s=json.loads(p.read_text());s['files'][0]['classification']='out_of_scope_profile';self.write('reports/full/SUMMARY.json',s)
        d=build(self.root,self.config)
        self.assertEqual(d['observations'],[])
        self.assertEqual(len(d['excluded_observations']),3)
        self.assertIn('reports/full/run.json',d['inputs_sha256'])

    def test_observation_payloads_are_not_counted_as_test_results(self):
        result=list(rows(dict(candidate='swi',results=[dict(id='A',status='fail',observation=dict(id='nested',status='fail'))])))
        self.assertEqual(len(result),1)
        self.assertEqual(result[0][0],'/results/0')
        self.assertEqual(result[0][1]['candidate'],'swi')

    def test_modified_historical_report_is_rejected(self):
        report=self.root/'reports/full'
        hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in report.glob('*.json')}
        self.write('reports/full/files-sha256.json',hashes)
        self.write('reports/full/run.json',dict(results=[]))
        with self.assertRaisesRegex(ValueError,'hash mismatch'):build(self.root,self.config)


if __name__=='__main__':unittest.main()
