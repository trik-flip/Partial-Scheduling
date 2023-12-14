import logging
from time import perf_counter

from Protato.profiler import Profiler

from .algorithms.greedy import greedy3_1
from .models.job import Job, create_from, reduce
from .models.schedule import Schedule
from .models.graph import generate
from .util import scenario

logging.basicConfig(filename="results.log", encoding="utf-8", level=logging.WARNING)

my_jobs = create_from(
    [
        (33, 1),
        (2, 60),
        (2, 68),
        (1, 142),
        (72, 2),
        (39, 5),
        (2, 114),
        (102, 3),
        (3, 110),
        (3, 118),
        (6, 72),
        (44, 10),
        (34, 14),
        (12, 41),
        (21, 24),
    ]
)

solution = create_from(
    [
        (44, 10),
        (2, 60),
        (102, 3),
        (2, 68),
        (33, 1),
        (2, 114),
        (39, 5),
        (72, 2),
        (12, 41),
        (1, 142),
    ]
)
sol = greedy3_1(my_jobs, 10)

print(sol == solution)
step = create_from(
    [
        (33, 1),
        (2, 60),
        (2, 68),
        (1, 142),
        (72, 2),
        (39, 5),
        (2, 114),
        (102, 3),
        (34, 14),
    ]
)
possible_jobs: list[Job] = []
for i in range(1, 100):
    for j in range(1, 100):
        new_j = Job(i, j)
        c = Schedule(step + [new_j]).cost
        if c == 4629:
            possible_jobs.append(new_j)
            print(c, new_j, new_j.cost)


for job in possible_jobs:
    sol = greedy3_1(my_jobs + [job], 10)
    if sol == solution:
        print(job)
exit()
counter: int = 0
algorithms = [greedy3_1]
timers = [0.0 for _ in algorithms]
starting_time = perf_counter()

for n in [30, 40, 45, 60, 80, 120, 160]:
    for k in [2, 3, 4, 5, 10, 15, 20, 30]:
        Profiler().clean()
        for _ in range(1_000_000):
            job_list = scenario.random(n)

            jobs: list[list[Job]] = []
            schedules: list[Schedule] = []

            for i, algorithm in enumerate(algorithms):
                start = perf_counter()
                jobs.append(list(algorithm(job_list, k)))
                schedules.append(Schedule(jobs[i]))
                delta = perf_counter() - start
                timers[i] += delta

            counter += 1
            print(
                f"n:{n},k:{k} | {counter:04}-{perf_counter() - starting_time:.1f}",
                end="\r",
            )
            INFO = " ".join(
                [f"{alg.__name__}:{timers[i]:.3f}" for i, alg in enumerate(algorithms)]
            )
            logging.info("[%(counter)i] %(info)s", {"counter": counter, "info": INFO})
            if not all_the_same(schedules):
                logging.warning("[ERROR] schedules are not same")
                logging.warning(
                    "\n".join(
                        [str([f"{x:03}" for x in row]) for row in generate(job_list)]
                    )
                )
                list_for_text = [
                    f"jobs: {job_list}",
                    f"purged: {reduce(job_list)}",
                ] + [
                    f"{alg.__name__}:{schedules[i]}" for i, alg in enumerate(algorithms)
                ]
                TEXT = "\n\t".join(list_for_text)
                logging.warning(TEXT)

        Profiler().show(zero_runners=False)
