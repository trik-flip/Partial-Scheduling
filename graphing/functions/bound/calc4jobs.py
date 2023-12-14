from collections.abc import Callable

import numpy as np

from partial_scheduling.models.job import Job


def lower_bound1(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    j1 = jobs[0]
    return lambda i: j1.cost / i


def lower_bound2(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    j2 = jobs[1]
    return lambda i: j2.cost / i


def lower_bound3(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    j1 = jobs[0]
    j2 = jobs[1]
    j3 = jobs[2]
    return lambda i: (j3.cost + j2.w * (j3.p + j2.p) - j1.cost) / (j1.p + i)


def lower_bound4(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    j2 = jobs[1]
    j3 = jobs[2]
    return lambda i: (j3.p * (j3.w + j2.w)) / (j2.p + i)


def lower_bound(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    l1 = lower_bound1(*jobs)
    l2 = lower_bound2(*jobs)
    l3 = lower_bound3(*jobs)
    l4 = lower_bound4(*jobs)
    return lambda i: np.maximum.reduce([l1(i), l2(i), l3(i), l4(i)])


def upper_bound(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    j2 = jobs[1]
    j3 = jobs[2]
    return lambda i: (j2.w * (j3.p + j2.p)) / (j3.p + i)
