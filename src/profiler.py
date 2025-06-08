from abc import ABCMeta
from time import perf_counter
from functools import wraps
from collections import defaultdict
from typing import Callable, Any, TypeVar, cast

T = TypeVar("T", bound=Callable[..., Any])
C = TypeVar("C", bound=type)

class_timings: dict[type, dict[str, tuple[float, int]]] = defaultdict(
    dict[str, tuple[float, int]]
)


def timed_method(cls: type) -> Callable[[T], T]:
    """Decorator factory that instruments a method of a class
    to record its execution time for performance reporting.

    Parameters
    ----------
    cls : type
        The class the method belongs to. Used as a key in the timing report.

    Returns
    -------
    Callable[[T], T]
        A decorator that wraps the method and records its execution time.

    Notes
    -----
    This is intended for use with `TimingMeta`, which applies the decorator
    automatically to all non-special methods of a class.
    """

    def decorator(method: T) -> T:
        @wraps(method)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            start = perf_counter()
            result = method(self, *args, **kwargs)
            duration = perf_counter() - start
            method_name = method.__name__
            if method_name not in class_timings[cls]:
                class_timings[cls][method_name] = (0, 0)
            time, count = class_timings[cls][method_name]
            class_timings[cls][method_name] = (time + duration, count + 1)
            return result

        return cast(T, wrapper)

    return decorator


class TimingMeta(ABCMeta):
    """Metaclass that automatically applies the `timed_method` decorator
    to all callable attributes (excluding special methods) of a class.

    Usage
    -----
    class MyClass(metaclass=TimingMeta):
        def slow_function(self):
            ...

    After running some methods, call `report_timings()` to see durations.
    """

    def __new__(
        mcs: type["TimingMeta"],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:
        cls = super().__new__(mcs, name, bases, namespace)
        for attr_name, attr_value in namespace.items():
            if callable(attr_value):  # and not attr_name.startswith("__"):
                wrapped = timed_method(cls)(attr_value)
                setattr(cls, attr_name, wrapped)
        return cls


def report_timings() -> None:
    """Prints a timing report of all methods instrumented by `TimingMeta`.

    Outputs
    -------
    - Execution time per method grouped by class
    - Total execution time

    After reporting, the stored timing data is cleared.
    """
    print("\nTiming Report:")
    for cls, t in sorted(
        class_timings.items(), key=lambda x: -sum([time for time, _ in x[1].values()])
    ):
        print(f"{cls.__name__}:")
        for k, (time, count) in sorted(t.items(), key=lambda x: -x[1][0]):
            print(f"    {k}: {time:.6f} seconds, called {count} times")
    class_timings.clear()
