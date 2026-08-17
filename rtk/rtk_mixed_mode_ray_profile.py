#!/usr/bin/env python3
"""Exact frozen-objective ray profile along the negative mixed mode from run 32065998894.

The base 7D Hessian at the accepted center is recenter-clear on its 101 tested
points but has one negative eigenvalue.  This worker evaluates exact likelihood
points directly along that eigenvector, which the axis/corner stencil does not
sample.  It is a diagnostic/recenter falsification test, not a new objective.
"""
from pathlib import Path
import hashlib, json, math, os, subprocess, sys, time
import numpy as np

sys.argv=['rtk_mixed_mode_ray_profile','planck_data']
import inference_core as L

STATE=json.loads(Path('../research/state/current.json').read_text())
CENTER=dict(STATE['rtk']['accepted_center'])
EXPECTED_CENTER={
    'As':2.0874341676903437e-09,
    'Ob':0.046834883174647964,
    'Om':0.25274346988872953,
    'h':0.6906937726797984,
    'lam':219966.90504044993,
    'ns':0.9644273896355182,
    'zre':7.317081734823917,
}
if any(float(CENTER[k])!=float(EXPECTED_CENTER[k]) for k in EXPECTED_CENTER):
    raise RuntimeError(f'accepted center changed; refusing stale mixed-mode profile: {CENTER}')

# Eigenvector of eff Hessian from base run 32065998894, ordered as
# [loglam,h,Ob,Om,As,ns,zre]. Sign chosen so h component is positive.
V=np.array([
    8.65188501e-05,
    7.15640269e-01,
   -3.76643177e-01,
   -4.16254198e-01,
   -3.30807047e-02,
    4.13552729e-01,
    2.47217568e-02,
],dtype=float)
V=V/np.linalg.norm(V)
BASE_RUN=32065998894
BASE_EIGENVALUE=-0.0044758233976694844
BASE_ARTIFACT_ID=9304537454
BASE_ARTIFACT_DIGEST='sha256:feff5d096411e270e1584a44fe24a3470e5d3178b6121bf18f89293d65c7bc22'

bs=STATE['rtk']['base_steps']
BASE=[('loglam',float(bs['loglam'])),('h',float(bs['h'])),('Ob',float(bs['Ob'])),('Om',float(bs['Om'])),('As',float(bs['As'])),('ns',float(bs['ns'])),('zre',float(bs['zre']))]
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE=STATE['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
orig=L.make_ini
OUT=Path('output/rtk_mixed_mode_ray_profile');OUT.mkdir(parents=True,exist_ok=True)


def canonical_hash(obj):
    raw=json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()

CENTER_FINGERPRINT=canonical_hash({'model':'RTK','center':CENTER,'objective':STATE['objective']['name'],'mapping':STATE.get('production_mapping','eff')})
if CENTER_FINGERPRINT!='78171ac0528a3436969a6d5c58f6db376c0643aee736d1b1b2c0c7633066fbef':
    raise RuntimeError(f'center fingerprint mismatch {CENTER_FINGERPRINT}')


def make_ini(model,p,tag):
    path=orig(model,p,tag);text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text:raise RuntimeError('production sparse z_pk line not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text);f.write('\n# exact current-center mixed Hessian eigenmode ray profile\n')
        for k,v in ULTRA.items():f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini


def pars(t):
    y=float(t)*V
    p=dict(CENTER)
    p['lam']=CENTER['lam']*math.exp(float(y[0])*BASE[0][1])
    for yi,(name,step) in zip(y[1:],BASE[1:]):
        p[name]=CENTER[name]+float(yi)*step
    return p,y


def cleanup(tag):
    if not tag:return
    for q in L.OUT.glob(tag+'_*'):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:q.unlink()
        except OSError:pass


def evaluate(t):
    p,y=pars(t);last=None
    for attempt in range(1,4):
        L.CACHE.clear()
        try:r=L.evaluate('RTK',p)
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            row={'t':float(t),'y':y.tolist(),'params':p,'attempt':attempt,
                 'score_eff':float(r['score']),'score_k01':float(r['score_k01'])}
            cleanup(r.get('tag'))
            print('RTK_MIXED_MODE_RAY_POINT',json.dumps(row,sort_keys=True),flush=True)
            return row
        last=r;cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3:time.sleep(2*attempt)
    raise RuntimeError(f't={t}: failed after exact retries: {last}')

T=[-2.0,-1.5,-1.0,-0.5,-0.25,0.0,0.25,0.5,1.0,1.5,2.0]
rows=[evaluate(t) for t in T]
by={r['t']:r for r in rows}
S0=by[0.0]['score_eff']
curv=[]
for t in (0.25,0.5,1.0,1.5,2.0):
    sp=by[t]['score_eff'];sm=by[-t]['score_eff']
    curv.append({'abs_t':t,
                 'symmetric_curvature_eff':(sp-2*S0+sm)/(t*t),
                 'symmetric_gradient_eff':(sp-sm)/(2*t),
                 'plus_improvement':S0-sp,
                 'minus_improvement':S0-sm})
best=min(rows,key=lambda r:r['score_eff'])
summary={
    'classification':'RTK_EXACT_MIXED_NEGATIVE_MODE_RAY_PROFILE',
    'objective':STATE['objective']['name'],
    'mapping':'eff',
    'center':CENTER,
    'center_fingerprint':CENTER_FINGERPRINT,
    'base_hessian_run':BASE_RUN,
    'base_artifact_id':BASE_ARTIFACT_ID,
    'base_artifact_digest':BASE_ARTIFACT_DIGEST,
    'base_eigenvalue':BASE_EIGENVALUE,
    'eigenvector_order':['loglam','h','Ob','Om','As','ns','zre'],
    'eigenvector':V.tolist(),
    'S_center':S0,
    'best_exact_S':best['score_eff'],
    'best_t':best['t'],
    'best_params':best['params'],
    'best_improvement':S0-best['score_eff'],
    'recenter_tolerance_S':float(STATE['objective']['recenter_tolerance_S']),
    'symmetric_scale_diagnostics':curv,
    'points':rows,
    'warning':'Exact diagnostic on the frozen objective along one Hessian eigenvector; not a global minimum proof or model-selection statistic.'
}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('RTK_MIXED_MODE_RAY_PROFILE_COMPLETE',json.dumps(summary,sort_keys=True),flush=True)
