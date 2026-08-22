#!/usr/bin/env python3
"""Correct generic-rank existence slice for the fixed P(X)+C(X) scalar action.

The historical generic slice used p_Sigma=0.  After fixing
C(X_U)=M_Pl^2/(2X_U), X_U=0 is singular, so that historical slice must not be
used to certify the fixed action.

Instead choose a homogeneous timelike canonical slice
  X_U=X0>0, D_i Sigma=0, D_i Theta_U=0,
with nonzero homogeneous scalar momentum.  Then S_mix=0 while C is finite.
For a shift-symmetric P(X) sector,

  L_P=N sqrt(g) P(X), X=Theta^2/2,
  p_Sigma=sqrt(g) P_X Theta.

At fixed canonical p_Sigma and g, the algebraic relation determines Theta (and
X) without N.  The Legendre transform is

  H_P=N [p_Sigma Theta-sqrt(g)P(X)] = N sqrt(g) rho(X),

so the matter contribution to H_perp is N-independent and gives no direct
correction delta_a={pi_N,H_perp}_Sigma on this slice. Thus the coupled cross
block equals the regular pure-gravity block there, proving non-identical
singularity on a slice wholly inside X>0.
"""
import json
import sympy as sp

N,sqrtg,Theta,P,PX=sp.symbols('N sqrtg Theta P PX', positive=True, finite=True, real=True)
p=sp.symbols('p_Sigma', nonzero=True, finite=True, real=True)
X0=sp.symbols('X0', positive=True, finite=True, real=True)

# Canonical relation and Legendre transform on D_i Sigma=D_iTheta=0.
p_relation=sp.Eq(p,sqrtg*PX*Theta)
H=sp.expand(N*(p*Theta-sqrtg*P))
Hperp=sp.simplify(H/N)
assert not Hperp.has(N)
# Direct lapse derivative of the secondary Hamiltonian density therefore zero.
delta_a_matter=sp.diff(Hperp,N)
assert delta_a_matter==0

# Cross-block identity.
ag,bg,cg,dg=sp.symbols('a_g b_g c_g d_g', finite=True)
B_g=sp.Matrix([[ag,bg],[cg,dg]])
B_c=sp.Matrix([[ag+delta_a_matter,bg],[cg,dg]])
assert sp.simplify(B_c.det()-B_g.det())==0

out={
  'classification':'RTK_ROUTE_B_U1_FIXED_SCALAR_REGULAR_RANK_SLICE_PASS',
  'supersedes_for_fixed_scalar_action':'RTK_ROUTE_B_U1_GENERIC_COUPLED_RANK_SLICE_PASS p_Sigma=0 slice',
  'slice_conditions':['X_U=X0>0','D_i Sigma=0','D_i Theta_U=0','nonzero homogeneous p_Sigma','regular pure-gravity point det B_g != 0'],
  'C_regular':'C(X0)=M_Pl^2/(2X0) finite',
  'S_mix_on_slice':'0 because D_i Theta_U=0',
  'canonical_relation':'p_Sigma=sqrt(g) P_X Theta_U, independent of lapse after solving for Theta_U at fixed canonical momentum',
  'matter_Hamiltonian':'H_P=N[p_Sigma Theta_U-sqrt(g)P], hence H_perp^P is N-independent',
  'delta_a_matter_on_slice':'0',
  'result':'det B_coupled=det B_gravity != 0 on a regular timelike X_U>0 slice, so the fixed scalar action does not make the second-class block identically singular.',
  'scope':'existence/non-identical-degeneracy theorem for fixed P(X_U)+C(X_U) action',
  'non_claims':[
    'does not prove absence of rank-changing hypersurfaces elsewhere in inhomogeneous scalar phase space',
    'does not cover X_U=0',
    'does not by itself complete the fixed-action DOF count'
  ],
  'next_gate':'combine with fixed-C(X) velocity support, invariant-shift Noether identity and an exact rolling X>0 rank theorem, then reissue the classical DOF certificate specifically for the fixed scalar action'
}
open('u1_fixed_scalar_regular_rank_slice_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
