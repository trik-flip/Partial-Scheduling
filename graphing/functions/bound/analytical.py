from collections.abc import Callable

import numpy as np

from partial_scheduling.models.job import Job


def lower_bound(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    j_max = max([j.cost for j in jobs[:2]])
    return lambda i: j_max / i


def lower_bound1(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    j1 = jobs[0]
    j2 = jobs[1]
    return lambda i: (j2.p * j2.w + i * j2.w) / (j1.p) - j1.w


def upper_bound1(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    """j3, j2 <= j1, j2"""
    j1 = jobs[0]
    j2 = jobs[1]
    return lambda i: ((j1.p * (j1.w + j2.w)) / i) - j2.w


def upper_bound2(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    """$j2, j3 <= j1, j2$"""
    j1 = jobs[0]
    j2 = jobs[1]
    return lambda i: (j1.p * (j1.w + j2.w)) / (i + j2.p)


def upper_bound3(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    """j_2, j_3 <= j_3, j_2"""
    j1 = jobs[0]
    j2 = jobs[1]
    return lambda i: (i * j2.w) / j2.p


def upper_bound(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    l1 = upper_bound1(*jobs)
    l2 = upper_bound2(*jobs)

    return lambda i: np.maximum.reduce([l1(i), l2(i)])
