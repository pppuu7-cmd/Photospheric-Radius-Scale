#!/usr/bin/env python3
"""Repository-synchronized RTK research orchestrator.

This is a deterministic scientific state machine. It does not pretend to be a
free-form LLM. It queries GitHub Actions, parses exact artifacts, applies the
predeclared gates in research/state/current.json, journals the decision, and
requests at most one new heavy workflow per iteration.
"""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/state/current.json"
LOCK = ROOT / "research/state/lock.json"
DISPATCH = ROOT / "research/state/dispatch_request.json"
ITER_DIR = ROOT / "research/iterations"
REPO = os.environ.get("GITHUB_REPOSITORY", "pppuu7-cmd/Photospheric-Radius-Scale")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
NOW = dt.datetime.now(dt.timezone.utc)
NOW_ISO = NOW.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(cmd, *, check=True):
    env = os.environ.copy()
    if TOKEN:
        env["GH_TOKEN"] = TOKEN
    p = subprocess.run(cmd, text=True, capture_output=True, env=env)
    if check and p.returncode != 0:
        raise RuntimeError(f"command failed {cmd}: {p.stderr.strip()}")
    return p


def gh_json(endpoint):
    p = run(["gh", "api", endpoint])
    return json.loads(p.stdout)


def get_run(run_id):
    return gh_json(f"repos/{REPO}/actions/runs/{int(run_id)}")


def latest_workflow_run(workflow_file):
    data = gh_json(f"repos/{REPO}/actions/workflows/{workflow_file}/runs?per_page=1")
    runs = data.get("workflow_runs", [])
    return runs[0] if runs else None


def download_artifact(run_id, artifact):
    td = Path(tempfile.mkdtemp(prefix=f"rtk-auto-{run_id}-"))
    p = run(["gh", "run", "download", str(run_id), "-R", REPO, "-n", artifact, "-D", str(td)], check=False)
    if p.returncode != 0:
        shutil.rmtree(td, ignore_errors=True)
        return None
    return td


def find_file(root, name):
    hits = list(Path(root).rglob(name))
    return hits[0] if hits else None


def load_summary(run_id, artifact, summary_name="summary.json"):
    td = download_artifact(run_id, artifact)
    if not td:
        return None, None
    f = find_file(td, summary_name)
    if not f:
        return None, td
    return json.loads(f.read_text()), td


def best_point_from_log(td, marker, score_key="score_eff"):
    if not td:
        return None
    best = None
    for f in Path(td).rglob("*.log"):
        for line in f.read_text(errors="replace").splitlines():
            if marker not in line:
                continue
            try:
                payload = line.split(marker, 1)[1].strip()
                row = json.loads(payload)
            except Exception:
                continue
            if score_key in row and (best is None or float(row[score_key]) < float(best[score_key])):
                best = row
    return best


def point_params(row):
    if not row:
        return None
    if isinstance(row.get("params"), dict):
        return dict(row["params"])
    keys = ("lam", "h", "Ob", "Om", "As", "ns", "zre")
    if all(k in row for k in keys):
        return {k: row[k] for k in keys}
    return None


def refresh_run(slot):
    if not slot:
        return slot
    if not slot.get("run_id") and slot.get("workflow"):
        r = latest_workflow_run(slot["workflow"])
        if r:
            slot["run_id"] = int(r["id"])
    if slot.get("run_id"):
        r = get_run(slot["run_id"])
        slot["status"] = r.get("status")
        slot["conclusion"] = r.get("conclusion")
        slot["html_url"] = r.get("html_url")
    return slot


def request_dispatch(state, workflow, reason, target):
    if DISPATCH.exists():
        return False
    req = {
        "created_at": NOW_ISO,
        "iteration": state["iteration"],
        "workflow": workflow,
        "ref": "main",
        "reason": reason,
        "target": target,
    }
    DISPATCH.write_text(json.dumps(req, indent=2, sort_keys=True) + "\n")
    state["dispatch"] = req
    return True


def record_iteration(state, actions, observations):
    ITER_DIR.mkdir(parents=True, exist_ok=True)
    stamp = NOW.strftime("%Y%m%dT%H%M%SZ")
    path = ITER_DIR / f"{state['iteration']:06d}_{stamp}.json"
    payload = {
        "schema_version": 1,
        "iteration": state["iteration"],
        "time": NOW_ISO,
        "stage": state.get("stage"),
        "observations": observations,
        "actions": actions,
        "next_dispatch": state.get("dispatch"),
        "comparison": state.get("comparison"),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return str(path.relative_to(ROOT))


def main():
    state = json.loads(STATE.read_text())
    tol = float(state["objective"]["recenter_tolerance_S"])
    state["iteration"] = int(state.get("iteration", 0)) + 1
    state["updated_at"] = NOW_ISO
    LOCK.write_text(json.dumps({
        "schema_version": 1,
        "holder": f"github-actions-iteration-{state['iteration']}",
        "acquired_at": NOW_ISO,
        "expires_at": (NOW + dt.timedelta(minutes=30)).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "note": "Human-readable mirror; workflow concurrency is authoritative."
    }, indent=2, sort_keys=True) + "\n")

    actions = []
    observations = []

    # Refresh every known run independently so RTK and LCDM can progress in parallel.
    state["rtk"]["axis_run"] = refresh_run(state["rtk"].get("axis_run"))
    state["rtk"]["hessian_run"] = refresh_run(state["rtk"].get("hessian_run"))
    state["lcdm"]["hessian_run"] = refresh_run(state["lcdm"].get("hessian_run"))

    # Parse RTK axis result once complete.
    ar = state["rtk"].get("axis_run")
    if ar and ar.get("status") == "completed" and ar.get("conclusion") == "success" and not ar.get("parsed"):
        summary, td = load_summary(ar["run_id"], ar["artifact"])
        if summary:
            state["rtk"]["axis_result"] = summary
            ar["parsed"] = True
            imp = float(summary.get("best_improvement_eff", 0.0))
            observations.append({"rtk_axis_run": ar["run_id"], "best_improvement_eff": imp, "gate": summary.get("gate")})
            if imp > tol:
                best = summary.get("best_eff")
                pars = point_params(best)
                if pars:
                    state["rtk"].setdefault("axis_history", []).append(summary)
                    state["rtk"]["accepted_center"] = pars
                    state["rtk"]["axis_result"] = None
                    state["rtk"]["axis_run"] = {
                        "run_id": None,
                        "workflow": "rtk-autonomous-dense-rtk-axis.yml",
                        "artifact": "rtk-autonomous-dense-rtk-axis",
                        "status": "requested"
                    }
                    state["stage"] = "rtk_axis_recenter_running"
                    if request_dispatch(state, "rtk-autonomous-dense-rtk-axis.yml", f"eff axis improvement {imp:.9g} > {tol}", "rtk_axis"):
                        actions.append("recenter_RTK_eff_and_dispatch_dynamic_axis")
                else:
                    state["stage"] = "rtk_axis_recenter_params_missing"
                    actions.append("halt_RTK_recenter_missing_best_params")
            elif state["rtk"].get("hessian_run") is None:
                state["rtk"]["hessian_run"] = {
                    "run_id": None,
                    "workflow": "rtk-autonomous-dense-rtk-stationarity.yml",
                    "artifact": "rtk-autonomous-dense-rtk-stationarity",
                    "status": "requested"
                }
                state["stage"] = "rtk_hessian_running"
                if request_dispatch(state, "rtk-autonomous-dense-rtk-stationarity.yml", f"RTK eff axis clear at tolerance {tol}", "rtk_hessian"):
                    actions.append("dispatch_RTK_dense_7D_hessian")
        if td:
            shutil.rmtree(td, ignore_errors=True)

    # Parse LCDM Hessian independently.
    lr = state["lcdm"].get("hessian_run")
    if lr and lr.get("status") == "completed" and lr.get("conclusion") == "success" and not lr.get("parsed"):
        summary, td = load_summary(lr["run_id"], lr["artifact"])
        if summary:
            best_log = best_point_from_log(td, "DENSE_LCDM_HESSIAN_POINT")
            summary["best_point_from_log"] = best_log
            state["lcdm"]["hessian_result"] = summary
            lr["parsed"] = True
            imp = float(summary.get("best_improvement", 0.0))
            observations.append({"lcdm_hessian_run": lr["run_id"], "best_improvement": imp, "positive_definite": summary.get("positive_definite")})
            if imp > tol:
                pars = point_params(best_log)
                if pars:
                    state["lcdm"].setdefault("hessian_history", []).append(summary)
                    state["lcdm"]["accepted_center"] = pars
                    state["lcdm"]["hessian_result"] = None
                    state["lcdm"]["hessian_run"] = {
                        "run_id": None,
                        "workflow": "rtk-autonomous-dense-lcdm-stationarity.yml",
                        "artifact": "rtk-autonomous-dense-lcdm-stationarity",
                        "status": "requested"
                    }
                    if request_dispatch(state, "rtk-autonomous-dense-lcdm-stationarity.yml", f"LCDM exact improvement {imp:.9g} > {tol}", "lcdm_hessian"):
                        actions.append("recenter_LCDM_and_redispatch_hessian")
                else:
                    state["lcdm"]["certification"] = "needs_recenter_but_params_missing"
                    actions.append("halt_LCDM_recenter_missing_best_params")
            else:
                state["lcdm"]["certification"] = "local_dense_accepted"
                best_s = float(summary.get("best_exact_S", summary["S_center"]))
                best_params = summary.get("best_params") or point_params(best_log) or dict(state["lcdm"]["accepted_center"])
                state["lcdm"]["accepted_score_eff"] = best_s
                state["lcdm"]["accepted_score_params"] = best_params
                state["lcdm"]["accepted_score_semantics"] = "best_exact_stencil_within_recenter_tolerance"
                actions.append("freeze_LCDM_local_dense_candidate_best_exact")
        if td:
            shutil.rmtree(td, ignore_errors=True)

    # Parse RTK Hessian once complete.
    hr = state["rtk"].get("hessian_run")
    if hr and hr.get("status") == "completed" and hr.get("conclusion") == "success" and not hr.get("parsed"):
        summary, td = load_summary(hr["run_id"], hr["artifact"])
        if summary:
            state["rtk"]["hessian_result"] = summary
            hr["parsed"] = True
            eff = summary.get("eff", {})
            imp = float(eff.get("best_improvement", 0.0))
            observations.append({"rtk_hessian_run": hr["run_id"], "best_improvement_eff": imp, "positive_definite": eff.get("positive_definite")})
            if imp > tol:
                pars = eff.get("best_params")
                if pars:
                    state["rtk"].setdefault("hessian_history", []).append(summary)
                    state["rtk"]["accepted_center"] = pars
                    state["rtk"]["hessian_result"] = None
                    state["rtk"]["hessian_run"] = None
                    state["rtk"]["axis_run"] = {
                        "run_id": None,
                        "workflow": "rtk-autonomous-dense-rtk-axis.yml",
                        "artifact": "rtk-autonomous-dense-rtk-axis",
                        "status": "requested"
                    }
                    state["stage"] = "rtk_axis_recenter_running"
                    if request_dispatch(state, "rtk-autonomous-dense-rtk-axis.yml", f"RTK Hessian exact improvement {imp:.9g} > {tol}", "rtk_axis"):
                        actions.append("recenter_RTK_from_hessian_and_dispatch_axis")
                else:
                    state["rtk"]["certification"] = "needs_recenter_but_best_params_missing"
                    actions.append("halt_RTK_hessian_recenter_missing_params")
            else:
                state["rtk"]["certification"] = "local_dense_accepted"
                best_s = float(eff.get("best_exact_S", eff["S_center"]))
                best_params = eff.get("best_params") or dict(state["rtk"]["accepted_center"])
                state["rtk"]["accepted_score_eff"] = best_s
                state["rtk"]["accepted_score_params"] = best_params
                state["rtk"]["accepted_score_semantics"] = "best_exact_stencil_within_recenter_tolerance"
                actions.append("freeze_RTK_local_dense_candidate_best_exact")
        if td:
            shutil.rmtree(td, ignore_errors=True)

    # Record explicit failures; do not silently treat compute failure as science.
    for model, key in (("rtk", "axis_run"), ("rtk", "hessian_run"), ("lcdm", "hessian_run")):
        slot = state[model].get(key)
        if slot and slot.get("status") == "completed" and slot.get("conclusion") not in (None, "success"):
            state[model][f"{key}_compute_failure"] = {"run_id": slot.get("run_id"), "conclusion": slot.get("conclusion")}
            observations.append({"compute_failure": f"{model}.{key}", "run_id": slot.get("run_id"), "conclusion": slot.get("conclusion")})

    # Matched raw comparison only after both local candidates are frozen.
    if state["rtk"].get("certification") == "local_dense_accepted" and state["lcdm"].get("certification") == "local_dense_accepted":
        sr = float(state["rtk"]["accepted_score_eff"])
        sl = float(state["lcdm"]["accepted_score_eff"])
        delta = sr - sl
        state["comparison"] = {
            "status": "matched_local_dense_raw_fit_ready",
            "mapping": "eff",
            "S_RTK": sr,
            "S_LCDM": sl,
            "dense_raw_delta_S": delta,
            "numerically_indistinguishable_at_0p005": abs(delta) <= tol,
            "warning": "Raw local objective comparison only; not AIC/BIC/Bayes evidence/significance."
        }
        state["stage"] = "matched_dense_ready"
        actions.append("compute_matched_dense_raw_delta_S")

    if not actions:
        actions.append("observe_and_wait_no_duplicate_heavy_dispatch")

    state["last_iteration"] = record_iteration(state, actions, observations)
    LOCK.write_text(json.dumps({
        "schema_version": 1,
        "holder": None,
        "acquired_at": None,
        "expires_at": None,
        "released_at": NOW_ISO,
        "note": "Human-readable mirror; workflow concurrency is authoritative."
    }, indent=2, sort_keys=True) + "\n")
    STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    print("RTK_AUTONOMOUS_ITERATION", json.dumps({
        "iteration": state["iteration"], "stage": state["stage"], "actions": actions,
        "observations": observations, "dispatch": state.get("dispatch")
    }, sort_keys=True))


if __name__ == "__main__":
    main()
