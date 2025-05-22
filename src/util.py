from functools import cache
from itertools import pairwise
from typing import Sequence, TypeVar
import random


T = TypeVar("T")


@cache
def create_all_rotations(values: Sequence[T]) -> list[tuple[T, ...]]:
    values_tup = tuple(values)
    return [rotate_by(values_tup, i) for i in range(len(values))]


@cache
def rotate_by(values: Sequence[T], shift: int) -> tuple[T, ...]:
    tup = tuple(values)
    return tup[shift:] + tup[:shift]


@cache
def get_minimal_rotation(values: Sequence[T]) -> tuple[T, ...]:
    return min(create_all_rotations(values))


@cache
def get_inner_intervals(dists_from_root: Sequence[int]) -> tuple[int, ...]:
    return tuple(b - a for a, b in pairwise(dists_from_root)) + (
        12 + dists_from_root[0] - dists_from_root[-1],
    )


def weighted_pick(options: dict[T, float]) -> T:
    ts = list(options.keys())
    weights = list(options.values())
    if all(weight == 0 for weight in weights):
        weights = [1 for _ in ts]
    return random.choices(ts, weights=weights, k=1)[0]
