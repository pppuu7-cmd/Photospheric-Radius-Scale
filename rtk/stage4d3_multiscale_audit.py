#!/usr/bin/env python3
"""Audit Stage4D3 stationarity across central-difference step scales.

Usage:
  python3 stage4d3_multiscale_audit.py summary_scale1.json summary_scale0p5.json summary_scale0p25.json

For a smooth objective, centered first/second derivatives have leading O(h^2)
truncation error.  With scales 1, 1/2, 1/4, Richardson extrapolation from the
two finest scales is therefore D* = D(h/4) + [D(h/4)-D(h/2)]/3.

This script adds a numerical-convergence audit on top of each exact stencil's
own acceptance gates.  It does not establish global optimality or statistical
preference.
"""
import json, math, sys
from pathlib import Path
import numpy as np

if len(sys.argv) != 4:
    raise SystemExit(__doc__)

items=[]
for p in sys.argv[1:]:
    d=json.loads(Path(p).read_text())
    items.append((float(d['step_scale']),d,str(p)))
items.sort(reverse=True)  # 1, .5, .25
scales=[x[0] for x in items]
if not (abs(scales[1]/scales[0]-0.5)<1e-8 and abs(scales[2]/scales[1]-0.5)<1e-8):
    raise SystemExit(f'scales must be geometric 1:1/2:1/4, got {scales}')

D=[x[1] for x in items]
if len({d['mapping'] for d in D}) != 1:
    raise SystemExit('mapping mismatch')
if len({round(float(d['lambda_D']),10) for d in D}) != 1:
    raise SystemExit('lambda_D center mismatch')

G=[np.asarray(d['gradient_base_scaled'],float) for d in D]
H=[np.asarray(d['hessian_base_scaled'],float) for d in D]
g_rich=G[2]+(G[2]-G[1])/3.0
H_rich=H[2]+(H[2]-H[1])/3.0
H_rich=(H_rich+H_rich.T)/2.0
eig_rich=np.linalg.eigvalsh(H_rich)

def infnorm(x): return float(np.max(np.abs(x)))
def fro(x): return float(np.linalg.norm(x,'fro'))

g_diff_coarse=infnorm(G[0]-G[1]); g_diff_fine=infnorm(G[1]-G[2])
h_diff_coarse=fro(H[0]-H[1]); h_diff_fine=fro(H[1]-H[2])
g_ratio=(g_diff_coarse/g_diff_fine if g_diff_fine>0 else math.inf)
h_ratio=(h_diff_coarse/h_diff_fine if h_diff_fine>0 else math.inf)
score_spread=max(float(d['S_center']) for d in D)-min(float(d['S_center']) for d in D)
grad_tol=min(float(d.get('gradient_tolerance_base_scaled',0.03)) for d in D)
improve_tol=min(float(d.get('improvement_tolerance',0.005)) for d in D)
rich_correction=infnorm(g_rich-G[2])

# Conservative internal numerical gate.  The correction requirement is tied
# directly to the declared stationarity tolerance rather than an unrelated
# absolute constant.
gates={
  'same_center_score_within_1e-6': bool(score_spread<=1e-6),
  'all_individual_stationarity_gates_pass': bool(all(d.get('stationarity_pass',False) for d in D)),
  'richardson_gradient_within_tolerance': bool(infnorm(g_rich)<=grad_tol),
  'richardson_gradient_correction_le_one_third_tolerance': bool(rich_correction<=grad_tol/3.0),
  'richardson_hessian_positive_definite': bool(float(eig_rich[0])>1e-8),
  'no_scale_has_exact_improvement_beyond_tolerance': bool(all(float(d.get('best_improvement_from_center',math.inf))<=improve_tol for d in D)),
}
summary={
  'stage':'4D3-multiscale-Richardson-audit',
  'mapping':D[0]['mapping'],'lambda_D':D[0]['lambda_D'],'scales':scales,
  'center_score_spread':score_spread,
  'gradient_inf_norm_by_scale':[infnorm(g) for g in G],
  'gradient_difference_coarse_to_mid_inf':g_diff_coarse,
  'gradient_difference_mid_to_fine_inf':g_diff_fine,
  'gradient_difference_ratio_expected_about_4_if_Oh2_dominates':g_ratio,
  'richardson_gradient':g_rich.tolist(),
  'richardson_gradient_inf_norm':infnorm(g_rich),
  'richardson_gradient_correction_inf':rich_correction,
  'hessian_fro_difference_coarse_to_mid':h_diff_coarse,
  'hessian_fro_difference_mid_to_fine':h_diff_fine,
  'hessian_difference_ratio_expected_about_4_if_Oh2_dominates':h_ratio,
  'richardson_hessian_eigenvalues':eig_rich.tolist(),
  'gradient_tolerance':grad_tol,'improvement_tolerance':improve_tol,
  'gates':gates,'multiscale_pass':bool(all(gates.values())),
  'warning':'Numerical local-convergence audit only; not global optimality, posterior evidence, or significance.'
}
print('STAGE4D3_MULTISCALE_RESULT',json.dumps(summary,sort_keys=True))
print('STAGE4D3_MULTISCALE_'+('PASS' if summary['multiscale_pass'] else 'FAIL'))
