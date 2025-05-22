from itertools import pairwise
from src.metrics.legal_notes import LegalNotes
from src.metrics.metric import Metric
from src.note import *
from src.voicing import Voicing


HANG_SMAM_NOTES: tuple[Note, list[Note]] = (D2, [A2, C3, E3, G3, C4, A3, F3, D3, Bf2])


class Hang(Metric):
    def __init__(
        self,
        hang_notes: tuple[Note, list[Note]] = HANG_SMAM_NOTES,
        require_pair: bool = True,
    ):
        super().__init__(0)
        self.ding, self.ring = hang_notes
        self.hang_notes = hang_notes
        self.legal_notes = LegalNotes([hang_notes[0]] + hang_notes[1])
        self.require_pair = require_pair

    def setup(self, history: list[Voicing]) -> None:
        pass

    def has_pair(self, candidate: Voicing) -> bool:
        if len(candidate) < 2:
            return False
        for note1, note2 in pairwise(self.ring + self.ring[:1]):
            if note1 in candidate and note2 in candidate:
                return True
        return False

    def _allows_partial(self, candidate: Voicing) -> bool:
        return self.legal_notes._allows_partial(candidate)  # type: ignore

    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool:
        return not self.require_pair or self.has_pair(candidate)

    def _score_assuming_legal(self, candidate: Voicing) -> float:
        return 0
