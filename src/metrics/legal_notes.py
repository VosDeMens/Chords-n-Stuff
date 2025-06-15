from typing import Iterable
from src.metrics.metric import Metric
from src.note import *
from src.distribution import Distribution


class LegalNotes(Metric):
    """Concerned with which notes are allowed.

    Attributes
    ----------
    legal_notes : set[Note]
        All notes need to be in this set.

    Enforces
    --------
    - All notes in a candidate are in `legal_notes`.
    """

    def __init__(self, legal_notes: Iterable[Note]):
        super().__init__(0)
        self.legal_notes = set(legal_notes)

    def setup(self, history: list[Distribution]) -> None:
        pass

    def _allows_partial(self, candidate: Distribution) -> bool:
        for note in candidate:
            if note not in self.legal_notes:
                return False
        return True

    def _allows_complete_assuming_pruned(self, candidate: Distribution) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Distribution) -> float:
        return 0
