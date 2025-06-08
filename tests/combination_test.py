import unittest

from src.pattern import *
from src.combination import Combination
from src.pitch_class import *
from src.cum_pattern import *


class CombinationTest(unittest.TestCase):
    C_MAJOR = Combination.from_cum(C, MAJOR)
    C_M7 = Combination.from_cum(C, M7)
    D_MAJOR = Combination.from_cum(D, MAJOR)
    C_MAJOR_D_MAJOR = Combination.from_cum(C, CumPattern([0, 2, 4, 6, 7, 9]))

    def test_from_cum(self):
        self.assertEqual(
            Combination.from_cum(C, MAJOR).bitmask,
            int16(1) << int16(0) | int16(1) << int16(4) | int16(1) << int16(7),
        )
        self.assertEqual(
            Combination.from_cum(D, MAJOR).bitmask,
            int16(1) << int16(2) | int16(1) << int16(6) | int16(1) << int16(9),
        )
        self.assertEqual(
            Combination.from_cum(C, MINOR).bitmask,
            int16(1) << int16(0) | int16(1) << int16(3) | int16(1) << int16(7),
        )
        self.assertEqual(
            Combination.from_cum(D, MINOR).bitmask,
            int16(1) << int16(2) | int16(1) << int16(5) | int16(1) << int16(9),
        )

    def test_match(self):
        # create
        c = self.C_MAJOR.match(MAJOR)
        cd = self.C_MAJOR_D_MAJOR.match(MAJOR)

        # check
        self.assertCountEqual(c, [C])
        self.assertCountEqual(cd, [C, D])

    def test_to_pattern(self):
        # create
        mary = self.C_MAJOR.pattern
        _222123 = self.C_MAJOR_D_MAJOR.pattern

        # check
        self.assertEqual(mary, MARY)
        self.assertEqual(_222123, Pattern([2, 2, 2, 1, 2, 3]))

    def test_addition(self):
        self.assertEqual(self.C_MAJOR + B, self.C_M7)
        self.assertEqual(self.C_MAJOR + self.D_MAJOR, self.C_MAJOR_D_MAJOR)

    def test_fits(self):
        self.assertTrue(self.C_MAJOR.fits(MARY))
        self.assertTrue(self.C_MAJOR.fits(M7.pattern))
        self.assertFalse(self.C_MAJOR.fits(MINNY))
