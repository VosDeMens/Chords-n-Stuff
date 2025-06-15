from src.metrics.metric import Metric
from src.distribution import Distribution


class NoDupNotes(Metric):
    """Concerned with just not having duplicate notes in a `Distribution`.

    Enforces
    --------
    No duplicate notes are in a candidate (for example C3 and C3, whereas havinf both C3 and C4 is allowed).
    """

    def __init__(self):
        super().__init__(0)

    def setup(self, history: list[Distribution]) -> None:
        pass

    def _allows_partial(self, candidate: Distribution) -> bool:
        return len(candidate) == len(set(candidate))

    def _allows_complete_assuming_pruned(self, candidate: Distribution) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Distribution) -> float:
        return 0
