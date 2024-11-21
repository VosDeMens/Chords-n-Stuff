from typing import TypeVar


T = TypeVar("T")


def create_all_translations(values: tuple[T, ...]) -> list[tuple[T, ...]]:
    return [values[i:] + values[:i] for i in range(len(values))]


def get_minimal_translation(values: tuple[T, ...]) -> tuple[T, ...]:
    return min(create_all_translations(values))
