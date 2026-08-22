#!/usr/bin/env python3
"""Exact existence/uniqueness and switch theorem for the fixed-action static zero-flux branch B.

For Sigma=q t+psi(r), zero invariant shift and X_U>0, define
  u=sqrt(X_U/X_star),
  q^2=2 X_star u0^2,
  a_N^2=g^rr (N'/N)^2.
The zero-flux branch B condition P_X+C_X Y=0 reduces exactly to

  F(u) = u0^2 a_N^2/N^2,
  F(u)=mu_K^2 u^3 (u-1)/sqrt(1-lambda_D (u-1)^2).

On the positive-enthalpy DBI branch 1<u<u_edge=1+1/sqrt(lambda_D), F is
strictly increasing from 0 to infinity. Profile reality additionally requires
u <= u0/N, because psi'^2 = 2 X_star (u0^2/N^2-u^2) >=0.

This theorem characterizes algebraic branch-B existence and the only smooth
zero-flux A<->B switch condition. It is not a global stellar solution theorem.
"""
import json, math
import sympy as sp

u,lam,mu,u0,N,a2=sp.symbols('u lambda_D mu_K u0 N a_N2', positive=True, finite=True, real=True)
D=sp.sqrt(1-lam*(u-1)**2)
F=mu**2*u**3*(u-1)/D
# Log derivative is manifestly positive on 1<u<u_edge.
logder=sp.simplify(sp.diff(F,u)/F)
expected=sp.simplify(3/u + 1/(u-1) + lam*(u-1)/(1-lam*(u-1)**2))
assert sp.simplify(logder-expected)==0

# Production z=0 inputs from the pinned scale dictionary.
lam0=219457.5727136581
mu0=1.572550669049847e-4 # Mpc^-1
u0=1.002134632964446
uedge=1.0+1.0/math.sqrt(lam0)
Nlower=u0/uedge
D0=math.sqrt(1-lam0*(u0-1)**2)
enthalpy0=2*mu0**2*u0*(u0-1)/D0
F0=mu0**2*u0**3*(u0-1)/D0
assert abs(F0-0.5*u0*u0*enthalpy0) <= 1e-18*max(1.0,abs(F0))
a_switch_at_N1=math.sqrt(enthalpy0/2.0)

# The exact smooth switch A -> B has psi'=0, hence u=u0/N.  Substitution gives
# a_switch^2 = N^2 F(u0/N)/u0^2, provided 1<u0/N<u_edge.
def Fnum(x):
    return mu0**2*x**3*(x-1.0)/math.sqrt(1.0-lam0*(x-1.0)**2)
def aswitch(Nv):
    ua=u0/Nv
    if not (1.0 < ua < uedge): return None
    return Nv/u0*math.sqrt(Fnum(ua))

# Representative switch thresholds before the lower constant-q edge.
N_samples=[1.0, 0.999999999, 0.999999995, Nlower+1e-10]
switch_rows=[]
for Nv in N_samples:
    aa=aswitch(Nv)
    switch_rows.append({'N':Nv,'u_A':u0/Nv,'a_switch_Mpc_inv':aa})
    assert aa is not None and aa>0

# Main existence theorem:
# upper admissible u is min(u_edge,u0/N). Since F increases 0->infinity,
# if u0/N >= u_edge (N<=Nlower), every finite a_N>0 has a unique algebraic
# branch-B root. If Nlower<N<u0, existence requires RHS <= F(u0/N), exactly
# a_N <= a_switch(N). For N>=u0 there is no u>1 satisfying profile reality.

out={
  'classification':'RTK_ROUTE_B_U1_STATIC_BRANCHB_EXISTENCE_UNIQUENESS_PASS',
  'fixed_scalar_action':'research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json',
  'exact_branch_B_equation':'mu_K^2 u^3 (u-1)/sqrt(1-lambda_D (u-1)^2) = u0^2 a_N^2/N^2',
  'positive_enthalpy_domain':'1 < u < u_edge = 1+1/sqrt(lambda_D)',
  'profile_reality':'u <= u0/N',
  'monotonicity':{
    'dlnF_du':str(expected),
    'result':'strictly positive for 1<u<u_edge; therefore at most one branch-B root for fixed N and a_N>0'
  },
  'existence_cases':[
    'N <= N_lower=u0/u_edge: u0/N >= u_edge, so every finite a_N>0 has exactly one algebraic branch-B root inside 1<u<u_edge',
    'N_lower < N < u0: a branch-B root exists iff a_N <= a_switch(N)=N/u0*sqrt(F(u0/N))',
    'N >= u0: no positive-enthalpy u>1 root satisfies u<=u0/N'
  ],
  'smooth_zero_flux_switch':{
    'condition':'A<->B switch with continuous psi_prime requires psi_prime=0, u=u0/N and a_N=a_switch(N)',
    'N_1_threshold_Mpc_inv':a_switch_at_N1,
    'rows':switch_rows
  },
  'z0':{
    'lambda_D':lam0,'mu_K_Mpc_inv':mu0,'u0':u0,'u_edge':uedge,
    'N_lower_constant_q':Nlower,'u_edge_minus_u0':uedge-u0,
    'enthalpy_8piG_Mpc_inv2':enthalpy0
  },
  'scientific_interpretation':'The lower constant-q DBI lapse boundary is not an algebraic no-go for the full fixed scalar action: branch B has a unique real algebraic root below that boundary for any finite nonzero ADM-lapse gradient. However a regular zero-flux stellar solution starting on branch A can enter branch B smoothly only on the codimension-one switch surface a_N=a_switch(N); global gravity/U1 equations must determine whether such a surface is actually reached.',
  'non_claims':[
    'does not prove a global regular stellar or black-hole solution',
    'does not determine the O4 ADM-lapse coefficient or beta_PPN',
    'does not include nonzero scalar flux/charge',
    'does not remove the X_U=0 or radiative/cutoff gates'
  ],
  'next_gate':'combine the O4 ADM-lapse solution/bound with a_switch(N) to decide whether a solar/stellar zero-flux solution can actually switch before the constant-q edge; then solve the radial gravity/U1 system on branch B'
}
open('u1_static_branchb_existence_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
