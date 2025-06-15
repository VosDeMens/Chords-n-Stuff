from src.metrics.metric import Metric
from src.note import Note
from src.distribution import Distribution


class LegalRange(Metric):
    """Concerned with the allowed range of notes.

    Attributes
    ----------
    lower_bound : Note
        No notes can be lower than this note (but can be as low as this note).
    upper_bound : Note
        No notes can be higher than this note (but can be as high as this note).

    Enforces
    --------
    - All notes in a candidate are within the legal range.
    """

    def __init__(self, lower_bound: Note, upper_bound: Note):
        super().__init__(0)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def setup(self, history: list[Distribution]) -> None:
        pass

    def _allows_partial(self, candidate: Distribution) -> bool:
        return all(self.lower_bound <= note <= self.upper_bound for note in candidate)

    def _allows_complete_assuming_pruned(self, candidate: Distribution) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Distribution) -> float:
        return 0
