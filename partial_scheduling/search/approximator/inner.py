from collections.abc import Callable, Iterable

from ...algorithms.greedy import greedy3_1
from ...models.job import Job
from ...models.schedule import Schedule


def ub_exp(
    jobs: list[Job],
    fixed_processing_time: float,
    k: int = 2,
    func: Callable[[Iterable[Job], int], Schedule] = greedy3_1,
    bound: float = 2e6,
    t: float = 1e-2,
    max_runs: int = 1000,
) -> float:
    def new_func(j: Job, s: list[Job] = jobs, k: int = k) -> Schedule:
        return func(s + [j], k)

    step = bound / 2

    val = func(jobs, k)
    i: int = func.iterations
    c = val.cost
    last = float("inf")
    error = float("inf")
    run_counter = 0
    while error > t and run_counter < max_runs:
        run_counter += 1
        j = Job(fixed_processing_time, bound)
        val2 = new_func(j)
        i2: int = func.iterations
        if c == val2.cost and i == i2:
            bound -= step
        elif i >= i2 and c > val2.cost:
            bound += step
        elif i2 > i and c == val2.cost:
            bound += step
        elif i2 > i and c > val2.cost:
            bound += step
        else:
            raise Exception(f"Not possible, i:{i}, i2: {i2}, c: {c}, sol: {val2.cost}")
        step /= 2
        error = abs(bound - last)
        last = bound
    return bound


def upper_bound(
    jobs: list[Job],
    fixed_processing_time: float,
    k: int = 2,
    func: Callable[[Iterable[Job], int], Schedule] = greedy3_1,
    bound: float = 20,
    step: float = 1,
    t: float = 1e-2,
    max_runs: int = 1000,
) -> float:
    def new_func(j: Job, s: list[Job] = jobs, k: int = k) -> Schedule:
        return func(s + [j], k)

    val = func(jobs, k)
    i: int = func.iterations
    c = val.cost
    last = float("inf")
    error = float("inf")
    run_counter = 0
    while error > t and run_counter < max_runs:
        run_counter += 1
        j = Job(fixed_processing_time, bound)
        val2 = new_func(j)
        i2: int = func.iterations
        if c > val2.cost or i2 > i and c == val2.cost:
            bound += step
            step /= 2
        else:
            bound -= step
        error = abs(bound - last)
        last = bound
    return bound


def lb_exp(
    jobs: list[Job],
    fixed_processing_time: float,
    k: int = 2,
    func: Callable[[Iterable[Job], int], Schedule] = greedy3_1,
    bound: float = 2e6,
    step: float = 1e6,
    t: float = 1e-2,
    max_runs: int = 1000,
) -> float:
    def new_func(j: Job, s: list[Job] = jobs, k: int = k) -> Schedule:
        return func(s + [j], k)

    val = func(jobs, k)
    i: int = func.iterations
    c = val.cost
    last = float("inf")
    error = float("inf")
    run_counter = 0
    while error > t and run_counter < max_runs:
        run_counter += 1
        j = Job(fixed_processing_time, bound)
        val2 = new_func(j)
        i2: int = func.iterations
        if c == val2.cost and i == i2:
            bound -= step
        elif i >= i2 and c > val2.cost:
            bound += step
        elif i2 > i and c == val2.cost:
            bound -= step
        elif i2 > i and c > val2.cost:
            bound += step
        else:
            raise Exception(f"Not possible, i:{i}, i2: {i2}, c: {c}, sol: {val2.cost}")
        step /= 2
        error = abs(bound - last)
        last = bound
    return bound


def lower_bound(
    jobs: list[Job],
    fixed_processing_time: float,
    k: int = 2,
    func: Callable[[Iterable[Job], int], Schedule] = greedy3_1,
    bound: float = 1,
    step: float = 1,
    t: float = 1e-2,
    max_runs: int = 1000,
) -> float:
    def new_func(j: Job, s: list[Job] = jobs, k: int = k) -> Schedule:
        return func(s + [j], k)

    val = func(jobs, k)
    i: int = func.iterations
    c = val.cost
    last = float("inf")
    error = float("inf")
    run_counter = 0
    while error > t and run_counter < max_runs:
        run_counter += 1
        j = Job(fixed_processing_time, bound)
        val2 = new_func(j)
        i2: int = func.iterations
        if c > val2.cost:
            bound += step
        elif i2 > i or c <= val2.cost:
            bound -= step
            step /= 2
        else:
            bound += step
        error = abs(bound - last)
        last = bound
    return bound
