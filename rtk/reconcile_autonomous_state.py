#!/usr/bin/env python3
"""Conservative reconciliation layer for the autonomous RTK research state.

This does not make scientific decisions. It repairs control-plane metadata that
can otherwise strand a valid replacement Actions run behind an older failed
run_id, normalizes frozen local raw-fit scores to the best exact stencil score,
and removes stale certification labels after an already-recorded recenter.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/state/current.json"
REPO = os.environ.get("GITHUB_REPOSITORY", "pppuu7-cmd/Photospheric-Radius-Scale")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")


def gh(endpoint):
    env = os.environ.copy()
    if TOKEN:
        env["GH_TOKEN"] = TOKEN
    p = subprocess.run(["gh", "api", endpoint], text=True, capture_output=True, env=env)
    if p.returncode:
        raise RuntimeError(p.stderr.strip())
    return json.loads(p.stdout)


def latest(workflow):
    d = gh(f"repos/{REPO}/actions/workflows/{workflow}/runs?per_page=1")
    rs = d.get("workflow_runs", [])
    return rs[0] if rs else None


def adopt_newer_replacement(state, model, key, changes):
    slot = state.get(model, {}).get(key)
    if not isinstance(slot, dict) or not slot.get("workflow"):
        return
    if slot.get("status") != "completed" or slot.get("conclusion") in (None, "success"):
        return
    old_id = int(slot.get("run_id") or 0)
    r = latest(slot["workflow"])
    if not r:
        return
    new_id = int(r.get("id") or 0)
    if new_id <= old_id or r.get("head_branch") != "main":
        return
    if r.get("status") == "completed" and r.get("conclusion") not in (None, "success"):
        return
    slot["adopted_replacement_of"] = old_id
    slot["run_id"] = new_id
    slot["status"] = r.get("status")
    slot["conclusion"] = r.get("conclusion")
    slot["html_url"] = r.get("html_url")
    slot.pop("parsed", None)
    state[model].pop(f"{key}_compute_failure", None)
    changes.append({"adopted_replacement": f"{model}.{key}", "old_run_id": old_id, "new_run_id": new_id})


def normalize_frozen_minimum(state, model, changes):
    m = state.get(model, {})
    if m.get("certification") != "local_dense_accepted":
        return
    tol = float(state["objective"]["recenter_tolerance_S"])
    result = m.get("hessian_result") or {}
    if result.get("objective") != state["objective"]["name"]:
        return
    if model == "rtk":
        eff = result.get("eff", {})
        imp = float(eff.get("best_improvement", 1e99))
        best = eff.get("best_exact_S")
        pars = eff.get("best_params")
    else:
        imp = float(result.get("best_improvement", 1e99))
        best = result.get("best_exact_S")
        pars = result.get("best_params")
    if best is None or imp > tol:
        return
    best = float(best)
    old = m.get("accepted_score_eff")
    if old is None or abs(float(old) - best) > 1e-12:
        m["accepted_score_eff"] = best
        if isinstance(pars, dict):
            m["accepted_score_params"] = dict(pars)
        m["accepted_score_semantics"] = "best_exact_stencil_within_recenter_tolerance"
        changes.append({"normalized_frozen_score": model, "old": old, "new": best, "improvement": imp})


def repair_pending_recenter_labels(state, changes):
    """Remove only labels contradicted by an already-committed recenter state."""
    rtk=state.get('rtk',{})
    pending=(
        rtk.get('certification')=='needs_recenter_from_exact_mixed_mode_ray'
        and rtk.get('accepted_score_eff') is None
        and isinstance(rtk.get('axis_run'),dict)
    )
    if not pending:
        return
    want='pending_stationarity_after_mixed_mode_recenter'
    old=rtk.get('raw_candidate_certification')
    if old!=want:
        rtk['raw_candidate_certification']=want
        changes.append({'repaired_raw_candidate_certification':{'old':old,'new':want}})
    if state.get('comparison',{}).get('dense_raw_delta_S') is not None:
        oldcmp=dict(state['comparison'])
        state['comparison']={'status':'pending_matched_stationarity','dense_raw_delta_S':None}
        changes.append({'cleared_stale_comparison_after_recenter':oldcmp})


def main():
    state = json.loads(STATE.read_text())
    changes = []
    for model, key in (("rtk", "axis_run"), ("rtk", "hessian_run"), ("lcdm", "hessian_run")):
        adopt_newer_replacement(state, model, key, changes)
    normalize_frozen_minimum(state, "lcdm", changes)
    normalize_frozen_minimum(state, "rtk", changes)
    repair_pending_recenter_labels(state, changes)
    if changes:
        state.setdefault("audit", {})["last_reconciliation"] = changes
        STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    print("RTK_STATE_RECONCILE", json.dumps(changes, sort_keys=True))


if __name__ == "__main__":
    main()
