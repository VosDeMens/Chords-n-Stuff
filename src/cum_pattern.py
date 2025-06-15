from typing import Iterable

from src.pattern import Pattern
from src.my_types import int16, int64
from src.profiler import TimingMeta
from src.util import (
    get_all_12bit_bitmask_rotations,
    intervals_from_root_to_cum_pattern_bitmask,
    is_12bit,
    rotate_12bit_bitmask_right,
    shape_bitmask_and_offset_to_cum_pattern_bitmask,
)


class CumPattern(metaclass=TimingMeta):
    """A `CumPattern` (cumulative pattern) is like a `Shape`, but all intervals are mod 12.

    The concept of ionian can be expressed by a `CumPattern`.
    In contrast to a `Pattern`, a `CumPattern` distinguishes between ionian and lydian for example,
    i.e. there's a fixed starting point. If we want to express a major triad as a `CumPattern`,
    we could do so in three different ways.
    """

    __slots__ = ("bitmask",)

    bitmask: int16

    def __init__(self, intervals_from_root: Iterable[int]):
        intervals_mod_12 = set(interval % 12 for interval in intervals_from_root)
        self.bitmask = intervals_from_root_to_cum_pattern_bitmask(intervals_mod_12)

    @classmethod
    def _from_12bit_bitmask(cls, bitmask: int16) -> "CumPattern":
        """Creates a `CumPattern` from a 12-bit bitmask.

        This bitmask does not need to be in normal form, but it needs
        to represent a `CumPattern`, not a `Combination`.

        Parameters
        ----------
        bitmask : int16
            A 12-bit bitmask representing the cumulative pattern.

        Returns
        -------
        CumPattern
            The resulting `CumPattern`.
        """
        assert is_12bit(bitmask), f"{bitmask = }"

        instance = cls.__new__(cls)
        instance.bitmask = bitmask
        return instance

    @classmethod
    def from_shape_bitmask_and_offset(
        cls, shape_bitmask: int64, offset: int = 0
    ) -> "CumPattern":
        bitmask = shape_bitmask_and_offset_to_cum_pattern_bitmask(shape_bitmask, offset)
        return CumPattern._from_12bit_bitmask(bitmask)

    @classmethod
    def all_from_pattern(cls, pattern: Pattern) -> "list[CumPattern]":
        all_bitmask_rotations = get_all_12bit_bitmask_rotations(pattern.bitmask)
        return [
            CumPattern._from_12bit_bitmask(rotation)
            for rotation in all_bitmask_rotations
        ]

    @property
    def intervals_from_root(self) -> list[int]:
        """Get the intervals from root as a sorted tuple.

        Returns
        -------
        tuple[int, ...]
            A sorted tuple of intervals from the root.
        """
        return [i for i in range(12) if self.bitmask & (int16(1) << int16(i))]

    @property
    def pattern(self) -> Pattern:
        return Pattern.from_12bit_bitmask(self.bitmask)

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
            new_bitmask = self.bitmask | (int16(1) << int16(other % 12))
            return CumPattern._from_12bit_bitmask(new_bitmask)
        else:  # CumPattern
            new_bitmask = self.bitmask | other.bitmask
            return CumPattern._from_12bit_bitmask(new_bitmask)

    def __iter__(self):
        return iter(self.intervals_from_root)

    def __len__(self):
        return self.bitmask.bit_count()

    def __str__(self):
        return f"CumPattern({list(self.intervals_from_root)})"

    def __repr__(self):
        return str(self)

    def __lshift__(self, i: int) -> "CumPattern":
        bitmask = rotate_12bit_bitmask_right(self.bitmask, i)
        return CumPattern._from_12bit_bitmask(bitmask)

    def __rshift__(self, i: int) -> "CumPattern":
        return self << -i

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CumPattern) and self.bitmask == other.bitmask

    def __hash__(self) -> int:
        return int(self.bitmask)


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
DORIAN = IONIAN << 2
PHRYGIAN = IONIAN << 4
LYDIAN = IONIAN << 5
MIXOLYDIAN = IONIAN << 7
AEOLIAN = IONIAN << 9
LOCRIAN = IONIAN << 11
