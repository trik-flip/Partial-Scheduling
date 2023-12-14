from collections.abc import Callable

import numpy as np

from partial_scheduling.models.job import Job


def split_jobs(*jobs):
    p = [j.p for j in jobs]
    w = [j.w for j in jobs]
    return p, w


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


def create_lower_bounds(n: int, with_initial_jobs=True):
    if with_initial_jobs:
        lower_bounds = [lower_bound1, lower_bound2]
    else:
        lower_bounds = []
    n -= 1
    if n & 1 == 0:  # then n is odd
        for i in range(0, n - 1):

            def func1(*jobs: Job, i=i):
                p, w = split_jobs(*jobs)
                return (
                    lambda j: (
                        (p[n - 2] * w[n - 2])
                        + ((p[n - 2] + p[n - 1]) * w[n - 1])
                        - (p[i] * w[i])
                    )
                    / j
                    - w[i]
                )

            lower_bounds.append(func1)

    else:
        for i in range(0, n - 1):

            def func2(*jobs: Job, i=i):
                p, w = split_jobs(*jobs)
                return lambda j: (
                    (p[n - 1] * w[n - 1])
                    + ((p[n - 1] + p[n - 2]) * w[n - 2])
                    - (p[i] * w[i])
                ) / (p[i] + j)

            lower_bounds.append(func2)
    return lower_bounds


def create_final_lower_bound(n: int, with_initial_jobs=True):
    lower_bounds = create_lower_bounds(n, with_initial_jobs)

    def lb(*jobs: Job):
        return lambda i: np.maximum.reduce([l(*jobs)(i) for l in lower_bounds])

    return lb


def create_final_upper_bound(
    n: int,
) -> Callable[
    [Job], Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]
]:
    n -= 1
    if n & 1 == 0:

        def ub_odd(
            *jobs: Job,
        ) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
            p, w = split_jobs(*jobs)
            return lambda j: (p[n - 2] * (w[n - 2] + w[n - 1])) / j - w[n - 1]

        return ub_odd

    else:

        def ub_even(
            *jobs: Job,
        ) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
            p, w = split_jobs(*jobs)
            return lambda j: ((p[n - 1] + p[n - 2]) * w[n - 2]) / (p[n - 1] + j)

        return ub_even
