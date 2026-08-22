#!/usr/bin/env python3
"""Scoped trilemma for the published nonprojectable U1 universal matter coupling.

Assumptions/class:
- Lin-Mukohyama-Wang-Zhu universal matter metric with nonsingular Omega(sigma),
- no additional A-charged compensator beyond ordinary matter,
- fixed RTK scalar sector is A-neutral,
- homogeneous pressureless ordinary dust is present,
- require no unwanted gravitational scalar nonlinearly: sigma1=sigma2=0,
- require the published weak-field/PPN branch compatible with observations.

Facts from arXiv:1310.6666 and arXiv:1504.07357:
1) Homogeneous comoving pressureless dust has, from Eq.(4.15),
      J_A = 2 Omega^3 a1 rho_H
   because N_i s^i=0 and g_ij s^ij=0.
2) The A constraint Eq.(2.18) is
      R3-2 Lambda_g-sigma1 a^2-sigma2 div(a)=8 pi G J_A.
   On flat homogeneous FLRW with sigma1=sigma2=0 this forces J_A to be a
   constant fixed by Lambda_g. For rho_dust~a^-3 and nonsingular Omega that
   asymptotes to a fixed regular matter frame, the clean source-free solution is
   a1=0 unless an extra A-source cancels the dust contribution. In the current
   frozen a2=0 frame Omega=1, this is exact for all a.
3) On sigma1=sigma2=0, Eq.(5.30) reduces to -2 kappa(a1-1)=0, so for
   nonzero kappa the PPN field equations require a1=1; the experimental analysis
   also gives |a1-1|<1e-5.
4) The paper's exact-GR minimal-matter special case a1=a2=0 instead uses
   sigma2=4 [Eq.(7.2)], leaving the no-gravity-scalar surface. Mukohyama et al.
   arXiv:1504.07357 show the unwanted gravity scalar is absent classically iff
   the two corresponding sigma/eta couplings are exactly zero.

Thus the three requirements cannot be met simultaneously inside this unchanged
published universal-matter architecture. A new A-source/constraint or matter
architecture is required.
"""
import json
import sympy as sp

a1,kappa,rho,Omega,G,Lg,a=sp.symbols('a1 kappa rho Omega G Lambda_g a', nonzero=True, finite=True, real=True)
# Homogeneous pressureless dust source.
JA=2*Omega**3*a1*rho
assert sp.simplify(JA/(2*Omega**3*rho)-a1)==0
# No-extra-scalar PPN phi constraint at sigma2=0.
phi_ppn=-2*kappa*(a1-1)
sol_a1=sp.solve(sp.Eq(phi_ppn,0),a1)
assert sol_a1==[1]
# Flat A constraint with current frozen a2=0 -> Omega=1 and dust rho=rho0/a^3.
rho0=sp.symbols('rho0', nonzero=True, finite=True, real=True)
flat_residual=sp.expand(-2*Lg-16*sp.pi*G*a1*rho0/a**3)
poly=sp.Poly(sp.expand(a**3*flat_residual),a)
assert poly.coeff_monomial(a**3)==-2*Lg
assert poly.coeff_monomial(a**0)==-16*sp.pi*G*a1*rho0
# Equality for all a with rho0,G nonzero forces Lg=0 and a1=0, contradicting PPN a1=1.

out={
  'classification':'RTK_ROUTE_B_U1_UNIVERSAL_MATTER_FLRW_PPN_DOF_TRILEMMA',
  'status_scope':'BLACK_SCOPED_PUBLISHED_UNIVERSAL_MATTER_NO_COMPENSATOR_CLASS',
  'assumptions':[
    'nonprojectable local-U1 gravity with published universal matter coupling',
    'ordinary homogeneous pressureless dust present',
    'no additional A-charged compensator/source',
    'fixed RTK P(X_U)+C(X_U) sector remains A-neutral',
    'no unwanted gravity scalar: sigma1=sigma2=0',
    'nonsingular matter metric Omega',
    'current production flat-FLRW embedding uses a2=0 so Omega=1 exactly'
  ],
  'exact_relations':{
    'dust_A_source':'J_A=2 Omega^3 a1 rho_H',
    'A_constraint':'R3-2 Lambda_g = 8 pi G J_A on homogeneous sigma1=sigma2=0 branch',
    'flat_current_frame':'-2 Lambda_g = 16 pi G a1 rho_dust0 a^-3',
    'PPN_phi_constraint_sigma2_zero':'-2 kappa(a1-1)=0 -> a1=1 for kappa!=0',
    'observational_PPN':'|a1-1|<1e-5 in the sigma1=sigma2=0 analysis',
    'minimal_coupling_GR_PPN_escape_in_paper':'a1=a2=0 requires sigma2=4 and beta0=-2(1+gamma1), hence it is outside the sigma2=0 no-gravity-scalar surface'
  },
  'result':'Within the unchanged published universal-matter class and without an extra A-charged compensator, flat evolving dust cosmology and the no-extra-gravity-scalar PPN branch require incompatible values a1=0 and a1=1. The known minimal-coupling PPN escape reintroduces the gravity scalar by sigma2!=0.',
  'interpretation':'The current U1 family-I fixed action remains valuable as a set of local classical theorems, but it cannot be promoted to the full production cosmological completion with the same universal ordinary-matter coupling. A genuinely new A-source/matter/constraint architecture is mandatory.',
  'non_claims':[
    'not a no-go for RTK, U1 gravity, Hořava gravity, or non-universal matter frames in general',
    'does not exclude an A-charged compensator that cancels the homogeneous dust source while preserving local PPN/DOF',
    'does not exclude a new structural degeneracy that tolerates sigma2!=0 without an extra propagating scalar',
    'does not erase the scoped static beta, TT, or fixed-action DOF results already proved'
  ],
  'next_gate':'construct the minimal A-source compensation/constraint architecture. Freeze its action before tests; require homogeneous J_A cancellation, unchanged production Friedmann background, exactly 2 tensor + 1 RTK scalar, local Newton/gamma/beta/preferred-frame pass, and radiative/cutoff protection on the same action.'
}
open('u1_universal_matter_flrw_ppn_dof_trilemma_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
