from typing import Iterable, overload

from src.profiler import TimingMeta
from src.cum_pattern import CumPattern
from src.my_types import int16, int64
from src.pitch_class import PitchClass
from src.pattern import Pattern
from src.util import (
    get_all_12bit_bitmask_rotations,
    get_set_bit_indices,
    is_12bit,
    rotate_12bit_bitmask_left,
    voicing_bitmask_to_combination_bitmask,
)


class Combination:
    """Represents a set of `PitchClass`es. The concept of C major can be expressed
    by a `Combination`, if the way the chord is voiced is not relevant.
    """

    __slots__ = ("bitmask",)

    bitmask: int16

    _instances: dict[int16, "Combination"] = {}

    def __new__(cls, pcs: Iterable[PitchClass]) -> "Combination":
        bitmask = int16(0)
        for pc in pcs:
            bitmask |= pc.bitmask
        return cls._get_or_create(bitmask)

    @classmethod
    def _get_or_create(cls, bitmask: int16) -> "Combination":
        assert is_12bit(bitmask), f"{bitmask = }"
        if bitmask in cls._instances:
            return cls._instances[bitmask]

        instance = super().__new__(cls)
        instance.bitmask = bitmask
        cls._instances[bitmask] = instance

        return instance

    @classmethod
    def from_cum(cls, root: PitchClass, cum_pattern: CumPattern) -> "Combination":
        """Creates a `Combination` from a root (`PitchClass`) and a `CumPattern`.

        Parameters
        ----------
        root : PitchClass
            The `PitchClass` to consider 0 in `cum_pattern`.
        cum_pattern : CumPattern
            The `CumPattern` from which to create a `Combination`.
        """
        bitmask = rotate_12bit_bitmask_left(cum_pattern.bitmask, root.value)
        return cls._get_or_create(bitmask)

    @classmethod
    def from_voicing_bitmask(cls, voicing_bitmask: int64) -> "Combination":
        bitmask = voicing_bitmask_to_combination_bitmask(voicing_bitmask)
        return cls._get_or_create(bitmask)

    @classmethod
    def all_from_pattern(cls, pattern: Pattern) -> "list[Combination]":
        all_bitmask_rotations = get_all_12bit_bitmask_rotations(pattern.bitmask)
        return [cls._get_or_create(rotation) for rotation in all_bitmask_rotations]

    def __iter__(self):
        return iter(self.pcs)

    def __str__(self):
        return f"Combination(PCs: {self.pcs})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Combination) and self.bitmask == other.bitmask

    def __hash__(self) -> int:
        return int(self.bitmask)

    def __len__(self) -> int:
        return self.bitmask.bit_count()

    def __contains__(self, other: "Combination | PitchClass") -> bool:
        if isinstance(other, Combination):
            return other.bitmask & self.bitmask == other.bitmask
        else:  # PitchClass
            return bool((int16(1) << int16(other.value)) & self.bitmask)

    @overload
    def __add__(self, other: "Combination") -> "Combination":
        """Adds together two `Combination`s, by taking the union of the sets they represent.

        The new `Combination` does not have a root.
        """
        ...

    @overload
    def __add__(self, other: PitchClass) -> "Combination":
        """Returns a new `Combination` with the `PitchClass`es in self, together with `other`."""
        ...

    def __add__(self, other: "Combination | PitchClass") -> "Combination":
        bitmask = self.bitmask | other.bitmask
        return Combination._get_or_create(bitmask)

    def match(self, cum: CumPattern) -> set[PitchClass]:
        """Finds all of the roots from which `cum` could be built using the notes in `self`.

        Parameters
        ----------
        cum : CumPattern
            The `CumPattern` we want to match for.

        Returns
        -------
        list[PitchClass]
            All of the roots from which `cum` could be built using the notes in `self`.
        """
        roots_for_matches: set[PitchClass] = set()
        for pc in self.pcs:
            rotated = rotate_12bit_bitmask_left(cum.bitmask, pc.value)
            if rotated & self.bitmask == rotated:
                roots_for_matches.add(pc)
        return roots_for_matches

    def fits(self, pattern: Pattern) -> bool:
        return self.pattern in pattern

    @property
    def pcs(self) -> set[PitchClass]:
        set_bit_indices = get_set_bit_indices(self.bitmask)
        return {PitchClass(index) for index in set_bit_indices}

    @property
    def pattern(self) -> Pattern:
        return Pattern.from_12bit_bitmask(self.bitmask)
