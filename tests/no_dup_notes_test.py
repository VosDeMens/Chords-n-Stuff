import unittest

from src.shape import *
from src.metrics.no_dup_notes import NoDupNotes
from src.note import *
from src.voicing import Voicing


class NoDupNotesTest(unittest.TestCase):
    def test_prune(self):
        # setup
        no_dup_notes = NoDupNotes()
        C3_MAJOR = Voicing([C3, E3, G3])
        C3_MAJOR_dup = Voicing([C3, E3, E3])
        C3_MAJOR_oct = Voicing([C3, E3, C4])
        allowed = {C3_MAJOR, C3_MAJOR_dup, C3_MAJOR_oct}

        pruned = no_dup_notes.prune(allowed)

        # check
        self.assertIn(C3_MAJOR, pruned)
        self.assertIn(C3_MAJOR_oct, pruned)
        self.assertNotIn(C3_MAJOR_dup, pruned)
