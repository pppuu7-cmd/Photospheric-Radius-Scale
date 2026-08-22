#!/usr/bin/env python3
"""Exact static clock consistency for the fixed shift-symmetric RTK scalar action.

Take a time-independent static gravitational configuration with zero invariant
shift and arbitrary spatially varying lapse N(x).  For the fixed scalar action

 L = N sqrt(g) [ P(X_U) + C(X_U) D_i Theta_U D^i Theta_U ],
 X_U = 1/2 [Theta_U^2 - D_i Sigma D^i Sigma],
 C(X_U)=M_Pl^2/(2X_U),

consider Sigma=q t with constant q and D_i Sigma=0. Then Theta_U=q/N(x).
The P(X) current has a static time component and zero spatial component, so its
divergence vanishes. The mixed term depends on Sigma through time derivatives
(and mixed spatial-time derivatives) but has no explicit Sigma dependence; all
corresponding canonical coefficients are time-independent on the ansatz, while
the spatial current proportional to D_i Sigma vanishes.

A generalized Euler-Lagrange audit is performed explicitly in a 1D spatial
slice with arbitrary N(z). Because no symmetry-specific 1D identity is used,
the vanishing extends componentwise to arbitrary static spatial dependence.
"""
import json
import sympy as sp

t,z,q,M=sp.symbols('t z q M', nonzero=True, finite=True, real=True)
N=sp.Function('N')(z)
S=sp.Function('S')(t,z)
P=sp.Function('P')

St=sp.diff(S,t)
Sz=sp.diff(S,z)
Theta=St/N
X=sp.Rational(1,2)*(Theta**2-Sz**2)
C=M**2/(2*X)
Theta_z=sp.diff(Theta,z)
L=N*P(X)+N*C*Theta_z**2

# L depends on S_t, S_z and S_tz. Generalized Euler-Lagrange operator:
# dL/dS - dt(dL/dS_t) - dz(dL/dS_z) + dt dz(dL/dS_tz).
E=(sp.diff(L,S)
   -sp.diff(sp.diff(L,St),t)
   -sp.diff(sp.diff(L,Sz),z)
   +sp.diff(sp.diff(L,sp.diff(S,t,z)),t,z))
E_static=sp.simplify(E.subs(S,q*t).doit())
assert E_static==0

# Background invariants on the static clock ansatz.
Theta_static=sp.simplify(Theta.subs(S,q*t).doit())
X_static=sp.simplify(X.subs(S,q*t).doit())
C_static=sp.simplify(C.subs(S,q*t).doit())
assert Theta_static==q/N
assert X_static==q**2/(2*N**2)
assert sp.simplify(C_static-M**2*N**2/q**2)==0

# Exact RTK product in orthonormal/background N=1 limit.
assert sp.simplify(C_static.subs(N,1)*q**2-M**2)==0

out={
  'classification':'RTK_ROUTE_B_U1_STATIC_CLOCK_CONSISTENCY_PASS',
  'scalar_action':'research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json',
  'ansatz':['time-independent N(x),g_ij(x)','zero invariant shift','Sigma=q t','q constant','D_i Sigma=0'],
  'Theta_static':'q/N(x)',
  'X_static':'q^2/[2 N(x)^2]',
  'generalized_Euler_Lagrange_result':'0 exactly for arbitrary static N(z) in the symbolic audit',
  'interpretation':'The reconstructed shift-symmetric P(X_U) plus C(X_U)(D Theta_U)^2 action does not require a local static deltaSigma profile on the constant-q clock branch; Sigma=q t is an exact scalar equation solution for static zero-shift geometry.',
  'status_scope':'STATIC_CLOCK_GREEN_ZERO_SHIFT',
  'non_claims':[
    'does not cover moving-source/time-dependent O(3) configurations with nonzero invariant shift',
    'does not establish global boundary conditions or compact-object regularity',
    'does not address the X_U->0 boundary where C(X_U) is singular',
    'does not establish radiative stability or EFT cutoff'
  ],
  'next_gate':'combine n_2=0 and exact static-clock consistency to prove equivalence of the explicit-S_mix and beta0_eff=2 static field equations through O(4); then evaluate the static beta_PPN coefficient on the published family-I reference system'
}
open('u1_static_clock_consistency_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
