\ Model qp
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  0 extra1[0,0] + 0 extra1[1,1] + 0 extra1[2,2] + 0 extra2[0,0]
   + 0 extra2[1,1] + 0 extra2[2,2]
Subject To
 xe1[0]: - e1[0] + e2[0] + 1000 x_{e1>e2}[0] >= 0
 xe1[1]: - e1[1] + e2[1] + 1000 x_{e1>e2}[1] >= 0
 xe1[2]: - e1[2] + e2[2] + 1000 x_{e1>e2}[2] >= 0
 xe2[0]: e1[0] - e2[0] - 1000 x_{e1>e2}[0] >= -1000
 xe2[1]: e1[1] - e2[1] - 1000 x_{e1>e2}[1] >= -1000
 xe2[2]: e1[2] - e2[2] - 1000 x_{e1>e2}[2] >= -1000
 c>c+1[0]: c[0] - c[1] >= 1
 c>c+1[1]: c[1] - c[2] >= 1
 c=min(e1,e2)[0]: c[0] - e1[0] + [ e1[0] * x_{e1>e2}[0]
   - e2[0] * x_{e1>e2}[0] ] = 0
 c=min(e1,e2)[1]: c[1] - e1[1] + [ e1[1] * x_{e1>e2}[1]
   - e2[1] * x_{e1>e2}[1] ] = 0
 c=min(e1,e2)[2]: c[2] - e1[2] + [ e1[2] * x_{e1>e2}[2]
   - e2[2] * x_{e1>e2}[2] ] = 0
 set_extra1[0,1]: extra1[1,0] + [ - p[0] * w[0] - p[1] * w[0] - p[1] * w[1]
   ] = 0
 set_extra1[0,2]: extra1[2,0] + [ - p[0] * w[0] - p[2] * w[0] - p[2] * w[2]
   ] = 0
 set_extra1[1,0]: extra1[0,1] + [ - p[0] * w[0] - p[0] * w[1] - p[1] * w[1]
   ] = 0
 set_extra1[1,2]: extra1[2,1] + [ - p[1] * w[1] - p[2] * w[1] - p[2] * w[2]
   ] = 0
 set_extra1[2,0]: extra1[0,2] + [ - p[0] * w[0] - p[0] * w[2] - p[2] * w[2]
   ] = 0
 set_extra1[2,1]: extra1[1,2] + [ - p[1] * w[1] - p[1] * w[2] - p[2] * w[2]
   ] = 0
 set_extra1[3,0]: extra1[0,3] + [ - p[0] * w[0] - p[0] * w[3] - p[3] * w[3]
   ] = 0
 set_extra1[3,1]: extra1[1,3] + [ - p[1] * w[1] - p[1] * w[3] - p[3] * w[3]
   ] = 0
 set_extra1[3,2]: extra1[2,3] + [ - p[2] * w[2] - p[2] * w[3] - p[3] * w[3]
   ] = 0
 set_extra2[0,1]: extra2[1,0] + [ - p[0] * w[1] - p[1] * w[0] - p[1] * w[1]
   ] = 0
 set_extra2[0,2]: extra2[2,0] + [ - p[0] * w[2] - p[2] * w[0] - p[2] * w[2]
   ] = 0
 set_extra2[1,0]: extra2[0,1] + [ - p[0] * w[0] - p[0] * w[1] - p[1] * w[0]
   ] = 0
 set_extra2[1,2]: extra2[2,1] + [ - p[1] * w[2] - p[2] * w[1] - p[2] * w[2]
   ] = 0
 set_extra2[2,0]: extra2[0,2] + [ - p[0] * w[0] - p[0] * w[2] - p[2] * w[0]
   ] = 0
 set_extra2[2,1]: extra2[1,2] + [ - p[1] * w[1] - p[1] * w[2] - p[2] * w[1]
   ] = 0
 set_extra2[3,0]: extra2[0,3] + [ - p[0] * w[0] - p[0] * w[3] - p[3] * w[0]
   ] = 0
 set_extra2[3,1]: extra2[1,3] + [ - p[1] * w[1] - p[1] * w[3] - p[3] * w[1]
   ] = 0
 set_extra2[3,2]: extra2[2,3] + [ - p[2] * w[2] - p[2] * w[3] - p[3] * w[2]
   ] = 0
 set_e1[0]: e1[0] + [ - p[0] * w[0] - p[0] * w[1] - p[1] * w[1] ] = 0
 set_e1[1]: e1[1] + [ - p[1] * w[1] - p[1] * w[2] - p[2] * w[2] ] = 0
 set_e1[2]: e1[2] + [ - p[2] * w[2] - p[2] * w[3] - p[3] * w[3] ] = 0
 set_e2[0]: e2[0] + [ - p[0] * w[0] - p[0] * w[1] - p[1] * w[0] ] = 0
 set_e2[1]: e2[1] + [ - p[1] * w[1] - p[1] * w[2] - p[2] * w[1] ] = 0
 set_e2[2]: e2[2] + [ - p[2] * w[2] - p[2] * w[3] - p[3] * w[2] ] = 0
 lowest_first[0]: [ ] <= 0
 lowest_first[1]: [ p[0] * w[0] - p[1] * w[1] ] <= 0
 lowest_first[2]: [ p[0] * w[0] - p[2] * w[2] ] <= 0
 lowest_first[3]: [ p[0] * w[0] - p[3] * w[3] ] <= 0
 lowest_first_2[1]: [ ] <= 0
 lowest_first_2[2]: [ p[1] * w[1] - p[2] * w[2] ] <= 0
 lowest_first_2[3]: [ p[1] * w[1] - p[3] * w[3] ] <= 0
Bounds
 1 <= p[0] <= 125
 1 <= p[1] <= 125
 1 <= p[2] <= 125
 1 <= p[3] <= 125
 1 <= w[0] <= 125
 1 <= w[1] <= 125
 1 <= w[2] <= 125
 1 <= w[3] <= 125
Binaries
 x_{e1>e2}[0] x_{e1>e2}[1] x_{e1>e2}[2]
Generals
 p[0] p[1] p[2] p[3] w[0] w[1] w[2] w[3] c[0] c[1] c[2] e1[0] e1[1] e1[2]
 e2[0] e2[1] e2[2] extra1[0,0] extra1[0,1] extra1[0,2] extra1[0,3]
 extra1[1,0] extra1[1,1] extra1[1,2] extra1[1,3] extra1[2,0] extra1[2,1]
 extra1[2,2] extra1[2,3] extra2[0,0] extra2[0,1] extra2[0,2] extra2[0,3]
 extra2[1,0] extra2[1,1] extra2[1,2] extra2[1,3] extra2[2,0] extra2[2,1]
 extra2[2,2] extra2[2,3]
End
