from itertools import pairwise
from src.metrics.metric import Metric
from src.voicing import Voicing


class InternalIntervalRange(Metric):
    """Concerned with the intervals between notes in a `Voicing`.

    Attributes
    ----------
    min_internal : int
        Smallest allowed internal interval.

    max_interval : int
        Biggest allowed internal interval.

    Enforces
    --------
    - Any interval between two adjacent notes (sorted) in a candidate to be within the legal range.
    """

    def __init__(self, min_internal: int, max_internal: int):
        super().__init__(0)
        self.min_internal = min_internal
        self.max_internal = max_internal

    def setup(self, history: list[Voicing]) -> None:
        pass

    def _allows_partial(self, candidate: Voicing) -> bool:
        for note1, note2 in pairwise(sorted(candidate.notes)):
            d = note2 - note1
            if d < self.min_internal or d > self.max_internal:
                return False
        return True

    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Voicing) -> float:
        return 0
