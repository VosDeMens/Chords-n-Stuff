from src.metrics.metric import Metric
from src.note import Note
from src.distribution import Distribution


class LegalRanges(Metric):
    """Concerned with the allowed range of notes, but each index in a `Distribution` has its own range.

    Attributes
    ----------
    ranges : list[tuple[Note, Note]]
        A lower and upper bound per `Distribution` index.

    Enforces
    --------
    - All notes in a candidate are within their individual legal range.
    """

    def __init__(self, ranges: list[tuple[Note, Note]]):
        super().__init__(0)
        self.ranges = ranges

    def setup(self, history: list[Distribution]) -> None:
        pass

    def _allows_partial(self, candidate: Distribution) -> bool:
        if len(candidate) > len(self.ranges):
            raise ValueError
        for note, (min_note, max_note) in zip(candidate, self.ranges):
            if note < min_note or note > max_note:
                return False
        return True

    def _allows_complete_assuming_pruned(self, candidate: Distribution) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Distribution) -> float:
        return 0
