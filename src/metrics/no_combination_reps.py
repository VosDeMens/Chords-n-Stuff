from src.constants import INF
from src.metrics.metric import Metric
from src.voicing import Voicing


class NoCombinationReps(Metric):
    """Concerned with not repeating `Combination`s.

    Attributes
    ----------
    min_lookback : int
        How far back in history to enforce no repetitions.

    max_lookback : int
        How far back in history to reward no repetitions.

    Enforces
    --------
    - No repetitions within the latest `min_lookback` `Voicing`s.

    Rewards
    -------
    - No repetitions within the latest `max_lookback` `Voicing`s.
    """

    def __init__(
        self, min_lookback: int = INF, max_lookback: int = INF, weight: float = 1
    ):
        super().__init__(weight)
        self.min_lookback = min_lookback
        self.max_lookback = max_lookback

    def setup(self, history: list[Voicing]) -> None:
        combination_history = [voicing.combination for voicing in history]
        self.reversed_combination_history = list(reversed(combination_history))
        self.actual_min_lookback = min(self.min_lookback, len(history))
        self.actual_max_lookback = min(self.max_lookback, len(history))
        if self.actual_max_lookback != self.actual_min_lookback:
            self.score_per_extra = 1 / (
                self.actual_max_lookback - self.actual_min_lookback
            )

    def _allows_partial(self, candidate: Voicing) -> bool:
        return True

    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool:
        return (
            candidate.combination
            not in self.reversed_combination_history[: self.actual_min_lookback]
        )

    def _score_assuming_legal(self, candidate: Voicing) -> float:
        score = 0
        for combination in self.reversed_combination_history[
            self.actual_min_lookback : self.actual_max_lookback
        ]:
            if combination == candidate.combination:
                return score
            score += self.score_per_extra

        return score
