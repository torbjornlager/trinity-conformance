"""Comparisons must preserve aliases, distinct variables and quoted text."""
import unittest
from baseline import variant_tokens
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
if __name__=='__main__':unittest.main()
