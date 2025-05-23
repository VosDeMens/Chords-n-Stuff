from functools import cache
from typing import Iterable

from src.cum_pattern import CumPattern
from src.note import PitchClass
from src.pattern import Pattern
from src.util import get_inner_intervals


class Combination:
    """Represents a set of `PitchClass`s. The concept of C major can be expressed
    by a `Combination`, if the way the chord is voiced is not relevant.
    """

    def __init__(self, pcs: Iterable[PitchClass], root: PitchClass | None = None):
        self.pcs = set(pcs)
        self.root = root

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
        return Combination([root + interval for interval in cum_pattern], root)

    def __iter__(self):
        return iter(self.pcs)

    def __str__(self):
        return f"Combination(Root: {self.root}, PCs: {self.pcs})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Combination):
            return False
        return self.pcs == other.pcs

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.pcs, key=lambda pc: pc.value)))

    def __len__(self) -> int:
        return len(self.pcs)

    def __add__(self, other: "Combination") -> "Combination":
        """Adds together two `Combination`s, by taking the union of the sets they represent.

        The new `Combination` does not have a root.
        """
        return Combination(self.pcs | other.pcs)

    def match(self, cum: CumPattern) -> list[PitchClass]:
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
        roots_for_matches: list[PitchClass] = []
        for pc in self.pcs:
            for interval in cum:
                if not pc + interval in self.pcs:
                    break
            else:
                roots_for_matches.append(pc)
        return roots_for_matches

    def fits(self, pattern: Pattern) -> bool:
        return self.pattern in pattern

    @property
    def pattern(self) -> Pattern:
        return _combination_to_pattern(self)


@cache
def _combination_to_pattern(combination: Combination) -> Pattern:
    return Pattern(get_inner_intervals(tuple(pc.value for pc in combination.pcs)))
