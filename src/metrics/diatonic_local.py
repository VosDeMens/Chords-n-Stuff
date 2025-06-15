from src.combination import Combination
from src.constants import INF
from src.cum_pattern import IONIAN
from src.metrics.metric import Metric
from src.pattern import Pattern
from src.distribution import Distribution


class DiatonicLocal(Metric):
    """Concerned with diatonicity with recent `Distribution`s.

    Attributes
    ----------
    min_lookback : int
        How far back in history to enforce diatonicity.

    max_lookback : int
        How far back in history to reward diatonicity.

    scale_pattern : Pattern
        Scale pattern within which to establish diatonicity.

    Enforces
    --------
    - The union of a candidate and the latest `min_lookback` `Distribution`s fit `self.scale_pattern`.

    Rewards
    -------
    - The more latest `Distribution`s in history we can add to this union.
    """

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
        self.concrete_combinations: list[Combination] = Combination.all_from_pattern(
            scale_pattern
        )

    def setup(self, history: list[Distribution]) -> None:
        actual_min_lookback = min(self.min_lookback, len(history))
        actual_max_lookback = min(self.max_lookback, len(history))
        combination_history = [
            distribution.combination for distribution in history[-actual_max_lookback:]
        ]
        reversed_history = list(reversed(combination_history))

        union_history_min_lookback = sum(
            reversed_history[:actual_min_lookback], Combination([])
        )
        self.fit_any_to_be_allowed = {
            concrete
            for concrete in self.concrete_combinations
            if union_history_min_lookback in concrete
        }

        fit_any_iteratively_for_bonus_points: list[set[Combination]] = []
        for i in range(actual_min_lookback, actual_max_lookback):
            union_history_bonus = sum(reversed_history[: i + 1], Combination([]))
            fit_any_iteratively_for_bonus_points.append(
                {
                    concrete
                    for concrete in self.concrete_combinations
                    if union_history_bonus in concrete
                }
            )

        bonus_per_fit: dict[Combination, float] = {}
        for i, combinations in reversed(
            list(enumerate(fit_any_iteratively_for_bonus_points))
        ):
            for combination in combinations:
                if combination not in bonus_per_fit:
                    bonus_per_fit[combination] = (i + 1) / len(
                        fit_any_iteratively_for_bonus_points
                    )

        self.bonus_per_fit: list[tuple[Combination, float]] = list(
            sorted(bonus_per_fit.items(), key=lambda cf: -cf[1])
        )

    def _allows_partial(self, candidate: Distribution) -> bool:
        candidate_combination = candidate.combination
        for to_fit in self.fit_any_to_be_allowed:
            if candidate_combination in to_fit:
                return True
        return False

    def _allows_complete_assuming_pruned(self, candidate: Distribution) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Distribution) -> float:
        candidate_combination = candidate.combination
        for to_fit, score in self.bonus_per_fit:
            if candidate_combination in to_fit:
                return score
        return 0
