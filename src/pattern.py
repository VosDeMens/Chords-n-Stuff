from src.util import get_minimal_translation


class Pattern:
    def __init__(self, intervals: tuple[int, ...]) -> None:
        assert sum(intervals) == 12, "Intervals should sum to 12"
        self.intervals = get_minimal_translation(intervals)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pattern):
            return False
        return self.intervals == other.intervals

    def __hash__(self) -> int:
        return hash(self.intervals)
