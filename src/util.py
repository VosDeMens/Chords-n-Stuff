from functools import cache
from itertools import pairwise
from typing import Sequence, TypeVar
import random


T = TypeVar("T")


@cache
def create_all_rotations(values: Sequence[T]) -> set[tuple[T, ...]]:
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
    return min(create_all_rotations(values))


@cache
def get_inner_intervals(dists_from_root: Sequence[int]) -> tuple[int, ...]:
    """Finds the distances between successive elements in a sequence of integers,
    ending in the distance from the last element back to the first element mod 12.

    Opposite of a cumsum, sort of.

    Examples
    --------
    >>> get_inner_intervals((0, 4, 7))
    (4, 3, 5)
    """
    if not dists_from_root:
        return tuple()
    dists_from_root = sorted(dists_from_root)
    return tuple(b - a for a, b in pairwise(dists_from_root)) + (
        (dists_from_root[0] - dists_from_root[-1]) % 12,
    )


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
