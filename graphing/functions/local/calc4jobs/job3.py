from collections.abc import Callable

import numpy as np

from partial_scheduling.models.job import Job


def upper_bound(*jobs: Job):
    j1 = jobs[0]
    j2 = jobs[1]
    # j3 < f({j1, j2}), otherwise we'd say
    return lambda i: (j1.p * j1.w + (j1.p + j2.p) * j2.w) / i


def lower_bound1(*jobs: Job):
    "j1, j2 < j1, j3"
    j1 = jobs[0]
    j2 = jobs[1]
    # f({j1, j2}) < f({j1, j3})
    # j1.p * j1.w + (j1.p + j2.p) * j2.w < j1.p * j1.w + (j1.p + j3.p) * j3.w
    # (j1.p + j2.p) * j2.w < (j1.p + j3.p) * j3.w
    # ((j1.p + j2.p) * j2.w)/(j1.p + j3.p) < j3.w
    return lambda i: ((j1.p + j2.p) * j2.w) / (j1.p + i)


def lower_bound2(*jobs: Job):
    "j1, j2 < j3, j1"
    j1 = jobs[0]
    j2 = jobs[1]
    # f({j1, j2}) < f({j3, j1})
    # j1.p * j1.w + (j1.p + j2.p) * j2.w < j3.p * j3.w + (j3.p + j1.p) * j1.w
    # (j1.p + j2.p) * j2.w < j3.p * j3.w + j3.p * j1.w
    # (j1.p + j2.p) * j2.w - j3.p * j1.w < j3.p * j3.w
    # ((j1.p + j2.p) * j2.w) / j3.p - j1.w < j3.w
    return lambda i: ((j1.p + j2.p) * j2.w) / i - j1.w


def lower_bound3(*jobs: Job):
    "j1, j2 < j2, j3"
    j1 = jobs[0]
    j2 = jobs[1]
    # f({j1, j2}) < f({j2, j3})
    # j1.p * j1.w + (j1.p + j2.p) * j2.w < j2.p * j2.w + (j2.p + j3.p) * j3.w
    # (j1.p * j1.w + j1.p * j2.w)/(j2.p + j3.p) < j3.w
    # (j1.p * (j1.w + j2.w))/(j2.p + j3.p) < j3.w
    return lambda i: (j1.p * (j1.w + j2.w)) / (j2.p + i)


def lower_bound4(*jobs: Job):
    "j1, j2 < j3, j2"
    j1 = jobs[0]
    j2 = jobs[1]
    # f({j1, j2}) < f({j3, j2})
    # j1.p * j1.w + (j1.p + j2.p) * j2.w < j3.p * j3.w + (j3.p + j2.p) * j2.w
    # j1.p * j1.w + j1.p * j2.w < j3.p * j3.w + j3.p * j2.w
    # j1.p * j1.w + j1.p * j2.w - j3.p * j2.w < j3.p * j3.w
    # (j1.p * j1.w + j1.p * j2.w) / j3.p - j2.w < j3.w
    # (j1.p * (j1.w + j2.w)) / j3.p - j2.w < j3.w
    return lambda i: (j1.p * (j1.w + j2.w)) / i - j2.w


def lower_bound(
    *jobs: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    l1 = lower_bound1(*jobs)
    l2 = lower_bound2(*jobs)
    l3 = lower_bound3(*jobs)
    l4 = lower_bound4(*jobs)
    return lambda i: np.maximum.reduce(
        [
            l1(i),
            l2(i),
            l3(i),
            l4(i),
        ]
    )
