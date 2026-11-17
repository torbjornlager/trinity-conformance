import copy
import unittest
from unittest.mock import patch

from library_prefix import http_prefix, prefix_spec, session_prefix


class ScriptedSession:
    shell = 1234567890

    def __init__(self, events):
        self.events = iter(events)
        self.commands = []

    def call(self, goal, options):
        self.commands.append(('call', goal, options))

    def next(self):
        self.commands.append(('next',))

    def send(self, command):
        self.commands.append(('send', command))

    def recv_type(self, expected, **kwargs):
        event = next(self.events)
        if event['type'] != expected:
            raise AssertionError(event)
        return event


class LibraryPrefixTests(unittest.TestCase):
    def setUp(self):
        self.case = dict(goal='generated(LibraryCheck)', bounded_prefix=dict(page_size=3, pages=2, first=1))
        self.events = [dict(type='success', more=True, data=[dict(LibraryCheck=str(n)) for n in ns])
                       for ns in ([1, 2, 3], [4, 5, 6])]
        self.events += [dict(type='stop'), dict(type='success', more=False, data=[dict(LibraryRecovered='passed')])]

    def test_pages_then_stop_then_same_session_recovery(self):
        session = ScriptedSession(self.events)
        self.assertEqual(session_prefix(self.case, session), self.events)
        self.assertEqual(session.commands, [
            ('call', 'generated(LibraryCheck)', '[limit(3)]'), ('next',),
            ('send', dict(command='toplevel_stop', pid=session.shell)),
            ('call', 'LibraryRecovered=passed', '[limit(1)]')])

    def test_missing_repeated_or_reordered_answers_cannot_pass(self):
        for values in ([1, 2], [1, 2, 2], [2, 1, 3]):
            events = [dict(type='success', more=True, data=[dict(LibraryCheck=str(v)) for v in values]), dict(type='stop')]
            session = ScriptedSession(events)
            with self.assertRaisesRegex(AssertionError, 'ordered prefix'):
                session_prefix(self.case, session)
            self.assertEqual(session.commands[-1][1]['command'], 'toplevel_stop')

    def test_exhaustion_or_failed_recovery_cannot_pass(self):
        for index in (0, 3):
            events = copy.deepcopy(self.events)
            if index == 0:
                events[index]['more'] = False
                events = events[:1] + [dict(type='stop')]
            else:
                events[index]['more'] = True
            with self.assertRaises(AssertionError):
                session_prefix(self.case, ScriptedSession(events))

    def test_http_checks_two_offsets_and_service_recovery(self):
        with patch('library_prefix.http_case', return_value=['observed']) as execute:
            self.assertEqual(http_prefix(self.case, 'source.', 'http://fixture'), ['observed'])
        requests = execute.call_args.args[0]['requests']
        self.assertEqual([r['params'].get('offset') for r in requests], [0, 3, None])
        self.assertEqual([r['expect_prolog'] for r in requests], [
            'success([1,2,3],true).', 'success([4,5,6],true).', 'success([passed],false).'])

    def test_invalid_unbounded_or_boolean_limits_are_rejected(self):
        for key, value in [('page_size', 0), ('page_size', 1000000), ('pages', 0), ('pages', True), ('first', 2)]:
            case = copy.deepcopy(self.case)
            case['bounded_prefix'][key] = value
            with self.assertRaisesRegex(ValueError, 'bounded'):
                prefix_spec(case)


if __name__ == '__main__':
    unittest.main()
