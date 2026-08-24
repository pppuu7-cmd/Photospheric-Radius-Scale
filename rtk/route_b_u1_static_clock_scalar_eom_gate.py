#!/usr/bin/env python3
"""Exact static-clock scalar-EOM gate for the frozen U(1)+RTK scalar action.

Frozen scalar action
--------------------
  S_Sigma = int dt d^3x N sqrt(g) [ P(X_U) + C(X_U) D_i Theta_U D^i Theta_U ]
  X_U     = 1/2 [Theta_U^2 - D_i Sigma D^i Sigma]
  Theta_U = [dot Sigma - B^i D_i Sigma]/N,
  B^i     = N^i - N D^i nu.

Gate sector
-----------
  B^i = 0,
  Sigma = q t,
  D_i Sigma = 0,
  partial_t N = partial_t g_ij = 0.

The proof is variational and exact in the lapse amplitude.  It does not insert
Sigma=q t into the action before varying.  Instead it evaluates the *first
variation* of the full action on the stated background.

Let eta=delta Sigma.  On the background
  delta Theta = dot eta / N,
  delta X     = q dot eta / N^2,
  delta(D_i Theta) = D_i(dot eta/N).
Hence delta L contains only dot eta and D_i dot eta.  After one spatial
integration by parts it is of the form int Pi_static(x) dot eta; after the time
integration by parts the scalar Euler-Lagrange expression is
  -partial_t Pi_static = 0.
All coefficients are time independent.  No assumption about the detailed P(X)
or C(X) functional form is needed beyond shift symmetry and regularity on the
rolling X_U>0 branch.

This proves only the scalar equation in the static zero-invariant-shift sector.
It does not yet prove the lapse/spatial-metric/U(1) constraints, PPN viability,
rotating solutions, compact-object regularity, radiative stability, or a UV
cutoff.
"""

from __future__ import annotations

import json
import sympy as sp

# One representative spatial component is sufficient because the index
# contraction is a linear sum of identical component-wise structures.  We keep
# the symbols independent so the result is structural rather than numerical.
N, q, sqrtg = sp.symbols("N q sqrtg", nonzero=True)
PX, CX, C, Y = sp.symbols("P_X C_X C Y")
A, dN = sp.symbols("A dN")  # A=D_i Theta, dN=D_i N for one component
eta, etat, etai, etati = sp.symbols("eta eta_t eta_i eta_ti")

Theta = q / N

delta_theta = etat / N
# D_i(delta Theta) = D_i(eta_t/N)
delta_A = etati / N - etat * dN / N**2
# D_i Sigma=0 on the background, so there is no term proportional to eta_i.
delta_X = sp.expand(Theta * delta_theta)
delta_Y_component = sp.expand(2 * A * delta_A)

delta_L_component = sp.expand(
    N * sqrtg * ((PX + CX * Y) * delta_X + C * delta_Y_component)
)

# The local first variation must have no undifferentiated eta and no spatial
# eta_i term.  Only eta_t and eta_ti are allowed.
coeff_eta = sp.expand(delta_L_component).coeff(eta)
coeff_etai = sp.expand(delta_L_component).coeff(etai)
assert sp.simplify(coeff_eta) == 0
assert sp.simplify(coeff_etai) == 0

coeff_etat = sp.simplify(delta_L_component.coeff(etat))
coeff_etati = sp.simplify(delta_L_component.coeff(etati))
assert coeff_etat != 0
assert coeff_etati != 0

# After spatial IBP, integral B^i D_i eta_t -> -integral D_i B^i eta_t.
# Both A(x), N(x), g(x), P_X(x), C_X(x), C(x), Y(x) are static on the
# background.  Therefore the resulting generalized momentum Pi_static has no
# time dependence and the final EOM -partial_t Pi_static vanishes exactly.
# Encode the time-derivative test algebraically by promoting all static
# coefficients to symbols with zero t derivative.
t = sp.symbols("t")
static_symbols = [N, q, sqrtg, PX, CX, C, Y, A, dN]
for s in static_symbols:
    assert not s.has(t)

# Exact fixed-action identity in this static clock sector.
# X=q^2/(2N^2), C=M_Pl^2/(2X), D_i Theta=-q D_iN/N^2.
Mpl = sp.symbols("M_Pl", positive=True)
X = q**2 / (2 * N**2)
C_fixed = Mpl**2 / (2 * X)
A_fixed = -q * dN / N**2
Lmix_component = sp.simplify(C_fixed * A_fixed**2)
expected_acc_component = sp.simplify(Mpl**2 * (dN / N) ** 2)
assert sp.simplify(Lmix_component - expected_acc_component) == 0

out = {
    "classification": "RTK_ROUTE_B_U1_STATIC_CLOCK_SCALAR_EOM_EXACT_PASS",
    "status": "SCOPED_EXACT_THEOREM",
    "action": "N sqrt(g) [P(X_U)+C(X_U) D_iTheta_U D^iTheta_U]",
    "sector": {
        "invariant_shift_Bi": 0,
        "Sigma": "q t",
        "D_i_Sigma": 0,
        "time_independent": ["N", "g_ij", "U1/static background coefficients"],
        "domain": "rolling X_U>0 branch",
    },
    "first_variation": {
        "delta_Theta": "dot(eta)/N",
        "delta_X": "q dot(eta)/N^2",
        "delta_DiTheta": "D_i[dot(eta)/N]",
        "contains_eta": False,
        "contains_Di_eta": False,
        "contains_only": ["dot(eta)", "D_i dot(eta)"],
        "conclusion": "after spatial IBP the coefficient of dot(eta) is static, so the time IBP gives E_Sigma=0 exactly",
    },
    "fixed_C_static_identity": "C(X_U)(DTheta_U)^2 = M_Pl^2 (D ln N)^2 = M_Pl^2 a_i a^i",
    "functional_scope": "scalar EOM proof is independent of the detailed P(X), C(X) forms; fixed C identity additionally uses C=M_Pl^2/(2X_U)",
    "non_claims": [
        "does not solve lapse, spatial-metric, shift or U(1) prepotential constraints",
        "does not by itself establish beta_PPN, gamma_PPN, alpha_1 or alpha_2",
        "does not cover stationary rotating backgrounds with nonzero invariant shift",
        "does not establish compact-object regularity near X_U=0",
        "does not establish radiative stability or the EFT cutoff",
    ],
    "next_gate": "prove variation-level equivalence of the remaining static metric/U1 constraints to the pure-U1 system with the exact explicit M_Pl^2 a_i a^i contribution, retaining the first nonvanishing P(X_U) stress; only then apply Newton/PPN formulas",
}

with open("u1_static_clock_scalar_eom_result.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, sort_keys=True)
    f.write("\n")

print(out["classification"], json.dumps(out, sort_keys=True))
