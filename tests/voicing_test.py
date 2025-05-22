import unittest

from src.note import *
from src.shape import *
from src.pitch_class import *
from src.voicing import Voicing


class VoicingTest(unittest.TestCase):
    def test_optimal(self):
        # setup
        C4_MAJOR = Voicing([C4, E4, G4])
        C4_MAJOR_OCT = Voicing([C4, E4, G4, C5])

        # raises
        with self.assertRaises(ValueError):
            C4_MAJOR.has_optimal_pc_spread(1)
        with self.assertRaises(ValueError):
            C4_MAJOR.has_optimal_pc_spread(2)
        with self.assertRaises(ValueError):
            C4_MAJOR_OCT.has_optimal_pc_spread(1)
        with self.assertRaises(ValueError):
            C4_MAJOR_OCT.has_optimal_pc_spread(2)

        # check
        self.assertTrue(C4_MAJOR.has_optimal_pc_spread(3))
        self.assertTrue(C4_MAJOR.has_optimal_pc_spread(4))
        self.assertTrue(C4_MAJOR_OCT.has_optimal_pc_spread(3))
        self.assertFalse(C4_MAJOR_OCT.has_optimal_pc_spread(4))
