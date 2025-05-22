from typing import Iterable
from src.metrics.metric import Metric
from src.note import *
from src.voicing import Voicing


class LegalNotes(Metric):
    def __init__(self, legal_notes: Iterable[Note]):
        super().__init__(0)
        self.legal_notes = set(legal_notes)

    def setup(self, history: list[Voicing]) -> None:
        pass

    def _allows_partial(self, candidate: Voicing) -> bool:
        for note in candidate:
            if note not in self.legal_notes:
                return False
        return True

    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Voicing) -> float:
        return 0
