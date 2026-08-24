#!/usr/bin/env python3
"""Exact baseline-A5 line profile from the historical LCDM center to the new cross-basin seed."""
from __future__ import annotations

from pathlib import Path
import copy, hashlib, json, math, os, subprocess, sys, time

sys.path.insert(0, str(Path.cwd()))
sys.argv = ["a5_lcdm_old_to_new_basin_line_profile", "planck_data"]
import inference_core as L
import numpy as np

ROOT = Path("..")
TARGET = json.loads((ROOT / "research/robustness/A5_LCDM_OLD_TO_NEW_BASIN_LINE_PROFILE_TARGET_v1.json").read_text())
STATE = json.loads((ROOT / "research/state/current.json").read_text())
assert TARGET["classification"] == "A5_LCDM_OLD_TO_NEW_BASIN_LINE_PROFILE_TARGET_V1_FROZEN"
assert TARGET["status"] == "FROZEN_BEFORE_ANY_LINE_PROFILE_SCORE"
assert TARGET["objective"] == STATE["objective"]["name"] == "matched-ultra-linstep2+dense-BOSS"
assert TARGET["production_mapping"] == "eff"

OLD = copy.deepcopy(TARGET["historical_center"])
NEW = copy.deepcopy(TARGET["new_cross_basin_seed"])
TGRID = [float(x) for x in TARGET["t_grid"]]
TOL = float(TARGET["endpoint_replay_abs_tolerance"])
OUT = ROOT / "output" / "a5_lcdm_old_to_new_basin_line_profile"
OUT.mkdir(parents=True, exist_ok=True)
POINTS = OUT / "points.jsonl"
FAILURES = OUT / "failures.jsonl"
SUMMARY = OUT / "summary.json"


def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def git_head(path):
    try:
        return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


SPARSE = "0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0"
DENSE = STATE["objective"]["dense_z_pk"]
ULTRA = {k: str(v) for k, v in STATE["objective"]["ultra"].items()}
ORIG = L.make_ini


def make_ini(model, p, tag):
    path = ORIG(model, p, tag)
    text = Path(path).read_text()
    if "z_pk = " + SPARSE in text:
        text = text.replace("z_pk = " + SPARSE, "z_pk = " + DENSE, 1)
    elif "z_pk = " + DENSE not in text:
        raise RuntimeError("could not establish frozen dense A5 objective")
    text += "\n# A5 LCDM old-to-new exact line profile\n"
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
        try: q.unlink()
        except OSError: pass
    for q in (Path(f"profile_{tag}.ini"), Path(f"profile_{tag}.log")):
        try: q.unlink()
        except OSError: pass


def params_at(t):
    p = {}
    for k in OLD:
        if k == "lam":
            p[k] = 0.0
        else:
            p[k] = float(OLD[k]) + float(t) * (float(NEW[k]) - float(OLD[k]))
    return p


def evaluate(t):
    p = params_at(t)
    last = None
    for attempt in (1, 2, 3):
        L.CACHE.clear()
        try:
            r = L.evaluate("LCDM", p)
        except Exception as exc:
            r = {"ok": False, "exception": repr(exc)}
        if r.get("ok"):
            row = {
                "t": float(t), "attempt": attempt, "params": p,
                "score_eff": float(r["score"]), "score_k01": float(r["score_k01"]),
                "components": {k: r.get(k) for k in ("logL_planck", "chi2_SN", "chi2_BOSS_eff", "chi2_BOSS_k01", "rd")},
            }
            if not math.isfinite(row["score_eff"]):
                raise RuntimeError("nonfinite exact line-profile score")
            append(POINTS, row); cleanup(r.get("tag"))
            print("A5_LCDM_BASIN_LINE_POINT", json.dumps(row, sort_keys=True), flush=True)
            return row
        last = r
        append(FAILURES, {"t": float(t), "attempt": attempt, "params": p, "result": r})
        cleanup(r.get("tag") if isinstance(r, dict) else None)
        if attempt < 3: time.sleep(2 * attempt)
    raise RuntimeError(f"line-profile evaluation failed at t={t}: {last}")


rows = [evaluate(t) for t in TGRID]
by_t = {round(float(r["t"]), 12): r for r in rows}
old_row = by_t[0.0]
new_row = by_t[1.0]
old_expected = float(TARGET["expected_endpoint_scores"]["t_0"])
new_expected = float(TARGET["expected_endpoint_scores"]["t_1"])
old_err = abs(old_row["score_eff"] - old_expected)
new_err = abs(new_row["score_eff"] - new_expected)
if old_err > TOL or new_err > TOL:
    raise RuntimeError(f"endpoint replay mismatch old={old_err} new={new_err} tol={TOL}")

S0 = float(old_row["score_eff"])
for r in rows:
    r["delta_S_vs_old"] = float(r["score_eff"]) - S0
interior = [r for r in rows if 0.0 < r["t"] < 1.0]
near = [r for r in rows if 0.0 < r["t"] <= 0.05]
barrier_row = max(interior, key=lambda r: r["score_eff"])
barrier_height = float(barrier_row["score_eff"]) - S0
first_below = next((r for r in sorted(rows, key=lambda r: r["t"]) if r["t"] > 0 and r["score_eff"] < S0), None)
best = min(rows, key=lambda r: r["score_eff"])
near_best_improvement = S0 - min(float(r["score_eff"]) for r in near)
if near_best_improvement > 0.005:
    classification = "A5_LCDM_LINE_PROFILE_HISTORICAL_LOCAL_INTERPRETATION_AUDIT_REQUIRED"
elif barrier_height > 0:
    classification = "A5_LCDM_LINE_PROFILE_STRAIGHT_PATH_BARRIER_OBSERVED"
else:
    classification = "A5_LCDM_LINE_PROFILE_NO_LARGE_NEAR_CENTER_DESCENT_LOWER_DISTANT_BASIN"

summary = {
    "status": "PASS",
    "classification": classification,
    "objective": TARGET["objective"],
    "production_mapping": "eff",
    "target_fingerprint": canonical_hash(TARGET),
    "endpoint_replay_abs_error": {"t_0": old_err, "t_1": new_err},
    "rows": rows,
    "near_center_max_exact_improvement": near_best_improvement,
    "barrier_height_above_historical": barrier_height,
    "barrier_t": float(barrier_row["t"]),
    "first_sample_below_historical_t": None if first_below is None else float(first_below["t"]),
    "best_sample_t": float(best["t"]),
    "best_sample_score": float(best["score_eff"]),
    "provenance": {
        "research_source_commit": git_head(ROOT),
        "class_upstream_commit": git_head(Path(".")),
        "pantheon_commit": git_head(Path("pantheon")),
        "numpy_version": np.__version__,
    },
    "warning": TARGET["guard"],
}
SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
print("A5_LCDM_OLD_TO_NEW_BASIN_LINE_PROFILE_COMPLETE", json.dumps(summary, sort_keys=True), flush=True)
