"""Comparisons must preserve aliases, distinct variables and quoted text."""
import unittest
from baseline import unmet_requirement, variant_tokens
class TermFixtureComparisons(unittest.TestCase):
    def test_variants(self):
        self.assertEqual(variant_tokens('success([pair(X,X)], false).'),variant_tokens('success([pair(_123,_123)],false).'))
    def test_sharing_is_not_erased(self):
        self.assertNotEqual(variant_tokens('pair(X,X)'),variant_tokens('pair(X,Y)'))
    def test_anonymous_variables_are_distinct(self):
        self.assertEqual(variant_tokens('pair(_,_)'),variant_tokens('pair(X,Y)'))
    def test_quotes_are_not_variables_or_whitespace(self):
        self.assertNotEqual(variant_tokens("'A B'"),variant_tokens("'AB'"))
        self.assertNotEqual(variant_tokens("pair('X','X')"),variant_tokens('pair(X,X)'))
class CaseRequirements(unittest.TestCase):
    case=dict(id='X-1',transport='query',goal='true',requires=['goal_sandbox'])
    def test_sandboxed_candidate_runs_the_case(self):
        self.assertIsNone(unmet_requirement(self.case,'actor',{'goal_sandbox'}))
    def test_candidate_without_goal_sandbox_is_unsupported(self):
        self.assertEqual(unmet_requirement(self.case,'actor',set()),'requires goal_sandbox')
    def test_profile_is_checked_first(self):
        self.assertEqual(unmet_requirement(self.case,'isotope',set()),'requires actor')
    def test_unknown_requirement_is_an_error(self):
        with self.assertRaises(ValueError):unmet_requirement(dict(self.case,requires=['typo']),'actor',set())
if __name__=='__main__':unittest.main()
