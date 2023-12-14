from itertools import combinations, permutations

from partial_scheduling.models.schedule import Schedule


def brute_force(jobs, k):
    job_cost = []
    for pos in combinations(jobs, k):
        cost = Schedule(pos).cost
        job_cost.append((pos, cost))
    return job_cost


def set_colors(job_cost):
    for pos, cost in job_cost:
        for p in permutations(pos):
            # TODO: implement
            pass
