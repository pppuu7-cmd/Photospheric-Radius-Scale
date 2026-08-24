#!/usr/bin/env python3
"""Exact baseline-A5 LCDM rays along the frozen soft negative base-Hessian mode.

This gate is frozen after the independent base-scale Hessian and before any ray
score is inspected.  It evaluates the unchanged matched-ultra+dense-BOSS
objective only; no standalone Planck lensing term is added.
"""
from __future__ import annotations

from pathlib import Path
import copy, hashlib, json, math, os, subprocess, sys, time
import numpy as np

sys.path.insert(0, str(Path.cwd()))
sys.argv = ["a5_lcdm_b9_seed_base_eigenmode_rays", "planck_data"]
import inference_core as L

ROOT = Path("..")
TARGET = json.loads((ROOT / "research/robustness/A5_LCDM_B9_SEED_BASE_EIGENMODE_RAYS_TARGET_v1.json").read_text())
PARENT = json.loads((ROOT / TARGET["parent_result"]).read_text())
STATE = json.loads((ROOT / "research/state/current.json").read_text())

assert TARGET["classification"] == "A5_LCDM_B9_SEED_BASE_EIGENMODE_RAYS_TARGET_V1_FROZEN"
assert TARGET["objective"] == STATE["objective"]["name"] == "matched-ultra-linstep2+dense-BOSS"
assert TARGET["production_mapping"] == "eff"
assert PARENT["classification"] == "A5_LCDM_B9_SEED_STATIONARITY_HESSIAN_COMPLETE"
assert PARENT["stencil_scale"] == 1.0
assert PARENT["eff"]["best_improvement"] <= TARGET["recenter_tolerance_S"]
assert PARENT["eff"]["positive_definite"] is False
assert len(TARGET["eigenmodes"]) == 1

CENTER = copy.deepcopy(TARGET["center"])
AXES = list(TARGET["axes"])
STEPS = {k: float(v) for k, v in TARGET["steps"].items()}
MODE = TARGET["eigenmodes"][0]
V = np.asarray(MODE["eigenvector_y"], dtype=float)
if abs(float(V @ V) - 1.0) > 1e-10:
    raise RuntimeError("frozen eigenvector is not unit normalized")
if float(MODE["eigenvalue_y"]) >= 0:
    raise RuntimeError("frozen ray mode is not negative")
AMPS = [float(x) for x in TARGET["ray_amplitudes"]]
TOL = float(TARGET["recenter_tolerance_S"])
REPLAY_TOL = float(TARGET["center_replay_abs_tolerance"])

OUT = ROOT / "output" / "a5_lcdm_b9_seed_base_eigenmode_rays"
OUT.mkdir(parents=True, exist_ok=True)
POINTS = OUT / "points.jsonl"
FAILURES = OUT / "failures.jsonl"
SUMMARY = OUT / "summary.json"
PROVFILE = OUT / "provenance.json"


def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def git_head(path):
    try:
        return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


PROV = {
    "target_fingerprint": canonical_hash(TARGET),
    "parent_result_fingerprint": canonical_hash(PARENT),
    "research_source_commit": git_head(ROOT),
    "class_upstream_commit": git_head(Path(".")),
    "pantheon_commit": git_head(Path("pantheon")),
    "numpy_version": np.__version__,
}
PROVFILE.write_text(json.dumps(PROV, indent=2, sort_keys=True) + "\n")

SPARSE = "0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0"
DENSE = STATE["objective"]["dense_z_pk"]
ULTRA = {k: str(v) for k, v in STATE["objective"]["ultra"].items()}
ORIG_MAKE_INI = L.make_ini


def make_ini(model, p, tag):
    path = ORIG_MAKE_INI(model, p, tag)
    text = Path(path).read_text()
    if "z_pk = " + SPARSE in text:
        text = text.replace("z_pk = " + SPARSE, "z_pk = " + DENSE, 1)
    elif "z_pk = " + DENSE not in text:
        raise RuntimeError("could not establish frozen dense A5 objective")
    text += "\n# A5 LCDM B9-seed exact eigenmode rays: frozen production precision\n"
    text += "".join(f"{k} = {v}\n" for k, v in ULTRA.items())
    Path(path).write_text(text)
    return path


L.make_ini = make_ini


def append(path, row):
    with path.open("a") as f:
        f.write(json.dumps(row, sort_keys=True, default=str) + "\n")
        f.flush()


def cleanup(tag):
    if not tag:
        return
    for q in L.OUT.glob(tag + "_*"):
        try:
            q.unlink()
        except OSError:
            pass
    for q in (Path(f"profile_{tag}.ini"), Path(f"profile_{tag}.log")):
        try:
            q.unlink()
        except OSError:
            pass


def params_from_y(y):
    y = np.asarray(y, dtype=float)
    p = copy.deepcopy(CENTER)
    for yi, axis in zip(y, AXES):
        p[axis] = float(CENTER[axis]) + float(yi) * STEPS[axis]
    p["lam"] = 0.0
    return p


def evaluate(y, label):
    y = np.asarray(y, dtype=float)
    p = params_from_y(y)
    last = None
    for attempt in (1, 2, 3):
        L.CACHE.clear()
        try:
            r = L.evaluate("LCDM", p)
        except Exception as exc:
            r = {"ok": False, "exception": repr(exc)}
        if r.get("ok"):
            row = {
                "label": label,
                "attempt": attempt,
                "y": y.tolist(),
                "params": p,
                "score_eff": float(r["score"]),
                "score_k01": float(r["score_k01"]),
                "components": {k: r.get(k) for k in ("logL_planck", "chi2_SN", "chi2_BOSS_eff", "chi2_BOSS_k01", "rd")},
            }
            if not math.isfinite(row["score_eff"]):
                raise RuntimeError("nonfinite exact ray score")
            append(POINTS, row)
            cleanup(r.get("tag"))
            print("A5_LCDM_B9_SEED_EIGENMODE_RAY_POINT", json.dumps(row, sort_keys=True), flush=True)
            return row
        last = r
        append(FAILURES, {"label": label, "attempt": attempt, "y": y.tolist(), "params": p, "result": r})
        cleanup(r.get("tag") if isinstance(r, dict) else None)
        if attempt < 3:
            time.sleep(2 * attempt)
    raise RuntimeError(f"exact ray evaluation failed after retries: {label}: {last}")


center = evaluate(np.zeros(len(AXES)), "center")
center_error = abs(float(center["score_eff"]) - float(TARGET["parent_center_S_eff"]))
if center_error > REPLAY_TOL:
    raise RuntimeError(f"center replay mismatch {center_error} > {REPLAY_TOL}")

rows = []
for amp in AMPS:
    row = evaluate(amp * V, f"mode0_amp_{amp:+g}")
    row["amplitude"] = amp
    row["improvement_from_center_eff"] = float(center["score_eff"]) - float(row["score_eff"])
    rows.append(row)

all_rows = [center] + rows
best = min(all_rows, key=lambda r: float(r["score_eff"]))
best_improvement = float(center["score_eff"]) - float(best["score_eff"])
classification = (
    "A5_LCDM_B9_SEED_BASE_EIGENMODE_RECENTER_REQUIRED"
    if best_improvement > TOL
    else "A5_LCDM_B9_SEED_BASE_EIGENMODE_RAYS_NO_DESCENT_GT_0P005"
)
summary = {
    "status": "PASS",
    "classification": classification,
    "objective": TARGET["objective"],
    "production_mapping": "eff",
    "center": CENTER,
    "S_center_eff": float(center["score_eff"]),
    "center_replay_abs_error": center_error,
    "mode_index": int(MODE["mode_index"]),
    "mode_eigenvalue_y": float(MODE["eigenvalue_y"]),
    "mode_eigenvector_y": V.tolist(),
    "ray_amplitudes": AMPS,
    "ray_results": rows,
    "best_label": best["label"],
    "best_params": best["params"],
    "best_exact_S_eff": float(best["score_eff"]),
    "max_exact_improvement_eff": best_improvement,
    "recenter_tolerance_S": TOL,
    "provenance": PROV,
    "warning": "Exact A5 local eigenmode-ray diagnostic only; not a global-minimum or model-selection claim.",
}
SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
print("A5_LCDM_B9_SEED_BASE_EIGENMODE_RAYS_COMPLETE", json.dumps(summary, sort_keys=True), flush=True)
