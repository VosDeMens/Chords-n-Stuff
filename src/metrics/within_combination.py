from src.combination import Combination
from src.metrics.metric import Metric
from src.voicing import Voicing


class WithinCombination(Metric):
    """Concerned with whether all `PitchClass`es in a `Voicing` are within a certain `Combination`.

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

    def setup(self, history: list[Voicing]) -> None:
        pass

    def _allows_partial(self, candidate: Voicing) -> bool:
        return candidate.fits(self.combination)

    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Voicing) -> float:
        return 0
