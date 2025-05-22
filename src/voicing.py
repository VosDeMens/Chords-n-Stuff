from typing import Sequence

from src.cum_pattern import CumPattern
from src.shape import Shape
from src.note import Note
from src.pattern import Pattern
from src.pitch_class import PitchClass
from src.combination import Combination


class Voicing:
    def __init__(self, notes: Sequence[Note], root: PitchClass | None = None) -> None:
        self.notes = list(notes)
        self.root = root

    def __iter__(self):
        return iter(self.notes)

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, i: int) -> Note:
        return self.notes[i]

    def __add__(self, other: Note | int) -> "Voicing":
        if isinstance(other, Note):
            return Voicing(self.notes + [other])
        else:  # int
            return Voicing([note + other for note in self])

    def __sub__(self, other: int) -> "Voicing":
        return self + (-other)

    def __str__(self) -> str:
        return f"Voicing(Root: {self.root}, Notes: {self.notes})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Voicing):
            return False
        return self.notes == other.notes

    def __hash__(self) -> int:
        return hash(tuple(self.notes))

    @classmethod
    def from_shape(cls, root_note: Note, shape: Shape) -> "Voicing":
        return Voicing([root_note + interval for interval in shape], root_note.pc)

    # @classmethod
    # def dense(cls, combination: Combination, root_degree: int = 3) -> "Voicing":
    #     assert combination.root is not None, "Combination has to have root"
    #     root_note = Note.from_pc(combination.root, root_degree)
    #     notes = [Note.from_pc_at_least(pc, root_note) for pc in combination]
    #     return Voicing(notes, combination.root)

    def fits(
        self, to_fit: Combination | Pattern, optimise_pc_spread: bool = False
    ) -> bool:
        if isinstance(to_fit, Combination):
            for note in self:
                if note.pc not in to_fit:
                    return False

            if optimise_pc_spread:
                return self.has_optimal_pc_spread(len(to_fit))

            return True
        else:  # Pattern
            return self.combination.fits(to_fit) and (
                not optimise_pc_spread or self.has_optimal_pc_spread(len(to_fit))
            )

    def match(self, cum: CumPattern) -> list[PitchClass]:
        return self.combination.match(cum)

    @property
    def combination(self) -> Combination:
        return Combination([note.pc for note in self])

    @property
    def shape(self) -> Shape:
        if not self.notes:
            return Shape([])

        notes_sorted = sorted(self, key=lambda note: note.value)

        if self.root:
            root_note = Note.from_pc_at_most(self.root, notes_sorted[0])
        else:
            root_note = notes_sorted[0]

        return Shape([note - root_note for note in notes_sorted])

    @property
    def pattern(self) -> Pattern:
        return self.combination.pattern

    @property
    def note_count(self) -> dict[Note, int]:
        note_count: dict[Note, int] = {}
        for note in self:
            if note not in note_count:
                note_count[note] = 0
            note_count[note] += 1
        return note_count

    @property
    def pc_count(self) -> dict[PitchClass, int]:
        pc_count: dict[PitchClass, int] = {}
        for pc in [note.pc for note in self]:
            if pc not in pc_count:
                pc_count[pc] = 0
            pc_count[pc] += 1
        return pc_count

    def has_optimal_pc_spread(self, nr_of_pcs: int) -> bool:
        occurences = self.pc_count.values()
        if len(occurences) > nr_of_pcs:
            raise ValueError
        if len(occurences) < nr_of_pcs:
            return max(occurences) == 1
        return max(occurences) - min(occurences) <= 1
