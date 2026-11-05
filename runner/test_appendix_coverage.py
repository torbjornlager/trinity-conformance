import hashlib,json,tempfile,unittest
from pathlib import Path
from appendix_coverage import validate

class CoverageEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.manual=self.root/'manual.tex';self.manual.write_text('capabilities\n')
        sha=hashlib.sha256(self.manual.read_bytes()).hexdigest()
        self.data={'source':{'sha256':sha},'targets':{'swi':'local APIs'},'requirements':[{'id':'B-1','minimum_profile':'isobase','source':{'start':1,'end':1,'sha256':sha},'targets':{'swi':{'status':'verified','evidence':[{'report':'run.json','candidate':'swi','cases':['RT-1']}]}}}]}
        self.report={'results':[{'id':'RT-1','candidate':'swi','status':'pass'}]};self.save()
    def save(self): (self.root/'run.json').write_text(json.dumps(self.report))
    def test_verified_requires_exact_passing_case(self):
        self.assertEqual(validate(self.data,self.manual,self.root)['swi'],{'verified':1})
        self.report['results'][0]['status']='fail';self.save()
        with self.assertRaisesRegex(ValueError,'non-passing'):validate(self.data,self.manual,self.root)
    def test_missing_case_cannot_be_counted(self):
        self.report['results']=[];self.save()
        with self.assertRaisesRegex(ValueError,'missing or duplicate'):validate(self.data,self.manual,self.root)
    def test_duplicate_case_cannot_be_counted(self):
        self.report['results']*=2;self.save()
        with self.assertRaisesRegex(ValueError,'missing or duplicate'):validate(self.data,self.manual,self.root)
    def test_other_target_cannot_supply_evidence(self):
        self.data['requirements'][0]['targets']['swi']['evidence'][0]['candidate']='gnu'
        with self.assertRaisesRegex(ValueError,'wrong target'):validate(self.data,self.manual,self.root)
    def test_document_drift_requires_review(self):
        self.manual.write_text('different capabilities\n')
        with self.assertRaisesRegex(ValueError,'Appendix B changed'):validate(self.data,self.manual,self.root)
    def test_no_evidence_or_profile_waiver_cannot_turn_green(self):
        cell=self.data['requirements'][0]['targets']['swi'];cell['evidence']=[]
        with self.assertRaisesRegex(ValueError,'execution evidence'):validate(self.data,self.manual,self.root)
        cell['status']='not_applicable'
        with self.assertRaisesRegex(ValueError,'waiver'):validate(self.data,self.manual,self.root)
    def test_known_failure_requires_a_failed_observation(self):
        self.data['requirements'][0]['targets']['swi']['status']='failing'
        with self.assertRaisesRegex(ValueError,'observed failure'):validate(self.data,self.manual,self.root)
        self.report['results'][0]['status']='fail';self.save()
        self.assertEqual(validate(self.data,self.manual,self.root)['swi'],{'failing':1})

if __name__=='__main__':unittest.main()
