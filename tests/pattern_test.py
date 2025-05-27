import unittest

from src.pitch_class import *
from src.cum_pattern import *
from src.pattern import *


class PatternTest(unittest.TestCase):
    def test_contains(self):
        self.assertTrue(MAJOR.pattern in M7.pattern)
        self.assertTrue(MINOR.pattern in M7.pattern)
        self.assertFalse(DIM.pattern in M7.pattern)
        self.assertTrue(MAJOR.pattern in m7.pattern)
        self.assertTrue(MINOR.pattern in m7.pattern)
        self.assertFalse(DIM.pattern in m7.pattern)
        self.assertTrue(MAJOR.pattern in DOM7.pattern)
        self.assertTrue(DIM.pattern in DOM7.pattern)
        self.assertFalse(MINOR.pattern in DOM7.pattern)

    def test_get_normal_form(self):
        self.assertTupleEqual(
            get_normal_form_from_intervals_from_root((0, 4, 7)), (3, 5, 4)
        )
        self.assertTupleEqual(
            get_normal_form_from_intervals_from_root((1, 4, 7)), (3, 3, 6)
        )
        self.assertTupleEqual(get_normal_form_from_intervals_from_root(()), ())
        self.assertTupleEqual(get_normal_form_from_intervals_from_root((4,)), (12,))

    def test_from_intervals_from_root(self):
        self.assertEqual(Pattern.from_intervals_from_root((0, 4, 7)), MARY)
        self.assertEqual(Pattern.from_intervals_from_root((1, 5, 8)), MARY)
        self.assertEqual(Pattern.from_intervals_from_root((7, 0, 4)), MARY)
        self.assertEqual(Pattern.from_intervals_from_root((7, 12, 4)), MARY)
        self.assertEqual(Pattern.from_intervals_from_root((0, 16, -5)), MARY)
        self.assertEqual(Pattern.from_intervals_from_root((0, 3, 6)), DIMMY)
