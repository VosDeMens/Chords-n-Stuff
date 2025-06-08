import unittest

from src.pattern import *
from src.cum_pattern import *
from src.shape import Shape


class CumPatternTest(unittest.TestCase):
    def test_to_pattern(self):
        self.assertEqual(SUS2.pattern, SUZY)
        self.assertEqual(SUS4.pattern, SUZY)
        self.assertEqual(Shape([0, 7, 16]).pattern, MARY)

    def test_addition(self):
        self.assertEqual(SUS2 + SUS4, SUS2 + 5)
        self.assertEqual(SUS2 + SUS4, SUS4 + 2)
        self.assertEqual(SUS2 + SUS4, SUS2SUS4)
        self.assertEqual(MAJOR + MINOR, MINOR + 4)
        self.assertEqual(MAJOR + MINOR, MAJOR + 3)
        self.assertEqual(MAJOR + MINOR, CumPattern((0, 3, 4, 7)))

    def test_shift(self):
        self.assertEqual(SUS2 << 7, SUS4)
        self.assertEqual(SUS2 >> 5, SUS4)
        self.assertEqual(SUS2 >> -7, SUS4)

    def test_equal(self):
        self.assertNotEqual(MAJOR, MINOR)
