#!/usr/bin/env python3
"""Fail closed if a completed autonomous artifact does not match current state.

The scientific orchestrator must never parse a successful artifact merely
because its workflow/run ID looks plausible. Before parsing, require the
artifact-declared objective and center to match the current accepted state.
For RTK Hessian proof artifacts, additionally require the canonical objective /
center fingerprints and the measured upstream/runtime provenance locked by the
project. For multiscale proof-gate runs, also require the declared stencil scale.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/state/current.json"
REPRO = ROOT / "rtk/reproducibility_lock.json"
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


def canonical_hash(obj):
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


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


def validate_rtk_hessian_provenance(state, repro, key, run_id, summary):
    """Require the provenance fields emitted by the hardened RTK Hessian worker."""
    prov = summary.get("provenance")
    if not isinstance(prov, dict):
        raise RuntimeError(f"artifact provenance missing rtk.{key} run={run_id}")

    expected_obj_fp = canonical_hash(state["objective"])
    actual_obj_fp = summary.get("objective_fingerprint") or prov.get("objective_fingerprint")
    if actual_obj_fp != expected_obj_fp:
        raise RuntimeError(
            f"artifact provenance mismatch rtk.{key} run={run_id}: "
            f"objective_fingerprint={actual_obj_fp!r} expected={expected_obj_fp!r}"
        )

    expected_center_fp = canonical_hash({
        "model": "RTK",
        "center": state["rtk"]["accepted_center"],
        "objective": state["objective"]["name"],
        "mapping": state.get("production_mapping", "eff"),
    })
    actual_center_fp = summary.get("center_fingerprint") or prov.get("center_fingerprint")
    if actual_center_fp != expected_center_fp:
        raise RuntimeError(
            f"artifact provenance mismatch rtk.{key} run={run_id}: "
            f"center_fingerprint={actual_center_fp!r} expected={expected_center_fp!r}"
        )

    expected_class = repro["external_git"]["class_public"]["commit"]
    expected_pantheon = repro["external_git"]["pantheon"]["commit"]
    expected_numpy = repro["python_packages"]["numpy"]
    observed = {
        "class_upstream_commit": prov.get("class_upstream_commit"),
        "pantheon_commit": prov.get("pantheon_commit"),
        "numpy_version": prov.get("numpy_version"),
    }
    expected = {
        "class_upstream_commit": expected_class,
        "pantheon_commit": expected_pantheon,
        "numpy_version": expected_numpy,
    }
    bad = {k: {"actual": observed[k], "expected": expected[k]}
           for k in expected if observed[k] != expected[k]}
    if bad:
        raise RuntimeError(
            f"artifact locked provenance mismatch rtk.{key} run={run_id}: "
            + json.dumps(bad, sort_keys=True)
        )
    return {
        "objective_fingerprint_match": True,
        "center_fingerprint_match": True,
        "class_upstream_commit": expected_class,
        "pantheon_commit": expected_pantheon,
        "numpy_version": expected_numpy,
        "rtk_source_commit": prov.get("rtk_source_commit"),
    }


def validate_slot(state, repro, model, key):
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
    expected_scale = slot.get("expected_stencil_scale")
    if expected_scale is not None:
        actual = summary.get("stencil_scale")
        try:
            scale_match = float(actual) == float(expected_scale)
        except (TypeError, ValueError):
            scale_match = False
        if not scale_match:
            raise RuntimeError(
                f"artifact identity mismatch {model}.{key} run={run_id}: "
                f"stencil_scale={actual!r} expected={expected_scale!r}"
            )

    row = {"slot": f"{model}.{key}", "run_id": run_id,
           "objective": expected_objective, "center_match": True,
           "stencil_scale": summary.get("stencil_scale")}
    if model == "rtk" and key in ("hessian_run", "half_hessian_run", "quarter_hessian_run"):
        row["locked_provenance"] = validate_rtk_hessian_provenance(state, repro, key, run_id, summary)
    return row


def main():
    state = json.loads(STATE.read_text())
    repro = json.loads(REPRO.read_text())
    checked = []
    for model, key in (("rtk", "axis_run"), ("rtk", "hessian_run"),
                       ("rtk", "half_hessian_run"), ("rtk", "quarter_hessian_run"),
                       ("lcdm", "hessian_run")):
        row = validate_slot(state, repro, model, key)
        if row:
            checked.append(row)
    print("RTK_ARTIFACT_IDENTITY_PASS", json.dumps(checked, sort_keys=True))


if __name__ == "__main__":
    main()
