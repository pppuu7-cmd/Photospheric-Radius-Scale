#!/usr/bin/env python3
"""Exact local-rest scalar-sector principal-symbol gate for the frozen U(1)+RTK scalar action.

Scope is deliberately narrow: the scalar action is expanded on the certified local
PPN rest background N=1, invariant shift=0, g_ij=delta_ij, Sigma=q(t+phi),
q^2=2 X_star.  This proves the scalar-sector quadratic principal structure before
integrating the full gravity/U(1) constraint system.  A full coupled eigenmode
claim therefore remains a separate gate.
"""
import json
import sympy as sp

TARGET='research/theory_targets/RTK_C8_U1_LOCAL_REST_SCALAR_PRINCIPAL_TARGET_v1.json'
ACTION='research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json'
t=json.load(open(TARGET))
a=json.load(open(ACTION))
assert t['classification']=='RTK_C8_U1_LOCAL_REST_SCALAR_PRINCIPAL_TARGET_V1_FROZEN'
assert a['mixed_operator']['C']=='M_Pl^2/(2 X_U)'
assert a['domain']['production_branch']=='u=1+r>0 with X_U>0'

# Exact DBI derivatives at X=X_star.
X,Xs,mu,lam=sp.symbols('X Xs mu lam', positive=True, finite=True)
u=sp.sqrt(X/Xs)
P=2*mu**2/lam*(1-sp.sqrt(1-lam*(u-1)**2))
PX=sp.simplify(sp.diff(P,X))
PXX=sp.simplify(sp.diff(P,X,2))
P0=sp.simplify(P.subs(X,Xs))
PX0=sp.simplify(PX.subs(X,Xs))
PXX0=sp.simplify(PXX.subs(X,Xs))
assert P0==0
assert PX0==0
assert sp.simplify(PXX0-mu**2/(2*Xs**2))==0
cs2=sp.simplify(PX/(PX+2*X*PXX))
cs20=sp.simplify(cs2.subs(X,Xs))
assert cs20==0

# Bookkeeping expansion in perturbation amplitude eps.
# d = dot(phi), g2 = |grad phi|^2/eps^2, gd2 = |grad dot(phi)|^2/eps^2.
eps,d,g2,gd2=sp.symbols('eps d g2 gd2', real=True, finite=True)
D=(1+eps*d)**2-eps**2*g2
sqrtD=sp.sqrt(D)
P_D=2*mu**2/lam*(1-sp.sqrt(1-lam*(sqrtD-1)**2))
# mixed/M_Pl^2 = |grad dot(phi)|^2 / D
Lmix=eps**2*gd2/D
seriesP=sp.series(P_D,eps,0,5).removeO().expand()
seriesM=sp.series(Lmix,eps,0,4).removeO().expand()
P2=sp.simplify(seriesP.coeff(eps,2))
M2=sp.simplify(seriesM.coeff(eps,2))
assert sp.simplify(P2-mu**2*d**2)==0
assert sp.simplify(M2-gd2)==0
# No quadratic |grad phi|^2 term.
assert sp.diff(P2,g2)==0
assert sp.diff(M2,g2)==0

# Static perturbation: d=0. First spatial DBI term is quartic.
P_static=sp.series(P_D.subs(d,0),eps,0,6).removeO().expand()
P_static2=sp.simplify(P_static.coeff(eps,2))
P_static4=sp.simplify(P_static.coeff(eps,4))
assert P_static2==0
assert sp.simplify(P_static4-mu**2*g2**2/4)==0

# Fourier quadratic scalar-sector kernel: (mu^2+k^2) omega^2, no k-only restoring term.
k,w=sp.symbols('k w', real=True, finite=True)
K=sp.expand((mu**2+k**2)*w**2)
assert sp.simplify(K.subs(w,0))==0

out={
  'classification':'RTK_C8_U1_LOCAL_REST_SCALAR_SPATIAL_PRINCIPAL_DEGENERACY_EXACT_PASS',
  'status':'SCALAR_SECTOR_LOCAL_REST_SPATIAL_PRINCIPAL_DEGENERATE_AT_TWO_DERIVATIVE_LEVEL',
  'target':TARGET,
  'action':ACTION,
  'exact_identities':{
    'P_X_at_Xstar':'0',
    'P_XX_at_Xstar':'mu_K^2/(2 X_star^2)',
    'c_s2_at_Xstar':'0',
    'quadratic_L_over_Mpl2':'mu_K^2 dot(phi)^2 + |grad dot(phi)|^2',
    'quadratic_grad_phi2_coefficient':'0',
    'fourier_scalar_sector_kernel':'(mu_K^2+k^2) omega^2',
    'static_first_spatial_DBI_term':'+mu_K^2/4 [|grad phi|^2]^2'
  },
  'interpretation':'On the exact local PPN rest vacuum, the frozen two-derivative RTK scalar sector has positive time-kinetic support but no quadratic spatial restoring term. Higher-spatial operators or a separately demonstrated gravity/U1 constraint-induced restoring term are required before a physical local scalar dispersion or cutoff can be claimed.',
  'non_claims':[
    'does not imply a ghost',
    'does not by itself prove a dynamical instability',
    'does not yet diagonalize the full coupled metric/U1/scalar quadratic system around the local rest vacuum',
    'does not exclude a restoring term generated after full nondynamical gravity/U1 constraint elimination',
    'does not apply to the cosmological rolling branch where P_X is nonzero',
    'does not compute the physical strong-coupling scale or UV cutoff'
  ],
  'next_gate':'derive and eliminate the complete local-rest quadratic metric/lapse/shift/U1 constraint system on the identical fixed action; if the physical scalar eigenmode remains spatially degenerate, freeze a minimal higher-spatial completion basis and require preservation of the cosmological RTK kernel, c_T=1, PPN quartet, and classical DOF count.'
}
open('u1_local_rest_scalar_principal_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
