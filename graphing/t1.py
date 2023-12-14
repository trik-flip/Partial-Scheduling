import logging

from partial_scheduling.algorithms.brute_force import brute_force
from partial_scheduling.algorithms.greedy import greedy3_1
from partial_scheduling.algorithms.ilp import ilp
from partial_scheduling.models.graph import Graph
from partial_scheduling.models.job import Job, create_from
from partial_scheduling.models.schedule import Schedule
from Protato import Profiler

# logging.basicConfig(
#     filename="extra_extra_jobs3.txt",
#     encoding="utf-8",
#     level=logging.WARNING,
#     format="%(message)s",
# )
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

# jobs = [(2, 37), (2, 40), (2, 42), (23, 4), (32, 3), (14, 7), (5, 20)]
# #                                     ^                          ^
K = 3
JOBS = create_from(
    [
        (1, 1),  # initial jobs
        (100, 100),  # initial jobs
        (100, 100),  # initial jobs
        (95, 110),  # 0,8357894737, 1,3590909091
        (120, 90),  # 0,8822222222, 1,2458333333
        # (79.4, 149.5),  # 0
        # 1,1335012595
        # (100.0, 1.0),  # 99.0
        # (1.0, 100.0),  # 18.0
        # (0.95, 110.0),  # 18.0
        # (0.1, 1050.0),  # 0.0
        # (10500.0, 0.01),  # 0.0
        # (1, 1),
        # (10, 10),
        # (10, 10),
        # (25, 5),  # add 1
        # (15, 7),  # add 2
        # (7, 15),  # add 3
        # (12.5, 8),  # add 4
        # (7.5, 13.5),  # add 5
    ]
)
K = 2
JOBS = create_from(
    [
        (5, 10),
        (10, 5),
        (8, 6),
    ]
)

s = brute_force(JOBS, K)
print(s)
s = greedy3_1(JOBS, K)
i = greedy3_1.iterations
print(s, i)
total_graph = Graph(JOBS)
total_graph.show()
g = Graph(s.ordered)
g.show()
# We check all 1/RATIO (in this case 0.1) changes
exit()

Profiler().disable()
RATIO = 1 / 0.01
X = int(100 * RATIO)
Y = int(300 * RATIO)
for p, w in (((p + 1) / RATIO, (w + 1) / RATIO) for p in range(X) for w in range(Y)):
    if w % 2 == 0:
        print(f"{p},{w}\t\t\t", end="\r")
    job = Job(p, w)
    sol, iters = greedy3_1(JOBS + [job], K)
    # with this condition we assure that the end result will always stay the same
    if iters > i:
        logging.warning("%s,  # %s", job, s.cost - sol.cost)
print()
exit()

logging.basicConfig(level=logging.INFO)
sol, iters = greedy3_1(JOBS, 3)
print(iters)
print(sol.cost == 330.000048)

exit()

print()
JOBS = create_from([(2, 37), (2, 40), (2, 42), (23, 4), (32, 3), (14, 7)])
sol2, _ = greedy3_1(JOBS, 3)

assert sol == sol2, f"{sol} {sol2}"

JOBS = create_from(
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
        (101, 4),
        (6, 72),
        (44, 10),
        (5, 91),
        (34, 14),
        (12, 41),
        (21, 24),
        (14, 38),
        (30, 18),
        (96, 6),
        (52, 12),
        (15, 47),
        (42, 19),
        (6, 138),
        (22, 38),
        (144, 6),
        (10, 94),
        (25, 39),
        (57, 18),
        (14, 81),
        (37, 31),
        (11, 110),
        (157, 8),
        (85, 15),
        (28, 50),
        (86, 17),
        (30, 53),
        (68, 25),
        (19, 90),
        (58, 31),
        (21, 87),
        (37, 51),
        (15, 128),
        (22, 95),
        (15, 145),
        (19, 122),
        (129, 18),
        (46, 51),
        (136, 18),
        (21, 119),
        (32, 84),
        (26, 109),
        (116, 25),
        (75, 39),
        (58, 52),
        (148, 21),
        (48, 66),
        (107, 30),
        (37, 87),
        (62, 53),
        (47, 71),
        (39, 86),
        (73, 46),
        (22, 154),
        (38, 93),
        (58, 62),
        (90, 41),
        (44, 84),
        (143, 26),
        (24, 157),
        (160, 24),
        (46, 85),
        (26, 151),
        (116, 36),
        (64, 66),
        (106, 40),
        (37, 126),
        (158, 31),
        (85, 58),
        (115, 43),
        (32, 158),
        (88, 58),
        (119, 43),
        (158, 33),
        (129, 42),
        (80, 68),
        (44, 127),
        (75, 75),
        (142, 41),
        (127, 48),
        (66, 96),
        (47, 138),
        (133, 49),
        (90, 73),
        (112, 60),
        (75, 90),
        (61, 117),
        (58, 131),
        (68, 112),
        (94, 83),
        (110, 72),
        (122, 65),
        (133, 60),
        (100, 80),
        (65, 124),
        (64, 144),
        (91, 102),
        (101, 92),
        (75, 125),
        (61, 160),
        (124, 80),
        (141, 71),
        (91, 112),
        (70, 147),
        (78, 133),
        (124, 84),
        (135, 78),
        (95, 111),
        (86, 123),
        (135, 80),
        (143, 76),
        (76, 144),
        (103, 111),
        (159, 72),
        (122, 94),
        (132, 88),
        (89, 131),
        (74, 160),
        (107, 111),
        (105, 115),
        (104, 118),
        (110, 112),
        (92, 134),
        (87, 142),
        (154, 81),
        (139, 90),
        (88, 145),
        (106, 124),
        (89, 158),
        (90, 158),
        (118, 122),
        (128, 114),
        (115, 128),
        (145, 102),
        (148, 100),
        (96, 155),
        (101, 149),
        (152, 101),
        (152, 101),
        (135, 115),
        (138, 115),
        (118, 135),
        (137, 129),
        (150, 126),
        (137, 143),
        (128, 159),
        (139, 153),
        (143, 159),
        (153, 156),
        (156, 160),
    ]
)

sol = ilp(JOBS, 10)
print(sol)
sol2 = greedy3_1(JOBS, 10)
assert sol.cost == sol2.cost
s1 = create_from([(2, 37), (2, 40), (2, 42)])
# replace (2,42) with (23,4), from 466 to 336
s2 = create_from([(2, 37), (23, 4), (2, 40)])
# replace (2,40) with (5,20), from 336 to 334
d3 = create_from([(2, 37), (5, 20), (23, 4)])
# replace (23,4) with (32,3), from 334 to 331
d4 = create_from([(2, 37), (32, 3), (5, 20)])
# replace (5,20) with (14,7), from 331 to 330
s5 = create_from([(2, 37), (32, 3), (14, 7)])

start = [1, 1, 1, 0, 0, 0, 0]
end = [1, 0, 0, 0, 1, 1, 0]
inter = [0, 0, 0, 1, 0, 0, 1]

new_jobs: list[Job] = []
for i in range(1, 50):
    for j in range(1, 50):
        new_job = Job(i, j)
        if Schedule([new_job] + s1[:-1]).cost == 336:
            new_jobs += [new_job]

solution = Schedule({(2, 37), (14, 7), (32, 3)})
pos: list[Job] = []
print(len(new_jobs))
for new_job in new_jobs:
    sol = greedy3_1(JOBS + [new_job], 3)
    sol_n = greedy3_1(JOBS, 3)
    print(sol)
    print(solution.cost, sol.cost, sol_n.cost)
    if sol == solution:
        print(new_job)
        pos.append(new_job)
    print()

print(pos)
