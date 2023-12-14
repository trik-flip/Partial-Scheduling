from collections.abc import Iterable
from itertools import combinations

from Protato import Profiler

from ..models.job import Job
from ..models.schedule import Schedule


@Profiler()
def brute_force_all(jobs: Iterable[Job], k: int) -> list[Schedule]:
    possible_schedules = combinations(jobs, k)

    min_cost = float("inf")
    schedules: dict[float, list[Schedule]] = dict()
    for possible_jobs in possible_schedules:
        pos_schedule = Schedule(possible_jobs)
        cost = pos_schedule.cost
        if cost not in schedules:
            schedules[cost] = []
        schedules[cost].append(pos_schedule)
        min_cost = min(cost, min_cost)

    assert isinstance(min_cost, int)
    return schedules[min_cost]


@Profiler()
def brute_force(jobs: Iterable[Job], k: int) -> Schedule:
    possible_schedules = combinations(jobs, k)

    min_cost = float("inf")
    schedule = None
    for possible_jobs in possible_schedules:
        pos_schedule = Schedule(possible_jobs)
        if (cost := pos_schedule.cost) < min_cost:
            min_cost = cost
            schedule = pos_schedule

    assert schedule is not None
    assert len(schedule) == k
    return schedule
