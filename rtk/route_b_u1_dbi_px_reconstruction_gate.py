#!/usr/bin/env python3
"""Exact reconstruction of a fixed shift-symmetric P(X) action for production RTK.

Production variables:
 x=x0/a^3,
 s=sqrt(1+lambda_D x^2), r=x/s, Q=1+r,
 p_8=2 mu_K^2 r x/(s+1),
 rho_8=2 mu_K^2 x[1+x/(s+1)].

For a purely kinetic scalar define an arbitrary positive normalization X_* and
 u=sqrt(X/X_*).  The field normalization is chosen so that u=Q=1+r on the
 production trajectory.  Then r=u-1 and

 P_8(X)=2 mu_K^2/lambda_D * [1-sqrt(1-lambda_D (u-1)^2)]

with continuous lambda_D->0 limit P_8=mu_K^2 (u-1)^2.

The theorem verifies p=P, rho=2X P_X-P, rho+p=2X P_X and the production
adiabatic sound speed exactly.  This gives a fixed, shift-symmetric covariant
clock action rather than an epoch-by-epoch F(t,N) reconstruction.
"""
import json
import sympy as sp

r,lam,mu,Xs,u=sp.symbols('r lambda_D mu_K X_star u', positive=True, finite=True, real=True)
X=sp.symbols('X', positive=True, finite=True, real=True)

# Use u as the kinetic variable and X=Xs*u^2.
s=1/sp.sqrt(1-lam*r**2)
x=r*s
Q=1+r
p_prod=sp.simplify(2*mu**2/lam*(1-1/s))
rho_prod=sp.simplify(2*mu**2*(x+(s-1)/lam))
enthalpy_prod=sp.simplify(rho_prod+p_prod)
assert sp.simplify(enthalpy_prod-2*mu**2*x*Q)==0

P_u=2*mu**2/lam*(1-sp.sqrt(1-lam*(u-1)**2))
# dP/dX = (dP/du)/(2 Xs u), so 2X P_X = u dP/du.
enthalpy_u=sp.simplify(u*sp.diff(P_u,u))
rho_u=sp.simplify(enthalpy_u-P_u)

# Map u=Q and sqrt(1-lam r^2)=1/s.
map_u={u:Q}
assert sp.simplify(P_u.subs(map_u)-p_prod)==0
assert sp.simplify(enthalpy_u.subs(map_u)-enthalpy_prod)==0
assert sp.simplify(rho_u.subs(map_u)-rho_prod)==0

# Sound speed c_s^2 = P_X/(P_X+2X P_XX) = (dP/du)/(u d/du[u dP/du])
# after X=Xs u^2. Equivalently dp/d rho along u.
dpdu=sp.diff(P_u,u)
drhdu=sp.diff(rho_u,u)
cs2_u=sp.factor(dpdu/drhdu)
cs2_prod=sp.factor(r/(s*(s+x)))
assert sp.simplify(cs2_u.subs(map_u)-cs2_prod)==0

# Chemical-potential reconstruction identity d ln u = dp/(rho+p).
ratio_u=sp.simplify(dpdu/enthalpy_u)
assert sp.simplify(ratio_u-1/u)==0

# lambda->0 continuous limit.
P_lam0=sp.simplify(sp.limit(P_u,lam,0,dir='+'))
assert P_lam0==mu**2*(u-1)**2

out={
  'classification':'RTK_ROUTE_B_U1_DBI_PX_RECONSTRUCTION_PASS',
  'kinetic_invariant':'X_U = 1/2 [Theta_U^2 - D_i Sigma D^i Sigma] in the preferred-foliation/U1-invariant ADM form',
  'dimensionless_kinetic_variable':'u=sqrt(X_U/X_star)=1+r on the production branch',
  'P_8piG':'2 mu_K^2/lambda_D * [1-sqrt(1-lambda_D (sqrt(X_U/X_star)-1)^2)]',
  'lambda_zero_limit':'mu_K^2 (sqrt(X_U/X_star)-1)^2',
  'field_normalization':'X_star>0 arbitrary; changing X_star is a Sigma field rescaling and does not alter production rho,p,c_s when the trajectory is rescaled consistently',
  'exact_checks':['P=p_production','2X P_X-P=rho_production','2X P_X=rho+p=2 mu_K^2 x(1+r)','c_s^2=dp/d rho=c_a^2 production','d ln u=dp/(rho+p)'],
  'status_scope':'FIXED_SHIFT_SYMMETRIC_DBI_CLOCK_GREEN_BACKGROUND_ACTION',
  'non_claims':[
    'does not by itself include the separate mixed operator C(state) D_i Theta_U D^i Theta_U',
    'does not establish radiative stability or a UV completion',
    'does not prove all inhomogeneous DBI solutions are healthy beyond the already tested quadratic production branch'
  ],
  'next_gate':'use shift symmetry of the reconstructed P(X_U) plus the explicit S_mix to prove that Sigma=q t with D_i Sigma=0 is a consistent static local clock solution for time-independent lapse/spatial metric and zero shift; then complete the static O(4) beta_PPN equivalence test'
}
open('u1_dbi_px_reconstruction_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
