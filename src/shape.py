from typing import Iterable

from src.cum_pattern import CumPattern
from src.pattern import Pattern


class Shape:
    """A `Shape` represents a chord shape, as a `set` of intervals from an arbitrary root.
    Can't contain duplicates. CAN contain negative intervals.
    """

    def __init__(self, intervals_from_root: Iterable[int]):
        self.intervals_from_root: set[int] = set(intervals_from_root)

    @property
    def pattern(self) -> Pattern:
        return Pattern.from_intervals_from_root(self)

    @property
    def cum_pattern(self) -> CumPattern:
        return CumPattern(self.intervals_from_root)

    def __add__(self, other: "int | Shape") -> "Shape":
        """Adds an individual interval, or all intervals from another `Shape`.

        Duplicates are always filtered.

        Parameters
        ----------
        other : int | Shape
            An individual interval, or a `Shape` to add.

        Returns
        -------
        Shape
            The resulting `Shape`.
        """
        if isinstance(other, int):
            return Shape((*self.intervals_from_root, other))
        else:  # if isinstance(other, Shape)
            return Shape((*self.intervals_from_root, *other.intervals_from_root))

    def __iter__(self):
        return iter(self.intervals_from_root)

    def __len__(self):
        return len(self.intervals_from_root)

    def __str__(self):
        return f"Shape({self.intervals_from_root})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other: object):
        if not isinstance(other, Shape):
            return False
        return self.intervals_from_root == other.intervals_from_root

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.intervals_from_root)))
