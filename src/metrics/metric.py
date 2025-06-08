from abc import ABC, abstractmethod

from src.profiler import TimingMeta
from src.distribution import Distribution


class Metric(ABC):
    """The blueprint of a metric used in the generation of distribution progressions.

    To Implement
    ------------
    In order to implement `Metric`, a class needs to implement the following:
    - `def __init__(self, ...): ...`

        Within the `__init__`, `super().__init__(weight)` has to be called.
        For a metric that doesn't score, just pass 0 into the super constructor.
        This is required in order to enforce being explicit.
    - `def setup(self, history: list[Distribution]) -> None: ...`

        This method is called once every start of the search for a next `Distribution`.
        It is used for any computation that can be done regardless of which individual
        candidates we'll be considering.
    - `def _allows_partial(self, candidate: Distribution) -> bool: ...`

        This method is called during pruning.
        It is used for filtering out partial distributions, so that we don't need to explore
        all the ways in which we could extend that distribution.
    - `def _allows_complete_assuming_pruned(self, candidate: Distribution) -> bool: ...`

        This method is called once per completed distribution, after pruning.
        It is used for metrics that can only determine for complete distributions
        whether they are allowed or not, and not during pruning.
    - `def _score_assuming_legal(self, candidate: Distribution) -> float: ...`

        This method awards a score to an assumed legal distribution, which is then
        multiplied by the metric's `weight` in pre-defined superlass logic.
    """

    def __init__(self, weight: float):
        self.weight = weight

    @abstractmethod
    def setup(self, history: list[Distribution]) -> None: ...

    def prune(self, candidates: set[Distribution]) -> set[Distribution]:
        pruned: set[Distribution] = set()

        for candidate in candidates:
            if self._allows_partial(
                candidate
            ) and self._allows_complete_assuming_pruned(candidate):
                pruned.add(candidate)

        return pruned

    @abstractmethod
    def _allows_partial(self, candidate: Distribution) -> bool: ...

    @abstractmethod
    def _allows_complete_assuming_pruned(self, candidate: Distribution) -> bool: ...

    def score(self, candidate: Distribution) -> float | None:
        if not self._allows_partial(candidate):
            return None
        return self.score_assuming_pruned(candidate)

    def score_assuming_pruned(self, candidate: Distribution) -> float | None:
        if not self._allows_complete_assuming_pruned(candidate):
            return None
        return self._score_assuming_legal(candidate) * self.weight

    @abstractmethod
    def _score_assuming_legal(self, candidate: Distribution) -> float: ...

    @classmethod
    def _get_ref_distribution(
        cls, history: list[Distribution], history_index: int
    ) -> Distribution | None:
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
    """The blueprint of a metric that can provide a set of partial distributions
    based on an existing partial distribution. We need one of these in an engine
    to create a set of candidates that other metrics can then prune.

    To Implement
    ------------
    In order to implement `GeneratingMetric`, a class needs to implement the following:
    - `def get_allowed(self, partial_distribution: Distribution) -> set[Distribution]: ...`

        Creates a set of new (partial) candidates, based on some partial Distribution
        that was already allowed by all relevant metrics.
    """

    @abstractmethod
    def get_allowed(self) -> set[Distribution]: ...
