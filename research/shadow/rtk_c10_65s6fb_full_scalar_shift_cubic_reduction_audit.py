#!/usr/bin/env python3
"""C10.65s6fB fixed-action completeness audit.

The frozen target permits a ZERO/NONZERO scientific PASS only after the scalar
shift is eliminated from one fully specified action.  This audit deliberately
fails closed if the repository does not specify enough of that action to make
the shift-exchange contribution unique.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "research/theory_targets/RTK_C10_65S6FB_FULL_SCALAR_SHIFT_CUBIC_REDUCTION_TARGET_v1.json"
S6E = ROOT / "research/theory_results/RTK_C10_65S6E_UV_MATCHING_SOFT_S_SOURCE_LOCK_RESULT_v1.json"
S6FA = ROOT / "research/theory_results/RTK_C10_65S6FA_LOCAL_ALPHA6_SOFT_S_OBSTRUCTION_RESULT_v1.json"
OUT = ROOT / "research/theory_results/RTK_C10_65S6FB_FULL_SCALAR_SHIFT_CUBIC_REDUCTION_RESULT_v1.json"
ARCHIVE = "13acfdbc16d2f3117f1299b8552bcf7b1f996bd1"
BIBLE = "research/methods/RTK_FORMULA_BIBLE.md"


def load(p: Path):
    return json.loads(p.read_text())


def git_show(ref: str, path: str) -> str:
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT, text=True)


def main() -> int:
    target = load(TARGET)
    s6e = load(S6E)
    s6fa = load(S6FA)
    bible = git_show(ARCHIVE, BIBLE)

    checks = {
        "target_frozen": target.get("status") == "FROZEN_BEFORE_IMPLEMENTATION",
        "s6e_parent_pass": s6e.get("classification") == target["parents"]["s6e"],
        "s6fa_parent_pass": s6fa.get("classification") == target["parents"]["s6fA"],
        "archived_bible_source_locked": "RTK Formula Bible" in bible,
        "final_covariant_action_explicitly_not_fixed": (
            "The final covariant completion is not yet fixed" in bible
            and "Status: RED for the final carrier" in bible
        ),
        "k003_production_remains_blocked": target["frozen_scope"]["production_rule"].startswith("k=0.03"),
        "threshold_changed": False,
    }

    # A unique shift reduction needs the complete shift-dependent action, not
    # merely the intrinsic-curvature carrier and a local alpha6 state-function
    # condition.  In ADM language the equation is delta S / delta N_i = 0;
    # its quadratic kernel and cubic source depend on every shift-dependent
    # kinetic/mixed operator in S.  The frozen target does not enumerate those
    # operators/coefficient functions, while the canonical recovery source
    # explicitly says the final covariant carrier/action is not fixed.
    required_action_data = {
        "complete_shift_dependent_ADM_Lagrangian": False,
        "all_extrinsic_curvature_coefficients_and_state_dependence": False,
        "all_mixed_derivative_shift_couplings": False,
        "full_nonlinear_alpha6_state_function_not_just_local_slope_condition": False,
    }

    # Constructive underdetermination witness.  A projectable finite-k action
    # can be modified by a symmetry-allowed shift-dependent kinetic operator
    # without changing the stated intrinsic-curvature carrier itself.  Such a
    # term changes the N_i Hessian/source and therefore the exchange term after
    # integrating N_i out.  Unless its coefficient is fixed by the source
    # action, K_shift and J_shift are not unique.
    witness = {
        "operator": "DeltaS_mu = mu * integral N sqrt(gamma) (K_ij K^ij - K^2/3)",
        "reason": "contains the scalar shift through K_ij and changes delta^2 S/dN_i dN_j and cubic shift sources at finite k",
        "carrier_unchanged": "the explicitly stated alpha6(X) D_i R3 D^i R3 intrinsic-curvature carrier is unchanged by adding DeltaS_mu",
        "consequence": "without a source-locked value/rule for mu (or an explicit prohibition from the full action), the reduced shift-exchange cubic vertex is not uniquely determined by the frozen s6fB inputs",
    }

    complete = all(required_action_data.values())
    if not all(v for k, v in checks.items() if k != "threshold_changed"):
        classification = "C10_65S6FB_PREFLIGHT_SOURCE_INCONSISTENCY_FAIL_SCOPED"
        decision = "PARENT_OR_SOURCE_LOCK_FAILURE"
    elif not complete:
        classification = "C10_65S6FB_FULL_SCALAR_SHIFT_CUBIC_REDUCTION_BLOCKED_INCOMPLETE_FIXED_ACTION_SCOPED"
        decision = "DO_NOT_CLASSIFY_ZERO_OR_NONZERO_UNTIL_FULL_SHIFT_DEPENDENT_ACTION_IS_SOURCE_LOCKED"
    else:
        # Unreachable under current source state; retained to make fail-closed
        # semantics explicit rather than silently preferring either answer.
        classification = "C10_65S6FB_IMPLEMENTATION_REQUIRED_AFTER_COMPLETE_ACTION_SOURCE_LOCK"
        decision = "PROCEED_TO_EXACT_SYMBOLIC_REDUCTION"

    result = {
        "schema": "RTK_C10_65S6FB_FULL_SCALAR_SHIFT_CUBIC_REDUCTION_RESULT_v1",
        "gate": "C10.65s6fB",
        "target": str(TARGET.relative_to(ROOT)),
        "classification": classification,
        "decision": decision,
        "checks": checks,
        "required_action_data": required_action_data,
        "underdetermination_witness": witness,
        "bare_carrier_parent": {
            "K3_s": "-96 k^6",
            "source": "C10.65s6e",
        },
        "alpha6_state_function_parent": {
            "decision": s6fa.get("decision"),
            "source": "C10.65s6fA",
        },
        "shift_reduction": {
            "quadratic_kernel": "UNDEFINED_FROM_CURRENT_FIXED_INPUTS",
            "cubic_source": "UNDEFINED_FROM_CURRENT_FIXED_INPUTS",
            "exchange_contribution": "UNDEFINED_FROM_CURRENT_FIXED_INPUTS",
            "total_reduced_vertex": "NOT_CLASSIFIED",
            "exact_cancellation_residual": "NOT_DEFINED",
        },
        "interpretation": (
            "The frozen s6fB ZERO/NONZERO alternatives cannot yet be evaluated without inventing missing action data. "
            "The repository's canonical archived Formula Bible explicitly states that the final covariant completion is not fixed. "
            "Because scalar-shift elimination depends on all shift-dependent kinetic/mixed operators, the exchange contribution is underdetermined by the carrier and local alpha6 information alone. "
            "This is a scoped scientific blocker, not evidence for or against cancellation."
        ),
        "next_gate": (
            "C10.65s6fC fixed-action closure: source-lock one complete nonlinear projectable scalar action, including every shift-dependent ADM operator and the full alpha6(X) rule, while preserving already certified IR/linear constraints; only then rerun the unchanged s6fB reduction target."
        ),
        "non_claims": [
            "not an exact-zero result",
            "not an exact-nonzero result",
            "not a no-go for n=2 after a fully specified constraint reduction",
            "not radiative-naturalness closure",
            "not permission for k=0.03 production",
        ],
        "threshold_changed": False,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(classification, decision)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
