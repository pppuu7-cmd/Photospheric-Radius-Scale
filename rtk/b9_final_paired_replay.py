#!/usr/bin/env python3
"""Final exact paired B9 replay at the preregistered certified LCDM/RTK centers.

This worker is intentionally narrow: it evaluates exactly the two centers frozen in
research/robustness/B9_FINAL_PAIRED_REPLAY_TARGET_v1.json under one common fresh
CLASS/Pantheon/Planck environment.  It performs no optimization and no recentering.

Scientific PASS is allowed only when the prior RTK independent fresh-tree
certification has already been persisted as PASS and all frozen replay tolerances
are satisfied.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import math
import os
import subprocess
import sys
import time

import numpy as np

os.environ.setdefault("CLIPY_NOJAX", "1")
sys.argv = ["b9_final_paired_replay", "planck_data"]
import clipy
import inference_core as C

ROOT = Path("..")
TARGET = json.loads((ROOT / "research/robustness/B9_FINAL_PAIRED_REPLAY_TARGET_v1.json").read_text())
B9 = json.loads((ROOT / "research/robustness/B9_PAIRED_REOPTIMIZATION_TARGET_v1.json").read_text())
STATE = json.loads((ROOT / "research/state/current.json").read_text())
FRESH_RESULT_PATH = ROOT / "research/robustness/B9_RTK_FRESH_TREE_CERTIFICATION_RESULT_v1.json"

assert TARGET["status"] == "PREREGISTERED_BEFORE_RTK_FRESH_TREE_RESULT_IS_INSPECTED"
assert TARGET["objective"] == B9["objective"] == "matched-ultra-linstep2+dense-BOSS+PlanckR3-lensing-v1"
assert TARGET["production_mapping"] == B9["mapping"] == "eff"
assert B9["baseline_objective"] == STATE["objective"]["name"]
assert B9["baseline_objective_fingerprint"] == "754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666"
if not FRESH_RESULT_PATH.is_file():
    raise RuntimeError("missing persisted RTK fresh-tree certification precondition")
FRESH = json.loads(FRESH_RESULT_PATH.read_text())
if FRESH.get("classification") != "B9_RTK_INDEPENDENT_FRESH_TREE_CERTIFICATION_PASS":
    raise RuntimeError(f"RTK fresh-tree precondition is not PASS: {FRESH.get('classification')!r}")

OUT = ROOT / "output" / "b9_final_paired_replay"
OUT.mkdir(parents=True, exist_ok=True)
POINTS = OUT / "points.jsonl"
RESULT = OUT / "result.json"
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
    "b9_protocol_fingerprint": canonical_hash(B9),
    "research_source_commit": git_head(ROOT),
    "class_upstream_commit": git_head(Path(".")),
    "pantheon_commit": git_head(Path("pantheon")),
    "numpy_version": np.__version__,
    "python_version": sys.version.split()[0],
    "fresh_tree_precondition": FRESH,
}
PROVFILE.write_text(json.dumps(PROV, indent=2, sort_keys=True, allow_nan=False) + "\n")

# Exact frozen baseline objective, identical dense-z and ultra precision semantics.
ORIG_MAKE_INI = C.make_ini
DENSE = STATE["objective"]["dense_z_pk"]
ULTRA = {k: str(v) for k, v in STATE["objective"]["ultra"].items()}
SPARSE = "0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0"


def make_ini(model, p, tag):
    path = ORIG_MAKE_INI(model, p, tag)
    text = Path(path).read_text()
    if "z_pk = " + SPARSE in text:
        text = text.replace("z_pk = " + SPARSE, "z_pk = " + DENSE, 1)
    elif "z_pk = " + DENSE not in text:
        raise RuntimeError("could not establish dense B9 z_pk objective")
    text += "\n# B9 final paired replay: frozen production precision\n"
    text += "".join(f"{k} = {v}\n" for k, v in ULTRA.items())
    Path(path).write_text(text)
    return path


C.make_ini = make_ini

# Frozen standalone Planck R3 lensing adapter contract.
PLANCK = Path("planck_data")
LENS_PATH = PLANCK / B9["lensing_product"]
if not LENS_PATH.is_dir():
    raise RuntimeError(f"missing frozen B9 lensing product: {LENS_PATH}")
LENS = clipy.clik(str(LENS_PATH))
LMAX = [int(x) for x in LENS.get_lmax()]
if LMAX != B9["lensing_lmax"]:
    raise RuntimeError(f"B9 lmax contract drift: {LMAX}")
DEFAULT = np.asarray(LENS.default_par, dtype=float)
SPEC_NAMES = ["phiphi", "TT", "EE", "BB", "TE", "TB", "EB"]
CL_LEN = sum(x + 1 for x in LMAX if x >= 0)
EXTRA_NAMES = [str(x) for x in LENS.get_extra_parameter_names()]
if len(DEFAULT) != 10005 or CL_LEN != 10004 or CL_LEN + len(EXTRA_NAMES) != len(DEFAULT):
    raise RuntimeError((len(DEFAULT), CL_LEN, EXTRA_NAMES))


def scalar(x):
    a = np.asarray(x, dtype=float).reshape(-1)
    if a.size < 1 or not np.isfinite(a[0]):
        raise RuntimeError(f"nonfinite lensing likelihood result: {a}")
    return float(a[0])


if not math.isfinite(scalar(LENS(DEFAULT.copy()))):
    raise RuntimeError("B9 default-vector selfcheck failed")

UK2 = (2.7255e6) ** 2


def class_lensed_cls(path):
    path = Path(path)
    if not path.is_file():
        raise RuntimeError(f"missing CLASS lensed spectrum: {path}")
    lines = path.read_text().splitlines()
    header = "\n".join(lines[:12])
    for token in ("TT", "EE", "TE", "BB", "phiphi"):
        if token not in header:
            raise RuntimeError(f"{token} missing from CLASS lensed header")
    vals = {}
    for line in lines:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        a = s.split()
        ell = int(float(a[0]))
        if len(a) < 6:
            raise RuntimeError(f"too few CLASS lensed columns at ell {ell}")
        fac = ell * (ell + 1) / (2 * math.pi)
        if fac <= 0:
            continue
        dtt, dee, dte, dbb, dpp = map(float, a[1:6])
        vals[ell] = {
            "phiphi": dpp / fac,
            "TT": dtt / fac * UK2,
            "EE": dee / fac * UK2,
            "BB": dbb / fac * UK2,
            "TE": dte / fac * UK2,
            "TB": 0.0,
            "EB": 0.0,
        }
    required = max(x for x in LMAX if x >= 0)
    if not vals or max(vals) < required:
        raise RuntimeError(f"CLASS lensed spectrum insufficient: max ell={max(vals) if vals else None}")
    return vals


def lens_vector(cls):
    v = DEFAULT.copy()
    off = 0
    for spec, lm in enumerate(LMAX):
        if lm < 0:
            continue
        arr = np.zeros(lm + 1, dtype=float)
        name = SPEC_NAMES[spec]
        for ell in range(2, lm + 1):
            arr[ell] = cls[ell][name]
        if not np.all(np.isfinite(arr)):
            raise RuntimeError(f"nonfinite {name}")
        v[off : off + lm + 1] = arr
        off += lm + 1
    if off != CL_LEN:
        raise RuntimeError((off, CL_LEN))
    if not np.array_equal(v[CL_LEN:], DEFAULT[CL_LEN:]):
        raise RuntimeError("B9 nuisance/default tail changed")
    return v


def cleanup(tag):
    if not tag:
        return
    for q in C.OUT.glob(tag + "_*"):
        try:
            q.unlink()
        except OSError:
            pass
    for q in (Path(f"profile_{tag}.ini"), Path(f"profile_{tag}.log")):
        try:
            q.unlink()
        except OSError:
            pass


def append(row):
    with POINTS.open("a") as f:
        f.write(json.dumps(row, sort_keys=True, default=str) + "\n")
        f.flush()


def is_timeout(r):
    return "CLASS_TIMEOUT" in str(r.get("error", r.get("reason", ""))) if isinstance(r, dict) else False


def evaluate_exact(model, params):
    """Fail closed; allow exactly one identical retry only for CLASS timeout."""
    last = None
    for attempt in (1, 2):
        C.CACHE.clear()
        try:
            r = C.evaluate(model, params)
        except Exception as exc:
            r = {"ok": False, "exception": repr(exc)}
        if r.get("ok"):
            tag = r.get("tag")
            try:
                cls = class_lensed_cls(C.OUT / f"{tag}_cl_lensed.dat")
                logl = scalar(LENS(lens_vector(cls)))
                row = {
                    "model": model,
                    "attempt": attempt,
                    "params": params,
                    "S_base_eff": float(r["score"]),
                    "S_base_k01": float(r["score_k01"]),
                    "lensing_loglike": logl,
                    "lensing_minus2loglike": -2.0 * logl,
                    "S_B9_eff": float(r["score"]) - 2.0 * logl,
                    "S_B9_k01": float(r["score_k01"]) - 2.0 * logl,
                    "logL_planck": r.get("logL_planck"),
                    "chi2_SN": r.get("chi2_SN"),
                    "chi2_BOSS_eff": r.get("chi2_BOSS_eff"),
                    "chi2_BOSS_k01": r.get("chi2_BOSS_k01"),
                    "rd": r.get("rd"),
                }
                if not all(math.isfinite(float(row[x])) for x in ("S_B9_eff", "S_B9_k01", "lensing_loglike")):
                    raise RuntimeError("nonfinite B9 replay score")
                append(row)
                cleanup(tag)
                print("B9_FINAL_PAIRED_POINT", json.dumps(row, sort_keys=True), flush=True)
                return row
            except Exception:
                cleanup(tag)
                raise
        last = r
        cleanup(r.get("tag") if isinstance(r, dict) else None)
        if attempt == 1 and is_timeout(r):
            time.sleep(2)
            continue
        break
    raise RuntimeError(f"{model} exact replay failed: {last}")


lcdm = evaluate_exact("LCDM", dict(TARGET["lcdm"]["center"]))
rtk = evaluate_exact("RTK", dict(TARGET["rtk"]["center"]))

S_LCDM = float(lcdm["S_B9_eff"])
S_RTK = float(rtk["S_B9_eff"])
DELTA = S_RTK - S_LCDM
ERR_LCDM = abs(S_LCDM - float(TARGET["lcdm"]["expected_S_B9"]))
ERR_RTK = abs(S_RTK - float(TARGET["rtk"]["expected_S_B9"]))
ERR_DELTA = abs(DELTA - float(TARGET["expected_delta_S_RTK_minus_LCDM"]))
TOL_EACH = float(TARGET["replay_abs_tolerance_each"])
TOL_DELTA = float(TARGET["delta_replay_abs_tolerance"])

result = {
    "classification": "B9_FINAL_PAIRED_EXACT_REPLAY_PASS",
    "objective": TARGET["objective"],
    "production_mapping": TARGET["production_mapping"],
    "S_LCDM": S_LCDM,
    "S_RTK": S_RTK,
    "delta_S_RTK_minus_LCDM": DELTA,
    "lcdm_replay_abs_error": ERR_LCDM,
    "rtk_replay_abs_error": ERR_RTK,
    "delta_replay_abs_error": ERR_DELTA,
    "replay_abs_tolerance_each": TOL_EACH,
    "delta_replay_abs_tolerance": TOL_DELTA,
    "lensing_product": B9["lensing_product"],
    "lensing_lmax": LMAX,
    "target_fingerprint": canonical_hash(TARGET),
    "provenance": PROV,
    "warning": "Local frozen B9 robustness comparison only; not global optimality, significance, AIC/BIC, posterior preference or Bayes factor.",
}

if ERR_LCDM > TOL_EACH:
    raise RuntimeError(f"LCDM B9 replay drift {ERR_LCDM} > {TOL_EACH}")
if ERR_RTK > TOL_EACH:
    raise RuntimeError(f"RTK B9 replay drift {ERR_RTK} > {TOL_EACH}")
if ERR_DELTA > TOL_DELTA:
    raise RuntimeError(f"paired B9 delta replay drift {ERR_DELTA} > {TOL_DELTA}")

RESULT.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")
print("B9_FINAL_PAIRED_EXACT_REPLAY_PASS", json.dumps(result, sort_keys=True, allow_nan=False), flush=True)
