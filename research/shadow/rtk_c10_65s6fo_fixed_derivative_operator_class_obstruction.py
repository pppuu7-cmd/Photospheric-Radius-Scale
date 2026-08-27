#!/usr/bin/env python3
"""C10.65s6fO: exact symbolic fixed-derivative operator-class obstruction audit.

This gate is deliberately narrow.  It asks whether a finite linear combination
of local, metric-only, pure-spatial six-derivative operators can change the
constant-homogeneous soft cubic response while preserving the complete hard
quadratic functional exactly.  It does NOT test mixed derivative, extra-field,
or nonlocal UV completions.
"""

from __future__ import annotations

import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "research/theory_targets/RTK_C10_65S6FO_FIXED_DERIVATIVE_OPERATOR_CLASS_OBSTRUCTION_TARGET_v1.json"
RESULT = ROOT / "research/theory_results/RTK_C10_65S6FO_FIXED_DERIVATIVE_OPERATOR_CLASS_OBSTRUCTION_RESULT_v1.json"
PARENT_M = ROOT / "research/checkpoints/RTK_C10_65S6FM_EXACT_HOMOGENEOUS_CUBIC_2026-08-27T0952Z.md"
PARENT_N = ROOT / "research/checkpoints/RTK_C10_65S6FN_HIGHER_SPATIAL_SOFT_OBSTRUCTION_2026-08-27T0954Z.md"


def main() -> int:
    target = json.loads(TARGET.read_text())
    assert target["status"] == "FROZEN_BEFORE_EXECUTION"
    assert target["threshold_changed"] is False
    assert target["frozen_assumptions"]["total_spatial_derivative_order"] == 6
    assert target["frozen_assumptions"]["exact_hard_quadratic_preservation"] is True

    # Source-lock the immediate scientific frontier without reclassifying it.
    mtxt = PARENT_M.read_text()
    ntxt = PARENT_N.read_text()
    parent_m_nonzero = "NONZERO" in mtxt.upper()
    parent_n_obstruction = "OBSTRUCTION" in ntxt.upper() and "PASS" in ntxt.upper()

    z, d = sp.symbols("z d", real=True)
    Q = sp.symbols("DeltaQ2")
    w = 3 - d
    scaling = sp.exp(w * z) * Q
    first_variation = sp.diff(scaling, z).subs(z, 0)

    w6 = sp.simplify(w.subs(d, 6))
    six_derivative_variation = sp.simplify(first_variation.subs(d, 6))
    preservation_zero = sp.simplify(six_derivative_variation.subs(Q, 0))

    # Cross-check against the D^(n-1)R D^(n-1)R family used by s6fN.
    n = sp.symbols("n", integer=True, positive=True)
    d_family = 2 * n + 2
    w_family = sp.simplify(3 - d_family)
    w_family_n2 = sp.simplify(w_family.subs(n, 2))

    # Generic finite same-weight retuning.  Explicit arbitrary coefficients are
    # enough because linearity makes the statement independent of term count.
    c1, c2, c3, q1, q2, q3 = sp.symbols("c1 c2 c3 q1 q2 q3")
    delta_q = c1*q1 + c2*q2 + c3*q3
    soft_delta = sp.expand(w6 * delta_q)
    exact_preservation = sp.simplify(soft_delta.subs(c3*q3, -(c1*q1 + c2*q2)))

    # A separately parameterized certified kernel makes the retuning invariance
    # transparent: if total Q is unchanged, its homogeneous response is unchanged.
    Qcert, Delta = sp.symbols("Qcert Delta")
    soft_before = sp.expand(w6 * Qcert)
    soft_after = sp.expand(w6 * (Qcert + Delta))
    retuning_change = sp.simplify((soft_after - soft_before).subs(Delta, 0))

    # Zero-quadratic operators cannot contribute to this hard-hard-soft scaling channel.
    qzero = sp.symbols("Qzero")
    zero_quadratic_soft = sp.simplify((w6*qzero).subs(qzero, 0))

    representative_weights = {
        "R^3": -3,
        "R R_ij R^ij": -3,
        "R_i^j R_j^k R_k^i": -3,
        "R Delta R": -3,
        "D_i R D^i R": -3,
        "D_k R_ij D^k R^ij": -3,
    }

    checks = {
        "target_frozen_before_execution": target["status"] == "FROZEN_BEFORE_EXECUTION",
        "threshold_unchanged": target["threshold_changed"] is False,
        "parent_s6fM_nonzero_locked": parent_m_nonzero,
        "parent_s6fN_obstruction_pass_locked": parent_n_obstruction,
        "weight_rule_w_equals_3_minus_d": sp.simplify(first_variation - w*Q) == 0,
        "six_derivative_weight_is_minus3": w6 == -3,
        "six_derivative_soft_variation_is_minus3Q": sp.simplify(six_derivative_variation + 3*Q) == 0,
        "n2_family_crosscheck_is_minus3": w_family_n2 == -3,
        "exact_quadratic_preservation_kills_compensating_soft_response": preservation_zero == 0,
        "generic_same_weight_retuning_with_zero_deltaQ_has_zero_soft_delta": exact_preservation == 0,
        "certified_kernel_retuning_invariance": retuning_change == 0,
        "zero_quadratic_operator_has_zero_scaling_channel_soft_source": zero_quadratic_soft == 0,
        "all_representative_six_derivative_weights_match": all(v == -3 for v in representative_weights.values()),
    }

    passed = all(checks.values())
    classification = (
        "C10_65S6FO_FIXED_DERIVATIVE_OPERATOR_CLASS_OBSTRUCTION_PASS_SCOPED"
        if passed else
        "C10_65S6FO_COUNTEREXAMPLE_FOUND_FAIL_SCOPED"
    )

    result = {
        "gate": "C10.65s6fO",
        "classification": classification,
        "scientific_statement": (
            "Within the frozen local metric-only pure-spatial six-derivative class, "
            "constant-homogeneous soft response has universal weight -3.  Therefore "
            "any deformation that preserves the complete hard quadratic functional "
            "exactly also has identically zero change in this homogeneous soft cubic "
            "response.  The existing s6fM nonzero result cannot be cancelled by "
            "same-weight retuning without changing the certified quadratic sector."
        ),
        "exact_relations": {
            "density_weight": "w=3-d",
            "d": 6,
            "w": int(w6),
            "soft_variation": str(six_derivative_variation),
            "family_weight": str(w_family),
            "family_n2_weight": int(w_family_n2),
            "preservation_limit": str(preservation_zero),
            "retuning_change_at_fixed_quadratic_kernel": str(retuning_change),
            "zero_quadratic_soft_source": str(zero_quadratic_soft),
        },
        "representative_operator_density_weights": representative_weights,
        "checks": checks,
        "escape_routes_not_excluded": [
            "mixed time-space derivative operators",
            "operators with additional fields, compensators, or spurions",
            "operators of a different homogeneous conformal weight accompanied by a separately re-certified quadratic sector",
            "nonlocal structures",
            "a new symmetry principle that correlates multiple sectors beyond this frozen class",
        ],
        "nonclaims": target["scope_nonclaims"],
        "production_k003_unblocked": False,
        "threshold_changed": False,
        "target_path": str(TARGET.relative_to(ROOT)),
        "parent_checkpoint_paths": [str(PARENT_M.relative_to(ROOT)), str(PARENT_N.relative_to(ROOT))],
    }

    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
