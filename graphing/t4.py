# %%
from matplotlib import pyplot as plt
from numpy import arange

from partial_scheduling.algorithms.greedy import greedy3_1
from partial_scheduling.models.job import create_from, cost
from partial_scheduling.search.approximator import outer

# %% defining Constants
k = 2
LIMIT = 150
STEP_SIZE = 1e0

# %%
# jobs = create_from([(1e-6, 1e-6) for _ in range(k - 2)] + [(100, 100), (100, 100)])
starting_jobs = [(5, 3), (9, 23)]
jobs = create_from([(1e-6, 1e-6) for _ in range(k - 2)] + starting_jobs)
# jobs += create_from([(90, 115), (120, 85)])
# jobs += create_from([(150, 35)])
j = [
    (17, 23),
    (17, 23),
    (4, 112),
    (20, 20),
    (5, 85),
    (26, 16),
    (6, 68),
    (120, 4),
    (7, 56),
]
j = [(12, 10), (12, 10), (30, 5), (11, 11), (23, 6), (8, 17), (15, 8), (6, 25)]
j = [(25, 4), (9, 23)]
jobs = create_from((j))
# j = [
#     (17, 23),
#     (17, 23),
#     (4, 112),
#     (20, 20),
#     (5, 85),
#     (26, 16),
#     (6, 68),
#     (120, 4),
#     (7, 56),
# ]
# jobs = create_from(j)
x_data = arange(1, LIMIT, STEP_SIZE)
lb = [outer.lb_exp(jobs, i, k=k) for i in x_data]
ub = [outer.ub_exp(jobs, i, k=k) for i in x_data]
lb_errors = outer.lb_exp.errors
ub_errors = outer.ub_exp.errors
y_true = [max(map(cost, jobs)) / i for i in x_data]
schedule = greedy3_1(jobs, k)
print(schedule)
if schedule != len(j) - 1:
    exit()
xs1 = [j.p for j in jobs]
ys1 = [j.w for j in jobs]


# %%
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_title(f"cost: {schedule.cost}, iterations: {greedy3_1.iterations}")
# costs = []
# new_jobs: list[tuple[int, int]] = []
# for i, p in enumerate(x_data):
#     for w in arange(lb[i], ub[i], STEP_SIZE):
#         # for w in arange(1, min(ub[i] + 1, LIMIT), 1):
#         j = Job(p, w)
#         s = greedy3_1(jobs + [j], k)
#         cost = s.cost
#         costs.append(cost)
#         new_jobs.append((p, w))
# xs = [p for p, _ in new_jobs]
# ys = [w for _, w in new_jobs]
# scatter = ax.scatter(xs, ys, c=costs, alpha=0.6)
IS_LABEL_SET = False
# for x, y, c in zip(xs, ys, costs):
#     if c == a[0].cost:
#         if not IS_LABEL_SET:
#             IS_LABEL_SET = True
#             ax.scatter(x, y, c="green", alpha=0.6, label=f"{a[0].cost}")
#         else:
#             ax.scatter(x, y, c="green", alpha=0.6)
if len(lb_errors) > 1:
    ax.scatter(*zip(*lb_errors), color="red")
    ax.scatter(*zip(*ub_errors), color="green")
ax.scatter(xs1, ys1, label="Staring Jobs")
ax.plot(x_data, lb, "b-", label="lower bound")
ax.plot(x_data, ub, "g-", label="upper bound")
ax.plot(x_data, y_true, "r--", label="true bound")
# handles, labels = scatter.legend_elements(prop="colors", alpha=0.6)
ax.set_ylim((0, LIMIT))
l1 = ax.legend()
ax.add_artist(l1)
# ax.legend(handles, labels, loc="upper center")
plt.show()
