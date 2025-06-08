from typing import Sequence

from src.my_types import *
from src.profiler import TimingMeta
from src.util import (
    get_all_12bit_bitmask_rotations,
    get_normal_form_12bit_bitmask,
    inner_intervals_to_cum_pattern_bitmask,
    shape_bitmask_and_offset_to_cum_pattern_bitmask,
)


class Pattern:
    """A pattern represents the essence of a chord or scale.
    It is the most abstract way to represent a chord or scale.

    The concept of a major triad can be expressed as a `Pattern`.
    There's no distinction between the `Pattern` of ionian and lydian for example.
    """

    __slots__ = ("bitmask", "rotations")

    bitmask: int16
    rotations: int16list

    _instances: dict[int16, "Pattern"] = {}

    def __new__(cls, intervals: Sequence[int]) -> "Pattern":
        assert (
            sum(intervals) % 12 == 0
        ), f"Intervals should sum to 0 (mod 12), {intervals = }"
        cum_pattern_bitmask = inner_intervals_to_cum_pattern_bitmask(intervals)
        return cls._get_or_create(cum_pattern_bitmask)

    @classmethod
    def _get_or_create(cls, bitmask: int16) -> "Pattern":
        assert (
            bitmask & int16(0xFFF) == bitmask
        ), f"Bitmask {bitmask} is not 12 bits long."
        if bitmask in cls._instances:
            return cls._instances[bitmask]

        instance = super().__new__(cls)
        instance.bitmask = get_normal_form_12bit_bitmask(bitmask)
        instance.rotations = get_all_12bit_bitmask_rotations(instance.bitmask)

        for rotation in instance.rotations:
            cls._instances[rotation] = instance

        return instance

    @classmethod
    def from_12bit_bitmask(cls, input_bitmask: int16) -> "Pattern":
        """Creates a `Pattern` from a 12-bit bitmask, which does not need to be in normal form.

        Such a bitmask could be representing a `CumPattern`, or a `Combination`.

        Parameters
        ----------
        input_bitmask : int16
            A 12-bit bitmask representing the pattern.

        Returns
        -------
        Pattern
            The `Pattern` instance created from the input bitmask.
        """
        assert (
            input_bitmask & int16(0xFFF) == input_bitmask
        ), f"Bitmask {input_bitmask} is not 12 bits long."
        return cls._get_or_create(input_bitmask)

    @classmethod
    def from_64bit_bitmask(cls, input_bitmask: int64) -> "Pattern":
        """Creates a `Pattern` from a 64-bit bitmask.

        Such a bitmask could be representing a `Voicing` or a `Shape`.

        Parameters
        ----------
        input_bitmask : int64
            A 64-bit bitmask representing a `Voicing` or a `Shape`.

        Returns
        -------
        Pattern
            The `Pattern` instance created from the input bitmask.
        """
        # Works for Voicing as well, because, since we're in Pattern
        # we just need an arbitrary cum_pattern rotation for _get_or_create
        bitmask = shape_bitmask_and_offset_to_cum_pattern_bitmask(input_bitmask, 0)

        return cls._get_or_create(bitmask)

    def __hash__(self) -> int:
        return int(self.bitmask)

    def __len__(self) -> int:
        return self.bitmask.bit_count()

    def __str__(self) -> str:
        if self in PATTERN_NAMES:
            return PATTERN_NAMES[self]

        return f"Pattern({self.inner_intervals})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def inner_intervals(self) -> list[int]:
        """Returns the inner intervals of the pattern, always summing to 12."""
        inner_intervals: list[int] = []

        pos: int | None = None
        for i in range(12):
            if self.bitmask & (int16(1) << int16(i)):
                if pos is not None:
                    inner_intervals.append((i - pos) % 12)
                pos = i
        if pos is not None:
            inner_intervals.append(12 - pos % 12)
        return inner_intervals

    def __contains__(self, other: "Pattern") -> bool:
        """
        Examples
        --------
        >>> MAJOR.pattern in M7.pattern
        True

        >>> Pattern([1, 4, 7]) in M7.pattern
        True

        >>> DIM.pattern in M7.pattern
        False
        """
        for rotation in other.rotations:
            if (self.bitmask & rotation) == rotation:
                return True
        return False


MARY = Pattern([4, 3, 5])
MINNY = Pattern([3, 4, 5])
SUZY = Pattern([2, 5, 5])
DIMMY = Pattern([3, 3, 6])
AUGY = Pattern([4, 4, 4])
JIMMY = Pattern([6, 5, 1])
MISTY = Pattern([2, 1, 9])

PATTERN_NAMES = {
    MARY: "Mary",
    MINNY: "Minny",
    SUZY: "Suzy",
    DIMMY: "Dimmy",
    AUGY: "Augy",
    JIMMY: "Jimmy",
    MISTY: "Misty",
}
