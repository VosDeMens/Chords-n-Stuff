from typing import Any

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np


def plot(
    y: Any,
    x: Any = None,
    title: str = "line chart",
    xlabel: str = "X",
    ylabel: str = "Y",
    ylimit: float | None = None,
    xrange: tuple[float, float] | None = None,
    figure: Figure | None = None,
    red_lines: list[float] | None = None,
    green_lines: list[float] | list[int] | None = None,
) -> None:
    if x is None:
        x = np.arange(len(y))
    if figure is None:
        figure = plt.figure(figsize=(10, 5))  # type: ignore
    plt.plot(x, y, label="Wave")  # type: ignore
    plt.xlabel(xlabel)  # type: ignore
    plt.ylabel(ylabel)  # type: ignore
    plt.title(title)  # type: ignore
    plt.legend()  # type: ignore
    plt.grid(True)  # type: ignore
    if ylimit is not None:
        plt.ylim(0, ylimit)  # type: ignore
    if xrange is not None:
        plt.xlim(xrange[0], xrange[1])  # type: ignore
    if red_lines is not None:
        for line in red_lines:
            plt.axvline(x=line, color="red", linestyle="--", linewidth=2)  # type: ignore
    if green_lines is not None:
        for line in green_lines:
            plt.axvline(x=line, color="green", linestyle="--", linewidth=2)  # type: ignore
