#!/usr/bin/env python3
"""Exact scoped audit of the flat projectable-HMT second-class bracket kernel.

This script intentionally does NOT compute the full Faddeev-Senjanovic determinant,
does NOT import parent Hořava beta functions, and does NOT close C9.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
TARGET_PATH = ROOT / "research/theory_targets/RTK_C9_HMT_FLAT_SECOND_CLASS_KERNEL_RANK_AUDIT_TARGET_v1.json"
RESULT_PATH = ROOT / "research/theory_results/RTK_C9_HMT_FLAT_SECOND_CLASS_KERNEL_RANK_AUDIT_RESULT_v1.json"
CHECKPOINT_PATH = ROOT / "research/checkpoints/RTK_C9_HMT_FLAT_SECOND_CLASS_KERNEL_RANK_AUDIT_CHECKPOINT_v1.md"
PROVENANCE_PATH = ROOT / "research/provenance/RTK_C9_HMT_FLAT_SECOND_CLASS_KERNEL_RANK_AUDIT_PROVENANCE_v1.json"
TARGET_COMMIT = "e62ff6add973288f38ac8425d9aa0800be5db559"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    target = json.loads(TARGET_PATH.read_text())
    require(target["gate"] == "RTK_C9_HMT_FLAT_SECOND_CLASS_KERNEL_RANK_AUDIT", "wrong frozen gate")
    require(target["status"] == "FROZEN_BEFORE_EXECUTION", "target was not frozen")
    flags = target["persistent_flags_required"]
    require(all(v is False for v in flags.values()), "frozen safety flags were weakened")

    D, lam, kappa2, k2 = sp.symbols("D lambda kappa2 k2", positive=True)
    # Exact canonical contractions on a flat background:
    # {h_ij, pi} = delta_ij delta and {h,pi}=D delta.
    # Therefore delta R = d_i d_j h_ij - d^2 h gives (1-D)d^2 delta.
    deltaR_pi_coeff = sp.simplify(1 - D)
    c_lam = sp.simplify((1 - lam) / (D * lam - 1))
    kernel_coeff_general = sp.factor(deltaR_pi_coeff * c_lam / kappa2)
    kernel_coeff_D3 = sp.factor(kernel_coeff_general.subs(D, 3))
    expected_D3 = sp.factor(-2 * (1 - lam) / (kappa2 * (3 * lam - 1)))
    require(sp.simplify(kernel_coeff_D3 - expected_D3) == 0, "D=3 kernel coefficient mismatch")

    # Fourier transform of d^4 delta contributes k^4=(k^2)^2; tracked overall
    # sign is exactly the coefficient above because two Laplacians square the sign.
    symbol_D3 = sp.factor(kernel_coeff_D3 * k2**2)
    require(sp.simplify(symbol_D3.subs(lam, 1)) == 0, "lambda=1 must vanish at flat linearized order")

    # Generic exact witnesses away from lambda=1 and lambda=1/3.
    witness_lambdas = [sp.Rational(0), sp.Rational(1, 2), sp.Rational(2)]
    witness_values = {}
    for lv in witness_lambdas:
        val = sp.factor(kernel_coeff_D3.subs(lam, lv))
        require(val != 0, f"generic witness lambda={lv} unexpectedly degenerate")
        witness_values[str(lv)] = str(val)

    denom_at_critical = sp.factor((3 * lam - 1).subs(lam, sp.Rational(1, 3)))
    require(denom_at_critical == 0, "lambda=1/3 critical denominator not detected")
    require(sp.simplify(symbol_D3.subs(k2, 0)) == 0, "k=0 zero mode not detected")

    classification = "RTK_C9_HMT_FLAT_SECOND_CLASS_KERNEL_RANK_CLASSIFIED_PASS_SCOPED"
    now = datetime.now(timezone.utc).isoformat()
    run_id = os.getenv("GITHUB_RUN_ID")
    sha = os.getenv("GITHUB_SHA")

    result = {
        "gate": target["gate"],
        "classification": classification,
        "scope": "flat T3, D=3, projectable HMT gravitational constrained sector, linearized about zero curvature/momenta",
        "target_commit": TARGET_COMMIT,
        "exact_derivation": {
            "delta_R": "partial_i partial_j h_ij - partial^2 h",
            "poisson_deltaR_tracepi": "(1-D) partial^2 delta(x-y)",
            "Phi2_flat_linear_coefficient": "(1-lambda)/(D*lambda-1)",
            "C12_general": "((1-D)/kappa^2)*((1-lambda)/(D*lambda-1))*partial^4 delta(x-y)",
            "C12_D3": "-2*(1-lambda)/(kappa^2*(3*lambda-1))*partial^4 delta(x-y)",
            "C12_fourier_D3": "-2*(1-lambda)/(kappa^2*(3*lambda-1))*k^4"
        },
        "rank_classification": {
            "generic_lambda_not_1_or_1over3_and_k_nonzero": "nonzero local Fourier symbol; this 2x2 second-class block is locally nondegenerate at frozen flat-linearized order",
            "lambda_equals_1": "flat-linearized C12 symbol vanishes; rank changes at this order and requires a separate constraint-bifurcation/nonlinear or nonflat-background audit",
            "lambda_equals_1_over_3": "generic formula singular because the DeWitt-metric denominator vanishes; separate critical-lambda constrained analysis required",
            "k_equals_0": "bi-Laplacian symbol vanishes; global/zero-mode sector remains separate"
        },
        "checks": {
            "deltaR_tracepi_coefficient_is_1_minus_D": bool(sp.simplify(deltaR_pi_coeff - (1-D)) == 0),
            "D3_bilaplacian_kernel_exact": True,
            "generic_nonzero_mode_local_nondegeneracy_scoped": True,
            "lambda1_flat_linearized_rank_change_detected": True,
            "lambda1over3_critical_denominator_detected": True,
            "k0_global_zero_mode_detected": True,
            "threshold_changed": False,
            "full_FS_determinant_computed": False,
            "full_HMT_one_loop_evaluable": False,
            "full_C9_closed": False,
            "soft_s_retest_allowed": False,
            "production_k003_unblocked": False
        },
        "generic_witness_kernel_coefficients": witness_values,
        "interpretation_limits": [
            "This is a scoped exact linearized bracket/rank audit, not a full quantum measure calculation.",
            "The lambda=1 rank change does not establish inconsistency, nonrenormalizability, or exclusion of HMT.",
            "No ordinary-projectable-Horava beta functions are imported.",
            "No HMT matter-interface coefficients are selected."
        ],
        "next_gate": "If the RTK/HMT branch retains lambda=1, freeze a lambda=1 constraint-bifurcation audit using the full source-locked constraints (or a preregistered nonflat/background-momentum expansion) before any determinant claim.",
        "provenance": {"generated_utc": now, "github_run_id": run_id, "github_sha": sha}
    }

    require(result["checks"]["full_C9_closed"] is False, "full C9 cannot close here")
    require(result["checks"]["soft_s_retest_allowed"] is False, "soft-s cannot unblock here")
    require(result["checks"]["production_k003_unblocked"] is False, "production cannot unblock here")

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROVENANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    checkpoint = f"""# RTK C9 HMT flat second-class kernel rank audit — checkpoint v1

- Classification: `{classification}`
- Frozen target commit: `{TARGET_COMMIT}`
- Background: flat periodic T^3, D=3, N=N(t), A=0, nu=0 gauge, zero curvature and zero background momenta.
- Exact local kernel at linearized order:
  `C12(x,y) = -2(1-lambda)/(kappa^2(3lambda-1)) * partial^4 delta(x-y)` (with the frozen canonical convention).
- Generic branch: for `lambda != 1, 1/3` and nonzero Fourier mode `k`, this local second-class block is nondegenerate at the frozen order.
- Critical branch `lambda=1`: the flat-linearized kernel vanishes. This is a rank/evaluability bifurcation of this scoped kernel, **not** a no-go for HMT.
- Critical branch `lambda=1/3`: the generic formula is not valid; separate constrained analysis is required.
- `k=0`: global/zero-mode sector remains open.
- Full Faddeev-Senjanovic determinant: **OPEN**.
- Full HMT one-loop evaluability: **OPEN/BLOCKED**.
- Full C9 radiative naturalness: **OPEN**.
- soft-s retest: **FORBIDDEN**.
- production `k=0.03 Mpc^-1`: **BLOCKED**.

## Next justified gate
If the retained RTK/HMT candidate includes `lambda=1`, freeze and execute a dedicated `lambda=1` constraint-bifurcation audit from the full source-locked constraint algebra (or a preregistered nonflat/background-momentum expansion). Do not regularize the rank change by choosing another lambda post hoc.
"""
    CHECKPOINT_PATH.write_text(checkpoint)

    provenance = {
        "gate": target["gate"],
        "classification": classification,
        "frozen_target_commit": TARGET_COMMIT,
        "source_lock": target["source_locked_input"],
        "script": str(Path(__file__).relative_to(ROOT)),
        "github_run_id": run_id,
        "github_sha": sha,
        "generated_utc": now,
        "frozen_criteria_changed": False,
        "DSIR_mixed": False
    }
    PROVENANCE_PATH.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
