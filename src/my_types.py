from typing import Any
import numpy.typing as npt
import numpy as np


floatlist = npt.NDArray[np.floating[Any]]
intlist = npt.NDArray[np.integer[Any]]
boollist = npt.NDArray[np.bool_]
segbounds = list[tuple[int, int]]
