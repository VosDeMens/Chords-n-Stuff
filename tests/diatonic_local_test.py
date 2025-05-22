import unittest

from src.shape import *
from src.metrics.diatonic_local import DiatonicLocal
from src.note import *
from src.voicing import Voicing


class DiatonicLocalTest(unittest.TestCase):
    def test_prune1(self):
        # setup
        diatonic_local = DiatonicLocal()
        C3_MAJOR = Voicing([C3, E3, G3])
        MAJOR_CHORDS = {C3_MAJOR + d for d in range(12)}

        history = [C3_MAJOR]
        diatonic_local.setup(history)

        pruned = diatonic_local.prune(MAJOR_CHORDS)

        # check
        self.assertEqual(len(pruned), 5)
        self.assertIn(C3_MAJOR, pruned)
        self.assertIn(C3_MAJOR + 2, pruned)
        self.assertIn(C3_MAJOR + 10, pruned)
        self.assertIn(C3_MAJOR + 5, pruned)
        self.assertIn(C3_MAJOR + 7, pruned)

    def test_prune2(self):
        # setup
        diatonic_local = DiatonicLocal(2)
        C3_MAJOR = Voicing([C3, E3, G3])
        MAJOR_CHORDS = {C3_MAJOR + d for d in range(12)}

        history = [C3_MAJOR + 7, C3_MAJOR, C3_MAJOR + 5]
        diatonic_local.setup(history)

        pruned = diatonic_local.prune(MAJOR_CHORDS)

        # check
        self.assertEqual(len(pruned), 4)
        self.assertIn(C3_MAJOR, pruned)
        self.assertIn(C3_MAJOR + 10, pruned)
        self.assertIn(C3_MAJOR + 5, pruned)
        self.assertIn(C3_MAJOR + 7, pruned)

    def test_score(self):
        # setup
        diatonic_local = DiatonicLocal(1)
        A2_MINOR = Voicing([A2, C3, E3])
        C3_MAJOR = Voicing([C3, E3, G3])
        Bf2_MAJOR = C3_MAJOR - 2
        F3_MAJOR = C3_MAJOR + 5
        G3_MAJOR = C3_MAJOR + 7
        Cs3_MAJOR = C3_MAJOR + 1
        Ef3_MAJOR = C3_MAJOR + 3

        history = [G3_MAJOR, A2_MINOR, C3_MAJOR, F3_MAJOR]
        diatonic_local.setup(history)

        # create
        outA = diatonic_local.score(A2_MINOR)
        outC = diatonic_local.score(C3_MAJOR)
        outBf = diatonic_local.score(Bf2_MAJOR)
        outF = diatonic_local.score(F3_MAJOR)
        outG = diatonic_local.score(G3_MAJOR)
        outCs = diatonic_local.score(Cs3_MAJOR)
        outEf = diatonic_local.score(Ef3_MAJOR)

        # check
        self.assertIsNotNone(outA)
        if outA is not None:
            self.assertAlmostEqual(outA, 1)

        self.assertIsNotNone(outC)
        if outC is not None:
            self.assertAlmostEqual(outC, 1)

        self.assertIsNotNone(outBf)
        if outBf is not None:
            self.assertAlmostEqual(outBf, 2 / 3)

        self.assertIsNotNone(outF)
        if outF is not None:
            self.assertAlmostEqual(outF, 1)

        self.assertIsNotNone(outG)
        if outG is not None:
            self.assertAlmostEqual(outG, 1)

        self.assertIsNone(outCs)

        self.assertIsNotNone(outEf)
        if outEf is not None:
            self.assertAlmostEqual(outEf, 0)
