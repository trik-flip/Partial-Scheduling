from collections.abc import list, Sized
from typing import overload

from Protato import Profiler

from ..models.job import Job
from ..models.schedule import Schedule


# region: dynamic_programming
@overload
def dynamic_programming(
    jobs: list[Job],
    k: int,
) -> Schedule:
    ...


@overload
def dynamic_programming(
    jobs: list[Job],
    k: int,
    time: int,
) -> Schedule:
    ...


def dynamic_programming(
    jobs: list[Job],
    k: int,
    time: float | None = None,
) -> Schedule:
    if time is None:
        time = _calc_max_total_time(jobs, k)
    schedule = _dynamic_programming(Schedule(jobs), k, time)
    assert schedule is not None
    return schedule


@Profiler()
def _dynamic_programming(
    schedule: Schedule,
    k: int,
    time: float,
) -> Schedule | None:
    if k == 0:
        return Schedule()
    if len(schedule) == k:
        return schedule
    if (len(schedule) < k) or (time < 0):
        return None

    best_cost = float("inf")
    best_schedule = None

    for job in schedule.ordered:
        dp_schedule = _dynamic_programming(
            schedule.where(lambda j, j2=job: j.ratio <= j2.ratio) // job,
            k - 1,
            time - job.p,
        )
        if dp_schedule is None:
            continue
        cost = (dp_schedule | job).cost
        if cost < best_cost:
            best_cost = cost
            best_schedule = dp_schedule | job
    return best_schedule


# endregion


# region: dynamic_programming_with_schedule
@overload
def dynamic_programming_with_schedule(
    jobs: list[Job],
    k: int,
) -> Schedule:
    ...


@overload
def dynamic_programming_with_schedule(
    jobs: list[Job],
    k: int,
    time: int,
) -> Schedule:
    ...


def dynamic_programming_with_schedule(
    jobs: list[Job],
    k: int,
    time: int | float = float("inf"),
) -> Schedule:
    schedule = _dynamic_programming_with_schedule(Schedule(jobs), k, time, Schedule())
    assert schedule is not None
    return schedule


@Profiler()
def _dynamic_programming_with_schedule(
    jobs: Schedule,
    k: int,
    time: int,
    schedule: Schedule,
) -> Schedule | None:
    if k == 0:
        return Schedule()
    if len(jobs) == k:
        return jobs
    if (len(jobs) < k) or (time < 0):
        return None

    best_cost = float("inf")
    best_schedule = None

    for job in jobs.ordered:
        dp_schedule = _dynamic_programming_with_schedule(
            jobs.where(lambda j, j2=job: j.ratio <= j2.ratio) // job,
            k - 1,
            time - job.p,
            schedule | job,
        )
        if dp_schedule is None:
            continue
        cost = (dp_schedule | schedule | job).cost
        if cost < best_cost:
            best_cost = cost
            best_schedule = dp_schedule | job

    return best_schedule


# endregion


# region: TODO: dynamic_programming_job_for_job
def dynamic_programming_job_for_job(jobs: list[Job], k: int) -> Schedule:
    jobs = sort(jobs)  # With this we ensure that the solution stays consistent
    start = jobs[:k]
    for job in jobs[k:]:
        pass


# endregion


# region : Temp
@Profiler()
def dynamic_programming_ab(
    jobs: list[Job],
    k: int,
    max_time: int | float = float("inf"),
    best: int | float = float("inf"),
    current: int = 0,
) -> list[Job]:
    """Based on alpha beta pruning
    pass in a already discoverd lowest score, and pass this in with every search.
    Just like Alpha-beta pruning
    """
    if k == 0:
        return []
    min_cost = float("inf")
    best_s = None
    for j in jobs:
        if not (j.p < max_time and current + j.cost >= best):
            continue
        # only if it fits in the schedule try it
        # if current + job.cost >
        schedule = dynamic_programming_ab(
            filter(lambda x, j=j: x != j, jobs),
            k - 1,
            max_time - j.p,
            best,
            current,
        )
        schedule = Schedule(schedule + [j])
        if schedule.cost < min_cost:
            best_s = schedule.ordered
            min_cost = schedule.cost
    return best_s


# endregion


# region: Extra
def _calc_max_total_time(jobs: list[Job], k: int) -> float:
    """We calculate the absolute maximum t that a schedule could end

    Args:
        jobs (list[Job]): a set of all possible jobs
        k (int): the number of jobs to pick

    Returns:
        float: The maximum time at which the worst case schedule ends
    """
    selected_jobs = sorted(jobs, key=lambda j: j.p, reverse=True)[:k]
    return sum(j.p for j in selected_jobs)


# endregion
