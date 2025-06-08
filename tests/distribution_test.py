import unittest

from src.combination import Combination
from src.cum_pattern import *
from src.note import *
from src.shape import *
from src.pitch_class import *
from src.distribution import Distribution


class DistributionTest(unittest.TestCase):
    def test_optimal(self):
        # setup
        C4_MAJOR = Distribution([C4, E4, G4])
        C4_MAJOR_OCT = Distribution([C4, E4, G4, C5])

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

    def test_fits(self):
        # setup
        C4_MAJOR = Distribution([C4, E4, G4])
        C4_MAJOR_OCT = Distribution([C4, E4, G4, C5])
        C4_MAJOR_OCT_ = Distribution([C3, C4, E4, G4, C5])

        # check
        self.assertTrue(C4_MAJOR.fits(Combination.from_cum(C, MAJOR)))
        self.assertTrue(C4_MAJOR.fits(Combination.from_cum(C, MAJOR), True))
        self.assertTrue(C4_MAJOR_OCT.fits(Combination.from_cum(C, MAJOR)))
        self.assertTrue(C4_MAJOR_OCT.fits(Combination.from_cum(C, MAJOR), True))
        self.assertTrue(C4_MAJOR_OCT_.fits(Combination.from_cum(C, MAJOR)))
        self.assertFalse(C4_MAJOR_OCT_.fits(Combination.from_cum(C, MAJOR), True))

        self.assertFalse(C4_MAJOR.fits(Combination.from_cum(C, MINOR)))
        self.assertFalse(C4_MAJOR_OCT.fits(Combination.from_cum(C, MINOR)))
        self.assertFalse(C4_MAJOR_OCT_.fits(Combination.from_cum(C, MINOR)))
