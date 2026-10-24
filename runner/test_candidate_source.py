import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('local_promises',Path(__file__).resolve().parents[1]/'adapters/local_promises.py')
adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)

class CandidateSource(unittest.TestCase):
    def fixture(self,p):
        (p/'dependencies').mkdir();(p/'dependencies/swi-prolog-node.json').write_text(json.dumps({'revision':'pinned'}))
        for name in ['load.pl','pack.pl','prolog/web_prolog/node.pl']:
            f=p/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text('% fixture')
    def test_default_keeps_strict_checker(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.fixture(p)
            with patch.object(adapter.subprocess,'run') as run:
                out=adapter.validate_swi_source(p,p)
                run.assert_called_once();self.assertTrue(run.call_args.kwargs['check'])
                self.assertIn('--check',run.call_args.args[0])
                self.assertEqual(out['mode'],'strict pinned dependency')
    def test_explicit_candidate_records_pin_without_changing_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.fixture(p);pin=p/'dependencies/swi-prolog-node.json';before=pin.read_bytes()
            with patch.object(adapter,'git',return_value='pinned'),patch.object(adapter.subprocess,'run') as run:
                out=adapter.validate_swi_source(p,p,True);run.assert_not_called()
                self.assertEqual(out['mode'],'explicit working-tree candidate')
                self.assertEqual(out['pin_sha256'],adapter.sha(pin));self.assertEqual(pin.read_bytes(),before)
    def test_candidate_cannot_change_base_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.fixture(p)
            with patch.object(adapter,'git',return_value='other'):
                with self.assertRaisesRegex(ValueError,'unchanged pinned revision'):
                    adapter.validate_swi_source(p,p,True)

    def test_explicit_descendant_requires_exact_revision_and_ancestry(self):
        revision='a'*40
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.fixture(p)
            with patch.object(adapter,'git',side_effect=[revision,'']) as git:
                out=adapter.validate_swi_source(p,p,True,revision)
                self.assertEqual(out['candidate_base_revision'],revision)
                self.assertEqual(out['pin_revision'],'pinned')
                self.assertEqual(git.call_args.args[1:3],('merge-base','--is-ancestor'))
            with patch.object(adapter,'git',side_effect=[revision,adapter.subprocess.CalledProcessError(1,['git','merge-base'])]):
                with self.assertRaisesRegex(ValueError,'descend'):
                    adapter.validate_swi_source(p,p,True,revision)
    def test_revision_selection_is_not_an_implicit_bypass(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.fixture(p)
            with self.assertRaisesRegex(ValueError,'explicit candidate'):
                adapter.validate_swi_source(p,p,False,'a'*40)
            with patch.object(adapter,'git',return_value='a'*40):
                with self.assertRaisesRegex(ValueError,'full immutable'):
                    adapter.validate_swi_source(p,p,True,'HEAD')
                with self.assertRaisesRegex(ValueError,'explicitly selected revision'):
                    adapter.validate_swi_source(p,p,True,'b'*40)

if __name__=='__main__':unittest.main()
