"""Protocol/fixture regressions for the opt-in text draft, with no live nodes."""
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import portable_text as text
import run as actor
ROOT=Path(__file__).resolve().parents[1]

class FakeHarness:
    recv_type=actor.Harness.recv_type
    def __init__(self,events):self.events=iter(events);self.calls=[];self.sent=[];self.shell=None;self.halted=False
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def spawn_shell(self,options):self.options=options;self.shell=1234567890;return self.shell
    def call(self,goal,options):self.calls.append((goal,options))
    def recv(self,expected=None):
        event=next(self.events)
        if expected:actor.require(event['type']==expected,repr(event))
        return event
    def send(self,message):self.sent.append(message)
    def halt(self):self.halted=True;self.shell=None

def answer(text='[a,b]',more=False):return {'type':'success','data':[{'Text':text}],'more':more}

class PortableTextTests(unittest.TestCase):
    def setUp(self):self.manifest=json.loads((ROOT/'cases/portable-text-0.2.json').read_text())
    def run_case(self,case,events,**kwargs):
        h=FakeHarness(events)
        with patch.object(text.actor,'Harness',return_value=h):text.execute(None,case,**kwargs)
        return h
    def test_original_manifest_is_retained_as_prefix_metadata(self):
        old=json.loads((ROOT/'cases/portable-text-0.1.json').read_text())
        for before,after in zip(old['cases'],self.manifest['cases']):
            self.assertTrue(all(after[k]==v for k,v in before.items()))
    def test_full_pack_requires_declared_fixtures(self):
        with self.assertRaisesRegex(ValueError,'source-base'):text.validate(self.manifest,set())
        with self.assertRaisesRegex(ValueError,'peer'):text.validate(self.manifest,set(),source_base='http://127.0.0.1:1234')
        text.validate(self.manifest,set(),peer='http://127.0.0.1:1235',source_base='http://127.0.0.1:1234')
    def test_selected_local_cases_need_no_remote_fixture(self):
        text.validate(self.manifest,{'TXT-001','TXT-014'})
    def test_duplicate_ids_rejected(self):
        self.manifest['cases'].append(self.manifest['cases'][0])
        with self.assertRaisesRegex(ValueError,'duplicate'):text.validate(self.manifest,{'TXT-001'})
    def test_surrogate_metadata_rejected(self):
        self.manifest['cases'][0]['goal']='"\ud800"'
        with self.assertRaisesRegex(ValueError,'surrogate'):text.validate(self.manifest,{'TXT-001'})
    def test_fixture_credentials_rejected(self):
        with self.assertRaisesRegex(ValueError,'credentials'):text.validate(self.manifest,{'TXT-023'},peer='http://secret:password@example.org')
    def test_data_only_serializations(self):
        for rendered in ['[]','[a,b]', '"é😀"',r'"a\"\\b"',r"['\x1f600\','\\','\'']", "[e,'́']"]:
            self.assertTrue(text.safe_text_term(rendered),rendered)
        for rendered in ['[a],halt','[a].','(halt)','foo(a)','[a|b]','[]),halt,([]','[a/*comment*/]','"\ud800"']:
            self.assertFalse(text.safe_text_term(rendered),rendered)
    def test_round_trip_resubmits_original_spelling(self):
        rendered=r'"a\"\\b"'
        case={'execution':'round_trip','goal':'Text="x"','expected':'[x]'}
        h=self.run_case(case,[answer(rendered),answer()])
        self.assertEqual(h.calls[1][0],'('+rendered+')==([x])');self.assertTrue(h.halted)
    def test_unsafe_round_trip_cannot_be_executed(self):
        h=FakeHarness([answer('[a],halt')])
        with patch.object(text.actor,'Harness',return_value=h),self.assertRaises(actor.ConformanceFailure):
            text.execute(None,{'execution':'round_trip','goal':'Text="a"','expected':'[a]'})
        self.assertEqual(len(h.calls),1);self.assertTrue(h.halted)
    def test_more_and_query_failure_are_not_hidden(self):
        for event in [answer(more=True),{'type':'failure'},{'type':'error','details':'rejected'}]:
            h=FakeHarness([event])
            with patch.object(text.actor,'Harness',return_value=h),self.assertRaises(actor.ConformanceFailure):
                text.execute(None,{'execution':'goal','goal':'true'})
            self.assertTrue(h.halted)
    def test_constructed_list_is_sent_without_rewriting(self):
        clauses='[p([97,98]),q([a,b]),same(X,X)]'
        h=self.run_case({'execution':'source_list','clauses':clauses,'goal':'true'},[answer()])
        self.assertEqual(h.options,'[session(true),src_list('+clauses+')]')
    def test_source_payload_and_uri_fixture(self):
        h=self.run_case({'execution':'source_text','source':'p("ab").','goal':'true'},[answer()])
        self.assertIn("src_text('p(\"ab\").')",h.options)
        h=self.run_case({'execution':'source_uri','fixture':'portable-text.pl','goal':'true'},[answer()],source_base='http://127.0.0.1:1234/')
        self.assertIn("src_uri('http://127.0.0.1:1234/portable-text.pl')",h.options)
    def test_input_both_acknowledgement_orders(self):
        prompt={'type':'prompt','pid':1234567890,'data':'Portable text'}
        ack={'type':'responded'}
        for tail in [[ack,answer()],[answer(),ack]]:
            h=self.run_case({'execution':'input','reply':'"ab"','expected':'[a,b]'},[prompt]+tail)
            self.assertEqual(h.sent[0]['input'],'"ab"');self.assertTrue(h.halted)
    def test_input_failure_is_not_a_pass(self):
        events=[{'type':'prompt','pid':1234567890,'data':'Portable text'},{'type':'responded'},{'type':'failure'}]
        with self.assertRaises(actor.ConformanceFailure):self.run_case({'execution':'input','reply':'"ab"','expected':'[a,b]'},events)
    def test_peer_assertions_happen_on_peer(self):
        case=self.manifest['cases'][22]
        self.assertIn('pt_remote(T),T==[a,b]',case['goal'])
        h=self.run_case(case,[answer()],peer='http://127.0.0.1:1235')
        self.assertIn("rpc('http://127.0.0.1:1235'",h.calls[0][0]);self.assertNotIn('__PEER__',h.calls[0][0])

if __name__=='__main__':unittest.main()
