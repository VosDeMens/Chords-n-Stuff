from typing import overload

from math import log

from src.constants import FREQ_ROOT
from src.pitch_class import PitchClass
from src.profiler import TimingMeta


class Note(metaclass=TimingMeta):
    """A `Note` represents one specific pitch, like C4."""

    def __init__(self, value: int):
        if value < 0:
            raise ValueError("Note must be positive")
        self.value = value

    @classmethod
    def from_pc(cls, pc: PitchClass, degree: int) -> "Note":
        """
        Examples
        --------
        >>> Note.from_pc(C, 3)
        C3
        """
        return Note(pc.value + (degree + 2) * 12)

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
        return min(at_least, at_most, key=lambda note: abs(note - ref_note))

    @classmethod
    def from_pcs_closest_to(cls, pcs: list[PitchClass], ref_note: "Note") -> "Note":
        """Creates the `Note` with a `PitchClass` in `pcs` that is closest to `ref_note`."""
        options: list[Note] = []
        for pc in pcs:
            at_least = cls.from_pc_at_least(pc, ref_note)
            at_most = cls.from_pc_at_most(pc, ref_note)
            options.append(at_least)
            options.append(at_most)
        return min(options, key=lambda note: abs(note - ref_note))

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
        return f"{self.pc}{self.value//12-2}"

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, interval: int) -> "Note":
        """
        Examples
        --------
        >>> C4 + 2
        D4
        """
        return Note(self.value + interval)

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
            return self.value - other.value
        else:  # if int
            return Note(self.value - other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Note):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __gt__(self, other: "Note") -> bool:
        return self.value > other.value

    def __ge__(self, other: "Note") -> bool:
        return self.value >= other.value

    @property
    def pc(self):
        return PitchClass(self.value)

    @property
    def degree(self):
        return self.value // 12 - 2

    @property
    def freq(self):
        return 2 ** (self.value / 12) * FREQ_ROOT


C0 = Note(24)
Cs0 = Note(25)
Df0 = Note(25)
D0 = Note(26)
Ds0 = Note(27)
Ef0 = Note(27)
E0 = Note(28)
F0 = Note(29)
Fs0 = Note(30)
Gf0 = Note(30)
G0 = Note(31)
Gs0 = Note(32)
Af0 = Note(32)
A0 = Note(33)
As0 = Note(34)
Bf0 = Note(34)
B0 = Note(35)
C1 = Note(36)
Cs1 = Note(37)
Df1 = Note(37)
D1 = Note(38)
Ds1 = Note(39)
Ef1 = Note(39)
E1 = Note(40)
F1 = Note(41)
Fs1 = Note(42)
Gf1 = Note(42)
G1 = Note(43)
Gs1 = Note(44)
Af1 = Note(44)
A1 = Note(45)
As1 = Note(46)
Bf1 = Note(46)
B1 = Note(47)
C2 = Note(48)
Cs2 = Note(49)
Df2 = Note(49)
D2 = Note(50)
Ds2 = Note(51)
Ef2 = Note(51)
E2 = Note(52)
F2 = Note(53)
Fs2 = Note(54)
Gf2 = Note(54)
G2 = Note(55)
Gs2 = Note(56)
Af2 = Note(56)
A2 = Note(57)
As2 = Note(58)
Bf2 = Note(58)
B2 = Note(59)
C3 = Note(60)
Cs3 = Note(61)
Df3 = Note(61)
D3 = Note(62)
Ds3 = Note(63)
Ef3 = Note(63)
E3 = Note(64)
F3 = Note(65)
Fs3 = Note(66)
Gf3 = Note(66)
G3 = Note(67)
Gs3 = Note(68)
Af3 = Note(68)
A3 = Note(69)
As3 = Note(70)
Bf3 = Note(70)
B3 = Note(71)
C4 = Note(72)
Cs4 = Note(73)
Df4 = Note(73)
D4 = Note(74)
Ds4 = Note(75)
Ef4 = Note(75)
E4 = Note(76)
F4 = Note(77)
Fs4 = Note(78)
Gf4 = Note(78)
G4 = Note(79)
Gs4 = Note(80)
Af4 = Note(80)
A4 = Note(81)
As4 = Note(82)
Bf4 = Note(82)
B4 = Note(83)
C5 = Note(84)
Cs5 = Note(85)
Df5 = Note(85)
D5 = Note(86)
Ds5 = Note(87)
Ef5 = Note(87)
E5 = Note(88)
F5 = Note(89)
Fs5 = Note(90)
Gf5 = Note(90)
G5 = Note(91)
Gs5 = Note(92)
Af5 = Note(92)
A5 = Note(93)
As5 = Note(94)
Bf5 = Note(94)
B5 = Note(95)
C6 = Note(96)
Cs6 = Note(97)
Df6 = Note(97)
D6 = Note(98)
Ds6 = Note(99)
Ef6 = Note(99)
E6 = Note(100)
F6 = Note(101)
Fs6 = Note(102)
Gf6 = Note(102)
G6 = Note(103)
Gs6 = Note(104)
Af6 = Note(104)
A6 = Note(105)
As6 = Note(106)
Bf6 = Note(106)
B6 = Note(107)
C7 = Note(108)
Cs7 = Note(109)
Df7 = Note(109)
D7 = Note(110)
Ds7 = Note(111)
Ef7 = Note(111)
E7 = Note(112)
F7 = Note(113)
Fs7 = Note(114)
Gf7 = Note(114)
G7 = Note(115)
Gs7 = Note(116)
Af7 = Note(116)
A7 = Note(117)
As7 = Note(118)
Bf7 = Note(118)
B7 = Note(119)
