import unittest

from src.combination import Combination
from src.cum_pattern import *
from src.metrics.within_combination import WithinCombination
from src.note import *
from src.pitch_class import *
from src.voicing import Voicing


class WithinCombinationTest(unittest.TestCase):
    def test_prune1(self):
        # setup
        diatonic_global = WithinCombination(Combination.from_cum(C, IONIAN))
        C3_MAJOR = Voicing([C3, E3, G3])
        MAJOR_CHORDS = {C3_MAJOR + d for d in range(12)}

        pruned = diatonic_global.prune(MAJOR_CHORDS)

        # check
        self.assertEqual(len(pruned), 3)
        self.assertIn(C3_MAJOR, pruned)
        self.assertIn(C3_MAJOR + 5, pruned)
        self.assertIn(C3_MAJOR + 7, pruned)
