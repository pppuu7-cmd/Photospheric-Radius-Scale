#!/usr/bin/env python3
"""Scoped same-action cosmology obstruction for the current U1 family-I universal matter frame.

Primary external equations: Lin, Mukohyama, Wang, Zhu, arXiv:1310.6666.
- Eq. (2.18): R - 2 Lambda_g - sigma1 a_i a^i - sigma2 div(a) = 8 pi G J_A.
- Eq. (4.15), phi=0 gauge: for a2=0, Omega=1,
      J_A = 2 a1 rho_H.

Current fixed family-I tuple has a1=1, a2=0, sigma1=sigma2=0.
On homogeneous FLRW, a_i=0 and R^(3)=6 K/a^2. The fixed RTK scalar
P(X_U)+C(X_U)(D Theta_U)^2 is A-independent, so it contributes delta J_A=0.
Therefore the exact A constraint for universally coupled ordinary matter is

    6 K/a^2 - 2 Lambda_g = 16 pi G rho_H(a).

For flat production cosmology K=0, the left hand side is constant, so any
ordinary matter/radiation density with nonzero time evolution is incompatible.
Even allowing constant spatial curvature, the left hand side spans only
{a^0,a^-2}; it cannot equal a nonzero dust+radiation mixture
rho_m0 a^-3 + rho_r0 a^-4 for all a.

This is a scoped obstruction for the current universal a1=1,a2=0 matter frame,
not a no-go for U1/RTK. Escapes require a genuinely changed matter/A-source
architecture (e.g. an A-charged compensator/source cancellation, non-universal
matter frame, or another constraint structure) and must be retested from scratch.
"""
import json
import sympy as sp

a,K,Lg,G,rhom,rhor=sp.symbols('a K Lambda_g G rho_m0 rho_r0', positive=True, finite=True, real=True)
# K and Lg can have either sign in the algebra; replace with unconstrained symbols.
K=sp.symbols('K', finite=True, real=True)
Lg=sp.symbols('Lambda_g', finite=True, real=True)

R3=6*K/a**2
rho=rhom/a**3+rhor/a**4
lhs=sp.expand(R3-2*Lg)
rhs=sp.expand(16*sp.pi*G*rho)

# Multiply by a^4. Equality for all a requires coefficients of independent
# powers {a^4,a^2,a,1} to match. The dust and radiation coefficients therefore
# must vanish unless extra A-sources are present.
poly=sp.Poly(sp.expand(a**4*(lhs-rhs)),a)
coeffs={i:sp.simplify(poly.coeff_monomial(a**i)) for i in range(5)}
assert coeffs[4]==-2*Lg
assert coeffs[2]==6*K
assert coeffs[1]==-16*sp.pi*G*rhom
assert coeffs[0]==-16*sp.pi*G*rhor
# No a^3 term.
assert coeffs[3]==0

# Flat case is even sharper: K=0 forces rho_H(a)=-Lambda_g/(8 pi G), constant.
rho_flat_required=sp.simplify((-2*Lg)/(16*sp.pi*G))
assert rho_flat_required==-Lg/(8*sp.pi*G)

out={
  'classification':'RTK_ROUTE_B_U1_FAMILY1_FLRW_A_CONSTRAINT_OBSTRUCTION',
  'status_scope':'BLACK_SCOPED_CURRENT_UNIVERSAL_FAMILY1_MATTER_FRAME_FLRW',
  'external_source':'Lin-Mukohyama-Wang-Zhu arXiv:1310.6666 Eqs.(2.18),(4.15)',
  'frozen_tuple':{'a1':1,'a2':0,'sigma1':0,'sigma2':0,'kappa':1,'gamma1':-1,'beta0_bare':0},
  'fixed_rtk_scalar_A_source':'0 (neutral fixed P(X_U)+C(X_U) action is A-independent)',
  'homogeneous_A_constraint':'6 K/a^2 - 2 Lambda_g = 16 pi G rho_H(a)',
  'flat_case':'rho_H(a) = -Lambda_g/(8 pi G), hence rho_H must be constant',
  'dust_radiation_polynomial_coefficients':{str(k):str(v) for k,v in coeffs.items()},
  'result':'With nonzero universally coupled dust and/or radiation, no constant K and Lambda_g can satisfy the current family-I A constraint for all scale factors. In particular the flat production cosmology is impossible in this exact matter/A-source architecture.',
  'why_prior_ppn_pass_does_not_rescue':'The PPN family-I cancellation is a local weak-field statement; the same universal a1=1 matter coupling sources the homogeneous A constraint and fails before C9/UV completion on an evolving FLRW background.',
  'non_claims':[
    'not a no-go for U1 gravity or RTK generally',
    'does not exclude a new A-charged compensator whose homogeneous J_A cancels ordinary matter',
    'does not exclude a genuinely different/non-universal matter frame, but that is a new architecture and must re-pass equivalence principle/PPN/DOF gates',
    'does not exclude nonstandard cosmologies containing only a constant plus a^-2 A-source combination',
    'does not make the already established local static/DOF theorems mathematically false; it blocks their promotion to the current full cosmological completion'
  ],
  'next_gate':'do not spend the main research budget optimizing C9 for this unchanged matter frame; instead test the minimal consistent escape: add or derive an A-source compensator that cancels homogeneous ordinary-matter J_A while remaining perturbatively/background consistent, or redesign the matter frame/constraint architecture, then rerun DOF+PPN+GW+radiative gates on that same new action'
}
open('u1_family1_flrw_A_constraint_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
