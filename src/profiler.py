from abc import ABCMeta
from time import perf_counter
from functools import wraps
from collections import defaultdict
from typing import Callable, Any, TypeVar, cast

T = TypeVar("T", bound=Callable[..., Any])
C = TypeVar("C", bound=type)

class_timings: dict[type, dict[str, float]] = defaultdict(dict[str, float])


def timed_method(cls: type) -> Callable[[T], T]:
    def decorator(method: T) -> T:
        @wraps(method)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            start = perf_counter()
            result = method(self, *args, **kwargs)
            duration = perf_counter() - start
            method_name = method.__name__
            if method_name not in class_timings[cls]:
                class_timings[cls][method_name] = 0
            class_timings[cls][method_name] += duration
            return result

        return cast(T, wrapper)

    return decorator


class TimingMeta(ABCMeta):
    def __new__(
        mcs: type["TimingMeta"],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
    ) -> type:
        cls = super().__new__(mcs, name, bases, namespace)  # ✅ 3-arg call
        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                wrapped = timed_method(cls)(attr_value)
                setattr(cls, attr_name, wrapped)
        return cls


def report_timings() -> None:
    print("\nTiming Report:")
    total = 0
    for cls, t in sorted(class_timings.items(), key=lambda x: -sum(x[1].values())):
        print(f"{cls.__name__}:")
        for k, v in t.items():
            total += v
            print(f"    {k}: {v:.6f}")
    class_timings.clear()

    print(f"Total: {total}")
