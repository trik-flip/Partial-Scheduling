BASE_JOBS = (1, 2)
JOBS_IN_ORDER = [3, 1, 4, 2]


# we can't use zip because we don't know if we have the same number of jobs
def job_pairs(jobs_in_order: list[int], base_jobs: tuple[int, ...]):
    inserted_jobs = [job for job in JOBS_IN_ORDER if job not in BASE_JOBS]
    for new_job in inserted_jobs:
        new_job_index = jobs_in_order.index(new_job)
        for base_job in base_jobs:
            job_index = jobs_in_order.index(base_job)
            if new_job_index < job_index:
                yield (new_job, base_job)
            else:
                yield (base_job, new_job)
    return StopIteration


print(list(job_pairs(JOBS_IN_ORDER, BASE_JOBS)))
