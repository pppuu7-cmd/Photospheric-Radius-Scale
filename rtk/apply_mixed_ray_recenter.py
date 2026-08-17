#!/usr/bin/env python3
"""Apply the predeclared recenter rule to the exact mixed-mode ray result.

This script is intentionally narrow: it consumes run 32079620601 only, validates
its identity against the current accepted RTK center and frozen objective, and
restarts stationarity if the exact ray improvement exceeds the frozen 0.005
threshold. It never changes the objective, tolerance, mapping, or LCDM state.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'research/state/current.json'
RAY=Path('mixed_ray_artifact/summary.json')
EXPECTED_RUN=32079620601
EXPECTED_BASE_RUN=32065998894
EXPECTED_FP='78171ac0528a3436969a6d5c58f6db376c0643aee736d1b1b2c0c7633066fbef'
EXPECTED_OBJECTIVE='matched-ultra-linstep2+dense-BOSS'


def exact_center_equal(a,b):
    keys=('lam','h','Ob','Om','As','ns','zre')
    return all(float(a[k])==float(b[k]) for k in keys)


def main():
    state=json.loads(STATE.read_text())
    ray=json.loads(RAY.read_text())
    tol=float(state['objective']['recenter_tolerance_S'])
    if state['objective']['name']!=EXPECTED_OBJECTIVE:
        raise RuntimeError('frozen objective changed; refusing mixed-ray transition')
    if ray.get('objective')!=EXPECTED_OBJECTIVE or ray.get('base_hessian_run')!=EXPECTED_BASE_RUN:
        raise RuntimeError('mixed-ray objective/base-run identity mismatch')
    if ray.get('center_fingerprint')!=EXPECTED_FP:
        raise RuntimeError('mixed-ray center fingerprint mismatch')
    if not exact_center_equal(ray.get('center',{}),state['rtk']['accepted_center']):
        raise RuntimeError('mixed-ray center is no longer the accepted RTK center')
    imp=float(ray['best_improvement'])
    if not imp>tol:
        raise RuntimeError(f'mixed-ray improvement {imp} does not exceed frozen tolerance {tol}')
    best=ray.get('best_params')
    if not isinstance(best,dict):
        raise RuntimeError('best_params missing')

    rtk=state['rtk']
    if rtk.get('hessian_result') is not None:
        rtk.setdefault('hessian_history',[]).append(rtk['hessian_result'])
    rtk.setdefault('mixed_mode_ray_history',[]).append({
        'run_id':EXPECTED_RUN,
        'base_hessian_run':EXPECTED_BASE_RUN,
        'center_fingerprint':EXPECTED_FP,
        'best_improvement':imp,
        'best_t':ray.get('best_t'),
        'best_exact_S':ray.get('best_exact_S'),
        'best_params':best,
        'artifact_id':9305064814,
        'artifact_digest':'sha256:fcbdf2d0a24a7b8a6c3272894a86d21d14bbb3daf5567d243233d49acecc2058',
        'classification':ray.get('classification'),
    })
    old_half=rtk.get('half_hessian_run')
    if old_half is not None:
        stale=dict(old_half)
        stale['stale_reason']='accepted_center_recentered_by_exact_mixed_mode_ray'
        stale['old_center']=dict(rtk['accepted_center'])
        rtk.setdefault('stale_half_hessian_runs',[]).append(stale)

    rtk['accepted_center']=dict(best)
    rtk['accepted_score_eff']=None
    rtk['accepted_score_params']=None
    rtk['accepted_score_semantics']='pending_stationarity_after_mixed_mode_recenter'
    rtk['raw_candidate_certification']='pending_stationarity_after_mixed_mode_recenter'
    rtk['hessian_result']=None
    rtk['hessian_run']=None
    rtk['half_hessian_result']=None
    rtk['half_hessian_run']=None
    rtk['quarter_hessian_run']=None
    rtk['multiscale_curvature']=None
    rtk['axis_result']=None
    rtk['axis_run']={
        'run_id':None,
        'workflow':'rtk-autonomous-dense-rtk-axis.yml',
        'artifact':'rtk-autonomous-dense-rtk-axis',
        'status':'requested',
    }
    rtk['certification']='needs_recenter_from_exact_mixed_mode_ray'
    rtk['interior_minimum_certification']='N5_RESTART_AFTER_EXACT_MIXED_RAY_DOWNHILL'
    state['stage']='rtk_axis_recenter_running'
    state['comparison']={'status':'pending_matched_stationarity','dense_raw_delta_S':None}
    state['dispatch']={
        'iteration':state.get('iteration'),
        'workflow':'rtk-autonomous-dense-rtk-axis.yml',
        'ref':'main',
        'target':'rtk_axis',
        'status':'submitted_by_mixed_ray_transition',
        'reason':f'exact mixed-mode ray improvement {imp:.12g} > {tol}',
    }
    STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n')
    print('RTK_MIXED_RAY_RECENTER_APPLIED',json.dumps({
        'improvement':imp,'tolerance':tol,'best_t':ray.get('best_t'),
        'best_exact_S':ray.get('best_exact_S'),'new_center':best,
    },sort_keys=True))


if __name__=='__main__':
    main()
