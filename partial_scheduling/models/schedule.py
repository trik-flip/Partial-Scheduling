from collections.abc import Callable, Iterable
from typing import Any, Generator, overload

from Protato import Profiler

from .job import Job, combine, create_from, iter_equal, sort


class Schedule:
    jobs: Iterable[Job]
    is_sorted: bool
    iter_index: int

    @property
    def ordered(self) -> list[Job]:
        if not self.is_sorted:
            self.sort()
        assert isinstance(self.jobs, list)
        return self.jobs

    @property
    def cost(self) -> float:
        """The cost of the schedule"""
        total_cost = 0
        current_processing_time = 0

        for j in self.ordered:
            current_processing_time += j.p
            total_cost += j.w * current_processing_time
        return total_cost

    def __contains__(self, val: Job) -> bool:
        return val in self.jobs

    def __len__(self) -> int:
        if not isinstance(self.jobs, list):
            self.jobs = list(self.jobs)
        return len(self.jobs)

    def __iter__(self) -> "Schedule":
        self.iter_index = 0
        self.sort()
        return self

    def __next__(self) -> Job:
        assert isinstance(self.jobs, list)
        if self.iter_index == len(self.jobs):
            raise StopIteration
        job = self.jobs[self.iter_index]
        self.iter_index += 1
        return job

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Schedule):
            value = iter_equal(self.jobs, __value.jobs)
        else:
            value = NotImplemented
        return value

    def __floordiv__(self, other: object) -> "Schedule":
        if isinstance(other, Schedule):
            jobs = [j for j in self.jobs if j not in other.jobs]
        elif isinstance(other, tuple) and all(isinstance(j, Job) for j in other):
            jobs = [j for j in self.jobs if j is not other[1]] + [other[0]]
        elif isinstance(other, Job):
            jobs = [j for j in self.jobs if id(j) != id(other)]
        else:
            jobs = NotImplemented
        if jobs is not NotImplemented:
            jobs = Schedule(jobs)
        return jobs

    def __or__(self, other: object) -> "Schedule":
        if isinstance(other, Job):
            jobs = self.ordered + [other]
        elif isinstance(other, Schedule):
            jobs = self.ordered + other.ordered
        else:
            jobs = NotImplemented
        if jobs is not NotImplemented:
            jobs = Schedule(jobs)
        return jobs

    @overload
    def __init__(self) -> None:
        """Create an empty Schedule"""

    @overload
    def __init__(self, jobs: Iterable[Job]) -> None:
        """Create Schedule from a list, set or any other iterable containing Jobs

        Args:
            jobs (Iterable[Job]): An list,set or other iterable containing Job objects
        """

    @overload
    def __init__(self, jobs: Iterable[tuple[float, float]]) -> None:
        """Create Schedule from a list,
          set or any other iterable containing tuple of processing time and weights

        Args:
            jobs (Iterable[Job]): An iterable containing tuples with processing time and weights
        """

    @Profiler()
    def __init__(
        self, jobs: Iterable[Job] | Iterable[tuple[float, float]] | None = None
    ) -> None:
        self.is_sorted = False
        if jobs is None:
            jobs = []
        elif all(isinstance(job, tuple) for job in jobs):
            jobs = create_from(jobs)
        self.jobs = jobs

    @Profiler()
    def __repr__(self) -> str:
        return f"({self.cost})-{self.ordered}"

    @Profiler()
    def sort(self) -> None:
        self.jobs = sort(self.jobs)
        self.is_sorted = True

    def where(self, func: Callable[[Job], bool]) -> "Schedule":
        return Schedule([j for j in self.ordered if func(j)])

    @Profiler()
    def combine(
        self, jobs: "Schedule", reduced: bool = False, is_sorted: bool = False
    ) -> Generator[tuple[Job, Job], Any, None]:
        """combine all jobs from this schedule with the jobs from a other schedule

        Args:
            jobs (Schedule): The jobs we want to create pairs with
            reduced (bool, optional): whether or not we use the reduced form. Defaults to False.
            is_sorted (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_

        Yields:
            Generator[tuple[Job, Job], Any, None]: _description_
        """
        exclusive = jobs // self
        return combine(
            exclusive.ordered, self.ordered, reduced=reduced, is_sorted=is_sorted
        )
