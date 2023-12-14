from collections.abc import Callable

import numpy as np

from partial_scheduling.models.job import Job
from partial_scheduling.search.approximator import restricted


def lower_bound(
    *vectors: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    jobs = [(p, w) for p, w in vectors]

    def inner_func(x: np.ndarray[float, np.dtype]):
        return np.array([restricted.lb_exp(jobs, i, k=2, runs=1000) for i in x])

    return inner_func


def upper_bound(
    *vectors: Job,
) -> Callable[[np.ndarray[float, np.dtype]], np.ndarray[float, np.dtype]]:
    jobs = [(p, w) for p, w in vectors]

    def inner_func(x: np.ndarray[float, np.dtype]):
        return np.array([restricted.ub_exp(jobs, i, k=2, runs=1000) for i in x])

    return inner_func
