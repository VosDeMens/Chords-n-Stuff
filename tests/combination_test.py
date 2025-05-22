import unittest

from src.combination import Combination
from src.pitch_class import *
from src.cum_pattern import *


class CombinationTest(unittest.TestCase):
    def test_match(self):
        # create
        c = Combination.from_cum(C, MAJOR).match(MAJOR)
        cd = Combination.from_cum(C, CumPattern([0, 2, 4, 6, 7, 9])).match(MAJOR)

        # check
        self.assertCountEqual(c, [C])
        self.assertCountEqual(cd, [C, D])
