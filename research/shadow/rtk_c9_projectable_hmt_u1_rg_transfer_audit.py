#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "research/theory_targets/RTK_C9_PROJECTABLE_HMT_U1_RG_TRANSFER_AUDIT_TARGET_v1.json"
RESULT = ROOT / "research/theory_results/RTK_C9_PROJECTABLE_HMT_U1_RG_TRANSFER_AUDIT_RESULT_v1.json"
CHECKPOINT = ROOT / "research/checkpoints/RTK_C9_PROJECTABLE_HMT_U1_RG_TRANSFER_AUDIT_2026-08-28.md"

target = json.loads(TARGET.read_text())
sources = {s["id"]: s for s in target["required_sources"]}
checks = {
    "target_schema_exact": target.get("schema") == "RTK_C9_PROJECTABLE_HMT_U1_RG_TRANSFER_AUDIT_TARGET_v1",
    "parent_beta_source_present": sources.get("BarvinskyKurovSibiryakov_BetaFunctions_2022", {}).get("arxiv") == "2110.14688",
    "parent_rgflow_source_present": sources.get("BarvinskyKurovSibiryakov_RGFlow_2025", {}).get("doi") == "10.1103/PhysRevD.111.024030",
    "u1_hamiltonian_source_present": sources.get("MukohyamaNambaSaitouWatanabe_U1_Hamiltonian_2015", {}).get("arxiv") == "1504.07357",
    "additional_U1_fields_recognized": bool(target["frozen_checks"].get("HMT_U1_has_additional_A_and_nu_field_content")),
    "no_Hessian_ghost_equivalence_assumed": bool(target["frozen_checks"].get("do_not_infer_identical_gauge_fixed_Hessian_or_ghost_sector")),
    "no_parent_beta_transfer_assumed": bool(target["frozen_checks"].get("do_not_transfer_parent_beta_functions_without_explicit_U1_quantization")),
    "full_C9_not_claimed": bool(target["frozen_checks"].get("do_not_claim_full_C9_closed")),
    "soft_s_blocked": bool(target["frozen_checks"].get("do_not_unblock_soft_s")),
    "k003_blocked": bool(target["frozen_checks"].get("do_not_unblock_k003_production")),
    "threshold_unchanged": target["frozen_checks"].get("threshold_changed") is False,
}
passed = all(checks.values())
classification = target["pass_classification"] if passed else target["failure_classification"]

result = {
    "schema": "RTK_C9_PROJECTABLE_HMT_U1_RG_TRANSFER_AUDIT_RESULT_v1",
    "status": "PASS_SCOPED" if passed else "FAIL_SCOPED",
    "classification": classification,
    "checks": checks,
    "source_locked_distinction": {
        "ordinary_projectable_parent": {
            "quantitative_one_loop_beta_functions": True,
            "quantitative_RG_flow": True,
            "source": "Barvinsky-Kurov-Sibiryakov, PRD 105 044009 (2022); PRD 111 024030 (2025)"
        },
        "HMT_local_U1_extension": {
            "additional_fields": ["A", "nu"],
            "classical_constraint_structure_source_locked": True,
            "explicit_quantitative_one_loop_beta_functions_in_audited_sources": False,
            "explicit_transfer_theorem_from_parent_beta_functions_in_audited_sources": False,
            "source": "Mukohyama-Namba-Saitou-Watanabe, arXiv:1504.07357 / PRD 92 024005 (2015)"
        }
    },
    "decision": {
        "ordinary_projectable_parent_RG_control_survives": True,
        "HMT_U1_quantitative_RG_transfer_source_locked": False,
        "reason": "Adding the local U(1) constrained sector changes field/gauge content. The audited parent beta-function calculations cannot be promoted to the HMT A,nu theory without an explicit gauge-fixed one-loop derivation or an equivalence theorem for the Hessian, constraints and ghosts.",
        "full_C9_closed": False,
        "soft_s_retest_allowed": False,
        "production_k003_unblocked": False
    },
    "next_gate": "C9 projectable HMT U1 quantum-evaluability preflight: source-lock the complete fixed projectable HMT gravitational action and a BRST/gauge-fixing/ghost prescription sufficient to define its one-loop Hessian before any beta-function calculation; matter-interface beta functions remain separately blocked until that interface is fixed.",
    "nonclaims": target["nonclaims"],
    "threshold_changed": False
}
RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
CHECKPOINT.write_text(
    "# RTK C9 projectable HMT U(1) RG-transfer audit\n\n"
    f"Classification: `{classification}`\n\n"
    "The ordinary 3+1-dimensional projectable Horava gravity parent has source-locked quantitative one-loop beta functions and RG flow. The HMT local-U(1) extension has additional constrained fields A and nu and a different gauge/constraint structure. In the audited sources there is no explicit theorem showing that the parent's gauge-fixed Hessian, ghost determinant and beta functions transfer unchanged to that U(1)-extended theory. Therefore parent RG control remains a scoped parent result and cannot be promoted to full HMT+matter C9.\n\n"
    "Next scientific dependency: freeze a complete projectable HMT gravitational action plus a quantum gauge-fixing/BRST/ghost prescription sufficient to define the one-loop Hessian. Only after that source lock is it meaningful to test whether the known projectable-parent renormalization machinery extends to HMT. The unresolved physical-matter interface remains a separate blocker for full C9. Soft-s and k=0.03 production remain blocked.\n"
)
print(json.dumps(result, indent=2, sort_keys=True))
if not passed:
    raise SystemExit(1)
