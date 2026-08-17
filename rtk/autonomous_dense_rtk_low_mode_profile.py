#!/usr/bin/env python3
"""Targeted exact matched-dense RTK profile along a supplied Hessian low mode.

This worker is intentionally cheap compared with a full 7D Hessian.  It is a
conditional diagnostic for a repeated tiny non-positive curvature mode and is
not launched automatically before the base Hessian is known.

Environment:
  RTK_LOW_MODE_DIRECTION = 7 comma-separated y-space components in order
      loglam,h,Ob,Om,As,ns,zre. Default is the pure loglam axis.
  RTK_LOW_MODE_OFFSETS = comma-separated scalar offsets. Default spans ±8.
"""
from pathlib import Path
import hashlib, json, math, os, subprocess, sys, time
import numpy as np

sys.argv=['autonomous_dense_rtk_low_mode_profile','planck_data']
import inference_core as L

STATE=json.loads(Path('../research/state/current.json').read_text())
CENTER=dict(STATE['rtk']['accepted_center'])
bs=STATE['rtk']['base_steps']
BASE=[('loglam',float(bs['loglam'])),('h',float(bs['h'])),('Ob',float(bs['Ob'])),('Om',float(bs['Om'])),('As',float(bs['As'])),('ns',float(bs['ns'])),('zre',float(bs['zre']))]
ORDER=[x[0] for x in BASE]
DENSE=STATE['objective']['dense_z_pk']; ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
OUT=Path('output/autonomous_dense_rtk_low_mode'); OUT.mkdir(parents=True,exist_ok=True)
POINTS=OUT/'points.jsonl'; FAILURES=OUT/'failures.jsonl'

def parse_vec():
    raw=os.environ.get('RTK_LOW_MODE_DIRECTION','1,0,0,0,0,0,0')
    v=np.array([float(x) for x in raw.split(',')],float)
    if v.size!=7 or not np.all(np.isfinite(v)): raise RuntimeError(f'invalid direction {raw!r}')
    n=float(np.linalg.norm(v))
    if not (n>0): raise RuntimeError('zero low-mode direction')
    v=v/n
    if abs(v[0])>1e-14 and v[0]<0: v=-v
    return v

def parse_offsets():
    raw=os.environ.get('RTK_LOW_MODE_OFFSETS','-8,-4,-2,-1,-0.5,-0.25,0,0.25,0.5,1,2,4,8')
    x=sorted(set(float(t) for t in raw.split(',')))
    if 0.0 not in x or any(not math.isfinite(t) for t in x): raise RuntimeError(f'invalid offsets {raw!r}')
    return x
DIR=parse_vec(); OFFSETS=parse_offsets()

def canon(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
CENTER_FP=canon({'model':'RTK','center':CENTER,'objective':STATE['objective']['name'],'mapping':STATE.get('production_mapping','eff')})

def git_head(path):
    try:return subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return None

orig=L.make_ini
def make_ini(model,p,tag):
    path=orig(model,p,tag); text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text: raise RuntimeError('production sparse z_pk line not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text); f.write('\n# targeted exact low-mode profile on frozen matched-dense objective\n')
        for k,v in ULTRA.items(): f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini

def params_at(t):
    y=t*DIR; p=dict(CENTER); p['lam']=CENTER['lam']*math.exp(float(y[0])*BASE[0][1])
    for yi,(name,step) in zip(y[1:],BASE[1:]): p[name]=CENTER[name]+float(yi)*step
    return p,y

def cleanup(tag):
    if not tag:return
    for p in L.OUT.glob(tag+'_*'):
        try:p.unlink()
        except OSError:pass
    for p in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:p.unlink()
        except OSError:pass

def append(path,row):
    with path.open('a') as f:f.write(json.dumps(row,sort_keys=True,default=str)+'\n');f.flush()

def ev(t):
    p,y=params_at(t); last=None
    for attempt in range(1,4):
        L.CACHE.clear()
        try:r=L.evaluate('RTK',p)
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            row={'t':t,'attempt':attempt,'y':y.tolist(),'params':p,'score_eff':float(r['score']),'score_k01':float(r['score_k01']),'center_fingerprint':CENTER_FP}
            append(POINTS,row); cleanup(r.get('tag')); print('RTK_LOW_MODE_POINT',json.dumps(row,sort_keys=True),flush=True); return row
        last=r; fail={'t':t,'attempt':attempt,'y':y.tolist(),'params':p,'result':r}; append(FAILURES,fail); cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3:time.sleep(2*attempt)
    raise RuntimeError(f'low-mode t={t} failed after retries: {last}')

rows=[ev(t) for t in OFFSETS]
r0=next(r for r in rows if r['t']==0.0)
best_eff=min(rows,key=lambda r:r['score_eff']); best_k01=min(rows,key=lambda r:r['score_k01'])
summary={'stage':'targeted-dense-rtk-low-mode-profile','objective':STATE['objective']['name'],'state_iteration':STATE.get('iteration'),'center':CENTER,'center_fingerprint':CENTER_FP,'order':ORDER,'base_steps':dict(BASE),'direction_y':DIR.tolist(),'offsets':OFFSETS,'provenance':{'rtk_source_commit':git_head('..'),'class_upstream_commit':git_head('.'),'pantheon_commit':git_head('pantheon'),'numpy_version':np.__version__},'eff':{'S_center':r0['score_eff'],'best_exact_S':best_eff['score_eff'],'best_improvement':r0['score_eff']-best_eff['score_eff'],'best_t':best_eff['t'],'best_params':best_eff['params']},'k01':{'S_center':r0['score_k01'],'best_exact_S':best_k01['score_k01'],'best_improvement':r0['score_k01']-best_k01['score_k01'],'best_t':best_k01['t'],'best_params':best_k01['params']},'warning':'Conditional exact local profile only; not a global minimum, posterior, evidence, or replacement for the Stage4D3 half-stencil gate.'}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('RTK_LOW_MODE_PROFILE_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('RTK_LOW_MODE_PROFILE_COMPLETE',flush=True)
