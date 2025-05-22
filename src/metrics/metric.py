from abc import ABC, abstractmethod

from src.profiler import TimingMeta
from src.voicing import Voicing


class Metric(ABC, metaclass=TimingMeta):
    def __init__(self, weight: float):
        self.weight = weight

    # once, start of cycle
    @abstractmethod
    def setup(self, history: list[Voicing]) -> None: ...

    # note by note
    def prune(self, candidates: set[Voicing]) -> set[Voicing]:
        pruned: set[Voicing] = set()

        for candidate in candidates:
            if self._allows_partial(candidate):
                pruned.add(candidate)

        return pruned

    @abstractmethod
    def _allows_partial(self, candidate: Voicing) -> bool: ...

    @abstractmethod
    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool: ...

    def score(self, candidate: Voicing) -> float | None:
        if not self._allows_partial(candidate):
            return None
        return self.score_assuming_pruned(candidate)

    def score_assuming_pruned(self, candidate: Voicing) -> float | None:
        if not self._allows_complete_assuming_pruned(candidate):
            return None
        return self._score_assuming_legal(candidate) * self.weight

    @abstractmethod
    def _score_assuming_legal(self, candidate: Voicing) -> float: ...

    @classmethod
    def _get_ref_voicing(
        cls, history: list[Voicing], history_index: int
    ) -> Voicing | None:
        if history_index >= 0:
            if history_index < len(history):
                return history[history_index]
            else:
                return None

        else:
            if -history_index <= len(history):
                return history[history_index]
            else:
                return None


class GeneratingMetric(Metric, ABC):
    # note by note
    @abstractmethod
    def get_allowed(self, new_voicing: Voicing) -> set[Voicing]: ...


# TODO allemaal methods goed implementeren en super().__init__
