from typing import Sequence

from src.metrics.metric import GeneratingMetric, Metric
from src.util import weighted_pick
from src.voicing import Voicing


class StochasticVoicingEngine:
    """Creates a progression of `Voicing`s based on a list of `Metric`s.
    It iteratively picks a next `Voicing` by determining which `Voicing`s
    are allowed by all `Metric`s, and then making a weighted random pick,
    based on the scores provided by the `Metric`s.
    """

    def __init__(
        self,
        generating_metric: GeneratingMetric,
        other_metrics: Sequence[Metric],
        start: Voicing,
    ):
        self.generating_metric = generating_metric
        self.other_metrics = other_metrics
        self.all_metrics: list[Metric] = [generating_metric] + list(other_metrics)
        self.history = [start]
        self.nr_of_notes = len(start)

    def get_next(self) -> Voicing | None:
        """Picks the next `Voicing` in the progression.

        Returns
        -------
        Voicing | None
            The next `Voicing`, or `None` if there are no legal `Voicing`s.
        """
        for metric in self.all_metrics:
            metric.setup(self.history)

        frontier = [Voicing([])]

        for _ in range(self.nr_of_notes):
            new_frontier: list[Voicing] = []

            for voicing in frontier:
                candidates = self.generating_metric.get_allowed(voicing)
                for metric in self.other_metrics:
                    candidates = metric.prune(candidates)
                new_frontier += candidates

            frontier = new_frontier

        scored_voicings: dict[Voicing, float] = {}

        for voicing in frontier:
            scored_voicings[voicing] = 0
            for metric in self.all_metrics:
                new_score = metric.score_assuming_pruned(voicing)
                if new_score is None:
                    scored_voicings.pop(voicing)
                    break
                scored_voicings[voicing] += new_score

        if not scored_voicings:
            return None

        next_voicing = weighted_pick(scored_voicings)
        self.history.append(next_voicing)
        return next_voicing

    def reset(self, start: Voicing) -> None:
        """Whipes the history of the engine, and starts over with `start`.

        Parameters
        ----------
        start : Voicing
            The first `Voicing` in the new history.
        """
        self.history = [start]
