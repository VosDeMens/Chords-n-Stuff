from src.metrics.metric import Metric
from src.note import Note
from src.voicing import Voicing


class LegalRanges(Metric):
    def __init__(self, ranges: list[tuple[Note, Note]]):
        super().__init__(0)
        self.ranges = ranges

    def setup(self, history: list[Voicing]) -> None:
        pass

    def _allows_partial(self, candidate: Voicing) -> bool:
        if len(candidate) > len(self.ranges):
            raise ValueError
        for note, (min_note, max_note) in zip(candidate, self.ranges):
            if note < min_note or note > max_note:
                return False
        return True

    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Voicing) -> float:
        return 0
