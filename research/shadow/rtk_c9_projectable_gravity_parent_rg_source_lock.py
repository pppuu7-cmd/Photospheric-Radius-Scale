#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "research/theory_targets/RTK_C9_PROJECTABLE_GRAVITY_PARENT_RG_SOURCE_LOCK_TARGET_v1.json"
RESULT = ROOT / "research/theory_results/RTK_C9_PROJECTABLE_GRAVITY_PARENT_RG_SOURCE_LOCK_RESULT_v1.json"
CHECKPOINT = ROOT / "research/checkpoints/RTK_C9_PROJECTABLE_GRAVITY_PARENT_RG_SOURCE_LOCK_2026-08-28.md"

target = json.loads(TARGET.read_text())
required_arxiv = {s.get("arxiv") for s in target["required_sources"]}
checks = {
    "target_schema_exact": target.get("schema") == "RTK_C9_PROJECTABLE_GRAVITY_PARENT_RG_SOURCE_LOCK_TARGET_v1",
    "renormalizability_source_present": "1512.02250" in required_arxiv,
    "full_beta_source_present": "2110.14688" in required_arxiv,
    "af_flow_source_present": "2310.07841" in required_arxiv,
    "parent_not_promoted_to_HMT": bool(target["frozen_checks"].get("do_not_identify_plain_projectable_parent_with_HMT_U1_completion")),
    "matter_beta_not_claimed": bool(target["frozen_checks"].get("do_not_claim_matter_interface_beta_functions")),
    "full_C9_not_claimed": bool(target["frozen_checks"].get("do_not_claim_full_C9_closed")),
    "soft_s_blocked": bool(target["frozen_checks"].get("do_not_unblock_soft_s")),
    "k003_blocked": bool(target["frozen_checks"].get("do_not_unblock_k003_production")),
    "threshold_unchanged": target["frozen_checks"].get("threshold_changed") is False,
}
passed = all(checks.values())
classification = target["pass_classification"] if passed else target["failure_classification"]
result = {
    "schema": "RTK_C9_PROJECTABLE_GRAVITY_PARENT_RG_SOURCE_LOCK_RESULT_v1",
    "status": "PASS_SCOPED" if passed else "FAIL_SCOPED",
    "classification": classification,
    "checks": checks,
    "source_locked_literature": {
        "perturbative_renormalizability": "Barvinsky et al., arXiv:1512.02250",
        "full_3p1_marginal_beta_functions": "Barvinsky, Kurov, Sibiryakov, arXiv:2110.14688 / PRD 105 044009",
        "asymptotic_freedom_flow": "Barvinsky, Kurov, Sibiryakov, arXiv:2310.07841 / PRD 108 L121503"
    },
    "decision": {
        "pure_projectable_gravity_parent_has_quantitative_RG_control": passed,
        "HMT_U1_matter_completion_quantitative_RG_control_proven": False,
        "full_C9_closed": False,
        "unresolved_HMT_matter_interface_still_blocks_unique_same_action_full_loop": True,
        "soft_s_retest_allowed": False,
        "production_k003_unblocked": False
    },
    "interpretation": "Independent literature supplies genuine quantitative one-loop/RG control for the ordinary projectable Horava gravity parent. This narrows the remaining C9 obstruction: it is not absence of any projectable-gravity renormalization framework, but the unresolved extension to the specific HMT local-U(1)+matter RTK completion and its unfixed physical-matter interface.",
    "nonclaims": target["nonclaims"],
    "threshold_changed": False
}
RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
CHECKPOINT.write_text(
    "# RTK C9 projectable gravity-parent RG source-lock\n\n"
    f"Classification: `{classification}`\n\n"
    "Independent literature establishes perturbative renormalizability of projectable Horava gravity, full 3+1-dimensional beta functions for marginal essential gravitational couplings, and asymptotically-free RG structure. This is a scoped gravity-parent result only. It is not promoted to the HMT local-U(1)+matter completion, does not define beta functions for the unresolved HMT physical-matter interface, and does not close full C9.\n\n"
    "Next scientific dependency: an independently motivated same-action microscopic specification of the HMT physical-matter interface (or a derivation showing how the projectable-gravity RG framework extends to that fixed interface) before a unique full RTK one-loop/RG calculation is authorized. Soft-s and k=0.03 production remain blocked.\n"
)
print(json.dumps(result, indent=2, sort_keys=True))
if not passed:
    raise SystemExit(1)
