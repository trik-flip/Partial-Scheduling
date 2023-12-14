from collections.abc import Iterable
from itertools import combinations
from typing import overload

from .job import Job, sort

GraphRepresentation = list[list[float]]


class Graph:
    jobs: list[Job]
    """A list representation of the jobs,
      this ensures the jobs being in the same order every time,
        jobs will be sorted on ratio when created"""
    graph_table: GraphRepresentation
    """A graph representation of the jobs, where all the jobs plus connection cost are registered
    This should be a symmetrical matrix, with n rows and n columns,
      where n is the number of available jobs"""

    @property
    def nodes(self) -> list[float]:
        """Will return the values on the diagonal,
        is practically the same as [j.cost for j in graph.jobs]"""
        # return [self.graph_table[i][i] for i, _ in enumerate(self.jobs)]
        return [j.cost for j in self.jobs]

    def __init__(self, jobs: Iterable[Job]) -> None:
        self.jobs = sort(jobs)
        self.graph_table = generate(self.jobs)

    @overload
    def job_cost(self, job: int) -> int:
        """What is the cost of a job, with all the weights in mind

        Args:
            job (int): the index of the job in the schedule

        Returns:
            int: the total cost of the job in the graph
        """

    @overload
    def job_cost(self, job: Job) -> int:
        """What is the cost of a job, with all the weights in mind

        Args:
            job (Job): the job in the schedule

        Returns:
            int: the total cost of the job in the graph
        """

    @overload
    def job_cost(self, job: int, schedule: Iterable[Job]) -> int:
        """What is the cost of a job, given we've already selected some jobs

        Args:
            job (int): the index of the job in question
            jobs (Iterable[Job]): a Iterable of jobs which we've got in our schedule

        Returns:
            int: the total cost of the job in the graph
        """

    @overload
    def job_cost(self, job: Job, schedule: Iterable[Job]) -> int:
        """What is the cost of a job, given we've already selected some jobs

        Args:
            job (int): the job in question
            jobs (Iterable[Job]): a Iterable of jobs which we've got in our schedule

        Returns:
            int: the total cost of the job in the graph
        """

    def job_cost(self, job: int | Job, schedule: None | Iterable[Job] = None) -> float:
        if isinstance(job, Job):
            job = self.jobs.index(job)
        schedule = list(schedule) if schedule is not None else self.jobs
        return sum(
            [v for i, v in enumerate(self.graph_table[job]) if self.jobs[i] in schedule]
        )

    def show(self) -> None:
        """
        Show the graph table
        """
        print("---".join("-----" for _ in self.graph_table[0]))
        print(f"Jobs: {self.jobs}")
        print("---".join("-----" for _ in self.graph_table[0]))
        for i, row in enumerate(self.graph_table):
            print(
                " | ".join(f"{c:>5g}" if i <= j else "_____" for j, c in enumerate(row))
            )
        print("---".join("-----" for _ in self.graph_table[0]))


def generate(jobs: Iterable[Job]) -> GraphRepresentation:
    """Generate a graph from a iteration of jobs

    Args:
        jobs (Iterable[Job]): the jobs for which a graph needs to be generated

    Returns:
        list[list[int]]: The graph representation of the jobs
    """
    if not isinstance(jobs, list):
        jobs = sort(jobs)
    return [[min(i.p * j.w, j.p * i.w) for i in jobs] for j in jobs]


def cost(
    jobs: list[Job], chosen_jobs: list[Job], graph: GraphRepresentation | None = None
) -> float:
    graph = graph or generate(jobs)
    indexes = [jobs.index(j) for j in chosen_jobs]
    return sum(graph[i][j] for (i, j) in combinations(indexes, 2)) + sum(
        graph[i][i] for i in indexes
    )
