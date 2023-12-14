import logging
from collections.abc import Iterable

from Protato import Profiler

from ..models.graph import Graph, cost
from ..models.job import Job, cost, ratio, sort
from ..models.schedule import Schedule


# region: Greedy 1
@Profiler()
def greedy1(jobs: Iterable[Job], k: int) -> Schedule:
    """As from the thesis
    Has a really bad approximation
    """
    schedule = sorted(jobs, key=cost)[:k]
    return Schedule(schedule)


@Profiler()
def greedy1_1(jobs: Iterable[Job], k: int) -> Schedule:
    """We take the jobs adding the least cost,
    but if we have multiple jobs which add the same cost,
      we take the job with the lowest ratio
    """
    schedule = []
    while len(schedule) < k:
        next_best: list[Job] = sorted([j for j in jobs if j not in schedule], key=cost)
        min_cost = next_best[0].cost

        next_best = list(filter(lambda j, c=min_cost: j.cost == c, next_best))
        if len(schedule) + len(next_best) <= k:
            schedule += [next_best]
        else:
            schedule += sorted(next_best, key=ratio)[
                : len(schedule) + len(next_best) - k
            ]
    return Schedule(schedule)


# NOTE: This is worst than greedy1_1, since we over priorities on processing time,
# but there is a symmetry in the cost
def greedy1_2(jobs: Iterable[Job], k: int) -> Schedule:
    """instead of sorting with jp * jw, we sort with jp^2 * jw,
    increasing the importance of the processing time"""
    schedule = sorted(jobs, key=lambda j: j.cost * j.p**2)[:k]
    return Schedule(schedule)


# endregion


# region: Greedy 2
@Profiler()
def greedy2(jobs: Iterable[Job], k: int) -> Schedule:
    """
    Analyses greedy2
    ----------------
    ## k = 1, [(1, 10), (3, 3), (10, 1)]
        C1:
            alg pick job 'j', such that C(j) <= C(j_opt).
            Therefor it's optimal

    ## k = 2, [(1, 10), (3, 3), (10, 1)]
        C1: j_1 = (1, 10) || j_1 = (10, 1)
            alg picks an job 'j_1' from 'n' which is also in 'opt',
            Then j_2 will have a cost <= cost(opt),
            since it takes the job with the lowest increase in cost
        C2: j_1 = (3, 3)
            alg picks an job 'j' that is not in 'opt', then
            C2.1 second job 'j2' is in 'opt', then
                C2.1.1: r1 >= r2,
                then 'j' could have an higher potential cost then 'opt'
                C2.1.2: r1 < r2
                    Then the job not in 'opt' has a higher p or a lower w.
                    But if only processing time is higher,
                    then it's strictly worse,
                    and if only weight is lower then it's strictly better.
                    So both should be different!
                    But since the ratio is lower,
                    it should strictly be better if placed at the end of S!
                    TODO: check whether this is true or not
    Documented Mistake On K=2
    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(10)-[[2-2], [4-1]]
        greedy2:(10)-[[2-2], [4-1]]
        NOTE: Chose 2,2 over 1,4
        opt_ilp:(9)-[[1-4], [4-1]]
        opt_brute_force:(9)-[[1-4], [4-1]]
        greedy2_prefer_short:(9)-[[1-4], [4-1]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(38)-[[1-17], [2-7]]
        greedy2:(38)-[[1-17], [2-7]]
        opt_ilp:(37)-[[1-17], [3-5]]
        opt_brute_force:(37)-[[1-17], [3-5]]
        greedy2_prefer_short:(38)-[[1-17], [2-7]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(20)-[[2-4], [4-2]]
        greedy2:(20)-[[2-4], [4-2]]
        opt_ilp:(18)-[[1-8], [4-2]]
        opt_brute_force:(18)-[[1-8], [4-2]]
        greedy2_prefer_short:(18)-[[1-8], [4-2]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(73)-[[3-11], [7-4]]
        greedy2:(73)-[[3-11], [7-4]]
        opt_ilp:(71)-[[3-11], [16-2]]
        opt_brute_force:(71)-[[3-11], [16-2]]
        greedy2_prefer_short:(73)-[[3-11], [7-4]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(30)-[[1-14], [3-4]]
        greedy2:(30)-[[1-14], [3-4]]
        opt_ilp:(30)-[[1-14], [3-4]]
        opt_brute_force:(30)-[[1-14], [3-4]]
        greedy2_prefer_short:(32)-[[1-14], [2-6]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(30)-[[2-7], [6-2]]
        greedy2:(30)-[[2-7], [6-2]]
        opt_ilp:(29)-[[2-7], [13-1]]
        opt_brute_force:(29)-[[2-7], [13-1]]
        greedy2_prefer_short:(30)-[[2-7], [6-2]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(29)-[[1-13], [3-4]]
        greedy2:(29)-[[1-13], [3-4]]
        opt_ilp:(29)-[[1-13], [3-4]]
        opt_brute_force:(29)-[[1-13], [3-4]]
        greedy2_prefer_short:(31)-[[1-13], [2-6]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(14)-[[2-3], [6-1]]
        greedy2:(14)-[[2-3], [6-1]]
        opt_ilp:(13)-[[1-6], [6-1]]
        opt_brute_force:(13)-[[1-6], [6-1]]
        greedy2_prefer_short:(13)-[[1-6], [6-1]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(28)-[[1-13], [4-3]]
        greedy2:(28)-[[1-13], [4-3]]
        opt_ilp:(28)-[[1-13], [4-3]]
        opt_brute_force:(28)-[[1-13], [4-3]]
        greedy2_prefer_short:(30)-[[2-6], [4-3]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(29)-[[1-14], [4-3]]
        greedy2:(29)-[[1-14], [4-3]]
        opt_ilp:(29)-[[1-14], [4-3]]
        opt_brute_force:(29)-[[1-14], [4-3]]
        greedy2_prefer_short:(30)-[[1-14], [3-4]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(57)-[[3-9], [7-3]]
        greedy2:(57)-[[3-9], [7-3]]
        opt_ilp:(55)-[[3-9], [11-2]]
        opt_brute_force:(55)-[[3-9], [11-2]]
        greedy2_prefer_short:(57)-[[3-9], [7-3]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(28)-[[1-13], [4-3]]
        greedy2:(28)-[[1-13], [4-3]]
        opt_ilp:(27)-[[1-13], [13-1]]
        opt_brute_force:(27)-[[1-13], [13-1]]
        greedy2_prefer_short:(28)-[[1-13], [4-3]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(96)-[[8-5], [20-2]]
        greedy2:(96)-[[8-5], [20-2]]
        opt_ilp:(91)-[[3-15], [20-2]]
        opt_brute_force:(91)-[[3-15], [20-2]]
        greedy2_prefer_short:(96)-[[8-5], [20-2]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(30)-[[3-4], [6-2]]
        greedy2:(30)-[[3-4], [6-2]]
        opt_ilp:(28)-[[3-4], [13-1]]
        opt_brute_force:(28)-[[3-4], [13-1]]
        greedy2_prefer_short:(28)-[[3-4], [13-1]]

    WARNING:root:[ERROR] schedules are not same
        greedy_2_graph:(37)-[[7-2], [16-1]]
        greedy2:(37)-[[7-2], [16-1]]
        opt_ilp:(36)-[[4-4], [16-1]]
        opt_brute_force:(36)-[[4-4], [16-1]]
        greedy2_prefer_short:(37)-[[7-2], [16-1]]
    """
    schedule = []
    # while len(schedule) < k:
    for _ in range(k):
        costs = [(j, Schedule(schedule + [j]).cost) for j in jobs if j not in schedule]
        best_job = min(costs, key=lambda j: j[1])[0]
        schedule.append(best_job)
    return Schedule(schedule)


@Profiler()
def greedy2_throw_out(jobs: Iterable[Job], k: int) -> Schedule:
    schedule = []
    while len(schedule) < k:
        costs = [(j, Schedule(schedule + [j]).cost) for j in jobs if j not in schedule]
        best_job = min(costs, key=lambda j: j[1])[0]
        new_schedule = [j for j in schedule if j <= best_job]
        schedule = new_schedule + [best_job]
    return Schedule(schedule)


@Profiler()
def greedy2_short_first_throw_out(jobs: Iterable[Job], k: int) -> Schedule:
    schedule = []
    while len(schedule) < k:
        min_cost = float("inf")
        best_job = None
        for j in [j for j in jobs if j not in schedule]:
            c = Schedule(schedule + [j]).cost
            if c < min_cost:
                min_cost = c
                best_job = j
            elif c == min_cost and best_job is not None and j.p < best_job.p:
                best_job = j
        new_schedule = [j for j in schedule if j <= best_job]
        schedule = new_schedule + [best_job]
    return Schedule(schedule)


@Profiler()
def greedy2_short_first_throw_out_slack(jobs: Iterable[Job], k: int) -> Schedule:
    schedule = []
    while len(schedule) < k:
        min_cost = float("inf")
        best_job = None
        for j in [j for j in jobs if j not in schedule]:
            c = Schedule(schedule + [j]).cost
            if c < min_cost:
                min_cost = c
                best_job = j
            elif c == min_cost + 1 and best_job is not None and j.p < best_job.p:
                best_job = j
        new_schedule = [j for j in schedule if j <= best_job]
        schedule = new_schedule + [best_job]
    return Schedule(schedule)


@Profiler()
def greedy2_prefer_short(jobs: Iterable[Job], k: int) -> Schedule:
    """As from the Thesis"""
    schedule = []
    while len(schedule) < k:
        min_cost = float("inf")
        best_job = None
        for j in [j for j in jobs if j not in schedule]:
            c = Schedule(schedule + [j]).cost
            if c < min_cost:
                min_cost = c
                best_job = j
            elif c == min_cost and best_job is not None and j.p < best_job.p:
                best_job = j
        schedule.append(best_job)
    return Schedule(schedule)


@Profiler()
def greedy2_graph(jobs: Iterable[Job], k: int) -> Schedule:
    """picking the best, but then only from the graph"""
    schedule = []
    _g = Graph(jobs)

    while len(schedule) < k:
        min_cost = float("inf")
        best_job = None
        # costs = [
        #     (j, cost(_g.jobs, schedule + [j], _g.graph_table))
        #     for j in jobs
        #     if j not in schedule
        # ]
        # best_job = min(costs, key=lambda j: j[1])[0]

        for j in [j for j in jobs if j not in schedule]:
            c = cost(_g.jobs, schedule + [j], _g.graph_table)
            if c < min_cost:
                min_cost = c
                best_job = j
        schedule.append(best_job)
    return Schedule(schedule)


@Profiler()
def greedy2_list(jobs: Iterable[Job], k: int) -> Schedule:
    """This way we can preserve the order in which we choose the jobs"""
    schedule = []
    while len(schedule) < k:
        min_cost = float("inf")
        best_job = None
        for j in [j for j in jobs if j not in schedule]:
            if (c := Schedule(schedule + [j]).cost) < min_cost:
                min_cost = c
                best_job = j
        schedule.append(best_job)
    return Schedule(schedule)


@Profiler()
def greedy2_1(jobs: Iterable[Job], k: int) -> Schedule:
    """
    instead of checking only on min-cost,
    we'll also check on whether or not a job has a high potential cost,
    we can measure it in minimum potential cost
    NOTE: we don't need to test this, because in the worst case this will be reduced to the normal greedy2 algorithm
    """
    pass


# endregion


# region: Greedy 3
@Profiler()
def greedy3(jobs: Iterable[Job], k: int) -> Schedule:
    schedule = list(jobs)[:k]
    improved = True
    graph_model = Graph(jobs)
    last_cost = float("inf")
    while improved:
        best_job = min(
            (j for j in jobs if j not in schedule),
            key=lambda j, s=schedule: graph_model.job_cost(j, s),
        )
        new_schedule = schedule + [best_job]
        worst_job = max(
            (j for j in new_schedule),
            key=lambda j, s=new_schedule: graph_model.job_cost(j, s),
        )
        if best_job == worst_job:
            improved = False
            continue
        schedule.append(best_job)
        schedule.remove(worst_job)
        c = Schedule(schedule).cost
        if c >= last_cost:
            improved = False
            continue
        last_cost = c
    return Schedule(schedule)


@Profiler()
def greedy3_1(jobs: Iterable[Job], k: int, use_log_book=False) -> Schedule:
    """instead of just adding a job, and checking the cost in the graph,
    we'll check wether it's better while removing another job

    Args:
        jobs (Iterable[Job]): all the possible jobs
        k (int): the number of jobs to take

    Returns:
        set[Job]: the optimal subset of jobs, where |S| = k
    """

    jobs_ordered = sorted(sort(jobs), key=cost)
    schedule = Schedule(jobs_ordered[:k])
    s_jobs = Schedule(jobs)
    log_book: list[tuple[Job, Job]] | None = [] if use_log_book else None

    logging.info("initial_schedule = %s", schedule)
    greedy3_1.iterations = 0
    while True:  # Ohm(n), O(n^2)?
        greedy3_1.iterations += 1
        best_pair = _greedy3_1_inner(schedule, s_jobs, log_book)
        if best_pair is None:
            logging.info("final_schedule = %s", schedule)
            return schedule
        if log_book is not None:
            log_book.append(best_pair)
        schedule = schedule // best_pair

        logging.info(
            "swapping %s for %s, new_cost = %d",
            best_pair[1],
            best_pair[0],
            schedule.cost,
        )


@Profiler()
def _greedy3_1_inner(
    schedule: Schedule, s_jobs: Schedule, log_book: list[tuple[Job, Job]] | None = None
) -> tuple[Job, Job] | None:
    pair_cost: dict[float, list[tuple[Job, Job]]] = {}
    best_pair = None
    best_cost = schedule.cost
    for job1, job2 in schedule.combine(s_jobs, reduced=True):  # O(k(n-k))
        new_schedule = schedule // (job1, job2)
        c = new_schedule.cost
        if c not in pair_cost:
            pair_cost[c] = []
        pair_cost[c].append((job1, job2))
        if (
            log_book is not None and c <= best_cost and (job1, job2) not in log_book
        ) or (log_book is None and c < best_cost):
            best_cost = c
            best_pair = job1, job2
    if best_pair is not None:
        logging.info("best pairs: %s", pair_cost[best_cost])
    return best_pair


# endregion
