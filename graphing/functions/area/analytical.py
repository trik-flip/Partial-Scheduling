from collections.abc import Callable

import numpy as np

from partial_scheduling.models.job import Job


def viable(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    """j3,j2≤j1,j3"""
    j1, j2, *_j = jobs
    return lambda i: ((j2.p + i) * j2.w - j1.p * j1.w) / j1.p
