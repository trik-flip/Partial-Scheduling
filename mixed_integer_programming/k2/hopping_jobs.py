import os
import sys

BASE_DIR = "C:/Users/flipp/Documents/School/internship/partial_scheduling/Code/"

if ".venv2" in sys.prefix:
    os.environ["GUROBI_HOME"] = BASE_DIR + ".venv2/Lib/site-packages/gurobipy"
    os.environ["GRB_LICENSE_FILE"] = (
        BASE_DIR + ".venv2/Lib/site-packages/gurobipy/gurobi.lic"
    )


import gurobipy as gp
from gurobipy import GRB


def print_constraints(constrained_model):
    for constr in constrained_model.getConstrs():
        print(f"C: {constr.ConstrName}")


def set_variables(n, empty_model):
    _p = empty_model.addVars(n, lb=1, ub=UB, vtype=GRB.INTEGER, name="p")
    _w = empty_model.addVars(n, lb=1, ub=UB, vtype=GRB.INTEGER, name="w")

    _c = empty_model.addVars(n - 1, vtype=GRB.INTEGER, name="c")
    _e1 = empty_model.addVars(n - 1, vtype=GRB.INTEGER, name="e1")
    _e2 = empty_model.addVars(n - 1, vtype=GRB.INTEGER, name="e2")

    _xe1_e2 = empty_model.addVars(n - 1, vtype=GRB.BINARY, name="x_{e1>e2}")

    _extra1 = empty_model.addVars(n - 1, n, vtype=GRB.INTEGER, name="extra1")
    _extra2 = empty_model.addVars(n - 1, n, vtype=GRB.INTEGER, name="extra2")
    return _p, _w, _c, _e1, _e2, _xe1_e2, _extra1, _extra2


print("Start!")
N = 10

H = 1e10
UB = 30
model = gp.Model("qp")
print("Vars!")


p, w, c, e1, e2, xe1_e2, extra1, extra2 = set_variables(N, model)

print("Constr!")
model.addConstrs(((xe1_e2[i] * H) >= (e1[i] - e2[i]) for i in range(N - 1)), "xe1")
model.addConstrs(
    (((1 - xe1_e2[i]) * H) >= (e2[i] - e1[i]) for i in range(N - 1)), "xe2"
)

model.addConstrs(
    (c[i] == (((1 - xe1_e2[i]) * e1[i]) + (xe1_e2[i] * e2[i])) for i in range(N - 1)),
    "c=min(e1,e2)",
)
# model.addConstrs((c[i] >= (1 - xe1_e2[i]) * e1[i] for i in range(N - 1)), "c>e1")
# model.addConstrs((c[i] >= xe1_e2[i] * e2[i] for i in range(N - 1)), "c>e2")
# model.addConstrs((c[i] <= e1[i] for i in range(N - 1)), "c<e1")
# model.addConstrs((c[i] <= e2[i] for i in range(N - 1)), "c<e2")

model.addConstrs(
    (
        extra1[i, j] == ((p[i] * w[i]) + ((p[i] + p[j]) * w[j]))
        for j in range(N)
        for i in range(N - 1)
        if j != i
    ),
    "set_extra1",
)
model.addConstrs(
    (
        extra2[i, j] == ((p[j] * w[j]) + ((p[i] + p[j]) * w[i]))
        for j in range(N)
        for i in range(N - 1)
        if j != i
    ),
    "set_extra2",
)
model.addConstrs(
    (c[i] <= extra1[i, j] for j in range(N) for i in range(1, N - 1) if j != i),
    "must be best swap e1",
)
model.addConstrs(
    (c[i] <= extra2[i, j] for j in range(N) for i in range(1, N - 1) if j != i),
    "must be best swap e2",
)

model.addConstrs(
    (c[i] <= extra1[i - 1, j] for j in range(N) for i in range(1, N - 1) if j != i),
    "must be best swap e1",
)
model.addConstrs(
    (c[i] <= extra2[i - 1, j] for j in range(N) for i in range(1, N - 1) if j != i),
    "must be best swap e2",
)

model.addConstrs(
    (e1[i] == ((p[i] * w[i]) + ((p[i] + p[i + 1]) * w[i + 1])) for i in range(N - 1)),
    "set_e1",
)
model.addConstrs(
    (
        e2[i] == ((p[i + 1] * w[i + 1]) + ((p[i] + p[i + 1]) * w[i]))
        for i in range(N - 1)
    ),
    "set_e2",
)
# model.addConstrs(
#     (p[i] * w[i] <= p[i + 1] * w[i + 1] - 1 for i in range(N - 1)),
#     "j < j+1",
# )
model.addConstrs(
    (c[i] - 1 >= c[i + 1] for i in range(N - 2)),
    "c>c+1",
)
model.addConstrs(
    ((p[0] * w[0]) <= (p[i] * w[i]) for i in range(N)),
    "lowest_first",
)
model.addConstrs(
    ((p[1] * w[1]) <= (p[i] * w[i]) for i in range(1, N)),
    "lowest_first_2",
)

model.Params.NonConvex = 2
model.Params.Presolve = 0

model.optimize()

if model.Status != 2:
    # model.computeIIS()
    exit()
p_: list[int] = []
w_: list[int] = []
for v in model.getVars():
    if v.VarName[0] == "p":
        p_.append(int(v.X))
    elif v.VarName[0] == "w":
        w_.append(int(v.X))
    # print(f"V: {v.VarName} {int(v.X)}")
jobs = [x for x in zip(p_, w_)]
print(jobs)
