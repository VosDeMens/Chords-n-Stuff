from functools import lru_cache
import numpy as np
from typing import Iterable, Sequence, TypeVar
import random

from src.constants import MASK_12BIT
from src.my_types import int16, int16list, int64


T = TypeVar("T")


@lru_cache
def get_all_12bit_bitmask_rotations(bitmask: int16) -> int16list:
    """Get all 12 rotations of the bitmask.

    Parameters
    ----------
    bitmask : int16
        The 12-bit integer to rotate.

    Returns
    -------
    int16list
        A list of all 12 rotations of the bitmask.
    """
    return np.array(
        [rotate_12bit_bitmask_right(bitmask, i) for i in range(12)], dtype=int16
    )


@lru_cache
def get_normal_form_12bit_bitmask(bitmask: int16) -> int16:
    """Get the lexicographically smallest rotation starting with bit 0 set.

    This is the normal form of a pattern.

    Parameters
    ----------
    bitmask : int16
        The 12-bit integer to normalize.

    Returns
    -------
    int16
        The lexicographically smallest rotation of the bitmask.
    """
    rotations = get_all_12bit_bitmask_rotations(bitmask)
    return min(rotations)


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


def inner_intervals_to_cum_pattern_bitmask(inner_intervals: Sequence[int]) -> int16:
    """Convert inner intervals to a `CumPattern` bitmask.

    Parameters
    ----------
    inner_intervals : Sequence[int]
        A sequence of intervals that sum to 12, representing the inner structure of a cumulative pattern.

    Returns
    -------
    int16
        A 12-bit integer representing the cumulative pattern, where each bit corresponds to a position in the cumulative pattern.
    """
    bitmask = int16(0)
    pos = 0
    for interval in inner_intervals:
        bitmask |= int16(1) << int16(pos)
        pos = (pos + interval) % 12
    return bitmask


def intervals_from_root_to_cum_pattern_bitmask(
    intervals_from_root: Iterable[int],
) -> int16:
    """Convert intervals from root to a `CumPattern` bitmask.

    Parameters
    ----------
    intervals_from_root : Sequence[int]
        A sequence of intervals from the root note.

    Returns
    -------
    int16
        A 12-bit integer representing the cumulative pattern.
    """
    bitmask = int16(0)
    for interval in intervals_from_root:
        bitmask |= int16(1) << int16(interval % 12)
    return bitmask


@lru_cache
def rotate_12bit_bitmask_right(bitmask: int16, n: int | int16) -> int16:
    """Rotate bitmask right by n positions within 12 bits.

    Parameters
    ----------
    bitmask : int16
        The bitmask to rotate.
    n : int
        The number of positions to rotate the bitmask to the right.
    Returns
    -------
    int16
        The rotated bitmask, ensuring it remains within 12 bits.
    """
    assert is_12bit(bitmask), f"{bitmask = }"
    n = n % 12
    return ((bitmask >> int16(n)) | (bitmask << int16(12 - n))) & MASK_12BIT


@lru_cache
def rotate_12bit_bitmask_left(bitmask: int16, n: int | int16) -> int16:
    """Rotate bitmask left by n positions within 12 bits.

    Parameters
    ----------
    bitmask : int16
        The bitmask to rotate.
    n : int
        The number of positions to rotate the bitmask to the left.
    Returns
    -------
    int16
        The rotated bitmask, ensuring it remains within 12 bits.
    """
    assert is_12bit(bitmask), f"{bitmask = }"
    n = n % 12
    return ((bitmask << int16(n)) | (bitmask >> int16(12 - n))) & MASK_12BIT


@lru_cache
def tetris_12bit_bitmask(bitmask: int16) -> int16:
    """Shift the bitmask right until the least significant set bit is at bit 0.

    Parameters
    ----------
    bitmask : int16
        The bitmask to shift.

    Returns
    -------
    int16
        The shifted bitmask with the first set bit at position 0
    """
    assert is_12bit(bitmask), f"{bitmask = }"
    assert bitmask, f"{bitmask = }"

    first_set_bit_index = get_first_set_bit_index(bitmask)
    tetrissed_bitmask = bitmask >> int16(first_set_bit_index)

    return tetrissed_bitmask


@lru_cache
def tetris_64bit_bitmask(bitmask: int64) -> int64:
    """Shift the bitmask right until the least significant set bit is at bit 0.

    Parameters
    ----------
    bitmask : int64
        The bitmask to shift.

    Returns
    -------
    int64
        The shifted bitmask with the first set bit at position 0.
    """
    assert bitmask, "Bitmask must be non-empty."

    first_set_bit_index = get_first_set_bit_index(bitmask)
    tetrissed_bitmask = bitmask >> int64(first_set_bit_index)

    return tetrissed_bitmask


@lru_cache
def voicing_bitmask_to_combination_bitmask(voicing_bitmask: int64) -> int16:
    bitmask = int16(0)

    for _ in range(6):
        bitmask |= int16(voicing_bitmask & MASK_12BIT)
        voicing_bitmask >>= int64(12)
    return bitmask


def note_bitmask_to_pitch_class_bitmask(note_bitmask: int64) -> int16:
    # These are equivalent
    return voicing_bitmask_to_combination_bitmask(note_bitmask)


def shape_bitmask_and_offset_to_cum_pattern_bitmask(
    shape_bitmask: int64, offset: int
) -> int16:
    bitmask = voicing_bitmask_to_combination_bitmask(shape_bitmask)
    bitmask = rotate_12bit_bitmask_left(bitmask, int16(offset % 12))

    return bitmask


@lru_cache
def get_set_bit_indices(x: int16 | int64 | int) -> list[int]:
    indices: list[int] = []
    item = x if isinstance(x, int) else x.item()
    while item:
        index = get_first_set_bit_index(item)
        indices.append(index)
        item &= item - 1
    return indices


@lru_cache
def get_first_set_bit_index(x: int16 | int64 | int) -> int:
    item = x if isinstance(x, int) else x.item()
    lsb = item & -item
    index = lsb.bit_length() - 1
    return index


def is_12bit(x: int16) -> bool:
    return x & MASK_12BIT == x


# @cache
# def get_inner_intervals(intervals_from_root: Sequence[int]) -> tuple[int, ...]:
#     """Finds the distances between successive elements in a sequence of integers,
#     ending in the distance from the last element back to the first element mod 12.

#     Opposite of a cumsum, sort of.

#     Examples
#     --------
#     >>> get_inner_intervals((0, 4, 7))
#     (4, 3)
#     """
#     if not intervals_from_root:
#         return ()
#     return tuple(b - a for a, b in pairwise(intervals_from_root))


# @cache
# def get_intervals_from_root(
#     inner_intervals: Sequence[int], d_root_to_first_note: int = 0
# ) -> tuple[int, ...]:
#     """Finds the intervals from the root from the inner intervals (cumulative sum).

#     Examples
#     --------
#     >>> get_intervals_from_root((3, 4, 5))
#     (0, 3, 7)

#     >>> get_intervals_from_root((3, 4, 5), 1)
#     (1, 4, 8)
#     """
#     assert sum(inner_intervals) % 12 == 0, "inner intervals have to sum to 0 mod 12"

#     if not inner_intervals:
#         return ()
#     intervals_from_root: list[int] = [d_root_to_first_note]
#     for inner in inner_intervals[:-1]:
#         intervals_from_root.append(intervals_from_root[-1] + inner)
#     return tuple(intervals_from_root)
