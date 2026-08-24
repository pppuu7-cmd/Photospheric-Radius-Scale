#!/usr/bin/env python3
"""Fresh-tree exact replay of the preregistered replacement A5 local pair."""
from __future__ import annotations

from pathlib import Path
import hashlib, json, math, os, subprocess, sys, time

sys.path.insert(0, str(Path.cwd()))
sys.argv=["a5_final_replacement_paired_replay","planck_data"]
import inference_core as L
import numpy as np
import scipy

ROOT=Path("..")
TARGET=json.loads((ROOT/"research/robustness/A5_FINAL_REPLACEMENT_PAIRED_REPLAY_TARGET_v1.json").read_text())
STATE=json.loads((ROOT/"research/state/current.json").read_text())
assert TARGET["classification"]=="A5_FINAL_REPLACEMENT_PAIRED_REPLAY_TARGET_V1_FROZEN"
assert TARGET["objective"]==STATE["objective"]["name"]=="matched-ultra-linstep2+dense-BOSS"
assert TARGET["production_mapping"]=="eff"


def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()

if canonical_hash(STATE["objective"])!=TARGET["objective_fingerprint"]:
    raise RuntimeError("A5 objective fingerprint drift")

P=TARGET["prerequisites"]
CROSS=json.loads((ROOT/P["cross_basin_result"]).read_text())
BASE=json.loads((ROOT/P["base_result"]).read_text())
RAYS=json.loads((ROOT/P["base_rays_result"]).read_text())
HALF=json.loads((ROOT/P["half_result"]).read_text())
assert CROSS["classification"]==P["cross_basin_classification"]
assert BASE["eff"]["best_improvement"]<=P["base_required_best_improvement_le"]
assert RAYS["classification"]==P["base_rays_classification"]
assert RAYS["max_exact_improvement_eff"]<=0.005
assert float(HALF["stencil_scale"])==float(P["half_required_scale"])
assert HALF["eff"]["best_improvement"]<=P["half_required_best_improvement_le"]
assert HALF["eff"]["positive_definite"] is P["half_required_positive_definite"]
assert HALF["center"]==TARGET["lcdm"]["params"]

OUT=ROOT/"output/a5_final_replacement_paired_replay";OUT.mkdir(parents=True,exist_ok=True)
POINTS=OUT/"points.jsonl";FAILURES=OUT/"failures.jsonl";SUMMARY=OUT/"summary.json"

SPARSE="0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0"
DENSE=STATE["objective"]["dense_z_pk"]
ULTRA={k:str(v) for k,v in STATE["objective"]["ultra"].items()}
ORIG=L.make_ini

def make_ini(model,p,tag):
    path=ORIG(model,p,tag);text=Path(path).read_text()
    if "z_pk = "+SPARSE in text:text=text.replace("z_pk = "+SPARSE,"z_pk = "+DENSE,1)
    elif "z_pk = "+DENSE not in text:raise RuntimeError("could not establish frozen dense A5 objective")
    text+="\n# A5 final replacement paired replay: frozen production precision\n"
    text+="".join(f"{k} = {v}\n" for k,v in ULTRA.items())
    Path(path).write_text(text);return path
L.make_ini=make_ini


def git_head(path):
    try:return subprocess.check_output(["git","-C",str(path),"rev-parse","HEAD"],text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return None

def append(path,row):
    with path.open("a") as f:f.write(json.dumps(row,sort_keys=True,default=str)+"\n");f.flush()

def cleanup(tag):
    if not tag:return
    for q in L.OUT.glob(tag+"_*"):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f"profile_{tag}.ini"),Path(f"profile_{tag}.log")):
        try:q.unlink()
        except OSError:pass

def evaluate(model,params):
    last=None
    for attempt in (1,2,3):
        L.CACHE.clear()
        try:r=L.evaluate(model,dict(params))
        except Exception as exc:r={"ok":False,"exception":repr(exc)}
        if r.get("ok"):
            row={"model":model,"attempt":attempt,"params":dict(params),"score_eff":float(r["score"]),"score_k01":float(r["score_k01"]),"components":{k:r.get(k) for k in ("logL_planck","chi2_SN","chi2_BOSS_eff","chi2_BOSS_k01","rd")}}
            if not math.isfinite(row["score_eff"]):raise RuntimeError("nonfinite A5 replay score")
            append(POINTS,row);cleanup(r.get("tag"));return row
        last=r;append(FAILURES,{"model":model,"attempt":attempt,"params":params,"result":r});cleanup(r.get("tag") if isinstance(r,dict) else None)
        if attempt<3:time.sleep(2*attempt)
    raise RuntimeError(f"{model} replay failed after retries: {last}")

lcdm=evaluate("LCDM",TARGET["lcdm"]["params"])
rtk=evaluate("RTK",TARGET["rtk"]["params"])
SL=float(lcdm["score_eff"]);SR=float(rtk["score_eff"]);D=SR-SL
EL=float(TARGET["lcdm"]["expected_S_eff"]);ER=float(TARGET["rtk"]["expected_S_eff"]);ED=float(TARGET["expected_delta_S_RTK_minus_LCDM"])
errors={"lcdm":SL-EL,"rtk":SR-ER,"delta":D-ED}
score_tol=float(TARGET["score_replay_abs_tolerance_each"]);delta_tol=float(TARGET["delta_replay_abs_tolerance"])
passed=abs(errors["lcdm"])<=score_tol and abs(errors["rtk"])<=score_tol and abs(errors["delta"])<=delta_tol
summary={
 "status":"PASS" if passed else "FAIL",
 "classification":"A5_FINAL_REPLACEMENT_PAIRED_FRESH_TREE_REPLAY_PASS" if passed else "A5_FINAL_REPLACEMENT_PAIRED_FRESH_TREE_REPLAY_FAIL",
 "objective":TARGET["objective"],"objective_fingerprint":TARGET["objective_fingerprint"],"production_mapping":"eff",
 "target_fingerprint":canonical_hash(TARGET),"lcdm":lcdm,"rtk":rtk,"S_LCDM":SL,"S_RTK":SR,"delta_S_RTK_minus_LCDM":D,
 "expected_S_LCDM":EL,"expected_S_RTK":ER,"expected_delta_S_RTK_minus_LCDM":ED,
 "replay_errors":errors,"score_replay_abs_tolerance_each":score_tol,"delta_replay_abs_tolerance":delta_tol,
 "prerequisite_fingerprints":{"cross":canonical_hash(CROSS),"base":canonical_hash(BASE),"rays":canonical_hash(RAYS),"half":canonical_hash(HALF)},
 "provenance":{"research_source_commit":git_head(ROOT),"class_upstream_commit":git_head(Path(".")),"pantheon_commit":git_head(Path("pantheon")),"python_version":sys.version.split()[0],"numpy_version":np.__version__,"scipy_version":scipy.__version__},
 "warning":TARGET["guard"]}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
print("A5_FINAL_REPLACEMENT_PAIRED_REPLAY",json.dumps(summary,sort_keys=True),flush=True)
if not passed:raise SystemExit("A5_FINAL_REPLACEMENT_PAIRED_REPLAY_MISMATCH "+json.dumps(errors,sort_keys=True))
print("A5_FINAL_REPLACEMENT_PAIRED_REPLAY_PASS",flush=True)
