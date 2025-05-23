from typing import overload


class PitchClass:
    """A `PitchClass` represents a class of notes that are spaced apart by octaves.

    The concept of C can be expressed as a `PitchClass`.
    """

    def __init__(self, value: int):
        self._value = value % 12

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

    @property
    def value(self) -> int:
        return self._value

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
        return PitchClass(self._value + other)

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
            return (self._value - other._value) % 12
        else:  # if int
            return PitchClass(self._value - other)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PitchClass):
            return self._value == other._value
        if isinstance(other, int):
            return self._value == other
        return False

    def __hash__(self) -> int:
        return hash(self._value)


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
