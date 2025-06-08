import unittest

from src.shape import *
from src.metrics.no_combination_reps import NoCombinationReps
from src.note import *
from src.distribution import Distribution


class NoCombinationRepsTest(unittest.TestCase):
    def test_prune(self):
        # setup
        no_combination_reps = NoCombinationReps(2)
        C3_MAJOR = Distribution([C3, E3, G3])
        F3_MAJOR = Distribution([F3, A3, C4])
        G3_MAJOR = Distribution([G3, B3, D4])
        C4_MAJOR = Distribution([C4, E4, G4])

        history = [G3_MAJOR, F3_MAJOR, C3_MAJOR]
        no_combination_reps.setup(history)

        # create
        candidates = {C3_MAJOR, F3_MAJOR, G3_MAJOR, C4_MAJOR}
        pruned_candidates = no_combination_reps.prune(candidates)

        # check
        self.assertNotIn(C3_MAJOR, pruned_candidates)
        self.assertNotIn(F3_MAJOR, pruned_candidates)
        self.assertIn(G3_MAJOR, pruned_candidates)
        self.assertNotIn(C4_MAJOR, pruned_candidates)

    def test_score(self):
        # setup
        no_combination_reps = NoCombinationReps(2)
        C3_MAJOR = Distribution([C3, E3, G3])
        F3_MAJOR = Distribution([F3, A3, C4])
        G3_MAJOR = Distribution([G3, B3, D4])

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
