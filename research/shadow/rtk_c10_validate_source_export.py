#!/usr/bin/env python3
"""Validate C10 read-only scalar source-history exports from RT-CLASS.

No completion parameters are used here.  The validator only checks that the
production histories needed by a later shadow replay are present, finite and
consistent with the frozen CLASS->C10 source conventions.
"""
from __future__ import annotations

import argparse
import glob
import json
import math
from pathlib import Path
from typing import List

DIAG = [
    "c10_k_Mpc_inv",
    "c10_Hc",
    "c10_Hc_prime",
    "c10_H0_ord",
    "c10_H0_ord_prime",
    "c10_H0_ord_double_prime",
    "c10_deltaH0_ord",
    "c10_delta_mu_total",
    "c10_rpp_theta_total",
    "c10_delta_p_total",
    "c10_rpp_shear_total",
    "c10_W_total",
    "c10_rho_total_prime",
    "c10_p_total_prime",
    "c10_khr_w",
    "c10_khr_ca2",
]


def numeric_rows(path: str) -> List[List[float]]:
    rows=[]
    for raw in Path(path).read_text().splitlines():
        line=raw.strip()
        if not line or line.startswith("#"):
            continue
        vals=[float(x) for x in line.split()]
        rows.append(vals)
    if not rows:
        raise RuntimeError(f"no numeric rows in {path}")
    n=len(rows[0])
    if n < len(DIAG)+2:
        raise RuntimeError(f"too few columns in {path}: {n}")
    if any(len(r)!=n for r in rows):
        raise RuntimeError(f"ragged table {path}")
    return rows


def central_derivative(x, y, i):
    if len(x)<3:
        return float("nan")
    if i==0:
        j0,j1=0,1
    elif i==len(x)-1:
        j0,j1=len(x)-2,len(x)-1
    else:
        j0,j1=i-1,i+1
    dx=x[j1]-x[j0]
    return (y[j1]-y[j0])/dx if dx!=0 else float("nan")


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--glob", dest="pattern", required=True)
    ap.add_argument("--output", required=True)
    args=ap.parse_args()

    files=sorted(glob.glob(args.pattern))
    if not files:
        raise SystemExit(f"no files matched {args.pattern}")

    summaries=[]
    actual_ks=[]
    global_q_abs=0.0
    global_pi_abs=0.0
    max_h0p_rel_fd=0.0
    fd_count=0

    for path in files:
        text=Path(path).read_text()
        missing=[name for name in DIAG if name not in text]
        if missing:
            raise SystemExit(f"missing diagnostic column names in {path}: {missing}")
        rows=numeric_rows(path)
        tail=[r[-len(DIAG):] for r in rows]
        if any(not math.isfinite(v) for r in tail for v in r):
            raise SystemExit(f"nonfinite C10 diagnostic in {path}")

        cols={name:[r[j] for r in tail] for j,name in enumerate(DIAG)}
        ks=cols["c10_k_Mpc_inv"]
        k=sum(ks)/len(ks)
        kspread=max(abs(x-k) for x in ks)
        if not (k>0.0):
            raise SystemExit(f"non-positive k in {path}: {k}")
        if kspread>1e-10*max(1.0,abs(k)):
            raise SystemExit(f"k not constant within output file {path}: spread={kspread}")

        # The first two standard columns are tau and a in CLASS scalar output.
        tau=[r[0] for r in rows]
        a=[r[1] for r in rows]
        if any(tau[i+1] <= tau[i] for i in range(len(tau)-1)):
            raise SystemExit(f"tau is not strictly increasing in {path}")
        if any(x<=0.0 for x in a):
            raise SystemExit(f"non-positive a in {path}")

        q=[a[i]*cols["c10_rpp_theta_total"][i]/(k*k) for i in range(len(rows))]
        pi=[1.5*cols["c10_rpp_shear_total"][i]/(k*k) for i in range(len(rows))]
        if any(not math.isfinite(x) for x in q+pi):
            raise SystemExit(f"nonfinite q/Pi reconstruction in {path}")
        global_q_abs=max(global_q_abs,max(abs(x) for x in q))
        global_pi_abs=max(global_pi_abs,max(abs(x) for x in pi))

        # Independent derivative sanity check for the ordinary background channel.
        h0=cols["c10_H0_ord"]
        h0p=cols["c10_H0_ord_prime"]
        local_fd=[]
        for i in range(1,len(rows)-1):
            fd=central_derivative(tau,h0,i)
            if math.isfinite(fd):
                scale=max(abs(fd),abs(h0p[i]),1e-300)
                local_fd.append(abs(fd-h0p[i])/scale)
        if local_fd:
            max_h0p_rel_fd=max(max_h0p_rel_fd,max(local_fd))
            fd_count+=len(local_fd)

        summaries.append({
            "file":path,
            "rows":len(rows),
            "columns":len(rows[0]),
            "actual_k_Mpc_inv":k,
            "a_min":min(a),
            "a_max":max(a),
            "tau_min_Mpc":min(tau),
            "tau_max_Mpc":max(tau),
            "max_abs_q_N":max(abs(x) for x in q),
            "max_abs_Pi_N":max(abs(x) for x in pi),
            "max_abs_deltaH0_ord":max(abs(x) for x in cols["c10_deltaH0_ord"]),
            "max_abs_delta_mu_total":max(abs(x) for x in cols["c10_delta_mu_total"]),
            "max_H0prime_fd_relative_disagreement_interior":max(local_fd) if local_fd else None,
        })
        actual_ks.append(k)

    actual_ks_sorted=sorted(actual_ks)
    out={
        "classification":"C10_PHYSICAL_CLASS_SOURCE_EXPORT_PASS",
        "status_scope":"GREEN_PARAMETER_FREE_READONLY_PRODUCTION_SOURCE_HISTORY_EXPORT",
        "files":summaries,
        "file_count":len(files),
        "actual_k_values_Mpc_inv":actual_ks_sorted,
        "all_k_positive":all(k>0 for k in actual_ks_sorted),
        "all_required_diagnostics_finite":True,
        "class_to_c10_map":{
            "q_N":"a*rpp_theta_total/k^2",
            "Pi_N":"1.5*rpp_shear_total/k^2",
        },
        "global_max_abs_q_N":global_q_abs,
        "global_max_abs_Pi_N":global_pi_abs,
        "ordinary_H0_prime_fd_sanity":{
            "interior_sample_count":fd_count,
            "max_relative_disagreement":max_h0p_rel_fd if fd_count else None,
            "guard":"finite-difference check only; output sampling/approximation transitions make this diagnostic non-authoritative",
        },
        "production_modified":False,
        "completion_parameters_selected":False,
        "next_gate":"physical completed-U1 replay requires either a frozen diagnostic (lambda_HL,M_c,...) scan or a parameter-independent regularity theorem plus a frozen chi initial/boundary prescription",
        "non_claims":[
            "not a completed-U1 regularity pass",
            "not a completion-parameter choice",
            "not a completed metric feedback or Boltzmann integration",
            "not a spectra or likelihood result",
        ],
    }
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(out["classification"],len(files),actual_ks_sorted)

if __name__=="__main__":
    main()
