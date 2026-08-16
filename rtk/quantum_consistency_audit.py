#!/usr/bin/env python3
"""Baseline quantum/EFT consistency audit for the implemented DBI-Khronon background.

This does NOT claim a UV completion. It checks algebraic conditions directly implied by
rtk/khronon_background.c over a broad dimensionless grid:
  Q>0, rho>0, 1+w>0, ca2>=0, 0<=cs2<=ca2, DBI margin>0.
It also reports conservative kinetic/gradient proxy margins for the fluid-like scalar
sector. A full quadratic-action/Hamiltonian derivation remains a separate theorem task.
"""
import json, math

# dimensionless x and lambda scan; k/kstar is scanned independently
LAMBDAS=[1e-4,1e-2,1.0,1e2,1e4,1e6,1e8]
XS=[10.0**p for p in range(-12,13)]
KR=[0.0,1e-4,1e-2,1.0,1e2,1e4,1e8]

worst={"one_plus_w":float('inf'),"ca2":float('inf'),"cs2":float('inf'),"dbi_margin":float('inf'),"Q":float('inf')}
viol=[]; n=0
for lam in LAMBDAS:
  sl=math.sqrt(lam)
  for x in XS:
    y=sl*x; s=math.hypot(1.0,y); r=x/s; t=x/(s+1.0); Q=1.0+r
    rho=x*(1.0+t); p=r*t; w=p/rho
    ca2=r/(s*(s+x)); margin=1.0/(s*s)
    for kr in KR:
      cs2=ca2/(1.0+kr*kr)
      vals={"one_plus_w":1+w,"ca2":ca2,"cs2":cs2,"dbi_margin":margin,"Q":Q}
      n+=1
      for k,v in vals.items(): worst[k]=min(worst[k],v)
      ok=(Q>0 and rho>0 and 1+w>0 and ca2>=0 and cs2>=0 and cs2<=ca2*(1+1e-13) and margin>0 and all(math.isfinite(v) for v in vals.values()))
      if not ok: viol.append({"lambda":lam,"x":x,"k_over_kstar":kr,**vals})

out={
 "status":"PASS" if not viol else "FAIL",
 "points":n,
 "violations":viol[:20],
 "worst_margins":worst,
 "interpretation":{
   "classical_algebraic_stability":"tested on broad grid",
   "ghost_free_quadratic_action":"NOT_YET_DERIVED",
   "hamiltonian_boundedness":"NOT_YET_DERIVED",
   "strong_coupling_scale":"NOT_YET_DERIVED",
   "one_loop_radiative_stability":"NOT_YET_DERIVED",
   "uv_completion":"NOT_CLAIMED"
 }
}
print(json.dumps(out,indent=2,sort_keys=True))
if viol: raise SystemExit(2)
