import unittest

from src.shape import *
from src.metrics.no_combination_reps import NoCombinationReps
from src.note import *
from src.voicing import Voicing


class NoCombinationRepsTest(unittest.TestCase):
    def test_score(self):
        # setup
        no_combination_reps = NoCombinationReps(2)
        C3_MAJOR = Voicing([C3, E3, G3])
        F3_MAJOR = Voicing([F3, A3, C4])
        G3_MAJOR = Voicing([G3, B3, D4])

        history = [F3_MAJOR, C3_MAJOR, C3_MAJOR, C3_MAJOR]
        no_combination_reps.setup(history)

        # create
        out1 = no_combination_reps.score_assuming_pruned(C3_MAJOR)
        out2 = no_combination_reps.score_assuming_pruned(F3_MAJOR)
        out3 = no_combination_reps.score_assuming_pruned(G3_MAJOR)

        # check
        self.assertIsNone(out1)
        self.assertIsNotNone(out2)
        if out2 is not None:
            self.assertAlmostEqual(out2, 1 / 2)
        self.assertIsNotNone(out3)
        if out3 is not None:
            self.assertAlmostEqual(out3, 1)
