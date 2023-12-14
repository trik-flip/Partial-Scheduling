from collections.abc import Iterable

from pulp import LpInteger, LpMinimize, LpProblem, LpVariable, apis, lpSum

from Protato import Profiler

from ..models.graph import generate
from ..models.job import Job
from ..models.schedule import Schedule


@Profiler()
def ilp(jobs: Iterable[Job], k: int) -> Schedule:
    jobs = list(jobs)
    prob = LpProblem("Partial_Scheduling_Problem", LpMinimize)

    graph = generate(jobs)
    chosen_job_pairs = LpVariable.matrix(
        "y",
        # tuple([tuple([y + 1 for x in range(5)]) for y in range(5)]),
        (
            tuple(x + 1 for x, _ in enumerate(jobs)),
            tuple(x + 1 for x, _ in enumerate(jobs)),
        ),
        0,
        1,
        LpInteger,
    )
    chosen_jobs = LpVariable.matrix(
        "x", (tuple(x + 1 for x, _ in enumerate(jobs)),), 0, 1, LpInteger
    )
    prob += (
        lpSum(
            [
                graph[i1][i2] * chosen_job_pairs[i1][i2]
                for i1, _ in enumerate(jobs)
                for i2, _ in enumerate(jobs)
                if i1 <= i2
            ]
        ),
        "The cost of an schedule",
    )
    prob += (
        lpSum([chosen_jobs[i] for i, _ in enumerate(jobs)]) >= k,
        "pick k jobs",
    )
    for i, _ in enumerate(jobs):
        for j, _ in enumerate(jobs):
            prob += (
                chosen_job_pairs[i][j] - chosen_jobs[i] - chosen_jobs[j] >= -1,
                f"picking job couples {i} {j}",
            )
    prob.solve(apis.PULP_CBC_CMD(msg=False))
    chooser: list[int] = [i.varValue for i in chosen_jobs]
    assert sum(chooser) == k
    schedule = Schedule([j for j, x in zip(jobs, chooser) if x == 1])
    assert len(schedule) == k
    return schedule
