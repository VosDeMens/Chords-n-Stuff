import unittest

from src.cum_pattern import *
from src.metrics.legal_chord_changes import LegalChordChanges
from src.pitch_class import *
from src.note import *
from src.shape import *
from src.voicing import Voicing

V_F = Voicing([C4, F4, A4])
V_G = Voicing([B3, D4, G4])
V_D = Voicing([D4, Fs4, A4])
V_Fd = Voicing([C4, C4, F4])
V_Fo = Voicing([C4, F4, C5])

VOICINGS = {V_F, V_G, V_D, V_Fd, V_Fo}


class LegalChordChangesTest(unittest.TestCase):
    def test_prune(self):
        # create
        chord_change_rules_1 = LegalChordChanges()
        chord_change_rules_1.add_rule(MAJOR, MAJOR, 5)
        chord_change_rules_1.add_rule(MAJOR, MAJOR, 7)
        chord_change_rules_1.add_rule(MINOR, MAJOR, 3)
        history_C = [Voicing([C4, E4, G4])]
        chord_change_rules_1.setup(history_C)
        F_G_ = chord_change_rules_1.prune(VOICINGS)

        chord_change_rules_1.optimise_pc_spread = False
        F_G_Fo_ = chord_change_rules_1.prune(VOICINGS)

        # check
        self.assertCountEqual(F_G_, [V_F, V_G])
        self.assertCountEqual(F_G_Fo_, [V_F, V_G, V_Fo, V_Fd])
