from collections.abc import Iterable
from typing import Literal

from ..models.job import Job, ratio


def get_ratio(
    jobs: Iterable[Job],
    schedule: Iterable[Job],
) -> list[Literal[0] | Literal[1]]:
    jobs = sorted(jobs, key=ratio)
    return [1 if j in schedule else 0 for j in jobs]


def get_cost(
    jobs: Iterable[Job],
    schedule: Iterable[Job],
) -> list[Literal[0] | Literal[1]]:
    jobs = sorted(jobs, key=ratio)
    return [1 if j in schedule else 0 for j in jobs]
