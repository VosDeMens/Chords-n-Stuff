from src.metrics.metric import Metric
from src.voicing import Voicing


class NoDupNotes(Metric):
    def __init__(self):
        super().__init__(0)

    def setup(self, history: list[Voicing]) -> None:
        pass

    def _allows_partial(self, candidate: Voicing) -> bool:
        return len(candidate) == len(set(candidate))

    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Voicing) -> float:
        return 0
