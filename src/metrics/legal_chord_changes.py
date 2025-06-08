from typing import cast
from src.combination import Combination
from src.cum_pattern import CumPattern
from src.metrics.metric import Metric
from src.distribution import Distribution


class LegalChordChanges(Metric):
    """Concerned with which chord changes are allowed.

    Attributes
    ----------
    scored_rules : dict[CumPattern, set[tuple[CumPattern, int, float]]]
        Per `CumPattern` `cum`, which steps are allowed, expressed by
            - A next `CumPattern`
            - The interval between the 0 of `cum` and the `0` in the next
            - The score to assign to this chord change

    optimise_pc_spread : bool
        Whether to enforce that the `Note`s are spread over `PitchClass`es
        of the `CumPattern` evenly.

    Enforces
    --------
    - Only legal chord changes take place.
    if optimise_pc_spread:
        - Even spread of `Note`a over `PitchClass`es, e.g. twice a C, twice an E, one G
        for a major pattern is ok, but three times a C, one E and one G isn't.

    Rewards
    -------
    - Based on set scores (1 by default).
    """

    def __init__(
        self,
        rules: (
            dict[
                CumPattern, set[tuple[CumPattern, int, float] | tuple[CumPattern, int]]
            ]
            | None
        ) = None,
        optimise_pc_spread: bool = True,
        weight: float = 1,
    ):
        super().__init__(weight)
        if rules:
            for cum in rules:
                for dest in rules[cum]:
                    if len(dest) == 2:
                        rules[cum].remove(dest)
                        rules[cum].add(dest + (1,))
            self.scored_rules: dict[CumPattern, set[tuple[CumPattern, int, float]]] = (
                cast(dict[CumPattern, set[tuple[CumPattern, int, float]]], rules)
            )
        else:
            self.scored_rules = {}
        self.optimise_pc_spread = optimise_pc_spread

    def setup(self, history: list[Distribution]) -> None:
        self.allowed_combinations = self.get_allowed_combinations(history)

    def _allows_partial(self, candidate: Distribution) -> bool:
        for combination, _ in self.allowed_combinations.items():
            if candidate.fits(combination, self.optimise_pc_spread):
                return True
        return False

    def _allows_complete_assuming_pruned(self, candidate: Distribution) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Distribution) -> float:
        return self.allowed_combinations[candidate.combination]

    def get_allowed_combinations(
        self, history: list[Distribution]
    ) -> dict[Combination, float]:
        last_combination = history[-1].combination

        allowed: dict[Combination, float] = {}
        for cum, allowed_for_cum in self.scored_rules.items():
            roots_for_matches = last_combination.match(cum)
            for root in roots_for_matches:
                for new_cum, shift, score in allowed_for_cum:
                    combination = Combination.from_cum(root + shift, new_cum)
                    if combination not in allowed:
                        allowed[combination] = score
                        continue
                    allowed[combination] = max(allowed[combination], score)

        return allowed

    def add_rule(self, cum: CumPattern, dest: CumPattern, shift: int, score: float = 1):
        if cum not in self.scored_rules:
            self.scored_rules[cum] = set()
        self.scored_rules[cum].add((dest, shift, score))
