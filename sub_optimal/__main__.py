from random import randint, seed

import matplotlib.pyplot as plt
import numpy as np
from partial_scheduling.models.job import Job, ratio, cost


def cost_of_jobs(job1: Job, job2: Job):
    return job1.p * job1.w + (job1.p + job2.p) * job2.w


def calc(job1: Job, job2: Job):
    if ratio(job1) >= ratio(job2):
        job1, job2 = job2, job1
    return cost_of_jobs(job1, job2)


def cost_of_index(i, j, job_list):
    return calc(job_list[i], job_list[j])


if __name__ == "__main__":
    NUMBER_OF_JOBS = 400
    seed(42)

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    def r():
        return randint(1, 100)

    jobs = [Job(r(), r()) for _ in range(NUMBER_OF_JOBS)]
    jobs = sorted(jobs, key=ratio)
    for job in jobs:
        print(job)
    grid = [
        [
            calc(jobs[i], jobs[j]) if i != j else float("inf")
            for i in range(NUMBER_OF_JOBS)
        ]
        for j in range(NUMBER_OF_JOBS)
    ]
    x, y = np.meshgrid(range(NUMBER_OF_JOBS), range(NUMBER_OF_JOBS))
    z = np.array(grid)
    coord = np.unravel_index(z.argmin(), z.shape)
    ax.plot_surface(x, y, z, alpha=0.2)
    possible_jobs = [
        (i, j) for i in range(NUMBER_OF_JOBS) for j in range(NUMBER_OF_JOBS) if i != j
    ]
    job_costs = (cost_of_index(i, j, jobs) for i, j in possible_jobs)
    # for (x, y), z in zip(possible_jobs, job_costs):
    #     ax.scatter(x, y, z)
    ax.scatter(
        *reversed(coord), cost_of_index(*reversed(coord), job_list=jobs), marker="x"
    )
    ax.scatter(*coord, cost_of_index(*coord, job_list=jobs), marker="x")
    # ax.bar3d(*coord, cost_of_index(*coord, job_list=jobs), 0.5, 0.5, 0.5)
    plt.show()
