from typing import Iterable, cast
from src.exceptions import WronglyAssumedLegalityException
from src.metrics.metric import Metric
from src.pattern import Pattern
from src.voicing import Voicing


class LegalPatterns(Metric):
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
