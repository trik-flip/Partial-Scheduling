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
    j3 = jobs[2]
    j4 = jobs[3]
    return lambda i: (j3.p * j3.w + (j3.p + j4.p) * j4.w - (i + j1.p) * j1.w) / i


def lower_bound4(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    j2 = jobs[1]
    j3 = jobs[2]
    j4 = jobs[3]
    return lambda i: (j3.p * j3.w + (j3.p + j4.p) * j4.w - (i + j2.p) * j2.w) / i


def lower_bound5(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    j3 = jobs[2]
    j4 = jobs[3]
    return lambda i: ((j3.p + j4.p) * j4.w - i * j3.w) / i


def lower_bound(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    l1 = lower_bound1(*jobs)
    l2 = lower_bound2(*jobs)
    l3 = lower_bound3(*jobs)
    l4 = lower_bound4(*jobs)
    l5 = lower_bound5(*jobs)
    return lambda i: np.maximum.reduce(
        [
            l1(i),
            l2(i),
            l3(i),
            l4(i),
            l5(i),
        ]
    )


def upper_bound(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    j3 = jobs[2]
    j4 = jobs[3]
    return lambda i: (j3.p * j3.w + (j3.p - i) * j4.w) / i
