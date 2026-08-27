#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path

ARCHIVE="13acfdbc16d2f3117f1299b8552bcf7b1f996bd1"
FILES={
 "c8":"research/methods/RTK_FORMULA_BIBLE_C8_DEGENERATE_AUXILIARY_APPENDIX.md",
 "c9nat":"research/RTK_C9_U1_TECHNICAL_NATURALNESS_GATE_2026-08-22.md",
 "c9uv":"research/methods/RTK_FORMULA_BIBLE_C9_UV_O4_FRONTIER_2026-08-23T2155Z.md",
}

def show(path):
    return subprocess.check_output(["git","show",f"{ARCHIVE}:{path}"], text=True)

src={k:show(v) for k,v in FILES.items()}
c8=src["c8"]
c9nat=src["c9nat"]
c9uv=src["c9uv"]

checks={
 "c8_quadratic_scoped_not_final": "The statements here are quadratic and scoped. They do not constitute a final covariant completion." in c8,
 "c8_future_full_flrw_embedding": "embed the rank-one kinetic pair into the full FLRW lapse/shift scalar constraint block" in c8,
 "c8_future_source_from_same_action": "derive the source direction from the same action" in c8,
 "c8_pointwise_matching_only": "can therefore be matched **pointwise**" in c8,
 "c8_does_not_derive_epoch_source_alignment": "does not yet derive the required momentum/epoch dependence or source alignment from one RTK gravitational action" in c8,
 "c9nat_requires_same_completed_action": "same completed action" in c9nat,
 "c9nat_does_not_claim_final_completion": "not technically natural" in c9nat,
 "c9uv_not_globally_green": "C9 is **not globally GREEN**" in c9uv,
 "c9uv_open_nonlinear_constraint_reduction": "nonlinear lapse/shift reduction with the n=2 curvature carrier" in c9uv,
 "c9uv_no_selected_uv_scale": "No numerical `M_c` or `M_U` is selected by these theorems." in c9uv,
 "parent_result_present": Path("research/theory_results/RTK_C10_65S6FV_RANK_ONE_EMBEDDING_IDENTIFIABILITY_RESULT_v1.json").exists(),
 "target_present": Path("research/theory_targets/RTK_C10_65S6FW_PRE_SOFTS_ARCHIVE_PRINCIPLE_AUDIT_TARGET_v1.json").exists(),
}

parent=json.loads(Path("research/theory_results/RTK_C10_65S6FV_RANK_ONE_EMBEDDING_IDENTIFIABILITY_RESULT_v1.json").read_text())
checks["parent_is_exact_s6fv_pass"] = parent.get("classification")=="C10_65S6FV_RANK_ONE_FULL_EMBEDDING_NON_IDENTIFIABLE_PASS_SCOPED"

# The archive itself explicitly says the missing source alignment/full embedding remained future work.
# Therefore no pre-soft-s unique selector exists in the audited archive set.
all_required=all(checks.values())
classification=("C10_65S6FW_NO_INDEPENDENT_PRE_SOFTS_EMBEDDING_PRINCIPLE_FOUND_PASS_SCOPED" if all_required
                else "C10_65S6FW_ARCHIVE_AUDIT_INCOMPLETE_BLOCKED_SCOPED")
result={
 "schema":"RTK_C10_65S6FW_PRE_SOFTS_ARCHIVE_PRINCIPLE_AUDIT_RESULT_v1",
 "gate":"C10.65s6fW",
 "classification":classification,
 "archived_source_commit":ARCHIVE,
 "checks":checks,
 "finding":("The source-locked pre-soft-s C8/C9 archive contains no independently motivated rule that uniquely fixes the rank-one field map, potential/algebraic matrix and action-derived source direction. C8 explicitly leaves full FLRW lapse/shift embedding and source derivation from the same action as future work; C9 likewise remains an open same-completed-action/naturalness program." if all_required else "The frozen archive audit could not verify every required source-lock statement; fail closed."),
 "s6ft_embedding_ready":False,
 "soft_s_retest_allowed":False,
 "production_k003_unblocked":False,
 "next_gate":"C10.65s6fX: freeze an independent action-selection requirement outside the failed soft-s observable. Do not choose potential/source data from the s6fM obstruction. If no independently motivated candidate action exists, retain the s6fT blocker rather than inventing one.",
 "threshold_changed":False,
 "provenance":{"workflow":"rtk-c10-65s6fw-pre-softs-archive-principle-audit.yml","threshold_changed":False}
}
out=Path("research/theory_results/RTK_C10_65S6FW_PRE_SOFTS_ARCHIVE_PRINCIPLE_AUDIT_RESULT_v1.json")
out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps(result,indent=2,sort_keys=True))
sys.exit(0 if all_required else 2)
