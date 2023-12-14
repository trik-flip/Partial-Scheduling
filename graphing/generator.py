from collections.abc import Iterable
from math import log

import constraint
import numpy as np
from numpy import arange

from partial_scheduling.algorithms.greedy import greedy3_1
from partial_scheduling.models.job import Job, create_from
from partial_scheduling.models.schedule import Schedule
from Protato import Profiler


# This one is the slowest
def calc_evil_start_job(schedule: Schedule) -> list[Job]:
    """Generate a job such that it is not in the optimal schedule,
    but it will replace a job from the begin schedule

    Args:
        jobs (Iterable[Job]): The optimal end schedule

    Returns:
        Job: The evil starting job
    """
    possible: set[tuple[float, float]] | None = None
    for job in schedule:
        problem = constraint.Problem()
        problem.addVariables(["x", "y"], range(1, 10))

        def our_constraint(x: float, y: float, j: Job = job) -> bool:
            return x * y < j.cost and (schedule // j | Job(x, y)).cost > schedule.cost

        problem.addConstraint(our_constraint, ["x", "y"])
        solutions: list[dict[str, float]] = problem.getSolutions()
        assert isinstance(solutions, list)
        possible_jobs = {(sol["x"], sol["y"]) for sol in solutions}
        if possible is None:
            possible = possible_jobs
        else:
            possible &= possible_jobs
    assert possible is not None
    return create_from(possible)


def calc_evil_start_job2(
    schedule: Schedule, domain: range | list[int | float] = range(1, 10)
) -> list[Job]:
    """Generate a job such that it is not in the optimal schedule,
    but it will replace a job from the begin schedule

    Args:
        jobs (Iterable[Job]): The optimal end schedule

    Returns:
        Job: The evil starting job
    """
    assert 0 not in domain

    problem = constraint.Problem()
    problem.addVariables(["x", "y"], domain)

    for job in schedule:

        def c1(x: float, y: float, j: Job = job) -> bool:
            return (x * y) < j.cost

        def c2(x: float, y: float, j: Job = job) -> bool:
            return (schedule // j | Job(x, y)).cost > schedule.cost

        problem.addConstraint(c1, ["x", "y"])
        problem.addConstraint(c2, ["x", "y"])

    solutions: list[dict[str, float]] = problem.getSolutions()
    assert isinstance(solutions, list)
    possible = {(sol["x"], sol["y"]) for sol in solutions}
    return create_from(possible)


def calc_evil_start_job3(
    opt: Schedule,
    jobs: Iterable[Job],
    domain: range | list[int | float] = range(1, 10),
) -> list[Job]:
    """Generate a job such that it is not in the optimal schedule,
    but it will replace a job from the begin schedule

    Args:
        jobs (Iterable[Job]): The optimal end schedule

    Returns:
        Job: The evil starting job
    """
    cost = opt.cost
    step_ratio = -round(log(domain[1] - domain[0], 10))
    assert 0 not in domain

    problem = constraint.Problem()
    problem.addVariables(["x", "y"], domain)

    for job in jobs:

        def c1(x: float, y: float, j: Job = job) -> bool:
            return (x * y) < j.cost

        def c2(x: float, y: float, j: Job = job) -> bool:
            return (opt // j | Job(x, y)).cost > cost

        problem.addConstraint(c1, ["x", "y"])
        problem.addConstraint(c2, ["x", "y"])

    solutions: list[dict[str, float]] = problem.getSolutions()
    assert isinstance(solutions, list)
    possible = {
        (round(sol["x"], step_ratio), round(sol["y"], step_ratio)) for sol in solutions
    }
    return create_from(possible)


def calc_evil_start_job4(
    opt: Schedule,
    jobs: list[Job],
    domain: range | list[int | float] | np.ndarray[float, np.dtype] = range(1, 10),
    iters: int = 1,
    k: int = 2,
) -> list[Job]:
    """Generate a job such that it is not in the optimal schedule,
    but it will replace a job from the begin schedule

    Args:
        jobs (Iterable[Job]): The optimal end schedule

    Returns:
        Job: The evil starting job
    """
    cost = opt.cost
    step_ratio = -round(log(domain[1] - domain[0], 10))
    assert 0 not in domain

    problem = constraint.Problem()
    problem.addVariables(["x", "y"], domain)

    def c1(x: float, y: float, j: list[Job] = jobs) -> bool:
        sol = greedy3_1(j + [Job(x, y)], k)
        i: int = greedy3_1.iterations
        return sol.cost == cost and i > iters

    problem.addConstraint(c1, ["x", "y"])

    solutions: list[dict[str, float]] = problem.getSolutions()
    assert isinstance(solutions, list)
    possible = {
        (round(sol["x"], step_ratio), round(sol["y"], step_ratio)) for sol in solutions
    }
    return create_from(possible)


_jobs = create_from([(5, 10), (10, 5)])
"""
addition tree for [(5, 10), (10, 5)]
(6,8)
    (6,8)
    (7,7)
    (8,6)
        (4,14)
            (9.2,5.3)
            (8.9,5.4)
 (5,10)
 (7,7)
    (6,8)
    (7,7)
            (14,4)
            (4,14)
    (8,6)
            (4,14)
 (8,6)
    (6,8)
        (4,14)
            (9.2,5.3)
            (8.9,5.4)
    (7,7)
        (4,14)
    (8,6)
        (4,14)
            (9.2,5.3)
            (8.9,5.4)
"""


# logging.basicConfig(
#     level=logging.INFO,
#     format="%(message)s",
#     force=True,
# )


def find_improvement(
    jobs: list[Job] = _jobs, delta: float = 1, k: int = 2
) -> list[Job]:
    _ = greedy3_1(jobs, k=k)
    i: int = greedy3_1.iterations
    return calc_evil_start_job4(Schedule(jobs[:k]), jobs, arange(1, 25, delta), i, k)


def find_improvement_recursive(
    jobs: list[Job] = _jobs, delta: float = 1, level: int = 0, k: int = 2
) -> None:
    """Build a tree of jobs which prolong the finding of the final solution

    Args:
        jobs (_type_, optional): _description_. Defaults to _jobs.
        delta (int, optional): _description_. Defaults to 1.
        level (int, optional): _description_. Defaults to 0.
        k (int, optional): _description_. Defaults to 2.
    """
    _ = greedy3_1(jobs, k=k)
    i: int = greedy3_1.iterations
    possible_jobs = calc_evil_start_job4(
        Schedule(jobs[:k]), jobs, arange(1, 25, delta), i, k
    )
    for possible_job in possible_jobs:
        print("\t" * level, possible_job, sep="")
        find_improvement_recursive(jobs + [possible_job], delta, level + 1, k)

    print("\t" * (level - 1), "end", sep="")


def find_improvement_recursive_ex(
    jobs: list[Job] = _jobs, delta: float = 1, level: int = 0, k: int = 2
) -> None:
    """build a tree, which makes tinier steps when it doesn't seem enough

    Args:
        jobs (_type_, optional): _description_. Defaults to _jobs.
        delta (int, optional): _description_. Defaults to 1.
        level (int, optional): _description_. Defaults to 0.
        k (int, optional): _description_. Defaults to 2.
    """
    if level > 4:
        return
    _ = greedy3_1(jobs, k=k)
    i: int = greedy3_1.iterations
    possible_jobs = calc_evil_start_job4(
        Schedule(jobs[:k]), jobs, arange(1, 25, delta), i, k
    )
    if len(possible_jobs) == 0:
        delta = delta / 10
        possible_jobs = calc_evil_start_job4(
            Schedule(jobs[:k]), jobs, arange(1, 25, delta), i, k
        )
    for possible_job in possible_jobs:
        print("\t" * level, possible_job, sep="")
        find_improvement_recursive_ex(jobs + [possible_job], delta, level + 1, k)

    print("\t" * (level - 1), "end", sep="")


if __name__ == "__main__":
    Profiler().disable()
    find_improvement_recursive_ex(create_from([(1, 1), (5, 15), (15, 5)]), k=3)

    print("Done")
