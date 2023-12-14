# %%
from matplotlib import pyplot as plt
from numpy import arange, array

from partial_scheduling.algorithms.greedy import greedy3_1
from partial_scheduling.models.job import create_from
from partial_scheduling.search.approximator import outer

# %%
k = 2
LIMIT = 50

jobs = create_from([(1e-6, 1e-6) for _ in range(k - 2)] + [(10, 10), (10, 10)])
jobs += create_from([(7, 15), (15, 7), (5, 24), (18, 6.1)])

x_data = arange(0, LIMIT, 1e0)
lb: list[float] = [outer.lb_exp(jobs, i, k=k) for i in x_data]
ub: list[float] = [outer.ub_exp(jobs, i, k=k) for i in x_data]
y_true = [100 / i for i in x_data]
a = greedy3_1(jobs, k)
print(a)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [j.p for j in jobs]
ys = [j.w for j in jobs]
ax.set_title(f"k={k}")
ax.scatter(xs, ys, label="Staring Jobs")
ax.plot(x_data, lb, "b--", label="lower bound")
ax.plot(x_data, ub, "g--", label="upper bound")
# plt.plot(x_data, y_true, "r-", label="True")
possible_area = array(ub) - array(lb)
are_possible = [1 if x > 0 else -1 for x in possible_area]
are_possible_integer = [1 if x >= 1 else -1 for x in possible_area]
plt.plot(x_data, are_possible, "r.", label="possible job weight")
plt.plot(x_data, are_possible_integer, "g.", label="possible integer job")
ax.legend()
ax.set_ylim((0, LIMIT))
# ax.set_yscale("log")
plt.show()

# %%
