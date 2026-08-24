#!/usr/bin/env python3
"""Fresh-tree four-point audit of the historical A5 pair versus B9-derived cross-seeds.

No optimization is performed here.  The purpose is to test whether the B9
stationarity artifacts exposed a genuinely better LCDM basin of the *same*
matched-ultra-linstep2+dense-BOSS baseline objective.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
sys.argv = ["a5_b9_cross_basin_replay", "planck_data"]
import inference_core as L
import numpy as np
import scipy

ROOT = Path("..")
TARGET = json.loads((ROOT / "research/robustness/A5_B9_CROSS_BASIN_REPLAY_TARGET_v1.json").read_text())
STATE = json.loads((ROOT / "research/state/current.json").read_text())
OUT = Path("output/a5_b9_cross_basin_replay")
OUT.mkdir(parents=True, exist_ok=True)
POINTS = OUT / "points.jsonl"
FAILURES = OUT / "failures.jsonl"
SUMMARY = OUT / "summary.json"

TOL = float(TARGET["score_tolerance_abs"])
RECENTER_TOL = float(TARGET["recenter_tolerance_S"])


def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def git_head(path):
    try:
        return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def append_jsonl(path, row):
    with path.open("a") as f:
        f.write(json.dumps(row, sort_keys=True, default=str) + "\n")
        f.flush()


assert TARGET["status"] == "PREREGISTERED_BEFORE_INDEPENDENT_CROSS_BASIN_REPLAY"
assert TARGET["objective"] == STATE["objective"]["name"] == "matched-ultra-linstep2+dense-BOSS"
assert TARGET["production_mapping"] == "eff"
assert canonical_hash(STATE["objective"]) == TARGET["objective_fingerprint"]

SPARSE = "0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0"
DENSE = STATE["objective"]["dense_z_pk"]
ULTRA = {k: str(v) for k, v in STATE["objective"]["ultra"].items()}
orig = L.make_ini


def make_ini(model, p, tag):
    path = orig(model, p, tag)
    text = Path(path).read_text()
    if "z_pk = " + SPARSE in text:
        text = text.replace("z_pk = " + SPARSE, "z_pk = " + DENSE, 1)
    elif "z_pk = " + DENSE not in text:
        raise RuntimeError("could not establish frozen dense z_pk objective")
    with Path(path).open("w") as f:
        f.write(text)
        f.write("\n# A5/B9 cross-basin fresh-tree audit\n")
        for k, v in ULTRA.items():
            f.write(f"{k} = {v}\n")
    return path


L.make_ini = make_ini


def cleanup(tag):
    if not tag:
        return
    for p in L.OUT.glob(tag + "_*"):
        try:
            p.unlink()
        except OSError:
            pass
    for p in (Path(f"profile_{tag}.ini"), Path(f"profile_{tag}.log")):
        try:
            p.unlink()
        except OSError:
            pass


def is_timeout(r):
    return "CLASS_TIMEOUT" in str(r.get("error", r.get("reason", ""))) if isinstance(r, dict) else False


def evaluate_exact(label, model, params):
    last = None
    # Preserve fail-closed B9 semantics: one identical retry only for CLASS timeout.
    for attempt in (1, 2):
        L.CACHE.clear()
        try:
            r = L.evaluate(model, dict(params))
        except Exception as exc:
            r = {"ok": False, "exception": repr(exc)}
        if r.get("ok"):
            row = {
                "label": label,
                "model": model,
                "attempt": attempt,
                "params": dict(params),
                "score_eff": float(r["score"]),
                "score_k01": float(r["score_k01"]),
                "components": {k: r.get(k) for k in ("logL_planck", "chi2_SN", "chi2_BOSS_eff", "chi2_BOSS_k01", "rd")},
            }
            append_jsonl(POINTS, row)
            cleanup(r.get("tag"))
            print("A5_B9_CROSS_BASIN_POINT", json.dumps(row, sort_keys=True), flush=True)
            return row
        last = r
        append_jsonl(FAILURES, {"label": label, "model": model, "attempt": attempt, "params": dict(params), "result": r})
        cleanup(r.get("tag") if isinstance(r, dict) else None)
        if attempt == 1 and is_timeout(r):
            time.sleep(2)
            continue
        break
    raise RuntimeError(f"{label} exact replay failed: {last}")


rows = {}
for model in ("LCDM", "RTK"):
    h = TARGET["historical_A5"][model]
    rows[f"historical_{model}"] = evaluate_exact(f"historical_{model}", model, h["params"])
    b = TARGET["B9_cross_seeds"][model]
    rows[f"B9seed_{model}"] = evaluate_exact(f"B9seed_{model}", model, b["params"])

expected = {
    "historical_LCDM": float(TARGET["historical_A5"]["LCDM"]["expected_score_eff"]),
    "historical_RTK": float(TARGET["historical_A5"]["RTK"]["expected_score_eff"]),
    "B9seed_LCDM": float(TARGET["B9_cross_seeds"]["LCDM"]["expected_base_score_eff"]),
    "B9seed_RTK": float(TARGET["B9_cross_seeds"]["RTK"]["expected_base_score_eff"]),
}
actual = {k: float(v["score_eff"]) for k, v in rows.items()}
errors = {k: actual[k] - expected[k] for k in expected}
replay_pass = all(abs(v) <= TOL for v in errors.values())

lcdm_improvement = actual["historical_LCDM"] - actual["B9seed_LCDM"]
rtk_change = actual["B9seed_RTK"] - actual["historical_RTK"]
historical_delta = actual["historical_RTK"] - actual["historical_LCDM"]
cross_seed_delta = actual["B9seed_RTK"] - actual["B9seed_LCDM"]
delta_change = cross_seed_delta - historical_delta

classification = (
    "A5_B9_CROSS_BASIN_REPLAY_PASS_NEW_LCDM_SEED_CONFIRMED"
    if replay_pass and lcdm_improvement > RECENTER_TOL
    else "A5_B9_CROSS_BASIN_REPLAY_PASS_NO_MATERIAL_LCDM_IMPROVEMENT"
    if replay_pass
    else "A5_B9_CROSS_BASIN_REPLAY_MISMATCH"
)

summary = {
    "classification": classification,
    "status": "PASS" if replay_pass else "FAIL",
    "objective": STATE["objective"],
    "objective_fingerprint": canonical_hash(STATE["objective"]),
    "production_mapping": "eff",
    "score_tolerance_abs": TOL,
    "recenter_tolerance_S": RECENTER_TOL,
    "expected_scores": expected,
    "actual_scores": actual,
    "replay_errors": errors,
    "historical_delta_RTK_minus_LCDM": historical_delta,
    "cross_seed_delta_RTK_minus_LCDM": cross_seed_delta,
    "delta_change": delta_change,
    "LCDM_improvement_historical_minus_B9seed": lcdm_improvement,
    "RTK_change_B9seed_minus_historical": rtk_change,
    "points": rows,
    "provenance": {
        "research_source_commit": git_head(".."),
        "class_upstream_commit": git_head("."),
        "pantheon_commit": git_head("pantheon"),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "class_upstream_sha_expected": os.environ.get("RTK_CLASS_UPSTREAM_SHA"),
        "pantheon_sha_expected": os.environ.get("RTK_PANTHEON_SHA"),
        "planck_sha256_expected": os.environ.get("RTK_PLANCK_SHA256"),
        "cache_key_version": os.environ.get("RTK_CACHE_KEY_VERSION"),
    },
    "decision_if_confirmed": TARGET["decision_if_LCDM_improvement_reproduces"],
    "warning": TARGET["interpretation_guard"],
}
SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n")
print("A5_B9_CROSS_BASIN_REPLAY", json.dumps(summary, sort_keys=True, allow_nan=False), flush=True)
if not replay_pass:
    raise SystemExit("A5_B9_CROSS_BASIN_REPLAY_MISMATCH " + json.dumps(errors, sort_keys=True))
print(classification, flush=True)
