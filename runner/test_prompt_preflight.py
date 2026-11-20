"""Fixture failures cannot masquerade as executed prompt assertions."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import prompt_http


class PromptPreflight(unittest.TestCase):
    def test_probe_session_is_closed(self):
        with patch.object(prompt_http, 'post', side_effect=[
            dict(type='spawned', pid='probe'), dict(type='halted', pid='probe')]) as post:
            prompt_http.fixture_preflight('http://fixture')
        self.assertEqual([call.args[1] for call in post.call_args_list], ['spawn', 'halt'])

    def test_missing_routes_block_cases_and_fail_the_run(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)/'report.json'
            with patch('sys.argv', ['prompt_http', '--trealla', 'http://fixture', '--output', str(out)]), \
                 patch.object(prompt_http, 'fixture_preflight', side_effect=AssertionError('spawn: HTTP 404')), \
                 patch.object(prompt_http, 'check') as assertion, contextlib.redirect_stdout(io.StringIO()):
                code=prompt_http.main()
            report=json.loads(out.read_text())
        self.assertEqual(code,1)
        self.assertEqual(report['preconditions'][0]['status'],'error')
        self.assertEqual(len(report['results']),19)
        self.assertEqual({r['status'] for r in report['results']},{'blocked'})
        assertion.assert_not_called()

    def test_a_reachable_fixture_still_runs_and_can_fail_an_assertion(self):
        with patch('sys.argv',['prompt_http','--swi','http://fixture']), \
             patch.object(prompt_http,'fixture_preflight'), \
             patch.object(prompt_http,'MANIFEST') as manifest, \
             patch.object(prompt_http,'check',side_effect=AssertionError('bad prompt')), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            manifest.read_text.return_value=json.dumps(dict(suite='prompt-http',cases=[dict(id='PT-004')]))
            code=prompt_http.main()
        self.assertEqual(code,1)
        self.assertEqual(json.loads(output.getvalue())['results'][0]['status'],'fail')


if __name__=='__main__':
    unittest.main()
