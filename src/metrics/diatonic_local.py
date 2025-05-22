from src.constants import INF
from src.cum_pattern import IONIAN
from src.metrics.metric import Metric
from src.pattern import Pattern
from src.voicing import Voicing


class DiatonicLocal(Metric):
    def __init__(
        self,
        min_lookback: int = 1,
        max_lookback: int = INF,
        scale_pattern: Pattern = IONIAN.pattern,
        weight: float = 1,
    ):
        super().__init__(weight)
        self.min_lookback = min_lookback
        self.max_lookback = max_lookback
        self.scale_pattern = scale_pattern

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
        combination_should_match = sum(
            self.reversed_combination_history[: self.actual_min_lookback],
            start=candidate.combination,
        )
        return combination_should_match.fits(self.scale_pattern)

    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Voicing) -> float:
        score = 0
        for combination in self.reversed_combination_history[
            self.actual_min_lookback : self.actual_max_lookback
        ]:
            combined = candidate.combination + combination
            if not combined.fits(self.scale_pattern):
                return score
            score += self.score_per_extra

        return score


# TODO optimise
