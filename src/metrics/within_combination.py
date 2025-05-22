from src.combination import Combination
from src.metrics.metric import Metric
from src.voicing import Voicing


class WithinCombination(Metric):
    def __init__(self, combination: Combination, weight: float = 1):
        super().__init__(weight)
        self.combination = combination

    def setup(self, history: list[Voicing]) -> None:
        pass

    def _allows_partial(self, candidate: Voicing) -> bool:
        return candidate.fits(self.combination)

    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Voicing) -> float:
        return 0
