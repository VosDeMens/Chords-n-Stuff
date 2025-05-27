from typing import Iterable

from src.pattern import Pattern
from src.util import get_intervals_from_root


class CumPattern:
    """A `CumPattern` (cumulative pattern) is like a `Shape`, but all intervals are mod 12.

    The concept of ionian can be expressed by a `CumPattern`.
    In contrast to a `Pattern`, a `CumPattern` distinguishes between ionian and lydian for example,
    i.e. there's a fixed starting point. If we want to express a major triad as a `CumPattern`,
    we could do so in three different ways.
    """

    def __init__(self, intervals_from_root: Iterable[int]):
        self.intervals_from_root: tuple[int, ...] = tuple(
            sorted(set([interval % 12 for interval in intervals_from_root]))
        )

    @classmethod
    def from_pattern_normal_form(cls, pattern: Pattern):
        return CumPattern(get_intervals_from_root(pattern.normal_form))

    @property
    def pattern(self) -> Pattern:
        return Pattern.from_intervals_from_root(self)

    def __add__(self, other: "int | CumPattern") -> "CumPattern":
        """Adds an individual interval, or all intervals from another `CumPattern`.

        Duplicates are always filtered.

        Parameters
        ----------
        other : int | CumPattern
            An individual interval to add, or a `CumPattern` from which to add all intervals it contains.

        Returns
        -------
        CumPattern
            The resulting `CumPattern`.
        """
        if isinstance(other, int):
            return CumPattern(self.intervals_from_root + (other,))
        else:  # if isinstance(other, CumPattern)
            return CumPattern(self.intervals_from_root + other.intervals_from_root)

    def __iter__(self):
        return iter(self.intervals_from_root)

    def __len__(self):
        return len(self.intervals_from_root)

    def __str__(self):
        return f"CumPattern({self.intervals_from_root})"

    def __repr__(self):
        return str(self)

    def __rshift__(self, i: int) -> "CumPattern":
        """Shifts the root to the right `i` steps, and recalculates the intervals.

        Parameters
        ----------
        i : int
            Number of steps to shift to the right.

        Returns
        -------
        CumPattern
            Shifted result.
        """
        new_root = self.intervals_from_root[i % len(self)]
        intervals_from_root = [
            interval - new_root for interval in self.intervals_from_root
        ]
        return CumPattern(intervals_from_root)

    def __lshift__(self, i: int) -> "CumPattern":
        """Shifts the root to the left `i` steps, and recalculates the intervals.

        Parameters
        ----------
        i : int
            Number of steps to shift to the left.

        Returns
        -------
        CumPattern
            Shifted result.
        """
        return self >> -i

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CumPattern):
            return False
        return self.intervals_from_root == other.intervals_from_root

    def __hash__(self) -> int:
        return hash(self.intervals_from_root)


MAJOR = CumPattern([0, 4, 7])
MINOR = CumPattern([0, 3, 7])
SUS2 = CumPattern([0, 2, 7])
SUS4 = CumPattern([0, 5, 7])
LYDSUS4 = CumPattern([0, 6, 7])
DIM = CumPattern([0, 3, 6])
AUG = CumPattern([0, 4, 8])

ADD9 = MAJOR + 2
ADD4 = MAJOR + 5
M6 = MAJOR + 9
DOM7 = MAJOR + 10
M7 = MAJOR + 11

m6 = MINOR + 9
m7 = MINOR + 10
mM7 = MINOR + 11

SUS2ADD6 = SUS2 + M6
SUS2SUS4 = SUS2 + SUS4
DOM7SUS2 = DOM7 + SUS2
M7SUS2 = M7 + SUS2

DOM7SUS4 = DOM7 + SUS4
M7SUS4 = M7 + SUS4
M7LYDSUS4 = M7 + LYDSUS4

DIM7 = DIM + 9
HALFDIM7 = DIM + 10
DIMM7 = DIM + 11

AUG7 = AUG + 10
AUGM7 = AUG + 11


DOM7f9 = DOM7 + 1
DOM9 = DOM7 + 2
DOM7s9 = DOM7 + 3

M9 = M7 + 2
m9 = m7 + 2
DIM9 = DIM7 + 2
HALFDIM9 = HALFDIM7 + 2
M69 = M6 + 2
m69 = m6 + 2

IONIAN = CumPattern([0, 2, 4, 5, 7, 9, 11])
DORIAN = IONIAN >> 1
PHRYGIAN = IONIAN >> 2
LYDIAN = IONIAN >> 3
MIXOLYDIAN = IONIAN >> 4
AEOLIAN = IONIAN >> 5
LOCRIAN = IONIAN >> 6
