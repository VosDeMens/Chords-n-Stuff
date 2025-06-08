from src.exceptions import NoRefDistributionException
from src.metrics.metric import *
from src.note import Note
from src.distribution import Distribution


class IndividualSteps(GeneratingMetric):
    """Concerned with the intervals between notes in a previous Distribution and the next.

    Attributes
    ----------
    ref_distribution : Distribution
        The distribution to take as a reference when determining step sizes for a candidate. Determined in `setup`.

    min_step : int
        The smallest legal interval between a note in `ref_distribution` and the corresponding note in a candidate.

    max_step : int
        The biggest legal interval between a note in `ref_distribution` and the corresponding note in a candidate.

    ideal_step : float | None
        The ideal interval between a note in `ref_distribution` and the corresponding note in a candidate.

    history_index : int
        The index in the distribution history to find `ref_distribution` at.

    Enforces
    --------
    - All intervals between a note in `ref_distribution` and the corresponding note in a candidate
    to be in the legal range.

    Rewards
    -------
    - The smaller the sum of the differences between the intervals between notes in `ref_distribution`
    and the corresponding notes in a candidate and `ideal_step`.
    """

    def __init__(
        self,
        min_step: int,
        max_step: int,
        ideal_step: float | None = None,
        history_index: int = -1,
        weight: float = 1,
    ):
        super().__init__(weight)
        self.min_step = min_step
        self.max_step = max_step
        self.ideal_step = ideal_step
        self.history_index = history_index
        self.ref_distribution: Distribution | None = None
        if ideal_step is not None:
            self.max_deviation = max(
                abs(max_step - ideal_step), abs(min_step - ideal_step)
            )

    def setup(self, history: list[Distribution]) -> None:
        self.ref_distribution = self._get_ref_distribution(history, self.history_index)

    def _allows_partial(self, candidate: Distribution) -> bool:
        if self.ref_distribution is None:
            return True

        for ref_note, can_note in zip(self.ref_distribution, candidate):
            d = self.distance(ref_note, can_note)
            if not (self.min_step <= d <= self.max_step):
                return False

        return True

    def _allows_complete_assuming_pruned(self, candidate: Distribution) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Distribution) -> float:
        if self.ref_distribution is None or self.ideal_step is None:
            return 0

        penalty = 0

        for ref_note, can_note in zip(self.ref_distribution, candidate):
            d = self.distance(ref_note, can_note)
            penalty += abs(d - self.ideal_step)

        return 1 - penalty / len(candidate) / self.max_deviation

    @classmethod
    def distance(cls, ref_note: Note, can_note: Note) -> float:
        return abs(can_note - ref_note)

    def get_allowed(self) -> set[Distribution]:
        if self.ref_distribution is None:
            raise NoRefDistributionException

        allowed: set[Distribution] = {Distribution([])}
        for ref_note in self.ref_distribution:
            new_allowed: set[Distribution] = set()
            for partial_distribution in allowed:
                for d in range(self.min_step, self.max_step + 1):
                    new_note_up = ref_note + d
                    new_allowed.add(partial_distribution + new_note_up)

                    if d == 0:
                        continue

                    new_note_down = ref_note - d
                    new_allowed.add(partial_distribution + new_note_down)
            allowed = new_allowed

        return allowed
