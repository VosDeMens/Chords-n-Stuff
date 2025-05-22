from src.metrics.metric import Metric
from src.voicing import Voicing


class WithinOctave(Metric):
    def __init__(self):
        super().__init__(0)

    def setup(self, history: list[Voicing]) -> None:
        pass

    def _allows_partial(self, candidate: Voicing) -> bool:
        return max(candidate) - min(candidate) <= 12

    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Voicing) -> float:
        return 0
