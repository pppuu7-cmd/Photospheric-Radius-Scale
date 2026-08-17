#!/usr/bin/env python3
"""Fail closed if a completed autonomous artifact does not match current state.

The scientific orchestrator must never parse a successful artifact merely
because its workflow/run ID looks plausible. Before parsing, require the
artifact-declared objective and center to match the current accepted state.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/state/current.json"
REPO = os.environ.get("GITHUB_REPOSITORY", "pppuu7-cmd/Photospheric-Radius-Scale")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")


def run(cmd, check=True):
    env = os.environ.copy()
    if TOKEN:
        env["GH_TOKEN"] = TOKEN
    p = subprocess.run(cmd, text=True, capture_output=True, env=env)
    if check and p.returncode:
        raise RuntimeError(p.stderr.strip())
    return p


def download_summary(run_id, artifact):
    td = Path(tempfile.mkdtemp(prefix=f"rtk-identity-{run_id}-"))
    try:
        p = run(["gh", "run", "download", str(run_id), "-R", REPO,
                 "-n", artifact, "-D", str(td)], check=False)
        if p.returncode:
            raise RuntimeError(f"completed-success run {run_id} has no downloadable artifact {artifact}: {p.stderr.strip()}")
        hits = list(td.rglob("summary.json"))
        if len(hits) != 1:
            raise RuntimeError(f"run {run_id}: expected exactly one summary.json, found {len(hits)}")
        return json.loads(hits[0].read_text())
    finally:
        shutil.rmtree(td, ignore_errors=True)


def exact_center_equal(a, b):
    if not isinstance(a, dict) or not isinstance(b, dict):
        return False
    keys = ("lam", "h", "Ob", "Om", "As", "ns", "zre")
    try:
        return all(float(a[k]) == float(b[k]) for k in keys)
    except (KeyError, TypeError, ValueError):
        return False


def validate_slot(state, model, key):
    slot = state.get(model, {}).get(key)
    if not isinstance(slot, dict):
        return None
    if slot.get("status") != "completed" or slot.get("conclusion") != "success" or slot.get("parsed"):
        return None
    run_id = int(slot["run_id"])
    summary = download_summary(run_id, slot["artifact"])
    expected_objective = state["objective"]["name"]
    if summary.get("objective") != expected_objective:
        raise RuntimeError(
            f"artifact identity mismatch {model}.{key} run={run_id}: "
            f"objective={summary.get('objective')!r} expected={expected_objective!r}"
        )
    expected_center = state[model]["accepted_center"]
    if not exact_center_equal(summary.get("center"), expected_center):
        raise RuntimeError(
            f"artifact identity mismatch {model}.{key} run={run_id}: "
            f"summary center does not equal current accepted_center"
        )
    return {"slot": f"{model}.{key}", "run_id": run_id, "objective": expected_objective,
            "center_match": True}


def main():
    state = json.loads(STATE.read_text())
    checked = []
    for model, key in (("rtk", "axis_run"), ("rtk", "hessian_run"), ("lcdm", "hessian_run")):
        row = validate_slot(state, model, key)
        if row:
            checked.append(row)
    print("RTK_ARTIFACT_IDENTITY_PASS", json.dumps(checked, sort_keys=True))


if __name__ == "__main__":
    main()
