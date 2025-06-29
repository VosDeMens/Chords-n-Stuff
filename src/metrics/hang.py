from itertools import pairwise
from src.metrics.legal_notes import LegalNotes
from src.metrics.metric import Metric
from src.note import *
from src.distribution import Distribution


HANG_SMAM_NOTES: tuple[Note, list[Note]] = (D2, [A2, C3, E3, G3, C4, A3, F3, D3, Bf2])


class Hang(Metric):
    """Concerned with playability on the hang (instrument).

    Attributes
    ----------
    ding : Note
        The note of the ding (middle area of the hang).

    ring : list[Note]
        The notes in the ring, ordered going around the ring, such that two notes
        that are next to each other on the ring are next to each other in `self.ring`.

    require_pair : bool
        Requires that at least two notes are next to each other.

    Enforces
    --------
    - All notes in a candidate to be available on the hang (self.ding and self.ring).

    if require_pair:
        - Two notes from the distribution to be playable simultaneously with one hand.
    """

    def __init__(
        self,
        hang_notes: tuple[Note, list[Note]] = HANG_SMAM_NOTES,
        require_pair: bool = True,
    ):
        super().__init__(0)
        self.ding, self.ring = hang_notes
        self.legal_notes = LegalNotes([hang_notes[0]] + hang_notes[1])
        self.require_pair = require_pair

    def setup(self, history: list[Distribution]) -> None:
        pass

    def has_pair(self, candidate: Distribution) -> bool:
        if len(candidate) < 2:
            return False
        for note1, note2 in pairwise(self.ring + self.ring[:1]):
            if note1 in candidate and note2 in candidate:
                return True
        return False

    def _allows_partial(self, candidate: Distribution) -> bool:
        return self.legal_notes._allows_partial(candidate)  # type: ignore

    def _allows_complete_assuming_pruned(self, candidate: Distribution) -> bool:
        return not self.require_pair or self.has_pair(candidate)

    def _score_assuming_legal(self, candidate: Distribution) -> float:
        return 0


# TODO requires pair -> requires playability
# (twee- noten altijd goed, drie noten -> pair, vier noten -> twee pair, vijf+ -> nee)
