C0 means opt would pick job 1 and 2, where we pick job 3 and 4 in the global ordering of [1, 2, 3, 4]


Set parameter NonConvex to value 2
Gurobi Optimizer version 10.0.3 build v10.0.3rc0 (win64)

CPU model: 12th Gen Intel(R) Core(TM) i5-12500H, instruction set [SSE2|AVX|AVX2]
Thread count: 12 physical cores, 16 logical processors, using up to 16 threads

Optimize a model with 6 rows, 14 columns and 10 nonzeros
Model fingerprint: 0x329751a1
Model has 9 quadratic constraints
Coefficient statistics:
  Matrix range     [1e+00, 1e+00]
  QMatrix range    [1e+00, 1e+00]
  QLMatrix range   [1e+00, 1e+00]
  Objective range  [0e+00, 0e+00]
  Bounds range     [1e+00, 1e+00]
  RHS range        [1e+00, 1e+00]
Presolve removed 1 rows and 0 columns

Continuous model is non-convex -- solving as a MIP

Presolve removed 1 rows and 0 columns
Presolve time: 0.00s
Presolved: 60 rows, 28 columns, 142 nonzeros
Presolved model has 13 bilinear constraint(s)
Variable types: 28 continuous, 0 integer (0 binary)

Root relaxation: objective 0.000000e+00, 15 iterations, 0.00 seconds (0.00 work units)


*184116697  3205             804       0.0000000    0.00000  0.00%   3.7 4875s

Explored 184118995 nodes (676631210 simplex iterations) in 4875.10 seconds (785.10 work units)     
Thread count was 16 (of 16 available processors)

Solution count 1: 0

Optimal solution found (tolerance 1.00e-04)
Warning: max constraint violation (1.1200e+02) exceeds tolerance
         (model may be infeasible or unbounded - try turning presolve off)
Best objective 0.000000000000e+00, best bound 0.000000000000e+00, gap 0.0000%
[(1, 297526220), (9, 34925555), (9, 34925555), (294159126, 1)]
This is not a feasable solution, since the best cost of this job set is the following
j1=0, j2=1, cost(j1, j2)=646781770
j1=0, j2=2, cost(j1, j2)=646781770
j1=0, j2=3, cost(j1, j2)=591685347
j1=1, j2=2, cost(j1, j2)=942989985
j1=1, j2=3, cost(j1, j2)=608489130
j1=2, j2=3, cost(j1, j2)=608489130

We choose combination 1, thus constraining the model that there is an local minimum at j1=0, j2=1.
But we can clearly see that j1=0, j2=3 is lower, thus this is not an local minimum. And therefor thus is not an proof by contradiction


