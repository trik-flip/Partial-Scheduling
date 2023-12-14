import os
import sys
from itertools import combinations
from random import choice

HOME_DIR = "C:/Users/flipp/Documents/School/internship/partial_scheduling/Code/"

if ".venv2" in sys.prefix:
    os.environ["GUROBI_HOME"] = HOME_DIR + ".venv2/Lib/site-packages/gurobipy"
    os.environ["GRB_LICENSE_FILE"] = (
        HOME_DIR + ".venv2/Lib/site-packages/gurobipy/gurobi.lic"
    )

import gurobipy as gp
from gurobipy import GRB

JOBS = [0, 1, 2, 3]
JOB_COMBINATIONS = list(combinations(JOBS, 2))


choice = 4
starting_jobs = tuple(j for j in JOBS if j not in JOB_COMBINATIONS[choice])
init_index = JOB_COMBINATIONS.index(starting_jobs)
print("Start!")

model = gp.Model("qp")


# region: Vars
p = model.addVars(4, lb=1, vtype=GRB.INTEGER, name="p")
w = model.addVars(4, lb=1, vtype=GRB.INTEGER, name="w")
c = model.addVars(6, vtype=GRB.INTEGER, name="c")
# endregion

# region: Constraints
for i in range(3):
    model.addQConstr(p[i] * w[i + 1] <= p[i + 1] * w[i], f"ordering {i}")
for i, (j1, j2) in enumerate(JOB_COMBINATIONS):
    model.addQConstr(
        (c[i] == p[j1] * w[j1] + (p[j1] + p[j2]) * w[j2]),
        f"cost {i}",
    )
for i in range(6):
    if i != choice:
        model.addQConstr((c[init_index] <= c[i]), "can not swap")

model.addQConstr(c[choice] <= c[init_index] - 1, "opt better greedy")
# endregion

model.Params.NonConvex = 2
# model.Params.Presolve = 0
model.optimize()

if model.Status != 2:
    print("Can't solve")
    exit()
p_: list[int] = []
w_: list[int] = []
c_: list[int] = []
for v in model.getVars():
    if v.VarName[0] == "p":
        p_.append(int(v.X))
    elif v.VarName[0] == "w":
        w_.append(int(v.X))
    elif v.VarName[0] == "c":
        c_.append(int(v.X))
jobs = list(zip(p_, w_))
print(JOB_COMBINATIONS[choice])


def get_jobs(job_list, indexes):
    i, j = indexes
    return job_list[i], job_list[j]


print(get_jobs(jobs, JOB_COMBINATIONS[choice]))
print(get_jobs(jobs, starting_jobs))
print(jobs)
for x, c in zip(JOB_COMBINATIONS, c_):
    print(get_jobs(jobs, x), c)
