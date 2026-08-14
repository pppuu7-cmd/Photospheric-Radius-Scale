#!/usr/bin/env python3
"""First coarse data test for the RT+DBI-Khronon lambda_D grid.

This is intentionally NOT a replacement for official Planck/BOSS/Pantheon
likelihoods. It is a ranking/diagnostic layer designed to decide whether the
current grid is promising enough to justify a full likelihood implementation.

Data used:
  * Pantheon 40-bin Hubble diagram (Scolnic et al. 2018), diagonal errors only
    with an added 0.02 mag floor. The absolute SN magnitude/H0 offset is
    analytically minimized out.
  * BOSS DR12 anisotropic BAO points at z=0.38, 0.51, 0.61, using a diagonal
    approximation in this first pass.
  * BOSS DR12 f sigma8 measurements at the same redshifts, diagonal errors.
    Because RTK growth is scale dependent, both an effective sigma8 derivative
    and the k=0.1 h/Mpc diagnostic are reported.
  * CMB TT shape-consistency proxy versus the matched LCDM run. This is NOT a
    Planck likelihood; it only measures displacement from the matched control.

For BAO the exact CLASS baryon-drag redshift z_d and comoving sound horizon r_d
are parsed from each model's own thermodynamics log. Full BOSS covariance and
official Planck/Pantheon likelihoods remain for the next-stage implementation.
"""

from pathlib import Path
from bisect import bisect_left
import csv
import math
import re

OUT = Path('output')
C_KM_S = 299792.458
R_FID = 147.78

MODELS = [
    ('LCDM', None, 'lcdm', Path('../lcdm_run.log')),
    ('RTK', 8000.0, 'rtk8', Path('../rtk8_run.log')),
    ('RTK', 10000.0, 'rtk', Path('../rtk_run.log')),
    ('RTK', 12500.0, 'rtk125', Path('../rtk125_run.log')),
    ('RTK', 15000.0, 'rtk15', Path('../rtk15_run.log')),
    ('RTK', 20000.0, 'rtk20', Path('../rtk20_run.log')),
]

BAO = [
    (0.38, 1518.0, 22.0, 81.5, 1.9),
    (0.51, 1977.0, 27.0, 90.4, 1.9),
    (0.61, 2283.0, 32.0, 97.3, 2.1),
]

RSD = [
    (0.38, 0.430, 0.054),
    (0.51, 0.452, 0.057),
    (0.61, 0.457, 0.052),
]


def load_numeric(path, min_cols=2):
    rows = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            vals = [float(x) for x in s.split()]
            if len(vals) >= min_cols:
                rows.append(vals)
    return rows


def load_background(prefix):
    # z,t,tau,H,DM,DA,DL,rs are the first eight columns in CLASS v2.4.5.
    rows = load_numeric(OUT / f'{prefix}_background.dat', 8)
    rows.sort(key=lambda r: r[0])
    return rows


def interp_rows(rows, col, z):
    zs = [r[0] for r in rows]
    if z <= zs[0]:
        return rows[0][col]
    if z >= zs[-1]:
        return rows[-1][col]
    j = bisect_left(zs, z)
    z0, z1 = zs[j-1], zs[j]
    y0, y1 = rows[j-1][col], rows[j][col]
    if z1 == z0:
        return y0
    t = (z-z0)/(z1-z0)
    return y0 + t*(y1-y0)


def parse_drag_horizon(log_path):
    z_d = None
    r_d = None
    z_re = re.compile(r'baryon drag stops at z\s*=\s*([0-9eE+\-.]+)')
    r_re = re.compile(r'with comoving sound horizon rs\s*=\s*([0-9eE+\-.]+)\s*Mpc')
    with open(log_path) as f:
        for line in f:
            mz = z_re.search(line)
            if mz:
                z_d = float(mz.group(1))
            mr = r_re.search(line)
            if mr and z_d is not None:
                r_d = float(mr.group(1))
    if z_d is None or r_d is None:
        raise RuntimeError(f'Could not parse exact CLASS z_d/r_d from {log_path}')
    return z_d, r_d


def sn_chi2(bg):
    dat = load_numeric('pantheon_binned_lcparam_DS17f.txt', 6)
    ys, ws, residual_inputs = [], [], []
    for r in dat:
        z, mb, dmb = r[1], r[4], r[5]
        dl = interp_rows(bg, 6, z)
        mu_geom = 5.0*math.log10(dl) + 25.0
        sig = math.sqrt(dmb*dmb + 0.02*0.02)
        y = mb-mu_geom
        w = 1.0/(sig*sig)
        ys.append(y); ws.append(w); residual_inputs.append((y,sig))
    offset = sum(w*y for w,y in zip(ws,ys))/sum(ws)
    residuals = [(y-offset, sig) for y,sig in residual_inputs]
    chi2 = sum((res/sig)**2 for res,sig in residuals)
    max_abs = max(abs(res) for res,_ in residuals)
    return chi2, offset, max_abs


def bao_chi2(bg, z_d, r_d):
    chi2 = 0.0
    pred_rows = []
    for z, dm_obs, dm_err, h_obs, h_err in BAO:
        dm = interp_rows(bg, 4, z)
        h_km = interp_rows(bg, 3, z)*C_KM_S
        pred_dm = dm*R_FID/r_d
        pred_h = h_km*r_d/R_FID
        term = ((pred_dm-dm_obs)/dm_err)**2 + ((pred_h-h_obs)/h_err)**2
        chi2 += term
        pred_rows.append({
            'z': z,
            'DM_rfid_over_rd_pred': pred_dm,
            'H_rd_over_rfid_pred': pred_h,
            'z_drag_CLASS': z_d,
            'rd_mpc_CLASS': r_d,
        })
    return chi2, pred_rows


def load_growth():
    with open(OUT/'growth_scan.csv', newline='') as f:
        return list(csv.DictReader(f))


def growth_subset(growth, model, lam):
    out = []
    for r in growth:
        if r['model'] != model:
            continue
        if model == 'RTK' and abs(float(r['lambda_D'])-lam) > 1e-6:
            continue
        out.append(r)
    out.sort(key=lambda r: float(r['z']))
    return out


def interp_growth(rows, column, z):
    pts = [(float(r['z']), float(r[column])) for r in rows]
    if z <= pts[0][0]: return pts[0][1]
    if z >= pts[-1][0]: return pts[-1][1]
    zs = [p[0] for p in pts]
    j = bisect_left(zs, z)
    z0,y0 = pts[j-1]; z1,y1 = pts[j]
    return y0 + (z-z0)*(y1-y0)/(z1-z0)


def rsd_chi2(growth, model, lam, column):
    rows = growth_subset(growth, model, lam)
    chi2 = 0.0
    preds = []
    for z, obs, err in RSD:
        pred = interp_growth(rows, column, z)
        chi2 += ((pred-obs)/err)**2
        preds.append(pred)
    return chi2, preds


def load_tt(prefix):
    rows = load_numeric(OUT/f'{prefix}_cl.dat', 2)
    return {int(round(r[0])): r[1] for r in rows}


def cmb_shape_proxy(prefix):
    ref = load_tt('lcdm')
    cur = load_tt(prefix)
    ells = [ell for ell in sorted(set(ref).intersection(cur)) if 30 <= ell <= 1200]
    chi2 = 0.0
    shifts = []
    for ell in ells:
        ratio = cur[ell]/ref[ell]
        shift = ratio-1.0
        frac_sigma = math.sqrt(2.0/((2.0*ell+1.0)*0.7) + 0.01**2)
        chi2 += (shift/frac_sigma)**2
        shifts.append(shift)
    max_abs = max(abs(x) for x in shifts)
    rms = math.sqrt(sum(x*x for x in shifts)/len(shifts))
    return chi2, max_abs, rms


def write_csv(path, rows):
    if not rows:
        return
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


growth = load_growth()
summary = []
bao_rows = []
rsd_rows = []

for model, lam, prefix, log_path in MODELS:
    bg = load_background(prefix)
    z_d, r_d = parse_drag_horizon(log_path)
    c2_sn, sn_offset, max_sn_res = sn_chi2(bg)
    c2_bao, bp = bao_chi2(bg, z_d, r_d)
    c2_rsd_eff, pred_eff = rsd_chi2(growth, model, lam, 'fs8_eff')
    c2_rsd_k01, pred_k01 = rsd_chi2(growth, model, lam, 'fs8_k0p1')
    c2_cmb, cmb_max, cmb_rms = cmb_shape_proxy(prefix)

    row = {
        'model': model,
        'lambda_D': '' if lam is None else lam,
        'chi2_sn_diag_floor': c2_sn,
        'chi2_bao_diag': c2_bao,
        'chi2_rsd_eff_diag': c2_rsd_eff,
        'chi2_rsd_k0p1_diag': c2_rsd_k01,
        'cmb_tt_shape_proxy': c2_cmb,
        'chi2_data_eff': c2_sn+c2_bao+c2_rsd_eff,
        'chi2_data_k0p1': c2_sn+c2_bao+c2_rsd_k01,
        'score_eff_plus_cmb_proxy': c2_sn+c2_bao+c2_rsd_eff+c2_cmb,
        'z_drag_CLASS': z_d,
        'rd_mpc_CLASS': r_d,
        'sn_nuisance_offset': sn_offset,
        'sn_max_abs_residual_mag': max_sn_res,
        'cmb_max_abs_frac_shift': cmb_max,
        'cmb_rms_frac_shift': cmb_rms,
    }
    summary.append(row)

    for b in bp:
        b = dict(b)
        b['model'] = model; b['lambda_D'] = '' if lam is None else lam
        bao_rows.append(b)
    for (z,_,_), pe, pk in zip(RSD, pred_eff, pred_k01):
        rsd_rows.append({
            'model': model, 'lambda_D': '' if lam is None else lam, 'z': z,
            'fs8_eff_pred': pe, 'fs8_k0p1_pred': pk,
        })

lcdm = summary[0]
cols_to_delta = [
    'chi2_sn_diag_floor','chi2_bao_diag','chi2_rsd_eff_diag',
    'chi2_rsd_k0p1_diag','chi2_data_eff','chi2_data_k0p1',
    'score_eff_plus_cmb_proxy'
]
for row in summary:
    for col in cols_to_delta:
        row['delta_'+col] = row[col]-lcdm[col]

write_csv(OUT/'coarse_likelihood_summary.csv', summary)
write_csv(OUT/'coarse_bao_predictions.csv', bao_rows)
write_csv(OUT/'coarse_rsd_predictions.csv', rsd_rows)

print('COARSE LIKELIHOOD DIAGNOSTIC')
print('IMPORTANT: CMB term is a matched-LCDM TT-shape proxy, NOT the official Planck likelihood.')
print('Pantheon: diagonal binned errors + 0.02 mag floor. BOSS BAO/RSD: diagonal approximations.')
print('BAO ruler: exact z_d and r_d parsed from each CLASS thermodynamics run.')
print('model lambda z_drag rd_Mpc chi2_SN chi2_BAO chi2_RSD_eff chi2_RSD_k01 CMB_proxy dchi2_data_eff dscore_with_CMBproxy')
for r in summary:
    lam = '-' if r['lambda_D']=='' else f"{float(r['lambda_D']):.0f}"
    print(f"{r['model']:4s} {lam:6s} {r['z_drag_CLASS']:8.3f} {r['rd_mpc_CLASS']:8.4f} "
          f"{r['chi2_sn_diag_floor']:8.4f} {r['chi2_bao_diag']:9.4f} {r['chi2_rsd_eff_diag']:12.4f} "
          f"{r['chi2_rsd_k0p1_diag']:12.4f} {r['cmb_tt_shape_proxy']:9.3f} "
          f"{r['delta_chi2_data_eff']:15.4f} {r['delta_score_eff_plus_cmb_proxy']:20.4f}")

rtk = [r for r in summary if r['model']=='RTK']
best = min(rtk, key=lambda r: r['chi2_data_eff'])
print('\nBEST GRID POINT BY REAL-DATA COARSE SCORE (SN+BAO+RSD_eff):')
print(f"lambda_D={float(best['lambda_D']):.0f} delta_chi2_data_eff={best['delta_chi2_data_eff']:.6f} "
      f"delta_score_with_cmb_proxy={best['delta_score_eff_plus_cmb_proxy']:.6f}")
print('COARSE_LIKELIHOOD_PASS')
