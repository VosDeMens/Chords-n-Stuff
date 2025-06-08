import unittest

from src.combination import Combination
from src.cum_pattern import *
from src.note import *
from src.shape import *
from src.pitch_class import *
from src.voicing import Voicing


class VoicingTest(unittest.TestCase):
    def test_notes(self):
        self.assertCountEqual(Voicing(notes := [C3, E3, G3]).notes, notes)
        self.assertCountEqual(Voicing(notes := [C4, E3, G3]).notes, notes)
        self.assertCountEqual(Voicing(notes := [C3, D1, G3]).notes, notes)

    def test_fits(self):
        # setup
        C4_MAJOR = Voicing([C4, E4, G4])
        C4_MAJOR_OCT = Voicing([C4, E4, G4, C5])
        C4_MAJOR_OCT_ = Voicing([C3, C4, E4, G4, C5])

        # check
        self.assertTrue(C4_MAJOR.fits(Combination.from_cum(C, MAJOR)))
        self.assertTrue(C4_MAJOR_OCT.fits(Combination.from_cum(C, MAJOR)))
        self.assertTrue(C4_MAJOR_OCT_.fits(Combination.from_cum(C, MAJOR)))

        self.assertFalse(C4_MAJOR.fits(Combination.from_cum(C, MINOR)))
        self.assertFalse(C4_MAJOR_OCT.fits(Combination.from_cum(C, MINOR)))
        self.assertFalse(C4_MAJOR_OCT_.fits(Combination.from_cum(C, MINOR)))
