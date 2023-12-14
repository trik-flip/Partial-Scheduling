import logging
from collections.abc import Callable, Iterable

from ...algorithms.greedy import greedy3_1
from ...models.job import Job, create_from
from ...models.schedule import Schedule


def ub_exp(
    jobs: list[Job],
    fixed_processing_time: float,
    k: int = 2,
    func: Callable[[Iterable[Job], int], Schedule] = greedy3_1,
    bound: float = 2e6,
    step: float = 1e6,
    t: float = 1e-2,
    max_runs: int = 1000,
) -> float:
    errors = []

    def new_func(j: Job, s: list[Job] = jobs, k: int = k) -> Schedule:
        return func(s + [j], k)

    last = float("inf")
    error = float("inf")
    run_counter = 0

    sol = func(jobs, k)
    i: int = func.iterations
    c = sol.cost

    while error > t and run_counter < max_runs:
        run_counter += 1
        j = Job(fixed_processing_time, bound)
        sol = new_func(j)
        i2: int = func.iterations
        # If adding an unused job
        if i == i2 and c == sol.cost:
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
        error = abs(bound - last)
        last = bound

    if "_errors" not in ub_exp.__dict__:
        ub_exp.errors = []
    ub_exp.errors += [(w, fixed_processing_time) for w in errors]
    return bound


def upper_bound(
    jobs: list[Job],
    fixed_processing_time: float,
    k: int = 2,
    func: Callable[[Iterable[Job], int], Schedule] = greedy3_1,
    bound: float = 100,
    step: float = 1,
    t: float = 1e-2,
    max_runs: int = 1000,
) -> float:
    def new_func(j: Job, s: list[Job] = jobs, k: int = k) -> Schedule:
        return func(s + [j], k)

    sol = func(jobs, k)
    i: int = func.iterations
    c = sol.cost
    last = float("inf")
    error = float("inf")
    run_counter = 0
    while error > t and run_counter < max_runs:
        run_counter += 1
        j = Job(fixed_processing_time, bound)
        sol = new_func(j)
        i2: int = func.iterations
        # If adding an unused job
        if i == i2 and c == sol.cost:
            bound -= step * 1.5
        # if adding a job that makes an existing job obsolete
        elif i >= i2 and c > sol.cost:
            bound += step
        elif i < i2 and c >= sol.cost:
            bound += step
            step /= 2
        else:
            raise Exception(f"Not possible, i:{i}, i2: {i2}, c: {c}, sol: {sol.cost}")
        error = abs(bound - last)
        last = bound
    return bound


def lb_exp(
    jobs: list[Job],
    fixed_processing_time: float,
    k: int = 2,
    func: Callable[[Iterable[Job], int], Schedule] = greedy3_1,
    bound: float = 2e6,
    t: float = 1e-2,
    max_runs: int = 1000,
) -> float:
    jobs = create_from(jobs)

    def new_func(j: Job, s: list[Job] = jobs, k: int = k) -> Schedule:
        return func(s + [j], k)

    errors = []
    step = bound / 2
    sol = func(jobs, k)
    i: int = func.iterations
    c = sol.cost
    last = float("inf")
    correction = float("inf")
    run_counter = 0
    while run_counter < max_runs and correction > t:
        run_counter += 1
        j = Job(fixed_processing_time, bound)
        sol = new_func(j)
        i2: int = func.iterations
        # If adding an unused job
        if i == i2 and c == sol.cost:
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
        correction = abs(bound - last)
        last = bound
    if "_errors" not in lb_exp.__dict__:
        lb_exp.errors = []
    lb_exp.errors += [(w, fixed_processing_time) for w in errors]
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

    sol = func(jobs, k)
    i: int = func.iterations
    c = sol.cost
    last = float("inf")
    correction = float("inf")
    run_counter = 0

    while correction > t and run_counter < max_runs:
        run_counter += 1
        j = Job(fixed_processing_time, bound)
        sol = new_func(j)
        i2: int = func.iterations
        # If adding an unused job
        if i == i2 and c == sol.cost:
            bound -= step * 1.5
        # if adding a job that makes an existing job obsolete
        elif i >= i2 and c > sol.cost:
            bound += step
        # If we have a job that increases the iteration count
        elif i < i2 and c >= sol.cost:
            bound -= step
            step /= 2
        else:
            raise Exception(f"Not possible, i:{i}, i2: {i2}, c: {c}, sol: {sol.cost}")
        correction = abs(bound - last)
        last = bound
    return bound
