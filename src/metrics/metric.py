from abc import ABC, abstractmethod

from src.voicing import Voicing


class Metric(ABC):
    """The blueprint of a metric used in the generation of voicing progressions.

    To Implement
    ------------
    In order to implement `Metric`, a class needs to implement the following:
    - `def __init__(self, ...): ...`

        Within the `__init__`, `super().__init__(weight)` has to be called.
        For a metric that doesn't score, just pass 0 into the super constructor.
        This is required in order to enforce being explicit.
    - `def setup(self, history: list[Voicing]) -> None: ...`

        This method is called once every start of the search for a next `Voicing`.
        It is used for any computation that can be done regardless of which individual
        candidates we'll be considering.
    - `def _allows_partial(self, candidate: Voicing) -> bool: ...`

        This method is called during pruning.
        It is used for filtering out partial voicings, so that we don't need to explore
        all the ways in which we could extend that voicing.
    - `def _allows_complete_assuming_pruned(self, candidate: Voicing) -> bool: ...`

        This method is called once per completed voicing, after pruning.
        It is used for metrics that can only determine for complete voicings
        whether they are allowed or not, and not during pruning.
    - `def _score_assuming_legal(self, candidate: Voicing) -> float: ...`

        This method awards a score to an assumed legal voicing, which is then
        multiplied by the metric's `weight` in pre-defined superlass logic.
    """

    def __init__(self, weight: float):
        self.weight = weight

    @abstractmethod
    def setup(self, history: list[Voicing]) -> None: ...

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
    """The blueprint of a metric that can provide a set of partial voicings
    based on an existing partial voicing. We need one of these in an engine
    to create a set of candidates that other metrics can then prune.

    To Implement
    ------------
    In order to implement `GeneratingMetric`, a class needs to implement the following:
    - `def get_allowed(self, partial_voicing: Voicing) -> set[Voicing]: ...`

        Creates a set of new (partial) candidates, based on some partial Voicing
        that was already allowed by all relevant metrics.
    """

    @abstractmethod
    def get_allowed(self, partial_voicing: Voicing) -> set[Voicing]: ...
