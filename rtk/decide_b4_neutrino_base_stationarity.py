#!/usr/bin/env python3
"""Produce the preregistered B4 base-Hessian decision for RTK and LCDM."""
from pathlib import Path
import hashlib,json,math,sys

if len(sys.argv)!=3:
    raise SystemExit('usage: decide_b4_neutrino_base_stationarity.py RTK_SUMMARY LCDM_SUMMARY')
ROOT=Path(__file__).resolve().parents[1]
T=json.loads((ROOT/'research/robustness/b4_neutrino_stationarity_targets_v1.json').read_text())
TOL=float(T['recenter_tolerance_S'])

def canon(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
expected_target_fp=canon(T)

def one(model,path):
    s=json.loads(Path(path).read_text());cfg=T['models'][model]
    if s.get('classification')!='B4_NEUTRINO_STATIONARITY_HESSIAN_COMPLETE':raise RuntimeError(f'{model}: wrong classification')
    if s.get('model')!=model or s.get('objective')!=T['objective']:raise RuntimeError(f'{model}: identity mismatch')
    if s.get('center')!=cfg['center']:raise RuntimeError(f'{model}: center mismatch')
    if int(s.get('source_seed_run_id',-1))!=int(T['source_seed_run_id']):raise RuntimeError(f'{model}: seed run mismatch')
    if abs(float(s.get('stencil_scale',-1))-1.0)>1e-15:raise RuntimeError(f'{model}: not base scale')
    if s.get('target_fingerprint')!=expected_target_fp:raise RuntimeError(f'{model}: target fingerprint mismatch')
    e=s.get('eff') or {};k=s.get('k01') or {}
    imp=float(e.get('best_improvement',math.inf));pd=bool(e.get('positive_definite'))
    if not math.isfinite(imp):raise RuntimeError(f'{model}: invalid improvement')
    reclear=imp<=TOL
    return {
      'base_S_center':float(e['S_center']),'base_best_exact_S':float(e['best_exact_S']),'base_best_improvement':imp,
      'base_best_label':e.get('best_label'),'base_best_params':e.get('best_params'),
      'base_positive_definite':pd,'base_eigenvalues_y':e.get('eigenvalues_y'),
      'k01_S_center':float(k['S_center']),'k01_best_exact_S':float(k['best_exact_S']),'k01_best_improvement':float(k['best_improvement']),
      'k01_positive_definite':bool(k.get('positive_definite')),
      'base_recenter_clear':reclear,
      'recenter_required':not reclear,
      'same_scale_exact_ray_required':bool(reclear and not pd),
      'half_allowed':bool(reclear and pd),
      'decision':('RECENTER_RESTART' if not reclear else ('BASE_NONPD_REQUIRE_EXACT_RAY' if not pd else 'BASE_PD_REQUIRES_HALF')),
      'summary_provenance':s.get('provenance'),
    }

models={'RTK':one('RTK',sys.argv[1]),'LCDM':one('LCDM',sys.argv[2])}
out={
 'classification':'B4_NEUTRINO_BASE_STATIONARITY_DECISION_V1',
 'objective':T['objective'],'source_seed_run_id':T['source_seed_run_id'],'source_base_run_id':32236524767,
 'recenter_tolerance_S':TOL,'target_fingerprint':expected_target_fp,'models':models,
 'paired_half_dispatch_allowed':all(x['half_allowed'] for x in models.values()),
 'warning':'Base-scale local stationarity decision only. No B4 minimum or model-selection claim.'
}
print('B4_NEUTRINO_BASE_STATIONARITY_DECISION_V1',json.dumps(out,sort_keys=True))
if len(sys.argv)>0:
    p=ROOT/'research/robustness/b4_neutrino_base_stationarity_decision_v1.json'
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
