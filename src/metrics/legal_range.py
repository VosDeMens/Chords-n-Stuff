from src.metrics.metric import Metric
from src.note import Note
from src.voicing import Voicing


class LegalRange(Metric):
    def __init__(self, lower_bound: Note, upper_bound: Note):
        super().__init__(0)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def setup(self, history: list[Voicing]) -> None:
        pass

    def _allows_partial(self, candidate: Voicing) -> bool:
        return all(self.lower_bound <= note <= self.upper_bound for note in candidate)

    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Voicing) -> float:
        return 0
