from typing import Sequence

from src.profiler import TimingMeta
from src.cum_pattern import CumPattern
from src.shape import Shape
from src.my_types import int64
from src.note import Note
from src.pattern import Pattern
from src.pitch_class import PitchClass
from src.combination import Combination
from src.util import (
    get_set_bit_indices,
    voicing_bitmask_to_combination_bitmask,
)


class Voicing:
    """A `Voicing` represents a set of specific `Note`s.
    `Voicing`s are unordered and can't contain duplicate notes.
    It is the least abstract way to represent a chord or scale.
    """

    __slots__ = ("bitmask", "_combination", "_pattern", "_notes")

    bitmask: int64
    _combination: Combination | None
    _pattern: Pattern | None
    _notes: list[Note] | None

    def __init__(self, notes: Sequence[Note]):
        bitmask = int64(0)
        for note in notes:
            bitmask |= note.bitmask
        self.bitmask = bitmask
        self._combination = None
        self._pattern = None
        self._notes = None

    @classmethod
    def from_64bit_bitmask(cls, bitmask: int64) -> "Voicing":
        instance = cls.__new__(cls)
        instance.bitmask = bitmask
        instance._combination = None
        instance._pattern = None
        instance._notes = None
        return instance

    def __iter__(self):
        return iter(self.notes)

    def __len__(self):
        return self.bitmask.bit_count()

    def __getitem__(self, i: int) -> Note:
        return self.notes[i]

    def __add__(self, other: "Note | Voicing") -> "Voicing":
        bitmask = self.bitmask | other.bitmask
        return Voicing.from_64bit_bitmask(bitmask)

    def __lshift__(self, i: int) -> "Voicing":
        if i < 0:
            bitmask = int64(self.bitmask << -i)
        else:
            bitmask = int64(self.bitmask >> i)
        if bitmask.bit_count() != self.bitmask.bit_count():
            raise OverflowError()
        return Voicing.from_64bit_bitmask(bitmask)

    def __rshift__(self, i: int) -> "Voicing":
        return self << -i

    def __str__(self) -> str:
        return f"Voicing({self.notes})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Voicing) and self.bitmask == other.bitmask

    def __hash__(self) -> int:
        return int(self.bitmask)

    @classmethod
    def from_shape(cls, root_note: Note, shape: Shape) -> "Voicing":
        bitmask = shape.bitmask << (root_note.value + shape.offset)
        if bitmask.bit_count() != shape.bitmask.bit_count():
            raise OverflowError()
        return Voicing.from_64bit_bitmask(bitmask)

    def fits(self, to_fit: Combination | Pattern) -> bool:
        if isinstance(to_fit, Combination):
            bitmask = voicing_bitmask_to_combination_bitmask(self.bitmask)
            return bitmask & to_fit.bitmask == bitmask
        else:  # Pattern
            return self.pattern in to_fit

    def match(self, cum: CumPattern) -> set[PitchClass]:
        return self.combination.match(cum)

    @property
    def combination(self) -> Combination:
        if self._combination is None:
            self._combination = Combination.from_voicing_bitmask(self.bitmask)
        return self._combination

    @property
    def shape(self) -> Shape:
        return Shape.from_voicing_bitmask_and_root(self.bitmask)

    @property
    def pattern(self) -> Pattern:
        if self._pattern is None:
            self._pattern = Pattern.from_64bit_bitmask(self.bitmask)
        return self._pattern

    @property
    def pc_count(self) -> dict[PitchClass, int]:
        pc_count: dict[PitchClass, int] = {}
        for note in self:
            pc = note.pc
            if pc not in pc_count:
                pc_count[pc] = 0
            pc_count[pc] += 1
        return pc_count

    @property
    def notes(self) -> list[Note]:
        if self._notes is None:
            set_bit_indices = get_set_bit_indices(self.bitmask)
            self._notes = [Note(index) for index in set_bit_indices]
        return self._notes
