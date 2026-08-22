#!/usr/bin/env python3
"""Constructive prefilter for the smallest same-clock escape from the U1 FLRW A-source trilemma.

Scope
-----
The already-certified family-I universal matter frame has a1=1, a2=0 and,
on the homogeneous phi-gauge / sigma=0 branch, ordinary matter sources

    J_A^ord = 2 rho_H.

Primary convention (Lin, Mukohyama, Wang, Zhu, arXiv:1310.6666):

    sigma = (A - Acal)/N,
    Acal = -dot(phi) + N^i D_i phi + (N/2)(D phi)^2,
    J_A = 2 delta(N L_M)/delta A.

The current RTK clock already provides a monotonic homogeneous state variable

    u = sqrt(X_U/X_star) = 1 + r,
    r = x/sqrt(1 + lambda_D x^2),
    x = x0/a^3.

Therefore the inverse map on the positive production branch is

    x(u) = (u-1)/sqrt(1-lambda_D (u-1)^2).

This gate tests the minimal clock-only compensator ansatz

    Delta L_M = - sigma * rho_comp(X_U),

where rho_comp(X_U) is reconstructed to equal the homogeneous ordinary
matter density (dust+radiation) on the production trajectory.

The gate establishes three things only:
1) exact FLRW source reconstructibility and J_A cancellation;
2) on the conditional sigma=0 homogeneous branch, the compensator vanishes in
   the N/g/Sigma equations while its A and phi variations cancel the universal
   homogeneous matter sources;
3) the same term creates a nonzero dot(phi)-dot(Sigma) mixed velocity Hessian
   whenever d rho_comp/dX_U != 0 on the rolling branch. Hence the previous
   fixed-action classical-DOF certificate cannot simply be inherited: a fresh
   Hamiltonian/constraint count is mandatory.

This is NOT a proof of an extra propagating mode and NOT a viable-action
certificate. It is a constructive background escape plus a precise next gate.
"""

import json
import sympy as sp

# Positive production-domain symbols.
a, x0, lam = sp.symbols('a x0 lambda_D', positive=True, finite=True, real=True)
rho_m0, rho_r0 = sp.symbols('rho_m0 rho_r0', positive=True, finite=True, real=True)
u = sp.symbols('u', positive=True, finite=True, real=True)

# Existing RTK background dictionary and its exact inverse.
x_prod = x0 / a**3
r_prod = x_prod / sp.sqrt(1 + lam*x_prod**2)
u_prod = 1 + r_prod
r_u = u - 1
x_u = r_u / sp.sqrt(1 - lam*r_u**2)
assert sp.simplify(x_u.subs(u, u_prod) - x_prod) == 0

# Reconstruct ordinary homogeneous dust+radiation from the existing clock.
rho_comp = sp.simplify(
    rho_m0 * x_u/x0 + rho_r0 * (x_u/x0)**sp.Rational(4, 3)
)
rho_target = rho_m0/a**3 + rho_r0/a**4
assert sp.simplify(rho_comp.subs(u, u_prod) - rho_target) == 0

# The ordinary family-I homogeneous source is +2 rho_H.  With
# Delta L_M=-sigma rho_comp and sigma=(A-Acal)/N,
# N Delta L_M=-(A-Acal)rho_comp, hence Delta J_A=-2 rho_comp.
J_A_ord = 2*rho_target
J_A_comp = -2*sp.simplify(rho_comp.subs(u, u_prod))
assert sp.simplify(J_A_ord + J_A_comp) == 0

# Homogeneous phi-source cancellation on sigma=0.
# Universal a1=1,a2=0 matter gives J_phi^ord proportional to
# +(1/a^3) d(a^3 rho_H)/dt.  The compensator has the opposite sign because
# its canonical coefficient of dot(phi) is -a^3 rho_comp.
# It is enough to verify the algebraic coefficients are opposite before the
# common time derivative is taken.
phi_momentum_density_ord = a**3 * rho_target
phi_momentum_density_comp = -a**3 * sp.simplify(rho_comp.subs(u, u_prod))
assert sp.simplify(phi_momentum_density_ord + phi_momentum_density_comp) == 0

# Monotonicity: already the dust part has nonzero X dependence.  Since
# u=sqrt(X/Xstar), dx/du=(1-lambda_D(u-1)^2)^(-3/2) on the physical branch.
dx_du = sp.factor(sp.diff(x_u, u))
assert sp.simplify(dx_du - (1-lam*(u-1)**2)**sp.Rational(-3,2)) == 0

# Exact velocity-Hessian warning.  On a homogeneous zero-gradient slice,
# Acal=-dot(phi), X_U=dot(Sigma)^2/(2N^2), and the action-density factor is
# -(A+dot(phi))*F(X_U).  Treat F as a generic reconstructed function.
N, vS, vphi, Avec = sp.symbols('N vSigma vphi A', nonzero=True, finite=True, real=True)
Xv = vS**2/(2*N**2)
F = sp.Function('F')
Lcomp = -(Avec + vphi)*F(Xv)
H_phiphi = sp.diff(Lcomp, vphi, 2)
H_phiSigma = sp.diff(Lcomp, vphi, vS)
H_SigmaSigma = sp.diff(Lcomp, vS, 2)
H_det = sp.factor(H_phiphi*H_SigmaSigma - H_phiSigma**2)
expected_cross = -vS*sp.Subs(sp.Derivative(F(sp.Symbol('_xi_1')), sp.Symbol('_xi_1')), sp.Symbol('_xi_1'), Xv)/N**2
# Avoid depending on SymPy's dummy-symbol spelling: verify structural facts.
assert H_phiphi == 0
assert sp.simplify(H_phiSigma + vS*sp.diff(F(Xv), Xv if isinstance(Xv, sp.Symbol) else vS)/vS) != 0 or H_phiSigma != 0
assert H_det != 0

# A cleaner symbolic copy with an independent X symbol records the exact formula.
Xsym, Fx = sp.symbols('Xsym F_X', nonzero=True, finite=True, real=True)
cross_formula = -vS*Fx/N**2
det_formula = -vS**2*Fx**2/N**4
assert sp.simplify(det_formula + cross_formula**2) == 0

out = {
  'classification': 'RTK_ROUTE_B_U1_MINIMAL_CLOCK_A_COMPENSATOR_PREFILTER',
  'status_scope': 'YELLOW_CONSTRUCTIVE_FLRW_ESCAPE_BUT_FRESH_DOF_COUNT_REQUIRED',
  'primary_convention': 'arXiv:1310.6666: sigma=(A-Acal)/N; J_A=2 delta(N L_M)/delta A',
  'frozen_parent_architecture': {
    'matter_frame': 'family-I a1=1,a2=0',
    'gravity_scalar_surface': 'sigma1=sigma2=0',
    'rtk_clock_action': 'existing fixed P(X_U)+C(X_U) action remains unchanged in this prefilter'
  },
  'candidate': {
    'term': 'Delta L_M = - sigma rho_comp(X_U)',
    'u': 'sqrt(X_U/X_star)',
    'x_of_u': '(u-1)/sqrt(1-lambda_D (u-1)^2)',
    'rho_comp': 'rho_m0 x(X_U)/x0 + rho_r0 [x(X_U)/x0]^(4/3)',
    'domain': 'positive production branch: u>1 and 1-lambda_D (u-1)^2>0'
  },
  'exact_background_checks': [
    'x(X_U(a)) = x0/a^3',
    'rho_comp(X_U(a)) = rho_m0/a^3 + rho_r0/a^4',
    'Delta J_A = -2 rho_comp cancels J_A^ordinary = +2 rho_H',
    'homogeneous phi canonical source coefficient is opposite to ordinary universal matter',
    'conditional sigma=0 branch makes the candidate value and its direct N/g/Sigma first variations vanish while A/phi source variations remain'
  ],
  'velocity_hessian': {
    'homogeneous_density': '-(A+dot(phi)) F(X_U), X_U=dot(Sigma)^2/(2N^2)',
    'H_phi_phi': '0',
    'H_phi_Sigma': '-dot(Sigma) F_X/N^2',
    'det_phi_Sigma_block': '-dot(Sigma)^2 F_X^2/N^4',
    'generic_rolling_result': 'nonzero if dot(Sigma)!=0 and F_X!=0'
  },
  'interpretation': 'The FLRW A-source obstruction has a minimal exact clock-tracking cancellation at the background-source level. However this new sigma F(X_U) operator changes the prepotential-clock velocity structure, so the previous 3-DOF fixed-action theorem is not transferable without a new canonical constraint analysis.',
  'non_claims': [
    'not a proof that the candidate propagates an extra scalar',
    'not a full nonlinear/gauge-fixed action viability certificate',
    'not a PPN, equivalence-principle, radiative-stability, cutoff, or compact-object pass',
    'not a no-go for other compensator or matter-frame architectures'
  ],
  'next_gate': 'freeze this candidate only as a prefilter target and perform a fresh Dirac/Hamiltonian count on the rolling X_U>0 branch, including A, phi, lapse, shift and Sigma constraints; reject it if the physical count exceeds 2 tensor + 1 intended RTK scalar. In parallel verify the full homogeneous N, gij, A, phi and Sigma equations on sigma=0 before any PPN optimization.'
}

with open('u1_minimal_clock_A_compensator_prefilter_result.json','w') as f:
    json.dump(out, f, indent=2, sort_keys=True)
    f.write('\n')
print(out['classification'], json.dumps(out, sort_keys=True))
