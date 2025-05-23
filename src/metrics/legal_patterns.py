from typing import Iterable, cast
from src.exceptions import WronglyAssumedLegalityException
from src.metrics.metric import Metric
from src.pattern import Pattern
from src.voicing import Voicing


class LegalPatterns(Metric):
    """Concerned with which patterns are allowed.

    Attributes
    ----------
    scored_legal_patterns : list[tuple[Pattern, float]]
        A list of legal patterns and their scores (sorted).

    optimise_pc_spread : bool
        Whether to enforce that the `Note`s are spread over `PitchClass`es
        of the `CumPattern` evenly.

    Enforces
    --------
    - Only legal patterns used.
    if optimise_pc_spread:
        - Even spread of `Note`a over `PitchClass`es, e.g. twice a C, twice an E, one G
        for a major pattern is ok, but three times a C, one E and one G isn't.

    Rewards
    -------
    - Based on set scores (1 by default).
    """

    def __init__(
        self,
        legal_patterns: Iterable[Pattern] | Iterable[tuple[Pattern, float]],
        optimise_pc_spread: bool = True,
        weight: float = 1,
    ):
        assert legal_patterns, "Everything illegal :("

        super().__init__(weight)

        if any(isinstance(p, Pattern) for p in legal_patterns):
            legal_patterns = cast(Iterable[Pattern], legal_patterns)
            legal_patterns = [(pattern, 0) for pattern in legal_patterns]
        legal_patterns = cast(Iterable[tuple[Pattern, float]], legal_patterns)

        self.scored_legal_patterns = sorted(
            legal_patterns,
            key=lambda tup: len(tup[0]),
        )

        self.optimise_pc_spread = optimise_pc_spread

    def setup(self, history: list[Voicing]) -> None:
        pass

    def _allows_partial(self, candidate: Voicing) -> bool:
        for legal_pattern, _ in self.scored_legal_patterns:
            if candidate.fits(legal_pattern, self.optimise_pc_spread):
                return True
        return False

    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Voicing) -> float:
        for legal_pattern, score in self.scored_legal_patterns:
            if candidate.fits(legal_pattern, self.optimise_pc_spread):
                return score
        raise WronglyAssumedLegalityException()
