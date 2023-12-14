# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import logging

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from partial_scheduling.algorithms.greedy import greedy3_1
from partial_scheduling.models.job import create_from

# %%
from ..generator import (
    find_improvement,
    find_improvement_recursive,
    find_improvement_recursive_ex,
)


# %%
def func1(x: float, a: float, b: float, c: float, d: float) -> float:
    return b / (x**a - c) + d


def func1_print(a: float, b: float, c: float, d: float) -> str:
    return f"{b}/(x^{{{a}}} - {c}) + {d}"


def func2(x: float, a: float, b: float, c: float) -> float:
    return b / (x + a) + c


def func2_print(a: float, b: float, c: float) -> str:
    return f"{b}/(x + {a}) + {c}"


def func3(x: float, a: float, b: float, c: float) -> float:
    return b / (x**c - a) + a


def func3_print(a: float, b: float, c: float) -> str:
    return f"{b}/(x^{{{c}}}-{a}) + {a}"


# %%
data = [(4.65, 5.775), (6, 5), (10, 3.55), (20, 2.08)]
data.sort(key=lambda x: x[0])
x_data_list: list[float] = []
y_data_list: list[float] = []

for x_data, y_data in data:
    x_data_list.append(x_data)
    y_data_list.append(y_data)


# %%
popt1, pcov = curve_fit(func1, x_data_list, y_data_list)
func1_print(*popt1)


# %%
popt2, pcov = curve_fit(func2, x_data_list, y_data_list)
func2_print(*popt2)


# %%
plt.scatter(x_data_list, y_data_list)
span = np.linspace(0, x_data_list[-1] + 5, 1000)
plt.plot(span, func1(span, *popt1), "r--", label="lower limit f1")
plt.plot(span, func2(span, *popt2), "b--", label="lower limit f2")
plt.plot(span, func1(span, 1, 30, 0, 0), "g-", label="lower limit")
plt.xlim([0, x_data_list[-1] + 5])
plt.ylim([0, 20])
plt.xlabel("processing time")
plt.ylabel("weight")
plt.legend()
plt.show()
# print(func1(9, *popt1), func2(9, *popt2))


# %%

logging.basicConfig(level=logging.WARNING, format="%(message)s", force=True)

find_improvement_recursive(create_from([(1, 1), (5, 15), (15, 5)]), k=3)


# %%

logging.basicConfig(level=logging.INFO, format="%(message)s", force=True)

jobs = create_from(
    [
        (1, 1),
        (5, 15),
        (15, 5),
        (8, 8),
        (8, 8),
        (3.9, 21),
        # (3.89, 21),
    ]
)
greedy3_1(jobs, k=3)
