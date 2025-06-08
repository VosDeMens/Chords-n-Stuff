from src.metrics.metric import Metric
from src.distribution import Distribution


class WithinOctave(Metric):
    """Concerned with the span of notes.

    Enforces
    --------
    - All notes in a candidate are within an octave.
    """

    def __init__(self):
        super().__init__(0)

    def setup(self, history: list[Distribution]) -> None:
        pass

    def _allows_partial(self, candidate: Distribution) -> bool:
        return max(candidate) - min(candidate) < 12

    def _allows_complete_assuming_pruned(self, candidate: Distribution) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Distribution) -> float:
        return 0
