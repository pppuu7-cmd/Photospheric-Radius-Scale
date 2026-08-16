#!/usr/bin/env python3
"""Exact correlated-ray gate around the current Stage4D3 center.

Evaluates symmetric rays along a supplied base-scaled gradient direction.
A recenter is allowed only if an exact point improves S by more than the
configured improvement tolerance. This is a local gate, not a global proof.
"""
from pathlib import Path
import csv, json, math, os, sys
import numpy as np
import inference_core as L

if len(sys.argv) != 18:
    raise SystemExit('usage: PLANCK_DIR mapping lam h Ob Om As ns zre expected g0..g6')
MAPPING=sys.argv[2].lower(); LAM=float(sys.argv[3])
vals=list(map(float,sys.argv[4:10])); EXPECT=float(sys.argv[10])
gbase=np.array(list(map(float,sys.argv[11:18])),float)
if MAPPING not in ('eff','k01') or not (LAM>0 and np.all(np.isfinite(gbase))): raise SystemExit('bad input')
CENTER={'lam':LAM,**dict(zip(('h','Ob','Om','As','ns','zre'),vals))}
BASE=[('loglam',0.05),('h',0.00035),('Ob',0.00007),('Om',0.00070),('As',4e-12),('ns',0.00035),('zre',0.070)]
TOL=float(os.environ.get('RTK_STATIONARITY_IMPROVEMENT_TOL','0.005'))
OUT=Path('output/stage4d3_correlated_ray')/MAPPING/f'{LAM:.0f}'; OUT.mkdir(parents=True,exist_ok=True)

def score(r): return float(r['score'] if MAPPING=='eff' else r['score_k01'])
def params_from_base_delta(d):
    p=dict(CENTER)
    p['lam']=LAM*math.exp(float(d[0])*BASE[0][1])
    for di,(n,s) in zip(d[1:],BASE[1:]): p[n]=CENTER[n]+float(di)*s
    return p

def cleanup(tag):
    if not tag:return
    for p in L.OUT.glob(tag+'_*'):
        try:p.unlink()
        except OSError:pass
    for p in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:p.unlink()
        except OSError:pass

def ev(d,label):
    p=params_from_base_delta(d); r=L.evaluate('RTK',p)
    if not r.get('ok'): raise RuntimeError(f'{label}: {r}')
    S=score(r); cleanup(r.get('tag')); print('CORRELATED_RAY_EVAL',label,S,flush=True)
    row={'label':label,'S':S,**p}; rows.append(row); return S,p

norm=float(np.linalg.norm(gbase))
if not norm>0: raise SystemExit('zero gradient direction')
u=-gbase/norm
rows=[]
S0,p0=ev(np.zeros(7),'center')
if abs(S0-EXPECT)>0.03: raise SystemExit(f'center regression: {S0} vs {EXPECT}')
# Symmetric exact rays spanning sub-stencil through multi-base-step distances.
amps=[0.125,0.25,0.5,1.0,2.0]
best=(S0,p0,'center',0.0)
for a in amps:
    for sgn in (-1.0,1.0):
        t=sgn*a; S,p=ev(t*u,f'ray_{t:+.3f}')
        if S<best[0]: best=(S,p,f'ray_{t:+.3f}',t)
improvement=S0-best[0]
recenter_allowed=bool(improvement>TOL)
summary={'stage':'4D3-correlated-ray','mapping':MAPPING,'S_center':S0,'expected_S':EXPECT,
         'gradient_base_scaled':gbase.tolist(),'descent_unit_vector_base':u.tolist(),
         'amplitudes':amps,'best_exact_S':best[0],'best_label':best[2],
         'best_params':best[1],'best_improvement_from_center':improvement,
         'improvement_tolerance':TOL,'recenter_allowed':recenter_allowed,
         'gate':'RECENTER' if recenter_allowed else 'NO_RECENTER_CORRELATED_RAY_CLEAR',
         'warning':'Local exact correlated-ray gate only; not a global statistical proof.'}
(OUT/'correlated_ray_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
with (OUT/'correlated_ray_points.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print('STAGE4D3_CORRELATED_RAY_RESULT',json.dumps(summary,sort_keys=True),flush=True)
