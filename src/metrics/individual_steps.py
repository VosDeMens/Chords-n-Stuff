from src.exceptions import NoRefVoicingException
from src.metrics.metric import *
from src.note import Note
from src.voicing import Voicing


class IndividualSteps(GeneratingMetric):
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

    def get_allowed(self, new_voicing: Voicing) -> set[Voicing]:
        if self.ref_voicing is None:
            raise NoRefVoicingException

        ref_note = self.ref_voicing[len(new_voicing)]
        allowed: set[Voicing] = set()

        for d in range(self.min_step, self.max_step + 1):
            new_note_up = ref_note + d
            allowed.add(new_voicing + new_note_up)

            new_note_down = ref_note - d
            allowed.add(new_voicing + new_note_down)

        return allowed
