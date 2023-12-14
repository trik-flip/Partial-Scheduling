# %% imports
from matplotlib import pyplot as plt
from numpy import arange

from partial_scheduling.algorithms.greedy import greedy3_1
from partial_scheduling.models.job import cost, create_from
from partial_scheduling.search.approximator import outer

# %% defining constant values

K = 2
LIMIT = 25
STEP_SIZE = 1e-1

# %% Choosing starting jobs
base = [(5, 6), (5, 7), (5, 8), (5, 9)]
other = [(5, 5), (5, 7), (4, 5), (4, 7)]
fig = plt.figure()
TOTAL = len(base) * len(other)
for i, b in enumerate(base):
    for ii, o in enumerate(other):
        index = i * len(other) + ii + 1
        print(f"[{index}/{TOTAL}]\t", end="\r")
        ax = fig.add_subplot(
            len(other),
            len(base),
            index,
        )
        starting_jobs = [b, o]
        jobs = create_from([(1e-6, 1e-6) for _ in range(K - 2)])
        jobs += create_from(starting_jobs)

        xs1 = [j.p for j in jobs]
        ys1 = [j.w for j in jobs]

        x_data = arange(1, LIMIT, STEP_SIZE)

        lb = [outer.lb_exp(jobs, i, k=K) for i in x_data]
        ub = [outer.ub_exp(jobs, i, k=K) for i in x_data]
        y_true = [max(map(cost, jobs)) / i for i in x_data]

        original_solution = greedy3_1(jobs, K)
        ax.set_title(
            f"cost: {original_solution.cost}, iterations: {greedy3_1.iterations}"
        )

        ax.scatter(xs1, ys1, label="Staring Jobs")
        ax.plot(x_data, lb, "b-", label="lower bound")
        ax.plot(x_data, ub, "g-", label="upper bound")
        ax.plot(x_data, y_true, "r--", label="true bound")
        ax.set_ylim((0, LIMIT))

plt.legend()
plt.show()
