import unittest

from src.cum_pattern import *
from src.metrics.legal_patterns import LegalPatterns
from src.note import *
from src.pattern import *
from src.shape import Shape
from src.distribution import Distribution


class PatternRulesTest(unittest.TestCase):
    def test_prune_1(self):
        # setup
        pattern_rules = LegalPatterns({MARY, MINNY})
        C3_MAJOR = Distribution.from_shape_and_root(C3, Shape(MAJOR))
        F3_MAJOR = Distribution.from_shape_and_root(F3, Shape(MAJOR))
        F3_MINOR = Distribution.from_shape_and_root(F3, Shape(MINOR))
        F3_DIM = Distribution.from_shape_and_root(F3, Shape(DIM))

        candidates = {C3_MAJOR, F3_MAJOR, F3_MINOR, F3_DIM}
        pruned = pattern_rules.prune(candidates)

        # check
        self.assertIn(C3_MAJOR, pruned)
        self.assertIn(F3_MAJOR, pruned)
        self.assertIn(F3_MINOR, pruned)
        self.assertNotIn(F3_DIM, pruned)

    def test_prune_2(self):
        # setup
        pattern_rules = LegalPatterns({M7.pattern})
        C3_MAJOR = Distribution.from_shape_and_root(C3, Shape(MAJOR))
        C3_M7 = Distribution.from_shape_and_root(C3, Shape(M7))
        C3_M9 = Distribution.from_shape_and_root(C3, Shape(M9))

        candidates = {C3_MAJOR, C3_M7, C3_M9}
        pruned = pattern_rules.prune(candidates)

        # check
        self.assertIn(C3_MAJOR, pruned)
        self.assertIn(C3_M7, pruned)
        self.assertNotIn(C3_M9, pruned)
