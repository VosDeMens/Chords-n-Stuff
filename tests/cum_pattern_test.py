import unittest

from src.cum_pattern import *
from src.shape import Shape


class CumPatternTest(unittest.TestCase):
    def test_cum_pattern_to_pattern(self):
        # create
        sus2_pattern = SUS2.pattern
        sus4_pattern = SUS4.pattern
        maj_octaved_pattern = Shape([0, 7, 16]).pattern

        # check
        self.assertEqual(sus2_pattern.intervals, (2, 5, 5))
        self.assertEqual(sus4_pattern.intervals, (2, 5, 5))
        self.assertEqual(maj_octaved_pattern.intervals, (3, 5, 4))
