from typing import Iterable

from src.cum_pattern import CumPattern
from src.my_types import int64
from src.note import Note
from src.pattern import Pattern
from src.profiler import TimingMeta
from src.util import get_first_set_bit_index, tetris_64bit_bitmask


class Shape:
    """A `Shape` represents a chord shape, as a `set` of intervals from an arbitrary root.
    Can't contain duplicates. CAN contain negative intervals.
    """

    __slots__ = ("bitmask", "offset")

    bitmask: int64
    offset: int

    def __init__(self, intervals_from_root: Iterable[int]):
        assert (
            max(intervals_from_root) - max(intervals_from_root) < 64
        ), "range too large"
        bitmask = int64(0)
        min_interval = min(intervals_from_root)
        if min_interval < 0:
            intervals_from_root_positive = [
                interval - min_interval for interval in intervals_from_root
            ]
        else:
            intervals_from_root_positive = intervals_from_root
        for interval in intervals_from_root_positive:
            bitmask |= int64(1) << int64(interval)
        bitmask = tetris_64bit_bitmask(bitmask)
        self.bitmask = bitmask
        self.offset = min_interval

    @classmethod
    def _from_64bit_bitmask_and_offset(cls, bitmask: int64, offset: int) -> "Shape":
        instance = cls.__new__(cls)
        instance.bitmask = bitmask
        instance.offset = offset
        return instance

    @classmethod
    def from_voicing_bitmask_and_root(
        cls, voicing_bitmask: int64, root: Note | None = None
    ) -> "Shape":
        if not voicing_bitmask:
            return Shape._from_64bit_bitmask_and_offset(int64(0), 0)

        bitmask = tetris_64bit_bitmask(voicing_bitmask)
        if root is None:
            offset = 0
        else:
            offset = int(get_first_set_bit_index(voicing_bitmask) - root.value)
        return Shape._from_64bit_bitmask_and_offset(bitmask, offset)

    @property
    def pattern(self) -> Pattern:
        return Pattern.from_64bit_bitmask(self.bitmask)

    @property
    def cum_pattern(self) -> CumPattern:
        return CumPattern.from_shape_bitmask_and_offset(self.bitmask, self.offset)

    @property
    def intervals_from_root(self) -> list[int]:
        intervals_from_root: list[int] = []
        for i in range(64):
            if self.bitmask & (int64(1) << int64(i)):
                intervals_from_root.append(i)
        return intervals_from_root

    def __add__(self, other: "int | int64 | Shape") -> "Shape":
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
        if isinstance(other, Shape):
            if self.offset > other.offset:
                w_higher_offset = self
                w_lower_offset = other
            else:
                w_higher_offset = other
                w_lower_offset = self

            d_offset = int64(w_higher_offset.offset - w_lower_offset.offset)

            bitmask_w_higher_offset_shifted = w_higher_offset.bitmask << d_offset

            if (
                bitmask_w_higher_offset_shifted.bit_count()
                != w_higher_offset.bitmask.bit_count()
            ):
                raise OverflowError()

            bitmask = bitmask_w_higher_offset_shifted | w_lower_offset.bitmask
            offset = w_lower_offset.offset

            return Shape._from_64bit_bitmask_and_offset(bitmask, offset)

        else:  # int | int64
            if other < self.offset:
                bitmask = self.bitmask << int64(self.offset - other)
                if bitmask.bit_count() != self.bitmask.bit_count():
                    raise OverflowError()
                bitmask |= int64(1)
                offset = int(other)
            else:
                bitmask = self.bitmask | (int64(1) << (int64(other) - self.offset))
                offset = self.offset
            return Shape._from_64bit_bitmask_and_offset(bitmask, offset)

    def __iter__(self):
        return iter(self.intervals_from_root)

    def __len__(self):
        return self.bitmask.bit_count()

    def __str__(self):
        return f"Shape({self.intervals_from_root})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other: object):
        return (
            isinstance(other, Shape)
            and self.bitmask == other.bitmask
            and self.offset == other.offset
        )

    def __hash__(self) -> int:
        return int(self.bitmask)
