from typing import Any
import numpy.typing as npt
import numpy as np

int16 = np.uint16
int64 = np.uint64

floatlist = npt.NDArray[np.floating[Any]]
intlist = npt.NDArray[np.integer[Any]]
int16list = npt.NDArray[int16]
int64list = npt.NDArray[int64]
boollist = npt.NDArray[np.bool_]
segbounds = list[tuple[int, int]]
