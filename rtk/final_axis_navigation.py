#!/usr/bin/env python3
"""Low-budget 7D exact navigation gate for the candidate-final objective.

Usage:
  python3 final_axis_navigation.py PLANCK_DIR MAPPING lam h Ob Om As ns zre expected_S scale

The imported ``inference_core`` must already be built by
``prepare_final_inference_core.py``.  This script evaluates the exact center,
+/- one step on each of the seven Stage4D3 coordinates (15 points total), then
one conservative separable-quadratic proposal when positive diagonal curvature
exists.  It is deliberately *not* a stationarity test: no cross-Hessian is
constructed and no PASS marker can be interpreted as local stationarity.

Decision rule: if any exact point improves the supplied center by >0.005, that
point is a recenter candidate.  Otherwise a full strict cross-Hessian is the
next required gate.
"""
from pathlib import Path
import csv, json, math, sys
import numpy as np
import inference_core as L

if len(sys.argv) != 12:
    raise SystemExit('usage: final_axis_navigation.py PLANCK_DIR MAPPING lam h Ob Om As ns zre expected_S scale')

MAPPING=sys.argv[2].lower()
if MAPPING not in ('eff','k01'):
    raise SystemExit('mapping must be eff or k01')
CENTER={
 'lam':float(sys.argv[3]),'h':float(sys.argv[4]),'Ob':float(sys.argv[5]),
 'Om':float(sys.argv[6]),'As':float(sys.argv[7]),'ns':float(sys.argv[8]),
 'zre':float(sys.argv[9]),
}
EXPECTED=float(sys.argv[10]); SCALE=float(sys.argv[11])
if not (SCALE>0 and math.isfinite(SCALE)):
    raise SystemExit('scale must be positive finite')

IMPROVEMENT_TOL=0.005
CENTER_REG_TOL=1e-6
BASE={
 'loglam':0.05,'h':0.00035,'Ob':0.00007,'Om':0.00070,
 'As':4.0e-12,'ns':0.00035,'zre':0.070,
}
AXES=list(BASE)
OUT=Path('output/final_axis_navigation')/MAPPING/f'scale_{SCALE:g}'
OUT.mkdir(parents=True,exist_ok=True)
ROWS=[]; EVALS={}

def target(r):
    return float(r['score'] if MAPPING=='eff' else r['score_k01'])

def cleanup(tag):
    if not tag:return
    for q in L.OUT.glob(tag+'_*'):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:q.unlink()
        except OSError:pass

def shift(center,axis,u_base):
    p=dict(center)
    if axis=='loglam': p['lam']=center['lam']*math.exp(u_base*BASE[axis])
    else: p[axis]=center[axis]+u_base*BASE[axis]
    return p

def key(p):
    return tuple(float(p[k]).hex() for k in ('lam','h','Ob','Om','As','ns','zre'))

def evaluate(p,label,u=None):
    k=key(p)
    if k in EVALS:return EVALS[k]
    L.CACHE.clear()
    r=L.evaluate('RTK',dict(p))
    if not r.get('ok'):
        raise RuntimeError(f'{label}: {r}')
    rr=dict(r); rr['params']=dict(p); rr['label']=label; rr['u']=u
    EVALS[k]=rr
    row={'label':label,'target':target(rr),**p}
    if u is not None:
        for a in AXES: row['u_'+a]=float(u.get(a,0.0))
    for q in ('score','score_k01','logL_planck','logL_high','logL_lowT','logL_lowE','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):
        row[q]=rr.get(q)
    ROWS.append(row); cleanup(rr.get('tag'))
    print('FINAL_AXIS_POINT',json.dumps(row,sort_keys=True),flush=True)
    return rr

zero={a:0.0 for a in AXES}
r0=evaluate(CENTER,'center',zero); S0=target(r0)
reg=S0-EXPECTED
print('FINAL_AXIS_CENTER_REGRESSION',json.dumps({'score':S0,'expected':EXPECTED,'delta':reg,'tol':CENTER_REG_TOL},sort_keys=True),flush=True)
if abs(reg)>CENTER_REG_TOL:
    raise RuntimeError(f'center regression failed: {reg}')

samples={}
for a in AXES:
    samples[a]={0:r0}
    for sign in (-1,+1):
        u=sign*SCALE
        uv={x:0.0 for x in AXES};uv[a]=u
        samples[a][sign]=evaluate(shift(CENTER,a,u),f'{a}_{sign:+d}',uv)

# Derivatives are expressed in units of the *base* Stage4D3 steps, not the
# current scaled stencil step. This makes gradients comparable across scales.
diag={}; proposal_u={a:0.0 for a in AXES}
for a in AXES:
    fm=target(samples[a][-1]); f0=S0; fp=target(samples[a][+1])
    g=(fp-fm)/(2.0*SCALE)
    h=(fp-2.0*f0+fm)/(SCALE*SCALE)
    info={'f_minus':fm,'f0':f0,'f_plus':fp,'gradient_base_scaled':g,'diag_hessian_base_scaled':h}
    if h>0 and math.isfinite(h):
        raw=-g/h
        # Conservative: never combine more than 0.8 of the sampled radius on
        # any coordinate. The proposal is exact-evaluated, never trusted as a
        # surrogate result.
        u=float(np.clip(raw,-0.8*SCALE,0.8*SCALE))
        proposal_u[a]=u;info['quadratic_u_raw']=raw;info['quadratic_u_clipped']=u
    else:
        info['quadratic_u_raw']=None;info['quadratic_u_clipped']=0.0
    diag[a]=info

# Build the combined proposal sequentially so log(lambda) remains multiplicative.
pp=dict(CENTER)
for a in AXES:
    if proposal_u[a]==0:continue
    if a=='loglam': pp['lam']=pp['lam']*math.exp(proposal_u[a]*BASE[a])
    else: pp[a]=pp[a]+proposal_u[a]*BASE[a]
rq=evaluate(pp,'diag_quadratic_exact',proposal_u)

valid=list(EVALS.values()); best=min(valid,key=target); bestS=target(best)
improvement=S0-bestS
axis_only=[r for r in valid if r['label']!='diag_quadratic_exact']
best_axis=min(axis_only,key=target); best_axis_gain=S0-target(best_axis)
maxgrad=max(abs(diag[a]['gradient_base_scaled']) for a in AXES)
summary={
 'stage':'candidate-final-axis-navigation',
 'scope':'exact_axis_navigation_not_stationarity_not_global',
 'mapping':MAPPING,'scale':SCALE,'center':CENTER,'center_S':S0,
 'expected_center_S':EXPECTED,'center_regression_delta':reg,
 'improvement_tolerance':IMPROVEMENT_TOL,
 'base_steps':BASE,'diagonal_geometry':diag,
 'max_abs_gradient_base_scaled':maxgrad,
 'proposal_u_base_units':proposal_u,
 'proposal_S':target(rq),
 'best_axis_label':best_axis['label'],'best_axis_S':target(best_axis),
 'best_axis_improvement':best_axis_gain,
 'best_label':best['label'],'best_S':bestS,'best_params':best['params'],
 'best_improvement':improvement,
 'recenter_required':bool(improvement>IMPROVEMENT_TOL),
 'next_gate':('recenter_on_best_exact_point' if improvement>IMPROVEMENT_TOL else 'full_strict_cross_hessian_required'),
 'exact_likelihood_calls':int(L.COUNTER),
}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
fields=[]
for row in ROWS:
    for k in row:
        if k not in fields:fields.append(k)
with (OUT/'trace.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(ROWS)
print('FINAL_AXIS_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('FINAL_AXIS_NAVIGATION_COMPLETE',flush=True)
