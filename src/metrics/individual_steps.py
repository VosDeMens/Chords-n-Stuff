from src.exceptions import NoRefVoicingException
from src.metrics.metric import *
from src.note import Note
from src.voicing import Voicing


class IndividualSteps(GeneratingMetric):
    """Concerned with the intervals between notes in a previous Voicing and the next.

    Attributes
    ----------
    ref_voicing : Voicing
        The voicing to take as a reference when determining step sizes for a candidate. Determined in `setup`.

    min_step : int
        The smallest legal interval between a note in `ref_voicing` and the corresponding note in a candidate.

    max_step : int
        The biggest legal interval between a note in `ref_voicing` and the corresponding note in a candidate.

    ideal_step : float | None
        The ideal interval between a note in `ref_voicing` and the corresponding note in a candidate.

    history_index : int
        The index in the voicing history to find `ref_voicing` at.

    Enforces
    --------
    - All intervals between a note in `ref_voicing` and the corresponding note in a candidate
    to be in the legal range.

    Rewards
    -------
    - The smaller the sum of the differences between the intervals between notes in `ref_voicing`
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
        self.ref_voicing: Voicing | None = None
        if ideal_step is not None:
            self.max_deviation = max(
                abs(max_step - ideal_step), abs(min_step - ideal_step)
            )

    def setup(self, history: list[Voicing]) -> None:
        self.ref_voicing = self._get_ref_voicing(history, self.history_index)

    def _allows_partial(self, candidate: Voicing) -> bool:
        if self.ref_voicing is None:
            return True

        for ref_note, can_note in zip(self.ref_voicing, candidate):
            d = self.distance(ref_note, can_note)
            if not (self.min_step <= d <= self.max_step):
                return False

        return True

    def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool:
        return True

    def _score_assuming_legal(self, candidate: Voicing) -> float:
        if self.ref_voicing is None or self.ideal_step is None:
            return 0

        penalty = 0

        for ref_note, can_note in zip(self.ref_voicing, candidate):
            d = self.distance(ref_note, can_note)
            penalty += abs(d - self.ideal_step)

        return 1 - penalty / len(candidate) / self.max_deviation

    @classmethod
    def distance(cls, ref_note: Note, can_note: Note) -> float:
        return abs(can_note - ref_note)

    def get_allowed(self, partial_voicing: Voicing) -> set[Voicing]:
        if self.ref_voicing is None:
            raise NoRefVoicingException

        ref_note = self.ref_voicing[len(partial_voicing)]
        allowed: set[Voicing] = set()

        for d in range(self.min_step, self.max_step + 1):
            new_note_up = ref_note + d
            allowed.add(partial_voicing + new_note_up)

            new_note_down = ref_note - d
            allowed.add(partial_voicing + new_note_down)

        return allowed
