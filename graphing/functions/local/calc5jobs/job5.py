from typing import Callable

import numpy as np

from partial_scheduling.models.job import Job


def lower_bound1(*jobs: Job):
    j1 = jobs[0]
    j2 = jobs[1]
    j3 = jobs[2]
    return lambda i: (j3.p * j3.w + (j3.p + j2.p) * j2.w - j1.p * j1.w) / (i) - j1.w


def lower_bound2(*jobs: Job):
    j2 = jobs[1]
    j3 = jobs[2]
    return lambda i: (j3.p * (j3.w + j2.w)) / (i) - j2.w


def lower_bound3(*jobs: Job):
    j2 = jobs[1]
    j3 = jobs[2]
    return lambda i: ((j3.p + j2.p) * j2.w) / (i) - j3.w


def upper_bound(*jobs: Job):
    j2 = jobs[1]
    j3 = jobs[2]
    j4 = jobs[3]
    return lambda i: (j3.p * j3.w + (j3.p + j2.p) * j2.w - j4.p * j4.w) / (i) - j4.w


def lower_bound(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    l1 = lower_bound1(*jobs)
    l2 = lower_bound2(*jobs)
    l3 = lower_bound3(*jobs)
    return lambda i: np.maximum.reduce(
        [
            l1(i),
            l2(i),
            l3(i),
        ]
    )
