from src.combination import Combination
from src.metrics.metric import Metric
from src.distribution import Distribution


class WithinCombination(Metric):
    """Concerned with whether all `PitchClass`es in a `Distribution` are within a certain `Combination`.

    Attributes
    ----------
    combination : Combination
        The allowed `PitchClass`es.

    Enforces
    --------
    - No `Note`s in a candidate have a `PitchClass` outside of `combination`.
    """

    def __init__(self, combination: Combination):
        super().__init__(0)
        self.combination = combination

    def setup(self, history: list[Distribution]) -> None:
        pass

    def _allows_partial(self, candidate: Distribution) -> bool:
        return candidate.fits(self.combination)

    def _allows_complete_assuming_pruned(self, candidate: Distribution) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Distribution) -> float:
        return 0
