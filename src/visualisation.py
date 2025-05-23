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
    """Wrapper for pyplot linechart, which is actually able to just plot something in one line.

    matplotlib why you gotta be like this.

    Parameters
    ----------
    y : Any
        Data to plot
    x : Any, optional
        To plot against, by default None
    title : str, optional
        Title of the plot, by default "line chart"
    xlabel : str, optional
        Label of the X axis, by default "X"
    ylabel : str, optional
        Label of the Y axis, by default "Y"
    ylimit : float | None, optional
        Max value on the Y axis, by default just above max(Y)
    xrange : tuple[float, float] | None, optional
        Range of the X axis, by default just arounf min(X) and max(X)
    figure : Figure | None, optional
        Existing `Figure` to add to, by default None for a fresh `Figure`
    red_lines : list[float] | None, optional
        X values for which to plot red vertical dashed lines, by default []
    green_lines : list[float] | list[int] | None, optional
        X values for which to plot green vertical dashed lines, by default []
    """
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
