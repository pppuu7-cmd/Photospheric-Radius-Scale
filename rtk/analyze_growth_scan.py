#!/usr/bin/env python3
"""Analyze the RT+DBI-Khronon lambda_D scan from CLASS P(k,z) outputs.

Outputs:
  output/growth_scan.csv       - sigma8 and growth diagnostics vs z
  output/pk_ratio_scan.csv     - P_RTK/P_LCDM vs selected (z,k)
  output/lambda_scan_summary.csv - one compact row per lambda_D

For scale-dependent growth there is no unique survey-independent f*sigma8.
We therefore report two diagnostics:
  fs8_eff = d sigma8 / d ln(a)
  fs8_k0p1 = f(k=0.1 h/Mpc,z) * sigma8(z),
where f(k,z)=0.5 d ln P(k,z)/d ln(a).
"""
from pathlib import Path
from bisect import bisect_left
import csv
import math
import re

OUT = Path("output")
MODELS = [
    (8000,  "rtk8_",  Path("../rtk8_run.log")),
    (10000, "rtk_",   Path("../rtk_run.log")),
    (12500, "rtk125_",Path("../rtk125_run.log")),
    (15000, "rtk15_", Path("../rtk15_run.log")),
    (20000, "rtk20_", Path("../rtk20_run.log")),
]
LCDM_PREFIX = "lcdm_"
TARGET_Z = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
PK_Z = [0.0, 0.5, 1.0, 2.0, 3.0]
K_SAMPLES = [0.05, 0.1, 0.2, 0.5, 1.0]
F_K = [0.05, 0.1, 0.2]


def load_table(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        a = s.split()
        rows.append((float(a[0]), float(a[1])))
    if len(rows) < 3:
        raise RuntimeError(f"too few P(k) rows in {path}")
    return rows


def redshift_from_header(path):
    for line in Path(path).read_text().splitlines()[:8]:
        m = re.search(r"redshift z=([+\-0-9.eE]+)", line)
        if m:
            return float(m.group(1))
    raise RuntimeError(f"cannot read redshift from header: {path}")


def load_pk_family(prefix):
    files = sorted(OUT.glob(prefix + "z*_pk.dat"))
    if not files:
        # Keep compatibility with a single z_pk output.
        p = OUT / (prefix + "pk.dat")
        if p.exists():
            files = [p]
    if not files:
        raise RuntimeError(f"no P(k,z) outputs found for prefix {prefix}")
    data = {}
    for p in files:
        z = redshift_from_header(p)
        if z in data:
            raise RuntimeError(f"duplicate redshift {z} for prefix {prefix}")
        data[z] = load_table(p)
    return data


def interp(x, rows):
    xs = [r[0] for r in rows]
    if x < xs[0] or x > xs[-1]:
        raise RuntimeError(f"k={x} outside [{xs[0]},{xs[-1]}]")
    i = bisect_left(xs, x)
    if i == 0:
        return rows[0][1]
    if i == len(rows):
        return rows[-1][1]
    x0, y0 = rows[i-1]
    x1, y1 = rows[i]
    if x1 == x0:
        return y0
    return y0 + (y1-y0)*(x-x0)/(x1-x0)


def top_hat(x):
    ax = abs(x)
    if ax < 1.0e-3:
        x2 = x*x
        return 1.0 - x2/10.0 + x2*x2/280.0
    return 3.0*(math.sin(x)-x*math.cos(x))/(x*x*x)


def sigma_R(rows, R=8.0, k_cut=None):
    use = [(k,p) for (k,p) in rows if (k_cut is None or k <= k_cut)]
    if len(use) < 3:
        raise RuntimeError("insufficient k coverage for sigma_R")
    terms = []
    for k, p in use:
        W = top_hat(k*R)
        terms.append((math.log(k), k*k*k*p*W*W))
    integ = 0.0
    for i in range(1, len(terms)):
        x0,y0 = terms[i-1]
        x1,y1 = terms[i]
        integ += 0.5*(y0+y1)*(x1-x0)
    var = integ/(2.0*math.pi*math.pi)
    if not (var > 0.0 and math.isfinite(var)):
        raise RuntimeError(f"non-positive/non-finite sigma^2={var}")
    return math.sqrt(var)


def exact_z_key(data, z, tol=1e-9):
    best = min(data.keys(), key=lambda q: abs(q-z))
    if abs(best-z) > tol:
        raise RuntimeError(f"requested z={z} not present; nearest={best}")
    return best


def derivative_three(x0,y0,x1,y1,x2,y2,xt):
    # Derivative of the quadratic Lagrange interpolant at xt.
    d0 = (2.0*xt-x1-x2)/((x0-x1)*(x0-x2))
    d1 = (2.0*xt-x0-x2)/((x1-x0)*(x1-x2))
    d2 = (2.0*xt-x0-x1)/((x2-x0)*(x2-x1))
    return y0*d0 + y1*d1 + y2*d2


def local_derivative(xy, xt):
    pts = sorted(xy)
    i = min(range(len(pts)), key=lambda j: abs(pts[j][0]-xt))
    if abs(pts[i][0]-xt) > 1e-10:
        raise RuntimeError("target derivative point is not in the grid")
    if i == 0:
        sel = pts[0:3]
    elif i == len(pts)-1:
        sel = pts[-3:]
    else:
        sel = pts[i-1:i+2]
    return derivative_three(sel[0][0],sel[0][1],sel[1][0],sel[1][1],sel[2][0],sel[2][1],xt)


def growth_metrics(pk_by_z):
    sig = {}
    tail = {}
    for z, rows in pk_by_z.items():
        sig[z] = sigma_R(rows, 8.0)
        s3 = sigma_R(rows, 8.0, 3.0)
        tail[z] = abs(sig[z]-s3)/sig[z]

    sig_xy = [(math.log(1.0/(1.0+z)), s) for z,s in sig.items()]
    result = {}
    for z0 in TARGET_Z:
        z = exact_z_key(pk_by_z, z0)
        x = math.log(1.0/(1.0+z))
        fs8_eff = local_derivative(sig_xy, x)
        fvals = {}
        for k in F_K:
            lnp_xy = []
            for zz, rows in pk_by_z.items():
                p = interp(k, rows)
                if not (p > 0.0):
                    raise RuntimeError(f"non-positive P(k,z) at k={k}, z={zz}")
                lnp_xy.append((math.log(1.0/(1.0+zz)), math.log(p)))
            fvals[k] = 0.5*local_derivative(lnp_xy, x)
        result[z0] = {
            "sigma8": sig[z],
            "fs8_eff": fs8_eff,
            "f005": fvals[0.05],
            "f010": fvals[0.1],
            "f020": fvals[0.2],
            "fs8_k0p1": fvals[0.1]*sig[z],
            "tail_sensitivity": tail[z],
        }
    return result, sig, tail


def parse_gamma(log_path):
    text = log_path.read_text()
    hits = re.findall(r"RTK_LOG_GAMMA_ROOT[^\n]*?gamma=([+\-0-9.eE]+)[^\n]*?F=([+\-0-9.eE]+)", text)
    if not hits:
        raise RuntimeError(f"gamma root not found in {log_path}")
    gamma, residual = hits[-1]
    return float(gamma), float(residual)


def write_csv(path, fieldnames, rows):
    with Path(path).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


lcdm_pk = load_pk_family(LCDM_PREFIX)
lcdm_metrics, lcdm_sig, lcdm_tail = growth_metrics(lcdm_pk)

scan_rows = []
ratio_rows = []
summary_rows = []

# Include LCDM diagnostic rows first.
for z in TARGET_Z:
    m = lcdm_metrics[z]
    scan_rows.append({
        "model":"LCDM","lambda_D":"","gamma":"","gamma_residual":"","z":z,
        "sigma8":m["sigma8"],"fs8_eff":m["fs8_eff"],"fs8_eff_over_lcdm":1.0,
        "f_k0p05":m["f005"],"f_k0p1":m["f010"],"f_k0p2":m["f020"],
        "fs8_k0p1":m["fs8_k0p1"],"fs8_k0p1_over_lcdm":1.0,
        "sigma8_tail_k3_vs_k5":m["tail_sensitivity"]})

for lam, prefix, log_path in MODELS:
    pk = load_pk_family(prefix)
    metrics, sig, tail = growth_metrics(pk)
    gamma, gres = parse_gamma(log_path)

    for z in TARGET_Z:
        m = metrics[z]
        c = lcdm_metrics[z]
        scan_rows.append({
            "model":"RTK","lambda_D":lam,"gamma":gamma,"gamma_residual":gres,"z":z,
            "sigma8":m["sigma8"],"fs8_eff":m["fs8_eff"],
            "fs8_eff_over_lcdm":m["fs8_eff"]/c["fs8_eff"],
            "f_k0p05":m["f005"],"f_k0p1":m["f010"],"f_k0p2":m["f020"],
            "fs8_k0p1":m["fs8_k0p1"],
            "fs8_k0p1_over_lcdm":m["fs8_k0p1"]/c["fs8_k0p1"],
            "sigma8_tail_k3_vs_k5":m["tail_sensitivity"]})

    for z0 in PK_Z:
        z = exact_z_key(pk, z0)
        zc = exact_z_key(lcdm_pk, z0)
        for k in K_SAMPLES:
            ratio_rows.append({
                "lambda_D":lam,"gamma":gamma,"z":z0,"k_h_Mpc":k,
                "P_RTK_over_LCDM":interp(k,pk[z])/interp(k,lcdm_pk[zc])})

    def ratio_at(z,k):
        zr=exact_z_key(pk,z); zc=exact_z_key(lcdm_pk,z)
        return interp(k,pk[zr])/interp(k,lcdm_pk[zc])

    summary_rows.append({
        "lambda_D":lam,"gamma":gamma,"gamma_residual":gres,
        "sigma8_z0":metrics[0.0]["sigma8"],
        "sigma8_over_lcdm_z0":metrics[0.0]["sigma8"]/lcdm_metrics[0.0]["sigma8"],
        "fs8_eff_z0":metrics[0.0]["fs8_eff"],
        "fs8_eff_z0_over_lcdm":metrics[0.0]["fs8_eff"]/lcdm_metrics[0.0]["fs8_eff"],
        "fs8_eff_z0p5":metrics[0.5]["fs8_eff"],
        "fs8_eff_z0p5_over_lcdm":metrics[0.5]["fs8_eff"]/lcdm_metrics[0.5]["fs8_eff"],
        "fs8_eff_z1":metrics[1.0]["fs8_eff"],
        "fs8_eff_z1_over_lcdm":metrics[1.0]["fs8_eff"]/lcdm_metrics[1.0]["fs8_eff"],
        "P_ratio_k0p2_z0":ratio_at(0.0,0.2),
        "P_ratio_k0p5_z0":ratio_at(0.0,0.5),
        "P_ratio_k1_z0":ratio_at(0.0,1.0),
        "P_ratio_k0p2_z1":ratio_at(1.0,0.2),
        "P_ratio_k0p5_z1":ratio_at(1.0,0.5),
        "P_ratio_k1_z1":ratio_at(1.0,1.0),
    })

write_csv(OUT/"growth_scan.csv",
          ["model","lambda_D","gamma","gamma_residual","z","sigma8","fs8_eff","fs8_eff_over_lcdm",
           "f_k0p05","f_k0p1","f_k0p2","fs8_k0p1","fs8_k0p1_over_lcdm","sigma8_tail_k3_vs_k5"],
          scan_rows)
write_csv(OUT/"pk_ratio_scan.csv",
          ["lambda_D","gamma","z","k_h_Mpc","P_RTK_over_LCDM"], ratio_rows)
write_csv(OUT/"lambda_scan_summary.csv",
          ["lambda_D","gamma","gamma_residual","sigma8_z0","sigma8_over_lcdm_z0",
           "fs8_eff_z0","fs8_eff_z0_over_lcdm","fs8_eff_z0p5","fs8_eff_z0p5_over_lcdm",
           "fs8_eff_z1","fs8_eff_z1_over_lcdm","P_ratio_k0p2_z0","P_ratio_k0p5_z0","P_ratio_k1_z0",
           "P_ratio_k0p2_z1","P_ratio_k0p5_z1","P_ratio_k1_z1"], summary_rows)

print("LCDM reference")
for z in [0.0,0.5,1.0,2.0]:
    m=lcdm_metrics[z]
    print(f"z={z:g} sigma8={m['sigma8']:.8f} fs8_eff={m['fs8_eff']:.8f} f(k=.1)={m['f010']:.8f}")
print("max sigma8 tail sensitivity |kmax=3 vs 5|/sigma8 =",
      max(max(lcdm_tail.values()), max(r["sigma8_tail_k3_vs_k5"] for r in scan_rows if r["model"]=="RTK")))

print("lambda_D scan summary")
print("lambda gamma sigma8(z0) fs8eff(z0) fs8eff(z0.5) fs8eff(z1) P0(k=.2) P0(k=.5) P0(k=1) P1(k=.5)")
for r in summary_rows:
    print(f"{int(r['lambda_D']):5d} {r['gamma']:.10f} {r['sigma8_z0']:.7f} "
          f"{r['fs8_eff_z0']:.7f} {r['fs8_eff_z0p5']:.7f} {r['fs8_eff_z1']:.7f} "
          f"{r['P_ratio_k0p2_z0']:.7f} {r['P_ratio_k0p5_z0']:.7f} {r['P_ratio_k1_z0']:.7f} {r['P_ratio_k0p5_z1']:.7f}")

# Hard numerical sanity gates, deliberately not observational cuts.
for r in scan_rows:
    for key in ["sigma8","fs8_eff","f_k0p05","f_k0p1","f_k0p2","fs8_k0p1"]:
        v=float(r[key])
        if not math.isfinite(v):
            raise RuntimeError(f"non-finite {key}: {r}")
    if float(r["sigma8"]) <= 0.0:
        raise RuntimeError(f"non-positive sigma8: {r}")
for r in ratio_rows:
    q=float(r["P_RTK_over_LCDM"])
    if not (math.isfinite(q) and q>0.0):
        raise RuntimeError(f"bad P ratio: {r}")

print("GROWTH_SCAN_ANALYSIS_PASS")
