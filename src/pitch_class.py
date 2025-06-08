from typing import overload

from src.my_types import int16, int64
from src.profiler import TimingMeta
from src.util import (
    is_12bit,
    note_bitmask_to_pitch_class_bitmask,
    rotate_12bit_bitmask_left,
)


class PitchClass(metaclass=TimingMeta):
    """A `PitchClass` represents a class of notes that are spaced apart by octaves.

    The concept of C can be expressed as a `PitchClass`.
    """

    __slots__ = ("bitmask",)

    bitmask: int16

    _instances: dict[int16, "PitchClass"] = {}

    def __new__(cls, value: int | int16 | int64):
        bitmask = int16(1) << int16(value % 12)
        return cls._from_12bit_bitmask(bitmask)

    @classmethod
    def _from_12bit_bitmask(cls, bitmask: int16) -> "PitchClass":
        assert is_12bit(bitmask), f"{bitmask = }"
        assert bitmask.bit_count() == 1, f"{bitmask.bit_count() = }"
        return cls._get_or_create(bitmask)

    @classmethod
    def _get_or_create(cls, bitmask: int16) -> "PitchClass":
        if bitmask in cls._instances:
            return cls._instances[bitmask]

        instance = super().__new__(cls)
        instance.bitmask = bitmask
        cls._instances[bitmask] = instance

        return instance

    @classmethod
    def from_note_bitmask(cls, note_bitmask: int64) -> "PitchClass":
        bitmask = note_bitmask_to_pitch_class_bitmask(note_bitmask)
        return PitchClass._from_12bit_bitmask(bitmask)

    @classmethod
    def from_str(cls, s: str) -> "PitchClass":
        """
        Examples
        --------
        >>> PitchClass("C#")
        Cs

        Can't use the # symbol in variable names, but it's used in string representations.
        """
        return PC_NAMES_REV[s]

    def __str__(self) -> str:
        return PC_NAMES[self]

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other: int) -> "PitchClass":
        """
        Examples
        --------
        >>> C + 2
        D
        """
        bitmask = rotate_12bit_bitmask_left(self.bitmask, other)
        return PitchClass._from_12bit_bitmask(bitmask)

    @overload
    def __sub__(self, other: "PitchClass") -> int:
        """
        Examples
        --------
        >>> D - C
        2

        >>> C - D
        10
        """
        ...

    @overload
    def __sub__(self, other: int) -> "PitchClass":
        """
        Examples
        --------
        >>> D - 2
        C

        >>> C - 10
        D
        """
        ...

    def __sub__(self, other: "PitchClass | int") -> "PitchClass | int":
        if isinstance(other, PitchClass):
            return (self.value - other.value) % 12
        else:  # int
            return PitchClass(int(self.value) - other)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PitchClass) and self.bitmask == other.bitmask

    def __hash__(self) -> int:
        return int(self.bitmask)

    @property
    def value(self) -> int16:
        return int16(self.bitmask.item().bit_length() - 1)


C = PitchClass(0)
Cs = PitchClass(1)
Df = PitchClass(1)
D = PitchClass(2)
Ds = PitchClass(3)
Ef = PitchClass(3)
E = PitchClass(4)
F = PitchClass(5)
Fs = PitchClass(6)
Gf = PitchClass(6)
G = PitchClass(7)
Gs = PitchClass(8)
Af = PitchClass(8)
A = PitchClass(9)
As = PitchClass(10)
Bf = PitchClass(10)
B = PitchClass(11)

PC_NAMES = {
    C: "C",
    Df: "Db",
    D: "D",
    Ef: "Eb",
    E: "E",
    F: "F",
    Fs: "F#",
    G: "G",
    Af: "Ab",
    A: "A",
    Bf: "Bb",
    B: "B",
}

ALL_PCS = list(sorted(PC_NAMES.keys(), key=lambda pc: int(pc.bitmask)))

ALTERNATIVE_PC_NAMES = {
    Cs: "C#",
    Ds: "D#",
    Gf: "Gb",
    Gs: "G#",
    As: "A#",
}

PC_NAMES_REV = {
    v: k for k, v in tuple(PC_NAMES.items()) + tuple(ALTERNATIVE_PC_NAMES.items())
}
