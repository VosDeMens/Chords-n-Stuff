from functools import cache
from typing import Iterable, Sequence

from src.util import (
    get_inner_intervals,
    get_intervals_from_root,
    get_minimal_rotation,
    rotate_by,
)


class Pattern:
    """A pattern represents the essence of a chord or scale.
    It is the most abstract way to represent a chord or scale.

    The concept of a major triad can be expressed as a `Pattern`.
    There's no distinction between the `Pattern` of ionian and lydian for example.
    """

    def __init__(self, intervals: Sequence[int]) -> None:
        assert (
            sum(intervals) % 12 == 0
        ), f"Intervals should sum to 0 (mod 12), {intervals = }"
        intervals_reduced = reduce_inner_intervals(tuple(intervals))
        self.normal_form: tuple[int, ...] = get_minimal_rotation(intervals_reduced)

    @classmethod
    def from_intervals_from_root(cls, intervals_from_root: Iterable[int]) -> "Pattern":
        self = cls.__new__(cls)
        self.normal_form = get_normal_form_from_intervals_from_root(intervals_from_root)
        return self

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pattern):
            return False
        return self.normal_form == other.normal_form

    def __hash__(self) -> int:
        return hash(tuple(self.normal_form))

    def __len__(self) -> int:
        return len(self.normal_form)

    def __str__(self) -> str:
        if self in PATTERN_NAMES:
            return PATTERN_NAMES[self]
        return f"Pattern(Intervals: {self.normal_form})"

    def __repr__(self) -> str:
        return str(self)

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
        for shift in range(len(self)):
            rotated_intervals = rotate_by(self.normal_form, shift)

            if _matches(other.normal_form, rotated_intervals):
                return True
        return False


@cache
def reduce_inner_intervals(inner_intervals: Sequence[int]) -> tuple[int, ...]:
    """Reduces a `Sequence` of intervals to sum to 12.

    Parameters
    ----------
    inner_intervals : Sequence[int]
        The intervals between some collection of notes.

    Returns
    -------
    tuple[int, ...]
        The reduced version

    Examples
    --------
    >>> reduce_intervals((4, 3, 5))
    (4, 3, 5)

    >>> reduce_intervals([10, 10, 4])
    (8, 2, 2)
    """
    assert (
        sum(inner_intervals) % 12 == 0
    ), f"{inner_intervals = } should sum to 0 mod 12 but sum to {sum(inner_intervals)} mod 12"
    intervals_from_roots = get_intervals_from_root(inner_intervals)
    return get_normal_form_from_intervals_from_root(intervals_from_roots)


@cache
def get_normal_form_from_intervals_from_root(
    intervals_from_root: Iterable[int],
) -> tuple[int, ...]:
    intervals_from_root = set(intervals_from_root)
    if not intervals_from_root:
        return ()
    if len(intervals_from_root) == 1:
        return (12,)
    reduced = [d % 12 for d in intervals_from_root]
    reduced_sorted = tuple(sorted(reduced))
    inner_intervals = get_inner_intervals(reduced_sorted)
    inner_intervals_wrapped_around: tuple[int, ...] = (
        *inner_intervals,
        (reduced_sorted[0] - reduced_sorted[-1]) % 12,
    )
    normal_form: tuple[int, ...] = get_minimal_rotation(inner_intervals_wrapped_around)
    return normal_form


@cache
def _matches(p1: tuple[int, ...], p2: tuple[int, ...]) -> bool:
    """Determines whether `p1` can be constructed from `p2` by summing adjacent values.

    Parameters
    ----------
    p1 : tuple[int, ...]
        To construct into.
    p2 : tuple[int, ...]
        To construct from.

    Returns
    -------
    bool
        Whether it's possible.

    Examples
    --------
    >>> _matches((3, 4, 5), (1, 2, 4, 5))
    True

    >>> _matches((1, 2, 4, 5), (3, 4, 5))
    False
    """

    def match(i: int, j: int) -> bool:
        if i == len(p1) and j == len(p2):
            return True
        if i == len(p1) or j == len(p2):
            return False

        total = 0
        for k in range(j, len(p2)):
            total += p2[k]
            if total == p1[i]:
                if match(i + 1, k + 1):
                    return True
            elif total > p1[i]:
                break
        return False

    return match(0, 0)


MARY = Pattern([4, 3, 5])
MINNY = Pattern([3, 4, 5])
SUZY = Pattern([2, 5, 5])
DIMMY = Pattern([3, 3, 6])
AUGY = Pattern([4, 4, 4])
JIMMY = Pattern([6, 5, 1])

PATTERN_NAMES = {
    MARY: "Mary",
    MINNY: "Minny",
    SUZY: "Suzy",
    DIMMY: "Dimmy",
    AUGY: "Augy",
    JIMMY: "Jimmy",
}
