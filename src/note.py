from typing import overload

from math import log
import numpy as np

from src.constants import FREQ_ROOT
from src.my_types import int64
from src.pitch_class import PitchClass
from src.profiler import TimingMeta


class Note:
    """A `Note` represents one specific pitch, like C4."""

    __slots__ = ("bitmask",)

    bitmask: int64

    _instances: dict[int64, "Note"] = {}

    def __new__(cls, value: int) -> "Note":
        assert 0 <= value < 64, "out of bounds"
        bitmask = int64(1) << int64(value)
        return cls.from_64bit_bitmask(bitmask)

    @classmethod
    def from_64bit_bitmask(cls, bitmask: int64) -> "Note":
        assert bitmask.bit_count() == 1, f"{bitmask.bit_count() = }"
        return cls._get_or_create(bitmask)

    @classmethod
    def _get_or_create(cls, bitmask: int64) -> "Note":
        if bitmask in cls._instances:
            return cls._instances[bitmask]

        instance = super().__new__(cls)
        instance.bitmask = bitmask
        cls._instances[bitmask] = instance

        return instance

    @classmethod
    def from_pc(cls, pc: PitchClass, degree: int) -> "Note":
        """
        Examples
        --------
        >>> Note.from_pc(C, 3)
        C3
        """
        bitmask = int64(pc.bitmask) << int64(degree * 12)
        return Note.from_64bit_bitmask(bitmask)

    @classmethod
    def from_pc_at_least(cls, pc: PitchClass, ref_note: "Note") -> "Note":
        """
        Examples
        --------
        >>> Note.from_pc_at_least(D, C3)
        D3
        """
        d_to_ref = pc - ref_note.pc
        return ref_note + d_to_ref

    @classmethod
    def from_pc_at_most(cls, pc: PitchClass, ref_note: "Note") -> "Note":
        """
        Examples
        --------
        >>> Note.from_pc_at_most(C, D3)
        C3
        """
        d_to_ref = ref_note.pc - pc
        return ref_note - d_to_ref

    @classmethod
    def from_pc_closest_to(cls, pc: PitchClass, ref_note: "Note") -> "Note":
        """
        Examples
        --------
        >>> Note.from_pc_closest_to(C, E4)
        C4
        """
        at_least = cls.from_pc_at_least(pc, ref_note)
        at_most = cls.from_pc_at_most(pc, ref_note)
        return min(at_least, at_most, key=lambda note: np.abs(note - ref_note))

    @classmethod
    def from_pcs_closest_to(cls, pcs: list[PitchClass], ref_note: "Note") -> "Note":
        """Creates the `Note` with a `PitchClass` in `pcs` that is closest to `ref_note`."""
        options: list[Note] = []
        for pc in pcs:
            at_least = cls.from_pc_at_least(pc, ref_note)
            at_most = cls.from_pc_at_most(pc, ref_note)
            options.append(at_least)
            options.append(at_most)
        return min(options, key=lambda note: np.abs(note - ref_note))

    @classmethod
    def from_str(cls, s: str) -> "Note":
        """
        Examples
        --------
        >>> Note.from_str("C3")
        C3
        """
        letters = s[:-1]
        number = int(s[-1])
        return cls.from_pc(PitchClass.from_str(letters), number)

    @classmethod
    def from_freq(cls, freq: float) -> "Note":
        """Creates the note whose frequency is closest to `freq`."""
        return Note(round(log(freq / FREQ_ROOT, 2) * 12))

    def __str__(self) -> str:
        return f"{self.pc}{self.value//12}"

    def __repr__(self) -> str:
        return str(self)

    def __lshift__(self, i: int) -> "Note":
        if i < 0:
            bitmask = int64(self.bitmask << -i)
        else:
            bitmask = int64(self.bitmask >> i)
        return Note.from_64bit_bitmask(bitmask)

    def __rshift__(self, i: int) -> "Note":
        return self << -i

    def __add__(self, interval: int) -> "Note":
        return self << -interval

    @overload
    def __sub__(self, other: "Note") -> int:
        """
        Examples
        --------
        >>> D4 - C4
        2
        """
        ...

    @overload
    def __sub__(self, other: int) -> "Note":
        """
        Examples
        --------
        >>> D4 - 2
        C4
        """
        ...

    def __sub__(self, other: "Note | int") -> "Note | int":
        if isinstance(other, Note):
            return int(self.value) - int(other.value)
        else:  # int
            return self << other

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Note) and self.bitmask == other.bitmask

    def __hash__(self) -> int:
        return int(self.bitmask)

    def __gt__(self, other: "Note") -> bool:
        return bool(self.value > other.value)

    def __ge__(self, other: "Note") -> bool:
        return bool(self.value >= other.value)

    @property
    def pc(self) -> PitchClass:
        return PitchClass.from_note_bitmask(self.bitmask)

    @property
    def degree(self) -> int:
        return int(self.value) // 12

    @property
    def freq(self) -> float:
        return 2 ** float(self.value / 12) * FREQ_ROOT

    @property
    def midi_value(self) -> int:
        return int(self.value) + 24

    @property
    def value(self) -> int64:
        return int64(self.bitmask.item().bit_length() - 1)


C0 = Note(0)
Cs0 = Note(1)
Df0 = Note(1)
D0 = Note(2)
Ds0 = Note(3)
Ef0 = Note(3)
E0 = Note(4)
F0 = Note(5)
Fs0 = Note(6)
Gf0 = Note(6)
G0 = Note(7)
Gs0 = Note(8)
Af0 = Note(8)
A0 = Note(9)
As0 = Note(10)
Bf0 = Note(10)
B0 = Note(11)
C1 = Note(12)
Cs1 = Note(13)
Df1 = Note(13)
D1 = Note(14)
Ds1 = Note(15)
Ef1 = Note(15)
E1 = Note(16)
F1 = Note(17)
Fs1 = Note(18)
Gf1 = Note(18)
G1 = Note(19)
Gs1 = Note(20)
Af1 = Note(20)
A1 = Note(21)
As1 = Note(22)
Bf1 = Note(22)
B1 = Note(23)
C2 = Note(24)
Cs2 = Note(25)
Df2 = Note(25)
D2 = Note(26)
Ds2 = Note(27)
Ef2 = Note(27)
E2 = Note(28)
F2 = Note(29)
Fs2 = Note(30)
Gf2 = Note(30)
G2 = Note(31)
Gs2 = Note(32)
Af2 = Note(32)
A2 = Note(33)
As2 = Note(34)
Bf2 = Note(34)
B2 = Note(35)
C3 = Note(36)
Cs3 = Note(37)
Df3 = Note(37)
D3 = Note(38)
Ds3 = Note(39)
Ef3 = Note(39)
E3 = Note(40)
F3 = Note(41)
Fs3 = Note(42)
Gf3 = Note(42)
G3 = Note(43)
Gs3 = Note(44)
Af3 = Note(44)
A3 = Note(45)
As3 = Note(46)
Bf3 = Note(46)
B3 = Note(47)
C4 = Note(48)
Cs4 = Note(49)
Df4 = Note(49)
D4 = Note(50)
Ds4 = Note(51)
Ef4 = Note(51)
E4 = Note(52)
F4 = Note(53)
Fs4 = Note(54)
Gf4 = Note(54)
G4 = Note(55)
Gs4 = Note(56)
Af4 = Note(56)
A4 = Note(57)
As4 = Note(58)
Bf4 = Note(58)
B4 = Note(59)
C5 = Note(60)
Cs5 = Note(61)
Df5 = Note(61)
D5 = Note(62)
Ds5 = Note(63)
Ef5 = Note(63)
