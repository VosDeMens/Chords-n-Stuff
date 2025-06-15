import unittest

from src.cum_pattern import *
from src.metrics.legal_chord_changes import LegalChordChanges
from src.pitch_class import *
from src.note import *
from src.shape import *
from src.distribution import Distribution

V_F = Distribution([C4, F4, A4])
V_G = Distribution([B3, D4, G4])
V_D = Distribution([D4, Fs4, A4])
V_Fo = Distribution([C4, F4, C5])

VOICINGS = {V_F, V_G, V_D, V_Fo}


class LegalChordChangesTest(unittest.TestCase):
    def test_prune(self):
        # create
        chord_change_rules_1 = LegalChordChanges()
        chord_change_rules_1.add_rule(MAJOR, MAJOR, 5)
        chord_change_rules_1.add_rule(MAJOR, MAJOR, 7)
        chord_change_rules_1.add_rule(MINOR, MAJOR, 3)
        history_C = [Distribution([C4, E4, G4])]
        chord_change_rules_1.setup(history_C)
        F_G_ = chord_change_rules_1.prune(VOICINGS)

        chord_change_rules_1.optimise_pc_spread = False
        F_G_Fo_ = chord_change_rules_1.prune(VOICINGS)

        # check
        self.assertCountEqual(F_G_, [V_F, V_G])
        self.assertCountEqual(F_G_Fo_, [V_F, V_G, V_Fo])
