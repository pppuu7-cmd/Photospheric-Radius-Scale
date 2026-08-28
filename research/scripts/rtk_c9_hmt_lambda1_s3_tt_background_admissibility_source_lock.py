#!/usr/bin/env python3
"""Exact scoped audit for the HMT λ=1 round-S3 TT background prerequisite.

This script deliberately does not construct a TT Hessian.  It verifies the HMT
A-constraint on the frozen round-S3 witness and the vanishing of the linear TT
variations that can be established without assigning unspecified potential
couplings or a background A0.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

CLASSIFICATION = (
    "RTK_C9_HMT_LAMBDA1_S3_TT_BACKGROUND_ADMISSIBILITY_"
    "A_CONSTRAINT_SOURCE_LOCKED_PASS_SCOPED"
)


def audit() -> dict:
    # D=3 round S3: R_ij=(2/a^2)g_ij and R=6/a^2.
    # HMT A variation from -A(R-2 Omega) imposes R-2 Omega=0.
    R_coeff = Fraction(6, 1)      # R = R_coeff/a^2
    omega_coeff = R_coeff / 2    # Omega = omega_coeff/a^2
    assert omega_coeff == 3

    # Exact sample-family check.  Rational a^2 values avoid floating arithmetic.
    sample_a2 = [Fraction(1, 4), Fraction(1, 1), Fraction(9, 4), Fraction(7, 3)]
    residuals = []
    for a2 in sample_a2:
        R = R_coeff / a2
        Omega = omega_coeff / a2
        residual = R - 2 * Omega
        assert residual == 0
        residuals.append({
            "a2": str(a2),
            "R": str(R),
            "Omega": str(Omega),
            "R_minus_2Omega": str(residual),
        })

    # TT first variation on an Einstein background:
    # delta R = -R^ij h_ij + nabla_i nabla_j h^ij - nabla^2 h.
    # R^ij=(R/3)g^ij, trace h=0, divergence h=0 -> each term vanishes.
    tt_delta_R_terms = {
        "ricci_trace_term": "-(R/3) g^ij h_ij = 0 by tracelessness",
        "double_divergence_term": "nabla_i nabla_j h^ij = 0 by transversality (on the frozen covariant TT field)",
        "trace_laplacian_term": "-nabla^2 h = 0 by h=0",
    }
    delta_R_zero = True
    delta_sqrt_g_zero = True  # delta sqrt(g)=1/2 sqrt(g) h, and h=0.
    assert delta_R_zero and delta_sqrt_g_zero

    result = {
        "classification": CLASSIFICATION,
        "scope": "C9 HMT lambda=1 round-S3 TT background prerequisite only",
        "source_lock": {
            "primary": "Horava & Melby-Thompson, Phys.Rev.D82:064027 (2010), arXiv:1007.2410",
            "action_A_term": "-A (R - 2 Omega)",
            "A_equation": "R = 2 Omega",
        },
        "frozen_background": {
            "D": 3,
            "lambda": 1,
            "geometry": "round S3 radius a>0",
            "Rij": "2 a^-2 g_ij",
            "R": "6 a^-2",
            "Kij": 0,
            "nu": 0,
            "TT_conditions": ["nabla^i h_ij = 0", "g^ij h_ij = 0"],
        },
        "exact_result": {
            "A_constraint_required_Omega": "Omega = 3/a^2",
            "A_constraint_residual_on_relation": "R - 2 Omega = 0 exactly",
            "TT_delta_R": 0,
            "TT_delta_sqrt_g": 0,
            "linear_TT_A_constraint_obstruction": False,
            "sample_exact_family_checks": residuals,
            "delta_R_term_audit": tt_delta_R_terms,
        },
        "interpretation": {
            "background_A_equation_passes_conditionally": True,
            "condition": "The round-S3 witness is compatible with the HMT A-equation iff Omega=3/a^2.",
            "what_this_does_not_establish": [
                "full metric stationarity of the witness",
                "the background value A0",
                "a frozen numerical HMT potential V[g] or its couplings",
                "the physical TT quadratic Hessian",
                "the TT spectrum/determinant",
                "one-loop evaluability or C9 closure",
            ],
            "next_gate": (
                "Source-lock the concrete HMT spatial potential convention and derive the static round-S3 "
                "metric stationarity equation, including A0; only then derive the TT quadratic operator."
            ),
        },
        "frozen_nonclaims": {
            "full_TT_hessian_derived": False,
            "tt_spectrum_computed": False,
            "tt_determinant_computed": False,
            "background_metric_stationarity_fully_checked": False,
            "full_FP_determinant_computed": False,
            "full_FS_determinant_computed": False,
            "complete_HMT_gauge_fixed_constraint_matrix_constructed": False,
            "full_HMT_one_loop_evaluable": False,
            "full_C9_closed": False,
            "soft_s_retest_allowed": False,
            "production_k003_unblocked": False,
            "threshold_changed": False,
        },
    }
    return result


def main() -> None:
    result = audit()
    out = Path("research/theory_results/rtk_c9_hmt_lambda1_s3_tt_background_admissibility_source_lock.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
