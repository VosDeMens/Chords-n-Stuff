from typing import Iterable

from src.combination import Combination
from src.cum_pattern import CumPattern
from src.note import Note
from src.pattern import Pattern
from src.pitch_class import PitchClass
from src.profiler import TimingMeta
from src.shape import Shape
from src.voicing import Voicing


class Distribution:

    __slots__ = ("notes", "_voicing", "_pc_count")

    notes: list[Note]
    _voicing: Voicing | None
    _pc_count: dict[PitchClass, int] | None

    def __init__(self, notes: Iterable[Note]):
        self.notes = list(notes)
        self._voicing = None
        self._pc_count = None

    @classmethod
    def from_shape_and_root(cls, root: Note, shape: Shape) -> "Distribution":
        return Distribution([root + (shape.offset + interval) for interval in shape])

    def __iter__(self):
        return iter(self.notes)

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, i: int) -> Note:
        return self.notes[i]

    def __add__(self, other: Note) -> "Distribution":
        return Distribution([*self.notes, other])

    def __lshift__(self, i: int) -> "Distribution":
        notes = [note << i for note in self.notes]
        return Distribution(notes)

    def __rshift__(self, i: int) -> "Distribution":
        return self << -i

    def __str__(self) -> str:
        return f"Distribution({self.notes})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Distribution) and self.notes == other.notes

    def __hash__(self) -> int:
        return hash(tuple(note for note in self.notes))

    @property
    def voicing(self) -> Voicing:
        if self._voicing is None:
            self._voicing = Voicing(self.notes)
        return self._voicing

    def fits(
        self, to_fit: Combination | Pattern, optimise_pc_spread: bool = False
    ) -> bool:
        voicing = self.voicing
        if not voicing.fits(to_fit):
            return False
        if not optimise_pc_spread:
            return True
        return self.has_optimal_pc_spread(len(to_fit))

    def match(self, cum: CumPattern) -> set[PitchClass]:
        return self.voicing.match(cum)

    @property
    def combination(self) -> Combination:
        return self.voicing.combination

    @property
    def shape(self) -> Shape:
        return self.voicing.shape

    @property
    def pattern(self) -> Pattern:
        return self.voicing.pattern

    @property
    def pc_count(self) -> dict[PitchClass, int]:
        if self._pc_count is None:
            pc_count: dict[PitchClass, int] = {}
            for note in self:
                pc = note.pc
                if pc not in pc_count:
                    pc_count[pc] = 0
                pc_count[pc] += 1
            self._pc_count = pc_count
        return self._pc_count

    def has_optimal_pc_spread(self, nr_of_pcs: int) -> bool:
        pc_count = self.pc_count
        occurences = list(pc_count.values())
        if len(occurences) > nr_of_pcs:
            raise ValueError
        if len(occurences) < nr_of_pcs:
            return max(occurences) == 1
        return max(occurences) - min(occurences) <= 1
