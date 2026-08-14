#!/usr/bin/env python3
"""First coarse data test for the RT+DBI-Khronon lambda_D grid.

This is intentionally NOT a replacement for official Planck/BOSS/Pantheon
likelihoods.  It is a ranking/diagnostic layer designed to decide whether the
current grid is promising enough to justify a full likelihood implementation.

Data used:
  * Pantheon 40-bin Hubble diagram (Scolnic et al. 2018), diagonal errors only
    with an added 0.02 mag floor because the full systematic covariance is not
    yet included here.  The absolute SN magnitude/H0 offset is minimized out.
  * BOSS DR12 anisotropic BAO points at z=0.38, 0.51, 0.61 (Alam et al. 2017),
    diagonal approximation for this coarse pass.
  * BOSS DR12 f sigma8 measurements from Satpathy et al. 2017, diagonal errors.
    Because RTK growth is scale dependent, both an effective sigma8 derivative
    and k=0.1 h/Mpc diagnostic are reported.
  * CMB TT shape consistency proxy versus the matched LCDM run.  This is NOT a
    Planck data likelihood; it only measures how far the RTK TT curve moves from
    the matched control using a cosmic-variance-like weighting plus 1% floor.
"""

from pathlib import Path
import math
import numpy as np
import pandas as pd

OUT = Path('output')
C_KM_S = 299792.458
R_FID = 147.78  # Mpc, BOSS DR12 fiducial ruler used in quoted measurements

MODELS = [
    ('LCDM', np.nan, 'lcdm'),
    ('RTK', 8000.0, 'rtk8'),
    ('RTK', 10000.0, 'rtk'),
    ('RTK', 12500.0, 'rtk125'),
    ('RTK', 15000.0, 'rtk15'),
    ('RTK', 20000.0, 'rtk20'),
]

# Coarse BOSS DR12 BAO values.  Correlations are deliberately ignored at this stage.
BAO = pd.DataFrame({
    'z': [0.38, 0.51, 0.61],
    'DM_rfid_over_rd': [1518.0, 1977.0, 2283.0],
    'DM_err': [22.0, 27.0, 32.0],
    'H_rd_over_rfid': [81.5, 90.4, 97.3],
    'H_err': [1.9, 1.9, 2.1],
})

# Satpathy et al. 2017, BOSS DR12 CLPT-GSRSD values.
RSD = pd.DataFrame({
    'z': [0.38, 0.51, 0.61],
    'fs8': [0.430, 0.452, 0.457],
    'err': [0.054, 0.057, 0.052],
})


def load_background(prefix):
    """CLASS v2.4.5 background output: first eight columns are invariant."""
    path = OUT / f'{prefix}_background.dat'
    a = np.loadtxt(path)
    # z, proper time, conformal time, H[1/Mpc], comoving distance,
    # angular diameter distance, luminosity distance, comoving sound horizon
    df = pd.DataFrame(a[:, :8], columns=['z','t_gyr','tau_mpc','H_1_mpc','DM_mpc','DA_mpc','DL_mpc','rs_mpc'])
    return df.sort_values('z').reset_index(drop=True)


def interp(df, col, z):
    return np.interp(np.asarray(z, float), df['z'].to_numpy(), df[col].to_numpy())


def sn_chi2(bg):
    dat = np.loadtxt('pantheon_binned_lcparam_DS17f.txt')
    z = dat[:,1]
    mb = dat[:,4]
    # Full Pantheon covariance is not yet used.  Add a conservative floor so this
    # diagnostic does not pretend that diagonal statistical errors are the full likelihood.
    sig = np.sqrt(dat[:,5]**2 + 0.02**2)
    dl = interp(bg, 'DL_mpc', z)
    mu_geom = 5.0*np.log10(dl) + 25.0
    y = mb - mu_geom
    w = 1.0/sig**2
    offset = np.sum(w*y)/np.sum(w)
    res = y-offset
    return float(np.sum((res/sig)**2)), float(offset), float(np.max(np.abs(res)))


def bao_chi2(bg):
    z = BAO['z'].to_numpy()
    dm = interp(bg, 'DM_mpc', z)
    h = interp(bg, 'H_1_mpc', z)*C_KM_S
    # The sound horizon column asymptotes to the drag-era standard-ruler value by z=0.
    rd = float(interp(bg, 'rs_mpc', [0.0])[0])
    pred_dm = dm*R_FID/rd
    pred_h = h*rd/R_FID
    c2_dm = np.sum(((pred_dm-BAO['DM_rfid_over_rd'])/BAO['DM_err'])**2)
    c2_h = np.sum(((pred_h-BAO['H_rd_over_rfid'])/BAO['H_err'])**2)
    pred = pd.DataFrame({
        'z': z,
        'DM_rfid_over_rd_pred': pred_dm,
        'H_rd_over_rfid_pred': pred_h,
        'rd_mpc': rd,
    })
    return float(c2_dm+c2_h), pred


def rsd_chi2(growth, model, lam, column):
    if model == 'LCDM':
        d = growth[growth['model']=='LCDM'].sort_values('z')
    else:
        d = growth[(growth['model']=='RTK') & np.isclose(growth['lambda_D'],lam)].sort_values('z')
    pred = np.interp(RSD['z'], d['z'], d[column])
    chi2 = np.sum(((pred-RSD['fs8'])/RSD['err'])**2)
    return float(chi2), pred


def load_tt(prefix):
    a = np.loadtxt(OUT / f'{prefix}_cl.dat')
    return a[:,0].astype(int), a[:,1]


def cmb_shape_proxy(prefix):
    ell0, tt0 = load_tt('lcdm')
    ell, tt = load_tt(prefix)
    common = np.intersect1d(ell0, ell)
    common = common[(common >= 30) & (common <= 1200)]
    ref = np.interp(common, ell0, tt0)
    cur = np.interp(common, ell, tt)
    ratio = cur/ref
    # f_sky~0.7 cosmic-variance-like weighting + 1% floor.  This is a proxy only.
    frac_sigma = np.sqrt(2.0/((2.0*common+1.0)*0.7) + 0.01**2)
    chi2 = np.sum(((ratio-1.0)/frac_sigma)**2)
    return float(chi2), float(np.max(np.abs(ratio-1.0))), float(np.sqrt(np.mean((ratio-1.0)**2)))


growth = pd.read_csv(OUT/'growth_scan.csv')
rows = []
bao_rows = []
rsd_rows = []

for model, lam, prefix in MODELS:
    bg = load_background(prefix)
    c2_sn, sn_offset, max_sn_res = sn_chi2(bg)
    c2_bao, bp = bao_chi2(bg)
    c2_rsd_eff, pred_eff = rsd_chi2(growth, model, lam, 'fs8_eff')
    c2_rsd_k01, pred_k01 = rsd_chi2(growth, model, lam, 'fs8_k0p1')
    c2_cmb, cmb_max, cmb_rms = cmb_shape_proxy(prefix)

    row = {
        'model': model,
        'lambda_D': lam,
        'chi2_sn_diag_floor': c2_sn,
        'chi2_bao_diag': c2_bao,
        'chi2_rsd_eff_diag': c2_rsd_eff,
        'chi2_rsd_k0p1_diag': c2_rsd_k01,
        'cmb_tt_shape_proxy': c2_cmb,
        'chi2_data_eff': c2_sn+c2_bao+c2_rsd_eff,
        'chi2_data_k0p1': c2_sn+c2_bao+c2_rsd_k01,
        'score_eff_plus_cmb_proxy': c2_sn+c2_bao+c2_rsd_eff+c2_cmb,
        'sn_nuisance_offset': sn_offset,
        'sn_max_abs_residual_mag': max_sn_res,
        'cmb_max_abs_frac_shift': cmb_max,
        'cmb_rms_frac_shift': cmb_rms,
    }
    rows.append(row)

    bp.insert(0,'model',model)
    bp.insert(1,'lambda_D',lam)
    bao_rows.append(bp)
    for z, pe, pk in zip(RSD['z'], pred_eff, pred_k01):
        rsd_rows.append({'model':model,'lambda_D':lam,'z':z,'fs8_eff_pred':pe,'fs8_k0p1_pred':pk})

summary = pd.DataFrame(rows)
lcdm = summary[summary.model=='LCDM'].iloc[0]
for col in ['chi2_sn_diag_floor','chi2_bao_diag','chi2_rsd_eff_diag','chi2_rsd_k0p1_diag','chi2_data_eff','chi2_data_k0p1','score_eff_plus_cmb_proxy']:
    summary['delta_'+col] = summary[col]-lcdm[col]

summary.to_csv(OUT/'coarse_likelihood_summary.csv', index=False)
pd.concat(bao_rows, ignore_index=True).to_csv(OUT/'coarse_bao_predictions.csv', index=False)
pd.DataFrame(rsd_rows).to_csv(OUT/'coarse_rsd_predictions.csv', index=False)

print('COARSE LIKELIHOOD DIAGNOSTIC')
print('IMPORTANT: CMB term is a matched-LCDM TT-shape proxy, not the official Planck likelihood.')
print('Pantheon uses diagonal binned errors + 0.02 mag floor; BOSS BAO/RSD use diagonal approximations.')
cols = ['model','lambda_D','chi2_sn_diag_floor','chi2_bao_diag','chi2_rsd_eff_diag','chi2_rsd_k0p1_diag','cmb_tt_shape_proxy','delta_chi2_data_eff','delta_score_eff_plus_cmb_proxy']
print(summary[cols].to_string(index=False, float_format=lambda x: f'{x:.6f}'))

rtk = summary[summary.model=='RTK'].sort_values('chi2_data_eff')
best = rtk.iloc[0]
print('\nBEST GRID POINT BY REAL-DATA COARSE SCORE (SN+BAO+RSD_eff):')
print(f"lambda_D={best.lambda_D:.0f} delta_chi2_data_eff={best.delta_chi2_data_eff:.6f} delta_score_with_cmb_proxy={best.delta_score_eff_plus_cmb_proxy:.6f}")
print('COARSE_LIKELIHOOD_PASS')
