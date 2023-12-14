from collections.abc import Iterable
from typing import Self, overload

from .job import Job, cost


class Node:
    """A node for in a tree"""

    j: Job
    left: Self | None
    right: Self | None
    parent: Self | None

    @overload
    def __init__(self, job: Job) -> None:
        ...

    @overload
    def __init__(self, job: Job, parent: Self) -> None:
        ...

    def __init__(self, job: Job, parent: Self | None = None) -> None:
        self.j = job
        self.left = None
        self.right = None
        self.parent = parent

    def add(self, job: Job) -> None:
        if self.j.cost > job.cost:
            temp = self.j
            self.j = job
            job = temp
        if job.ratio < self.j.ratio:
            self.add_left(job)
        else:
            self.add_right(job)

    def get(self) -> Job:
        job = self.j

        return job

    def add_right(self, job: Job) -> None:
        if self.right is None:
            self.right = Node(job, self)
        else:
            self.right.add(job)

    def add_left(self, job: Job) -> None:
        if self.left is None:
            self.left = Node(job, self)
        else:
            self.left.add(job)


class BTree:
    jobs: list[Job]
    root: Node

    def __init__(self, jobs: Iterable[Job]) -> None:
        # sort it like in the schedule
        self.jobs = sorted(jobs, key=cost)
        self.root = Node(self.jobs[0])
        self.create()

    def create(self) -> None:
        for job in self.jobs[1:]:
            self.root.add(job)
