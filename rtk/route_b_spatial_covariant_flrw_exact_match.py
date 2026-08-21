#!/usr/bin/env python3
"""Exact FLRW scalar reduction for the local spatial-covariant RTK benchmark.

Candidate fixed action in unitary gauge:

  S = ∫ N sqrt(gamma) [ Mpl^2/2 (R3 + K_ij K^ij - K^2)
                        + F(t,N) + C_acc a_i a^i ],
  a_i = D_i ln N.

`F(t,N)` is the unitary-gauge representation of the already fixed Khronon/P(X)
background; explicit t-dependence is not a per-epoch fit, but the usual unitary-
gauge image of a covariant clock background.  The previous
`route_b_spatial_covariant_benchmark.py` proved the local Stückelberg dispersion
and velocity-Hessian/3-DOF benchmark.  Here we derive the flat-FLRW scalar
constraint reduction in comoving/unitary gauge and connect it to the exact
production Khronon background formulas.

For scalar perturbations

  N = 1+n,
  N_i = ∂_i psi,
  gamma_ij = a^2 exp(2 zeta) delta_ij,

and y=p^2=k^2/a^2>0, the background-equation-reduced quadratic action before
eliminating n,psi is encoded below.  The shift constraint is exact at this order
and gives n=dot(zeta)/H.  The acceleration term then becomes a spatially
dispersive kinetic operator proportional to y dot(zeta)^2.

The production DBI-Khronon formulas imply a stronger identity:

  K_8piG(a) = (rho_8piG+p_8piG)/c_a^2 = 2 M_K(a)^2.

Therefore in physical units K_phys=Mpl^2 K_8piG and the required acceleration
coefficient

  C_acc = K_phys/(2 M_K^2)

is exactly Mpl^2, independent of epoch and of the DBI state x.  No epoch-by-
epoch acceleration-coefficient fit is required.

The reduced scalar action is exactly

  S2 = 1/2 ∫ a^3/H^2 [ K_phys (1+y/M_K^2) dot(zeta)^2
                       - G_phys y zeta^2 ],

so

  omega^2 = c_a^2 y / (1+y/M_K^2),

which is the production RTK scalar sound-speed law with y=p^2.

Scope: exact quadratic scalar FLRW kernel for this local preferred-foliation
benchmark.  This does not yet prove acceptable PPN/compact-object behavior,
radiative stability, strong-coupling scale, nonlinear equivalence to the causal
RT auxiliary sector, or the full matter/source transfer-function map.
"""

from __future__ import annotations
import json
import sympy as sp

# ---------------------------------------------------------------------------
# 1. Exact bridge from production DBI-Khronon background to the acceleration
#    coefficient required by the local spatial-covariant benchmark.
# ---------------------------------------------------------------------------
x, lam, mu, Mpl = sp.symbols("x lambda_D mu_K Mpl", positive=True, finite=True)
s = sp.sqrt(1 + lam*x**2)
r = x/s
t = x/(s + 1)
Q = 1 + r

rho8 = 2*mu**2*x*(1+t)
p8 = 2*mu**2*r*t
ca2 = r/(s*(s+x))
MK = mu*Q*s*sp.sqrt(s)

G8 = sp.simplify(rho8+p8)
K8 = sp.simplify(G8/ca2)

assert sp.simplify(G8 - 2*mu**2*x*Q) == 0
assert sp.simplify(K8 - 2*mu**2*Q**2*s**3) == 0
assert sp.simplify(K8 - 2*MK**2) == 0

# rho_8piG = rho_phys/Mpl^2 because Mpl^2=(8 pi G)^(-1).
Gphys = sp.simplify(Mpl**2 * G8)
Kphys = sp.simplify(Mpl**2 * K8)
Cacc = sp.simplify(Kphys/(2*MK**2))
assert sp.simplify(Cacc - Mpl**2) == 0

# A useful state-variable inversion: r=x/s is monotone for x>0 and fixed lam>0.
# It obeys s=(1-lam*r^2)^(-1/2), so all ca2,MK,K are fixed functions of r.
assert sp.simplify(s**2 * (1-lam*r**2) - 1) == 0
ca2_r_form = sp.simplify(r*(1-lam*r**2)/(1+r))
MK_r_form = sp.simplify(mu*(1+r)*(1-lam*r**2)**(-sp.Rational(3,4)))
assert sp.simplify(ca2-ca2_r_form) == 0
assert sp.simplify(MK-MK_r_form) == 0

# ---------------------------------------------------------------------------
# 2. Flat-FLRW scalar ADM constraint reduction.
# ---------------------------------------------------------------------------
H, y = sp.symbols("H y", positive=True, finite=True)  # y=p^2=k^2/a^2
n, zdot, zeta, psi = sp.symbols("n zdot zeta psi", real=True, finite=True)

# After using the background equations and integrating only background/tadpole
# pieces, the quadratic scalar Lagrangian density divided by a^3 is
#
#  -3 Mpl^2 zdot^2 + 6 Mpl^2 H n zdot -3 Mpl^2 H^2 n^2
#  + Kphys/2 n^2 + Cacc y n^2
#  +2 Mpl^2 y n zeta + Mpl^2 y zeta^2
#  -2 Mpl^2 y (zdot-H n) psi.
#
# The terms can be reconstructed directly from the ADM action:
# - EH extrinsic curvature supplies the first line and shift mixing;
# - F(t,N) gives Kphys/2 n^2 after F_N,F_NN background identities;
# - R3 supplies 2 Mpl^2 y n zeta + Mpl^2 y zeta^2;
# - C_acc a_i a^i supplies Cacc y n^2.
L2 = (
    -3*Mpl**2*zdot**2
    + 6*Mpl**2*H*n*zdot
    - 3*Mpl**2*H**2*n**2
    + sp.Rational(1,2)*Kphys*n**2
    + Cacc*y*n**2
    + 2*Mpl**2*y*n*zeta
    + Mpl**2*y*zeta**2
    - 2*Mpl**2*y*(zdot-H*n)*psi
)

# Shift/momentum constraint: for y>0 it fixes the lapse perturbation exactly.
shift_eq = sp.factor(sp.diff(L2, psi))
assert sp.simplify(shift_eq - 2*Mpl**2*y*(H*n-zdot)) == 0
n_sol = sp.simplify(zdot/H)
assert sp.simplify(shift_eq.subs(n, n_sol)) == 0

# Lapse constraint determines the scalar shift once n=zdot/H is used.
psi_sol = sp.factor(sp.solve(sp.Eq(sp.diff(L2, n), 0), psi)[0].subs(n, n_sol))
psi_expected = sp.factor(
    -(Kphys+2*Cacc*y)*zdot/(2*Mpl**2*H**2*y) - zeta/H
)
assert sp.simplify(psi_sol-psi_expected) == 0

# Substituting the shift constraint leaves one zeta-zdot cross term.
L_after_constraints = sp.factor(sp.simplify(L2.subs(n, n_sol)))
L_pre_ibp = (
    (sp.Rational(1,2)*Kphys + Cacc*y)*zdot**2/H**2
    + 2*Mpl**2*y*zeta*zdot/H
    + Mpl**2*y*zeta**2
)
assert sp.simplify(L_after_constraints-L_pre_ibp) == 0

# Spatial y=k^2/a^2 implies a^3 y/H = a k^2/H.  Integrating
# 2 Mpl^2 a^3 y zeta zdot/H by parts produces
# -Mpl^2 a^3 y (1-dotH/H^2) zeta^2.  Together with +Mpl^2 y zeta^2,
# the net gradient is Mpl^2 y dotH/H^2 zeta^2.
dotH = sp.symbols("dotH", real=True, finite=True)
L_reduced_general = (
    (sp.Rational(1,2)*Kphys + Cacc*y)*zdot**2/H**2
    + Mpl**2*y*dotH*zeta**2/H**2
)

# Khronon background identity G_phys=rho+p=-2 Mpl^2 dotH.
dotH_rule = sp.Eq(dotH, -Gphys/(2*Mpl**2))
L_reduced = sp.simplify(L_reduced_general.subs(dotH, dotH_rule.rhs))
L_expected = (
    Kphys*(1+y/MK**2)*zdot**2/(2*H**2)
    - Gphys*y*zeta**2/(2*H**2)
)
assert sp.simplify(L_reduced-L_expected) == 0

omega2 = sp.simplify(Gphys*y/(Kphys*(1+y/MK**2)))
omega2_expected = sp.simplify(ca2*y/(1+y/MK**2))
assert sp.simplify(omega2-omega2_expected) == 0

# ---------------------------------------------------------------------------
# 3. Explicit nondynamical constraint matrix.  This also explains why the
#    earlier strict-single-linear-constraint-pole Schur gate is not the relevant
#    mechanism for this carrier: det M ∝ y^2, while the y factors cancel against
#    the source/mixing structure and the RTK factor is generated directly in the
#    kinetic operator after the momentum constraint.
# ---------------------------------------------------------------------------
Mnn = sp.simplify(Kphys - 6*Mpl**2*H**2 + 2*Cacc*y)
Mnpsi = sp.simplify(2*Mpl**2*H*y)
Mpsipsi = sp.Integer(0)
Mdet = sp.factor(Mnn*Mpsipsi - Mnpsi**2)
assert sp.simplify(Mdet + 4*Mpl**4*H**2*y**2) == 0

out = {
    "classification": "RTK_ROUTE_B_SPATIAL_COVARIANT_FLRW_EXACT_MATCH_PASS",
    "candidate_action": "N sqrt(gamma) [Mpl^2/2 (R3+KijKij-K^2) + F(t,N) + Mpl^2 a_i a^i]",
    "production_background_identities": {
        "G8": "rho8+p8 = 2 mu_K^2 x Q",
        "K8": "(rho8+p8)/c_a^2 = 2 mu_K^2 Q^2 s^3 = 2 M_K^2",
        "fixed_acceleration_coefficient": "C_acc = K_phys/(2 M_K^2) = Mpl^2 exactly"
    },
    "state_function_forms": {
        "r": "x/sqrt(1+lambda_D x^2)",
        "c_a^2": "r(1-lambda_D r^2)/(1+r)",
        "M_K": "mu_K(1+r)(1-lambda_D r^2)^(-3/4)"
    },
    "scalar_gauge": "N=1+n, N_i=partial_i psi, gamma_ij=a^2 exp(2 zeta) delta_ij",
    "momentum_constraint": "n = dot(zeta)/H for p^2>0",
    "shift_solution": "psi = -zeta/H - [K_phys+2 Mpl^2 p^2] dot(zeta)/(2 Mpl^2 H^2 p^2)",
    "reduced_action": "S2=1/2 int a^3/H^2 [K_phys(1+p^2/M_K^2) dot(zeta)^2 - G_phys p^2 zeta^2]",
    "dispersion": "omega^2=c_a^2 p^2/(1+p^2/M_K^2)",
    "constraint_matrix": {
        "M_nn": "K_phys-6 Mpl^2 H^2+2 Mpl^2 p^2",
        "M_npsi": "2 Mpl^2 H p^2",
        "M_psipsi": "0",
        "detM": "-4 Mpl^4 H^2 p^4"
    },
    "relation_to_schur_single_pole_gate": "This direct acceleration-kinetic carrier does not claim a strict linear constraint-determinant pole. detM is proportional to p^4; source/mixing powers cancel, and the RTK rational dispersion comes from the local p^2-dependent kinetic coefficient. Therefore the earlier D2=0 single-constraint-pole filter is inapplicable to this mechanism, not violated by it.",
    "theorem": "The fixed local spatial-covariant metric+Khronon benchmark with acceleration coefficient C_acc=Mpl^2 reproduces the exact production RTK quadratic scalar FLRW dispersion for every positive DBI background state x, without epoch-by-epoch tuning of C_acc.",
    "guards": [
        "quadratic scalar FLRW theorem only",
        "homogeneous p=0 mode is a separate background/gauge sector",
        "does not yet establish the full matter/source transfer-function map",
        "does not override existing PPN/compact-object restrictions on narrower covariant identifications",
        "does not prove radiative stability or a safe strong-coupling cutoff",
        "does not identify the causal RT auxiliary history with a local free dark-energy fluid"
    ],
    "next_step": "Audit the same fixed action against PPN/Newton/GW and compact-object constraints and derive the minimally coupled matter/source response. If those fail, retain this as an exact quadratic scalar benchmark rather than a final C7 completion."
}

print("RTK_ROUTE_B_SPATIAL_COVARIANT_FLRW_EXACT_MATCH_PASS", json.dumps(out, sort_keys=True))
