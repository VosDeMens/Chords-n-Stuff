from functools import cache
from itertools import pairwise
from typing import Sequence, TypeVar
import random


T = TypeVar("T")


@cache
def get_all_rotations(values: Sequence[T]) -> set[tuple[T, ...]]:
    """
    Examples
    --------
    >>> create_all_rotations((1, 2, 3))
    {(1, 2, 3), (2, 3, 1), (3, 1, 2)}
    """
    values_tup = tuple(values)
    return {rotate_by(values_tup, i) for i in range(len(values))}


@cache
def rotate_by(values: Sequence[T], shift: int) -> tuple[T, ...]:
    """
    Examples
    --------
    >>> rotate_by((1, 2, 3), 1)
    (2, 3, 1), (3, 1, 2)
    """
    tup = tuple(values)
    return tup[shift:] + tup[:shift]


@cache
def get_minimal_rotation(values: Sequence[T]) -> tuple[T, ...]:
    """Picks the smallest possible rotation according to tuple ordering.
    Examples
    --------
    >>> rotate_by((4, 1, 6))
    (1, 6, 4)
    """
    return min(get_all_rotations(values))


@cache
def get_inner_intervals(intervals_from_root: Sequence[int]) -> tuple[int, ...]:
    """Finds the distances between successive elements in a sequence of integers,
    ending in the distance from the last element back to the first element mod 12.

    Opposite of a cumsum, sort of.

    Examples
    --------
    >>> get_inner_intervals((0, 4, 7))
    (4, 3)
    """
    if not intervals_from_root:
        return ()
    return tuple(b - a for a, b in pairwise(intervals_from_root))


@cache
def get_intervals_from_root(
    inner_intervals: Sequence[int], d_root_to_first_note: int = 0
) -> tuple[int, ...]:
    """Finds the intervals from the root from the inner intervals (cumulative sum).

    Examples
    --------
    >>> get_intervals_from_root((3, 4, 5))
    (0, 3, 7)

    >>> get_intervals_from_root((3, 4, 5), 1)
    (1, 4, 8)
    """
    assert sum(inner_intervals) % 12 == 0, "inner intervals have to sum to 0 mod 12"

    if not inner_intervals:
        return ()
    intervals_from_root: list[int] = [d_root_to_first_note]
    for inner in inner_intervals[:-1]:
        intervals_from_root.append(intervals_from_root[-1] + inner)
    return tuple(intervals_from_root)


def weighted_pick(options: dict[T, float]) -> T:
    """Performs a weigthed pick, where the probability of an element being picked
    is directly proportional to its value.

    Parameters
    ----------
    options : dict[T, float]
        Dictionary of elements to be picked to their value.

    Returns
    -------
    T
        The picked element.
    """
    ts = list(options.keys())
    weights = list(options.values())
    if all(weight == 0 for weight in weights):
        weights = [1 for _ in ts]
    return random.choices(ts, weights=weights, k=1)[0]
