#!/usr/bin/env python3
"""C8 correction: exact static equivalence of fixed C(X) S_mix and beta0_eff=2.

The earlier static-lapse bridge temporarily held C at its homogeneous
background value while varying the lapse and therefore found a nonlinear
(1+n)^-3 versus (1+n)^-1 mismatch.  That was a useful intermediate audit but
is not the final fixed-action result.

The now reconstructed scalar action fixes

  X_U = 1/2 [Theta_U^2 - D_i Sigma D^i Sigma],
  C(X_U) = M_Pl^2/(2 X_U).

On the exact static zero-invariant-shift clock solution Sigma=q t,
D_i Sigma=0, so X_U=Theta_U^2/2 and

  D_i Theta_U = -Theta_U D_i ln N = -Theta_U a_i.

Therefore

  C(X_U) D_iTheta_U D^iTheta_U
   = [M_Pl^2/Theta_U^2] Theta_U^2 a_i a^i
   = M_Pl^2 a_i a^i

exactly for arbitrary spatially varying N(x), not merely perturbatively.
With the gravity convention (M_Pl^2/2) beta0 a_i a^i, this is precisely
beta0_eff=2 while beta0_bare remains zero.
"""
import json
import sympy as sp

M,Theta,a2=sp.symbols('M_Pl Theta a2', positive=True, finite=True, real=True)
X=Theta**2/2
C=M**2/(2*X)
DTheta2=Theta**2*a2
Lmix=sp.simplify(C*DTheta2)
Leff=sp.simplify(M**2*a2)
assert sp.simplify(Lmix-Leff)==0
beta_eff=sp.simplify(2*Lmix/(M**2*a2))
assert beta_eff==2

# Perturbative cross-check with N=1+n: exact equality persists through all
# algebraic lapse orders because a_i a^i=(D n)^2/(1+n)^2 appears on both sides.
n,Xgrad=sp.symbols('n Xgrad', finite=True, real=True)
a2_n=Xgrad/(1+n)**2
assert sp.simplify(Lmix.subs(a2,a2_n)-M**2*a2_n)==0

out={
  'classification':'RTK_ROUTE_B_U1_STATIC_EXACT_ACCELERATION_EQUIVALENCE_PASS',
  'fixed_scalar_action':'research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json',
  'static_clock_prerequisite':'Sigma=q t, D_i Sigma=0, zero invariant shift, arbitrary static N(x)',
  'identity':'C(X_U)(D Theta_U)^2 = M_Pl^2 a_i a^i exactly because X_U=Theta_U^2/2 and D_iTheta_U=-Theta_U a_i',
  'beta0_bare':0,
  'beta0_eff_static':2,
  'scope':'exact static zero-invariant-shift identity, all lapse amplitudes within X_U>0 branch',
  'supersedes_intermediate_interpretation':'The cubic mismatch in RTK_ROUTE_B_U1_STATIC_LAPSE_QUADRATIC_EQUIVALENCE_PASS came from holding C fixed off shell. It is historical for that intermediate representation and is not present in the final fixed C(X_U)=M_Pl^2/(2X_U) action.',
  'non_claims':[
    'does not establish moving-source/vector preferred-frame equations with nonzero invariant shift',
    'does not cover X_U=0 where C(X_U) is singular',
    'does not by itself remove the homogeneous P(X_U) stress-energy contribution in a local PPN patch',
    'does not establish radiative stability or EFT cutoff'
  ],
  'next_gate':'quantify the P(X_U) background/lapse-stiffness corrections relative to spatial-gradient gravity terms in the local PPN limit, then combine with the published family-I static equations to test beta_PPN on the same fixed action'
}
open('u1_static_exact_acceleration_equivalence_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
