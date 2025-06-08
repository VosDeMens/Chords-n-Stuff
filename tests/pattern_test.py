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
