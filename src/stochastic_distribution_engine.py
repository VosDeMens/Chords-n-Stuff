from typing import Sequence

from src.metrics.metric import GeneratingMetric, Metric
from src.profiler import TimingMeta
from src.util import weighted_pick
from src.distribution import Distribution


class StochasticDistributionEngine:
    """Creates a progression of `Distribution`s based on a list of `Metric`s.
    It iteratively picks a next `Distribution` by determining which `Distribution`s
    are allowed by all `Metric`s, and then making a weighted random pick,
    based on the scores provided by the `Metric`s.
    """

    def __init__(
        self,
        generating_metric: GeneratingMetric,
        other_metrics: Sequence[Metric],
        start: Distribution,
    ):
        self.generating_metric = generating_metric
        self.other_metrics = other_metrics
        self.all_metrics: list[Metric] = [generating_metric] + list(other_metrics)
        self.history = [start]
        self.nr_of_notes = len(start)

    def get_next(self) -> Distribution | None:
        """Picks the next `Distribution` in the progression.

        Returns
        -------
        Distribution | None
            The next `Distribution`, or `None` if there are no legal `Distribution`s.
        """
        for metric in self.all_metrics:
            metric.setup(self.history)

        candidates = self.generating_metric.get_allowed()
        for metric in self.other_metrics:
            candidates = metric.prune(candidates)

        scored_distributions: dict[Distribution, float] = {}

        for distribution in candidates:
            scored_distributions[distribution] = 0
            for metric in self.all_metrics:
                new_score = metric.score_assuming_pruned(distribution)
                if new_score is None:
                    scored_distributions.pop(distribution)
                    break
                scored_distributions[distribution] += new_score

        if not scored_distributions:
            return None

        next_distribution = weighted_pick(scored_distributions)
        self.history.append(next_distribution)
        return next_distribution

    def reset(self, start: Distribution) -> None:
        """Whipes the history of the engine, and starts over with `start`.

        Parameters
        ----------
        start : Distribution
            The first `Distribution` in the new history.
        """
        self.history = [start]
