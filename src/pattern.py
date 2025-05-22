from functools import cache
from typing import Sequence
from numpy import cumsum

from src.util import (
    get_inner_intervals,
    get_minimal_rotation,
    rotate_by,
)


class Pattern:
    def __init__(self, intervals: Sequence[int]) -> None:
        assert (
            sum(intervals) % 12 == 0
        ), f"Intervals should sum to 0 (mod 12), {intervals = }"
        intervals_reduced = reduce_intervals(tuple(intervals))
        self.intervals: tuple[int, ...] = get_minimal_rotation(intervals_reduced)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pattern):
            return False
        return self.intervals == other.intervals

    def __hash__(self) -> int:
        return hash(tuple(self.intervals))

    def __len__(self) -> int:
        return len(self.intervals)

    def __contains__(self, other: "Pattern") -> bool:
        for shift in range(len(self)):
            rotated_intervals = rotate_by(self.intervals, shift)

            if _matches(other.intervals, rotated_intervals):
                return True
        return False


@cache
def reduce_intervals(inner_intervals: Sequence[int]) -> tuple[int, ...]:
    cum = [int(d) for d in cumsum(inner_intervals)]
    cum_reduced = [d % 12 for d in cum]
    cum_sorted = tuple(sorted(cum_reduced))
    return get_inner_intervals(cum_sorted)


@cache
def _matches(p1: tuple[int, ...], p2: tuple[int, ...]) -> bool:
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
