from partial_scheduling.models.job import Job


def upper_bound(*jobs: Job):
    j1 = jobs[0]
    j2 = jobs[1]
    return lambda i: (j1.p * (j1.w + j2.w)) / (i) - j2.w
