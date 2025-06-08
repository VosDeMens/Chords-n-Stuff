import unittest

from src.shape import *
from src.metrics.individual_steps import IndividualSteps
from src.note import *
from src.distribution import Distribution


class IndividualStepsTest(unittest.TestCase):

    def test_get_allowed(self):
        # setup
        individual_steps = IndividualSteps(0, 2, 1)
        C3_MAJOR = Distribution([C3, E3, G3])

        history = [C3_MAJOR]
        individual_steps.setup(history)

        allowed = individual_steps.get_allowed()

        # check
        self.assertEqual(len(allowed), 125)

    def test_prune1(self):
        # setup
        individual_steps = IndividualSteps(0, 2, 1)
        C3_MAJOR = Distribution([C3, E3, G3])
        F3_MAJOR = Distribution([C3, F3, A3])
        G3_MAJOR = Distribution([G3, B3, D4])

        history = [C3_MAJOR]
        individual_steps.setup(history)

        pruned = individual_steps.prune({C3_MAJOR, F3_MAJOR, G3_MAJOR})

        # check
        self.assertIn(C3_MAJOR, pruned)
        self.assertIn(F3_MAJOR, pruned)
        self.assertNotIn(G3_MAJOR, pruned)

    def test_prune2(self):
        # setup
        individual_steps = IndividualSteps(1, 2, 1)
        C3_MAJOR = Distribution([C3, E3, G3])
        F3_MAJOR = Distribution([C3, F3, A3])
        G3_MAJOR = Distribution([G3, B3, D4])

        history = [C3_MAJOR]
        individual_steps.setup(history)

        pruned = individual_steps.prune({C3_MAJOR, F3_MAJOR, G3_MAJOR})

        # check
        self.assertNotIn(C3_MAJOR, pruned)
        self.assertNotIn(F3_MAJOR, pruned)
        self.assertNotIn(G3_MAJOR, pruned)

    def test_score(self):
        # setup
        individual_steps = IndividualSteps(0, 3, 1)
        C3_MAJOR = Distribution([C3, E3, G3])
        F3_MAJOR = Distribution([C3, F3, A3])
        G3_MAJOR = Distribution([G3, B3, D4])
        A2_MAJOR = Distribution([A2, Cs3, E3])

        history = [C3_MAJOR]
        individual_steps.setup(history)

        # create
        outC = individual_steps.score(C3_MAJOR)
        outF = individual_steps.score(F3_MAJOR)
        outG = individual_steps.score(G3_MAJOR)
        outA = individual_steps.score(A2_MAJOR)

        # check
        self.assertIsNotNone(outC)
        if outC is not None:
            self.assertAlmostEqual(outC, 1 / 2)
        self.assertIsNotNone(outF)
        if outF is not None:
            self.assertAlmostEqual(outF, 2 / 3)
        self.assertIsNone(outG)
        self.assertIsNotNone(outA)
        if outA is not None:
            self.assertAlmostEqual(outA, 0)
