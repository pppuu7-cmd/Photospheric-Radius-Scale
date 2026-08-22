#!/usr/bin/env python3
"""Constructive prefilter for a minimal same-clock escape from the U1 FLRW A-source trilemma.

Primary convention (Lin, Mukohyama, Wang, Zhu, arXiv:1310.6666):

    sigma = (A - Acal)/N,
    Acal = -dot(phi) + N^i D_i phi + (N/2)(D phi)^2,
    J_A = 2 delta(N L_M)/delta A.

On the already-certified family-I matter branch a1=1,a2=0, homogeneous
ordinary matter has J_A^ord=2 rho_H.  The current RTK clock provides the exact
production dictionary

    u=sqrt(X_U/X_star)=1+r,
    r=x/sqrt(1+lambda_D x^2),
    x=x0/a^3.

This gate studies only the minimal clock-tracking compensator

    Delta L_M = -sigma rho_comp(X_U),

with rho_comp reconstructed to equal homogeneous dust+radiation.  It tests:
(i) exact background-source cancellation; (ii) the conditional sigma=0 reduced
background equations; and (iii) whether the previous fixed-action DOF theorem
can be inherited without a fresh constraint analysis.

A nonzero dot(phi)-dot(Sigma) Hessian block is a warning that the old DOF proof
does not transfer.  It is NOT by itself proof of an extra physical mode.
"""

import json
import sympy as sp

# ---------- exact RTK clock -> FLRW density reconstruction ----------
a, x0, lam = sp.symbols('a x0 lambda_D', positive=True, finite=True, real=True)
rho_m0, rho_r0 = sp.symbols('rho_m0 rho_r0', positive=True, finite=True, real=True)
u = sp.symbols('u', positive=True, finite=True, real=True)

x_prod = x0/a**3
r_prod = x_prod/sp.sqrt(1 + lam*x_prod**2)
u_prod = 1 + r_prod

r_u = u - 1
x_u = r_u/sp.sqrt(1 - lam*r_u**2)
assert sp.simplify(x_u.subs(u, u_prod) - x_prod) == 0

rho_comp_u = sp.simplify(
    rho_m0*x_u/x0 + rho_r0*(x_u/x0)**sp.Rational(4, 3)
)
rho_target = rho_m0/a**3 + rho_r0/a**4
rho_comp_prod = sp.simplify(rho_comp_u.subs(u, u_prod))
assert sp.simplify(rho_comp_prod - rho_target) == 0

# Family-I a1=1,a2=0: J_A^ord=+2 rho_H.
# Delta L_M=-sigma rho_comp -> N Delta L_M=-(A-Acal)rho_comp,
# so Delta J_A=-2 rho_comp.
J_A_ord = 2*rho_target
J_A_comp = -2*rho_comp_prod
assert sp.simplify(J_A_ord + J_A_comp) == 0

# On a homogeneous zero-gradient slice Acal=-dot(phi).  The ordinary universal
# coupling and compensator have opposite coefficients of dot(phi), therefore
# their homogeneous phi source terms cancel after the common time derivative.
phi_momentum_ord = a**3*rho_target
phi_momentum_comp = -a**3*rho_comp_prod
assert sp.simplify(phi_momentum_ord + phi_momentum_comp) == 0

# Monotonicity of the exact inverse map on the physical branch.
dx_du = sp.factor(sp.diff(x_u, u))
assert sp.simplify(dx_du - (1-lam*(u-1)**2)**sp.Rational(-3, 2)) == 0

# ---------- conditional sigma=0 reduced-background check ----------
# Reduced homogeneous compensator density (irrelevant common sqrt(g) factor):
#   Lc=-(A+dot(phi))*F(X), X=dot(Sigma)^2/(2N^2).
# If B=A+dot(phi)=0 is an exact background branch, Lc and its direct N and
# scale-factor variations vanish; the Sigma momentum also carries B and
# vanishes on an identically maintained B=0 trajectory.  A and phi variations
# remain and are exactly the intended source terms above.
N, vS, vphi, Avec, volume = sp.symbols(
    'N vSigma vphi A volume', nonzero=True, finite=True, real=True
)
Xv = vS**2/(2*N**2)
F = sp.Function('F')
B = Avec + vphi
Lc = -volume*B*F(Xv)
assert sp.simplify(Lc.subs(Avec, -vphi)) == 0
assert sp.simplify(sp.diff(Lc, N).subs(Avec, -vphi)) == 0
assert sp.simplify(sp.diff(Lc, volume).subs(Avec, -vphi)) == 0
assert sp.simplify(sp.diff(Lc, vS).subs(Avec, -vphi)) == 0
assert sp.simplify(sp.diff(Lc, Avec).subs(Avec, -vphi) + volume*F(Xv)) == 0
assert sp.simplify(sp.diff(Lc, vphi).subs(Avec, -vphi) + volume*F(Xv)) == 0

# ---------- velocity-Hessian transfer test ----------
H_phiphi = sp.diff(Lc, vphi, 2)
H_phiSigma = sp.diff(Lc, vphi, vS)
H_SigmaSigma = sp.diff(Lc, vS, 2)
H_det = sp.factor(H_phiphi*H_SigmaSigma - H_phiSigma**2)

Y = sp.symbols('Y', positive=True, finite=True, real=True)
FY = sp.Function('F')(Y)
FX_at_Xv = sp.diff(FY, Y).subs(Y, Xv)
expected_cross = -volume*vS*FX_at_Xv/N**2
expected_det = -volume**2*vS**2*FX_at_Xv**2/N**4
assert H_phiphi == 0
assert sp.simplify(H_phiSigma - expected_cross) == 0
assert sp.simplify(H_det - expected_det) == 0

# The reconstructed source is genuinely state-dependent.  Dust alone already
# gives d rho_comp/dX != 0 because dx/du is nonzero and du/dX=1/(2 X_star u).
Xstar = sp.symbols('X_star', positive=True, finite=True, real=True)
drho_dust_dX = sp.simplify((rho_m0/x0)*dx_du/(2*Xstar*u))
assert drho_dust_dX != 0

out = {
  'classification': 'RTK_ROUTE_B_U1_MINIMAL_CLOCK_A_COMPENSATOR_PREFILTER',
  'status_scope': 'YELLOW_CONSTRUCTIVE_FLRW_ESCAPE_BUT_FRESH_DOF_COUNT_REQUIRED',
  'primary_convention': 'arXiv:1310.6666 Eqs.(2.5),(2.19),(4.2)-(4.3),(4.15)',
  'parent_obstruction': 'BLACK_SCOPED_PUBLISHED_UNIVERSAL_MATTER_NO_COMPENSATOR_CLASS',
  'candidate': {
    'term': 'Delta L_M=-sigma rho_comp(X_U)',
    'sigma': '(A-Acal)/N',
    'u': 'sqrt(X_U/X_star)',
    'x_of_u': '(u-1)/sqrt(1-lambda_D (u-1)^2)',
    'rho_comp': 'rho_m0*x(X_U)/x0 + rho_r0*[x(X_U)/x0]^(4/3)',
    'domain': 'positive rolling production branch with 1-lambda_D(u-1)^2>0'
  },
  'exact_background_results': [
    'x(X_U(a))=x0/a^3',
    'rho_comp(X_U(a))=rho_m0/a^3+rho_r0/a^4',
    'Delta J_A=-2 rho_comp exactly cancels J_A^ord=+2 rho_H for a1=1,a2=0',
    'homogeneous phi source coefficient cancels the universal-matter coefficient',
    'conditional sigma=0 (A=Acal) makes the compensator value and direct N/g/Sigma reduced-background variations vanish while A/phi source variations remain'
  ],
  'velocity_hessian': {
    'reduced_density': '-sqrt(g)*(A+dot(phi))*F(X_U)',
    'X_U': 'dot(Sigma)^2/(2N^2) on the homogeneous zero-gradient slice',
    'H_phi_phi': '0',
    'H_phi_Sigma': '-sqrt(g)*dot(Sigma)*F_X/N^2',
    'det_phi_Sigma_block': '-g*dot(Sigma)^2*F_X^2/N^4',
    'generic_rolling_status': 'nonzero for dot(Sigma)!=0 and F_X!=0'
  },
  'interpretation': 'The old FLRW A-source obstruction is not a general no-go: the existing RTK clock is sufficient to reconstruct an exact homogeneous compensating source without changing the target production rho(a).  The naive minimal local-U1 completion nevertheless changes the prepotential-clock kinetic/constraint structure, so the previous 3-DOF fixed-action certificate cannot be inherited.',
  'non_claims': [
    'not a proof that an extra physical scalar propagates',
    'not yet a full homogeneous solution theorem beyond the conditional sigma=0 reduced branch',
    'not a PPN/equivalence-principle/radiative/cutoff/compact-object pass',
    'not a no-go for degenerate compensators, constrained compensators, or redesigned matter frames'
  ],
  'next_gate': 'perform a fresh Dirac/Hamiltonian count for this frozen prefilter candidate on rolling X_U>0, including A, phi, lapse, shift and Sigma constraints, while independently verifying all homogeneous N,g_ij,A,phi,Sigma equations on the sigma=0 branch.  Only if the physical count remains 2 tensor + 1 intended RTK scalar may the candidate advance to PPN/GW/radiative/cutoff gates.'
}

with open('u1_minimal_clock_A_compensator_prefilter_result.json', 'w') as f:
    json.dump(out, f, indent=2, sort_keys=True)
    f.write('\n')
print(out['classification'], json.dumps(out, sort_keys=True))
