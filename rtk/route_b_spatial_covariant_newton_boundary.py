#!/usr/bin/env python3
"""Scoped Newton-normalization boundary for the exact direct FLRW carrier.

The exact spatial-covariant FLRW match proved by
`route_b_spatial_covariant_flrw_exact_match.py` requires

    C_acc = M_P^2

in

    S ⊃ ∫ N sqrt(gamma) C_acc a_i a^i.

The standard healthy non-projectable Hořava/BPS low-energy normalization is

    S = M_P^2/2 ∫ N sqrt(gamma)
        [K_ij K^ij - lambda K^2 + R + alpha a_i a^i + ...],

so alpha = 2 C_acc/M_P^2.  Exact direct RTK matching therefore lands at
alpha=2.

For the minimal/universal beta=0 matter branch with xi=1, BPS gives

    G_N = 1/[8 pi M_P^2 (1-alpha/2)],

or Mbar_N^2 = M_P^2(1-alpha/2), where Mbar_N^2=(8 pi G_N)^(-1).
Thus alpha=2 is a singular Newton-normalization boundary for finite bare M_P.

This is a scoped negative result for identifying the exact direct carrier with
the minimal xi=1,beta=0 healthy-Horava matter branch.  It does not exclude a
spatially covariant EFT, a nonminimal/disformal matter metric, xi!=1, companion
operators, auxiliary fields, or another covariant completion.
"""

import json
import sympy as sp

M, MK, p, eps = sp.symbols("M_P M_K p epsilon", positive=True, finite=True)
Cacc, alpha = sp.symbols("C_acc alpha", positive=True, finite=True)

# Production exact-match identity: K_phys=2 M_P^2 M_K^2.
Kphys = 2*M**2*MK**2

# Direct acceleration carrier produces K_eff=Kphys+2 Cacc p^2.
Keff = Kphys + 2*Cacc*p**2
Ktarget = Kphys*(1+p**2/MK**2)
C_solution = sp.solve(sp.Eq(Keff, Ktarget), Cacc)
assert C_solution == [M**2]

# Standard BPS action normalization: coefficient of +a_i a^i is M_P^2 alpha/2.
alpha_map = sp.simplify(2*C_solution[0]/M**2)
assert alpha_map == 2

# Minimal/universal beta=0, xi=1 Newton normalization.
newton_den = sp.simplify(1-alpha/2)
assert sp.simplify(newton_den.subs(alpha, alpha_map)) == 0
MbarN2 = sp.simplify(M**2*newton_den)
assert sp.simplify(MbarN2.subs(alpha, alpha_map)) == 0

# A regularized alpha=2(1-eps), 0<eps<1, has finite Newton factor eps but no
# longer reproduces the exact production M_K coefficient at fixed target Kphys,MK.
alpha_eps = 2*(1-eps)
C_eps = sp.simplify(M**2*alpha_eps/2)
Keff_eps = sp.factor(Keff.subs(Cacc, C_eps))
assert sp.simplify(Keff_eps - Kphys*(1+(1-eps)*p**2/MK**2)) == 0
assert sp.simplify(Keff_eps-Ktarget) == -2*M**2*eps*p**2
assert sp.simplify(newton_den.subs(alpha, alpha_eps)-eps) == 0

# Equivalently, the regularized carrier has Mdisp=MK/sqrt(1-eps), not MK.
Mdisp_eps = sp.simplify(MK/sp.sqrt(1-eps))
assert sp.simplify(1/Mdisp_eps**2-(1-eps)/MK**2) == 0

out = {
    "classification": "RTK_ROUTE_B_SPATIAL_COVARIANT_NEWTON_BOUNDARY_PASS",
    "exact_direct_match": {
        "K_phys": "2 M_P^2 M_K^2",
        "required_C_acc": "M_P^2",
        "bps_dimensionless_alpha": "2 C_acc/M_P^2 = 2"
    },
    "minimal_beta0_xi1_newton_relation": "G_N=1/[8 pi M_P^2(1-alpha/2)]",
    "boundary": "alpha=2 makes Mbar_N^2=M_P^2(1-alpha/2)=0 and G_N singular for finite bare M_P",
    "regularized_check": {
        "alpha": "2(1-epsilon)",
        "newton_factor": "1-alpha/2=epsilon",
        "kinetic_factor": "1+(1-epsilon)p^2/M_K^2",
        "effective_Mdisp": "M_K/sqrt(1-epsilon)",
        "conclusion": "any finite epsilon>0 restores the beta0 Newton denominator but spoils exact matching to the frozen production M_K if no other operator/normalization is changed"
    },
    "theorem": "The exact direct acceleration-only FLRW carrier cannot simultaneously reproduce the frozen production M_K coefficient and have a regular finite-bare-M_P Newton normalization in the minimal xi=1,beta=0 universally coupled BPS branch.",
    "scope": "minimal xi=1,beta=0 matter normalization plus direct acceleration-only identification",
    "non_claims": [
        "not a no-go for the spatially covariant quadratic scalar EFT itself",
        "not a no-go for xi!=1 or a nonminimal/disformal matter metric",
        "not a no-go for companion operators that alter the static/Newton sector while preserving the cosmological kinetic kernel",
        "not a no-go for auxiliary-field or broader covariant completions",
        "does not analyze a singular correlated M_P->infinity, alpha->2 limit"
    ],
    "next_step": "Search for the smallest fixed companion operator/matter-metric deformation that regularizes Newton/PPN while leaving C_acc=M_P^2 and the exact FLRW scalar kernel intact; then test GW and compact-object constraints on the same tuple."
}

print("RTK_ROUTE_B_SPATIAL_COVARIANT_NEWTON_BOUNDARY_PASS", json.dumps(out, sort_keys=True))
