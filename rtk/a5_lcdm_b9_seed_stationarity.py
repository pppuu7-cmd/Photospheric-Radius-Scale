#!/usr/bin/env python3
"""Exact baseline-objective LCDM stationarity audit around the B9-v7 cross-basin seed.

Execution is conditional on the independent four-point cross-basin replay confirming
that the seed really evaluates to the preregistered lower A5 score.  The same source
supports scale 1.0 and 0.5; scale selection is explicit via environment and never
changes the frozen center silently.
"""
from __future__ import annotations

from pathlib import Path
import copy
import hashlib
import json
import math
import os
import subprocess
import sys
import time

import numpy as np

sys.path.insert(0, str(Path.cwd()))
sys.argv = ["a5_lcdm_b9_seed_stationarity", "planck_data"]
import inference_core as L

ROOT = Path("..")
TARGET = json.loads((ROOT / "research/robustness/A5_LCDM_B9_SEED_STATIONARITY_TARGET_v1.json").read_text())
STATE = json.loads((ROOT / "research/state/current.json").read_text())
PREREQ_PATH = ROOT / TARGET["prerequisite"]["result"]
if not PREREQ_PATH.is_file():
    raise RuntimeError("cross-basin replay prerequisite result is missing")
PREREQ = json.loads(PREREQ_PATH.read_text())
if PREREQ.get("classification") != TARGET["prerequisite"]["required_classification"]:
    raise RuntimeError(f"cross-basin prerequisite not confirmed: {PREREQ.get('classification')!r}")

SCALE = float(os.environ.get("RTK_A5_LCDM_STENCIL_SCALE", "1.0"))
if SCALE not in (1.0, 0.5, 0.25, 0.125):
    raise RuntimeError(f"unsupported A5 LCDM stencil scale {SCALE}")

assert TARGET["objective"] == STATE["objective"]["name"] == "matched-ultra-linstep2+dense-BOSS"
assert TARGET["production_mapping"] == "eff"


def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


if canonical_hash(STATE["objective"]) != TARGET["objective_fingerprint"]:
    raise RuntimeError("baseline objective fingerprint drift")

CENTER = copy.deepcopy(TARGET["center"])
AXES = list(TARGET["axes"])
STEPS = {k: float(TARGET["base_steps"][k]) * SCALE for k in AXES}
N = len(AXES)
TOL = float(TARGET["recenter_tolerance_S"])
PD_THRESH = float(TARGET["positive_definite_threshold"])
REPLAY_TOL = float(TARGET["center_replay_abs_tolerance"])

OUT = ROOT / "output" / "a5_lcdm_b9_seed_stationarity" / f"scale_{SCALE:g}"
OUT.mkdir(parents=True, exist_ok=True)
POINTS = OUT / "points.jsonl"
FAILURES = OUT / "failures.jsonl"
SUMMARY = OUT / "summary.json"
PROVFILE = OUT / "provenance.json"


def git_head(path):
    try:
        return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


PROV = {
    "model": "LCDM",
    "stencil_scale": SCALE,
    "target_fingerprint": canonical_hash(TARGET),
    "center_fingerprint": canonical_hash({"model": "LCDM", "center": CENTER, "objective": TARGET["objective"], "mapping": "eff"}),
    "cross_basin_result_fingerprint": canonical_hash(PREREQ),
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
        raise RuntimeError("could not establish dense objective")
    text += "\n# A5 LCDM B9-seed stationarity: frozen production precision\n"
    text += "".join(f"{k} = {v}\n" for k, v in ULTRA.items())
    Path(path).write_text(text)
    return path


L.make_ini = make_ini
E = {}


def key(y):
    return tuple(float(x).hex() for x in np.asarray(y, float))


def pars(y):
    y = np.asarray(y, float)
    p = copy.deepcopy(CENTER)
    for yi, axis in zip(y, AXES):
        p[axis] = float(CENTER[axis]) + float(yi) * STEPS[axis]
    p["lam"] = 0.0
    return p


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


def append(path, row):
    with path.open("a") as f:
        f.write(json.dumps(row, sort_keys=True, default=str) + "\n")
        f.flush()


def is_timeout(r):
    return "CLASS_TIMEOUT" in str(r.get("error", r.get("reason", ""))) if isinstance(r, dict) else False


def ev(y, label):
    y = np.asarray(y, float)
    k = key(y)
    if k in E:
        return E[k]
    p = pars(y)
    last = None
    for attempt in (1, 2):
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
                "logL_planck": r.get("logL_planck"),
                "chi2_SN": r.get("chi2_SN"),
                "chi2_BOSS_eff": r.get("chi2_BOSS_eff"),
                "chi2_BOSS_k01": r.get("chi2_BOSS_k01"),
                "rd": r.get("rd"),
            }
            if not all(math.isfinite(float(row[x])) for x in ("score_eff", "score_k01")):
                raise RuntimeError("nonfinite stationarity score")
            E[k] = row
            append(POINTS, row)
            cleanup(r.get("tag"))
            print("A5_LCDM_B9SEED_HESSIAN_POINT", SCALE, json.dumps(row, sort_keys=True), flush=True)
            return row
        last = r
        append(FAILURES, {"label": label, "attempt": attempt, "y": y.tolist(), "params": p, "result": r})
        cleanup(r.get("tag") if isinstance(r, dict) else None)
        if attempt == 1 and is_timeout(r):
            time.sleep(2)
            continue
        break
    raise RuntimeError(f"LCDM {label}: failed exact evaluation: {last}")


z = np.zeros(N)
ev(z, "center")
center_err = abs(float(E[key(z)]["score_eff"]) - float(TARGET["expected_center_S_eff"]))
if center_err > REPLAY_TOL:
    raise RuntimeError(f"cross-basin center replay drift {center_err} > {REPLAY_TOL}")

for i in range(N):
    for s in (-1.0, 1.0):
        y = np.zeros(N)
        y[i] = s
        ev(y, f"axis_{i}_{int(s):+d}")
for i in range(N):
    for j in range(i + 1, N):
        for a in (-1.0, 1.0):
            for b in (-1.0, 1.0):
                y = np.zeros(N)
                y[i] = a
                y[j] = b
                ev(y, f"cross_{i}_{j}_{int(a):+d}_{int(b):+d}")


def build(which):
    fld = "score_eff" if which == "eff" else "score_k01"
    S0 = float(E[key(np.zeros(N))][fld])
    g = np.zeros(N)
    H = np.zeros((N, N))
    for i in range(N):
        yp = np.zeros(N)
        ym = np.zeros(N)
        yp[i] = 1
        ym[i] = -1
        sp = float(E[key(yp)][fld])
        sm = float(E[key(ym)][fld])
        g[i] = (sp - sm) / 2.0
        H[i, i] = sp - 2.0 * S0 + sm
    for i in range(N):
        for j in range(i + 1, N):
            vals = []
            for a, b in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                y = np.zeros(N)
                y[i] = a
                y[j] = b
                vals.append(float(E[key(y)][fld]))
            H[i, j] = H[j, i] = (vals[0] - vals[1] - vals[2] + vals[3]) / 4.0
    eig, vec = np.linalg.eigh(H)
    for j in range(vec.shape[1]):
        q = int(np.argmax(np.abs(vec[:, j])))
        if vec[q, j] < 0:
            vec[:, j] *= -1
    delta = -np.linalg.pinv(H, rcond=1e-10) @ g
    rn = ev(np.clip(delta, -1.0, 1.0), f"newton_trust_{which}")
    return {
        "S_center": S0,
        "gradient_y": g.tolist(),
        "max_abs_gradient_y": float(np.max(np.abs(g))),
        "hessian_y": H.tolist(),
        "eigenvalues_y": eig.tolist(),
        "eigenvectors_y": vec.T.tolist(),
        "positive_definite": bool(np.all(eig > PD_THRESH)),
        "newton_delta": delta.tolist(),
        "S_newton": float(rn[fld]),
        "newton_params": rn["params"],
    }


def finalize(block, which):
    fld = "score_eff" if which == "eff" else "score_k01"
    best = min(E.values(), key=lambda r: float(r[fld]))
    S0 = float(block["S_center"])
    block.update({
        "best_exact_S": float(best[fld]),
        "best_improvement": float(S0 - float(best[fld])),
        "best_label": best["label"],
        "best_params": best["params"],
        "best_selection_scope": "all exact stencil points after both eff/k01 Newton candidates",
    })
    return block


EFF = build("eff")
K01 = build("k01")
EFF = finalize(EFF, "eff")
K01 = finalize(K01, "k01")

summary = {
    "classification": "A5_LCDM_B9_SEED_STATIONARITY_HESSIAN_COMPLETE",
    "model": "LCDM",
    "objective": TARGET["objective"],
    "production_mapping": "eff",
    "center": CENTER,
    "stencil_scale": SCALE,
    "base_steps": TARGET["base_steps"],
    "scaled_steps": STEPS,
    "points": len(E),
    "center_replay_abs_error": center_err,
    "eff": EFF,
    "k01": K01,
    "recenter_tolerance_S": TOL,
    "positive_definite_threshold": PD_THRESH,
    "provenance": PROV,
    "warning": TARGET["interpretation_guard"],
}
SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n")
print("A5_LCDM_B9_SEED_STATIONARITY_HESSIAN_COMPLETE", SCALE, json.dumps(summary, sort_keys=True, allow_nan=False), flush=True)
