C1 means opt would pick job 1 and 3, where we pick job 2 and 4 in the global ordering of [1, 2, 3, 4]

solution = [(1, 7), (2, 3), (3, 2), (8, 1)]
we choice 1, thus meaning the optimal solution is 0,2, and we start from 1,3.
0 1 16 <-- reachable but not better
0 2 15 <-- opt
0 3 16 <-- reachable but not better
1 2 16 <-- reachable but not better
1 3 16 <-- start
2 3 17 <-- reachable but not better
These are the scores, and we see that the local minimum of 1,3 is as low as all the other direct combinations. thus we hit an plateau.
But there is an global minimum at 0, 2 with cost 15.