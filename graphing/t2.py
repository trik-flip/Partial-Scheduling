# %%
from matplotlib import pyplot as plt
from numpy import arange, array

from partial_scheduling.algorithms.greedy import greedy3_1
from partial_scheduling.models.job import create_from
from partial_scheduling.search.approximator import inner

# %%
k = 3
LIMIT = 50

jobs = create_from([(1e-6, 1e-6) for _ in range(k - 2)] + [(5, 15), (15, 5)])
jobs += create_from([])

xdata = arange(0, LIMIT, 0.1)
lb: list[float] = []
ub: list[float] = []
y_true: list[float] = []

for i in xdata:
    lb.append(inner.lb_exp(jobs, i, k=k, t=1e-5, max_runs=10000))
    ub.append(inner.ub_exp(jobs, i, k=k, t=1e-5, max_runs=10000))
    y_true.append(2 * 5 / i)
a = greedy3_1(jobs, k)
print(a)
# %%
xs = [j.p for j in jobs]
ys = [j.w for j in jobs]
plt.title(f"k={k}")
plt.scatter(xs, ys, label="Staring Jobs")
plt.plot(xdata, lb, "b--", label="lower bound")
plt.plot(xdata, ub, "g--", label="upper bound")
# plt.plot(xdata, y_true, "r-", label="True")
possible_area = array(ub) - array(lb)
are_possible = [1 if x > 0 else 0 for x in possible_area]
are_possible_integer = [1 if x >= 1 else 0 for x in possible_area]
# plt.plot(xdata, are_possible, "r.", label="possible job weight")
# plt.plot(xdata, are_possible_integer, "g.", label="possible integer job")
plt.ylim([0, LIMIT])
plt.legend()
plt.show()

# %%
