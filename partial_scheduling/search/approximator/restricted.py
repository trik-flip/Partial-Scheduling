import logging
from collections.abc import Callable, Iterable

from ...algorithms.greedy import greedy3_1
from ...models.job import Job, create_from
from ...models.schedule import Schedule


def ub_exp(
    _jobs: list[tuple[int, int]],
    fixed_processing_time: float,
    k: int = 2,
    func: Callable[[Iterable[Job], int], Schedule] = greedy3_1,
    bound: float = 2e6,
    runs: int = 1000,
) -> float:
    jobs = create_from(_jobs)
    j1 = jobs[0]
    j2 = jobs[1]

    def new_func(j: Job, s: list[Job] = jobs, k: int = k) -> Schedule:
        return func(s + [j], k)

    errors = []
    step = bound / 2

    run_counter = 0

    sol = func(jobs, k)
    i: int = func.iterations
    c = sol.cost

    while run_counter < runs:
        run_counter += 1
        j = Job(fixed_processing_time, bound)
        sol = new_func(j)
        i2: int = func.iterations
        if j1 in sol or j2 not in sol:
            bound -= step
        # If adding an unused job
        elif i == i2 and c == sol.cost:
            bound -= step
        # if adding a job that makes an existing job obsolete
        elif i >= i2 and c > sol.cost:
            bound += step
        elif i < i2 and c >= sol.cost:
            bound += step
        else:
            bound -= step
            logging.warning("UPPER_BOUND_ERROR %f, %f", fixed_processing_time, bound)
            errors.append((fixed_processing_time, bound))
            # raise Exception(
            #     f"Not possible, i:{i}, i2: {i2}, c: {c}, sol: {sol.cost}"
            # )
        step /= 2

    if "_errors" not in ub_exp.__dict__:
        ub_exp.errors = []
    ub_exp.errors += [(w, fixed_processing_time) for w in errors]
    return bound


def lb_exp(
    _jobs: list[tuple[int, int]],
    fixed_processing_time: float,
    k: int = 2,
    func: Callable[[Iterable[Job], int], Schedule] = greedy3_1,
    bound: float = 2e6,
    runs: int = 1000,
) -> float:
    jobs = create_from(_jobs)
    j1 = jobs[0]
    j2 = jobs[1]

    def new_func(j: Job, s: list[Job] = jobs, k: int = k) -> Schedule:
        return func(s + [j], k)

    errors = []
    step = bound / 2

    run_counter = 0

    sol = func(jobs, k)
    i: int = func.iterations
    c = sol.cost

    while run_counter < runs:
        run_counter += 1
        j = Job(fixed_processing_time, bound)
        sol = new_func(j)
        i2: int = func.iterations
        if j1 in sol or j2 not in sol:
            bound -= step
        # If adding an unused job
        elif i == i2 and c == sol.cost:
            bound -= step
        # if adding a job that makes an existing job obsolete
        elif i >= i2 and c > sol.cost:
            bound += step
        # If we have a job that increases the iteration count
        elif i < i2 and c >= sol.cost:
            bound -= step
        else:
            bound += step
            logging.warning("LOWER_BOUND_ERROR %f, %f", fixed_processing_time, bound)
            errors.append((fixed_processing_time, bound))
            # raise Exception(
            #     f"Not possible, i:{i}, i2: {i2}, c: {c}, sol: {sol.cost}"
            # )
        step /= 2
    if "_errors" not in lb_exp.__dict__:
        lb_exp.errors = []
    lb_exp.errors += [(w, fixed_processing_time) for w in errors]
    return bound
