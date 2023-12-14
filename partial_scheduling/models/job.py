from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Generator, overload


@dataclass
class Job:
    p: float
    w: float

    def __le__(self, other: object) -> bool:
        if isinstance(other, Job):
            return self.ratio <= other.ratio
        return NotImplemented

    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Job):
            return self.ratio == other.ratio and self.p == other.p
        return NotImplemented

    @property
    def ratio(self) -> float:
        return ratio(self)

    @property
    def cost(self) -> float:
        return cost(self)

    def __init__(self, processing_time: float = 1, weight: float = 1) -> None:
        # assert isinstance(processing_time, (float, int))
        # assert isinstance(weight, (float, int))
        self.p = processing_time
        self.w = weight

    def __repr__(self) -> str:
        return f"({self.p},{self.w})"

    def __iter__(self):
        return iter((self.p, self.w))


def cost(job):
    return job.p * job.w


def ratio(job):
    return job.p / job.w


def create_from(jobs: Iterable[tuple[float, float]]) -> list["Job"]:
    return [Job(x, y) for x, y in jobs]


def flip(jobs: Iterable[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(y, x) for x, y in jobs]


def iter_equal(jobs1: Iterable["Job"], jobs2: Iterable["Job"]) -> bool:
    jobs1 = sort(jobs1)
    jobs2 = sort(jobs2)
    if len(jobs1) != len(jobs2):
        return False
    for job1, job2 in zip(jobs1, jobs2):
        if job1 != job2:
            return False
    return True


def sort(jobs: Iterable["Job"], funcs=[cost, ratio]) -> list["Job"]:
    """
    O(n log n)
    """
    jobs = list(jobs)
    for func in funcs:
        jobs.sort(key=func)
    return jobs


@overload
def combine(
    jobs1: Iterable["Job"], jobs2: Iterable["Job"], /
) -> Generator[tuple["Job", "Job"], Any, None]:
    ...


@overload
def combine(
    jobs1: Iterable["Job"],
    jobs2: Iterable["Job"],
    /,
    *,
    reduced: bool,
) -> Generator[tuple["Job", "Job"], Any, None]:
    ...


@overload
def combine(
    jobs1: Iterable["Job"],
    jobs2: Iterable["Job"],
    /,
    *,
    reduced: bool,
    is_sorted: bool = False,
) -> Generator[tuple["Job", "Job"], Any, None]:
    ...


@overload
def combine(
    jobs1: Iterable["Job"],
    jobs2: Iterable["Job"],
    /,
    *,
    is_sorted: bool = False,
) -> Generator[tuple["Job", "Job"], Any, None]:
    ...


def combine(
    jobs1: Iterable["Job"],
    jobs2: Iterable["Job"],
    /,
    *,
    reduced: bool = False,
    is_sorted: bool = False,
) -> Generator[tuple["Job", "Job"], Any, None]:
    """
    O(nm)
    """
    if reduced:
        jobs1 = reduce(jobs1, True)

    if not is_sorted:
        jobs1 = sort(jobs1)

        jobs2 = sort(jobs2)

    for item1 in jobs1:
        for item2 in jobs2:
            if item1 != item2:
                yield item1, item2


def reduce(jobs: Iterable["Job"], weak: bool = False) -> list["Job"]:
    """
    Parameters
    ----------
    jobs: Iterable[Job]
        A set, list or any other Iterable
    weak: bool, default = False
        Whether or not to use the weakly_better or the strictly_better method
        Simply said, getting rid of all doubles from the strictly_better group

    Returns
    -------
    list[Job]
        A list of jobs, which all originate from the jobs parameter, but are all dominating jobs

    Example
    -------
    >>> reduce([Job(1,3),Job(1,3),Job(1,4),Job(2,2),Job(2,3)])
    [Job(1,3), Job(1,3), Job(2,2)]
    >>> reduce([Job(1,3),Job(1,3),Job(1,4),Job(2,2),Job(2,3)], True)
    [Job(1,3), Job(2,2)]
    """
    measure_method = weakly_better if weak else strictly_better
    jobs = list(jobs)
    counter = 0

    while counter < len(jobs):
        counter2 = 0
        while counter2 < len(jobs):
            if counter != counter2 and measure_method(jobs[counter], jobs[counter2]):
                del jobs[counter2]
                if counter2 < counter:
                    counter -= 1
            else:
                counter2 += 1
        counter += 1
    return sorted(jobs, key=lambda j: j.ratio)


def weakly_better(i: "Job", j: "Job") -> bool:
    return (i.p <= j.p) and (i.w <= j.w)


def strictly_better(i: "Job", j: "Job") -> bool:
    return ((i.p <= j.p) and (i.w < j.w)) or ((i.p < j.p) and (i.w <= j.w))
