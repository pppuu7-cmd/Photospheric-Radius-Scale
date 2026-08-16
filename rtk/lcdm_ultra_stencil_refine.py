#!/usr/bin/env python3
"""Checkpointed, low-budget exact LCDM local refinement at provisional ultra CLASS precision.

This is deliberately a local numerical refinement, not a global fit or posterior scan.
It replaces a slow two-start Powell run that hit the Actions timeout after finding a
substantially lower local candidate.  The algorithm is deterministic:
  1. evaluate the harvested partial-best center;
  2. evaluate +/- one axis step in all 6 LCDM nuisance coordinates;
  3. form one clipped separable-quadratic proposal and evaluate it exactly;
  4. recenter on the best exact point and repeat the axis poll at half steps;
  5. form/evaluate one second clipped quadratic proposal.
A JSON checkpoint and CSV trace are rewritten after every successful evaluation.
"""
from pathlib import Path
import csv, json, math, sys
import numpy as np
import inference_core as L

MAPPING=(sys.argv[2] if len(sys.argv)>2 else 'eff').lower()
if MAPPING not in ('eff','k01'):
    raise SystemExit('mapping must be eff or k01')

# Best common exact point harvested from the timed-out k01 ultra Powell run.
CENTER={
 'lam':0.0,
 'h':0.6779337587382693,
 'Ob':0.04872764689799632,
 'Om':0.26187225794495356,
 'As':2.1094040998203598e-9,
 'ns':0.9649685632254442,
 'zre':7.8583129349509475,
}
EXPECTED={'eff':1050.2310656457898,'k01':1050.2326184302317}
AXES=['h','Ob','Om','As','ns','zre']
STEP={
 'h':4.0e-5,
 'Ob':4.0e-6,
 'Om':2.0e-5,
 'As':4.0e-13,
 'ns':2.0e-5,
 'zre':1.5e-3,
}
ULTRA={
 'tol_background_integration':'3e-4',
 'tol_thermo_integration':'3e-4',
 'tol_perturb_integration':'3e-7',
 'perturb_sampling_stepsize':'0.0125',
 'k_per_decade_for_pk':'40',
 'k_per_decade_for_bao':'180',
 'k_max_tau0_over_l_max':'4.0',
 'l_logstep':'1.02',
 'l_linstep':'5',
}

OUT=Path('output/lcdm_ultra_stencil_refine')/MAPPING
OUT.mkdir(parents=True,exist_ok=True)
TRACE=OUT/'trace.csv'; SUMMARY=OUT/'summary.json'
ROWS=[]; CACHE={}
orig_make_ini=L.make_ini

def make_ini(model,p,tag):
    path=orig_make_ini(model,p,tag)
    with Path(path).open('a') as f:
        f.write('\n# provisional ultra precision overrides\n')
        for k,v in ULTRA.items(): f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini

def target(r):
    return float(r['score'] if MAPPING=='eff' else r['score_k01'])

def key(p):
    return tuple(float(p[k]).hex() for k in AXES)

def cleanup(tag):
    if not tag:return
    for q in L.OUT.glob(tag+'_*'):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:q.unlink()
        except OSError:pass

def persist(stage='running'):
    valid=[r for r in CACHE.values() if r.get('ok')]
    best=min(valid,key=target) if valid else None
    summary={
      'stage':'lcdm-ultra-stencil-refine','status':stage,'scope':'local_exact_refinement_not_global',
      'mapping':MAPPING,'ultra_overrides':ULTRA,'initial_center':CENTER,'initial_expected':EXPECTED[MAPPING],
      'base_steps':STEP,'exact_calls':int(L.COUNTER),'unique_points':len(CACHE),
      'best_S':target(best) if best else None,
      'best_params':best.get('params') if best else None,
      'best_components':({q:best.get(q) for q in ('score','score_k01','logL_planck','logL_high','logL_lowT','logL_lowE','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')} if best else None),
    }
    SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    if ROWS:
        fields=[]
        for r in ROWS:
            for k in r:
                if k not in fields: fields.append(k)
        with TRACE.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(ROWS)
    return summary

def evaluate(p,label):
    p=dict(p); p['lam']=0.0
    k=key(p)
    if k in CACHE:return CACHE[k]
    try:r=L.evaluate('LCDM',p)
    except Exception as e:r={'ok':False,'reason':repr(e)}
    if not r.get('ok'):
        rr={'ok':False,'reason':r.get('reason',str(r)),'params':p};CACHE[k]=rr;persist('evaluation_failure')
        print('LCDM_STENCIL_FAIL',label,rr['reason'],p,flush=True);return rr
    rr=dict(r);rr['params']=p;CACHE[k]=rr
    row={'label':label,'target':target(rr),**{a:p[a] for a in AXES}}
    for q in ('score','score_k01','logL_planck','logL_high','logL_lowT','logL_lowE','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):
        row[q]=rr.get(q)
    ROWS.append(row); cleanup(rr.get('tag')); persist('running')
    print('LCDM_STENCIL_POINT',json.dumps(row,sort_keys=True),flush=True)
    return rr

def axis_poll(center,steps,label):
    c=evaluate(center,label+'_center')
    vals={}
    for a in AXES:
        vals[a]={0:(center[a],target(c))}
        for s in (-1,+1):
            p=dict(center);p[a]=center[a]+s*steps[a]
            r=evaluate(p,f'{label}_{a}_{s:+d}')
            if r.get('ok'):vals[a][s]=(p[a],target(r))
    return vals

def quadratic_proposal(center,steps,vals,max_norm=0.8):
    p=dict(center); diag={}
    for a in AXES:
        if not all(s in vals[a] for s in (-1,0,1)):
            diag[a]={'used':False};continue
        fm=vals[a][-1][1]; f0=vals[a][0][1]; fp=vals[a][1][1]
        g=(fp-fm)/2.0
        hess=fp-2*f0+fm
        if hess>0 and math.isfinite(hess):
            x=float(np.clip(-g/hess,-max_norm,max_norm))
        else:
            candidates=[(-1,fm),(0,f0),(1,fp)];x=float(min(candidates,key=lambda z:z[1])[0])
            x=float(np.clip(x,-max_norm,max_norm))
        p[a]=center[a]+x*steps[a]
        diag[a]={'used':True,'g_step':g,'h_step':hess,'x_norm':x}
    return p,diag

# Center regression is intentionally strict enough to detect a changed objective,
# but wider than bit-level because the source point was harvested from a timed-out log.
r0=evaluate(CENTER,'initial')
if not r0.get('ok'):raise SystemExit('initial center failed')
reg=target(r0)-EXPECTED[MAPPING]
print('LCDM_STENCIL_CENTER_REGRESSION',MAPPING,target(r0),EXPECTED[MAPPING],reg,flush=True)
if abs(reg)>1e-6:raise SystemExit(f'center regression failed: {reg}')

v1=axis_poll(CENTER,STEP,'s1')
p1,d1=quadratic_proposal(CENTER,STEP,v1,0.8)
rp1=evaluate(p1,'quad1')
valid=[r for r in CACHE.values() if r.get('ok')]
best1=min(valid,key=target); c2=dict(best1['params'])
step2={a:0.5*STEP[a] for a in AXES}
v2=axis_poll(c2,step2,'s2')
p2,d2=quadratic_proposal(c2,step2,v2,0.8)
rp2=evaluate(p2,'quad2')

valid=[r for r in CACHE.values() if r.get('ok')]
best=min(valid,key=target)
summary=persist('complete')
summary['quadratic_diagnostics']={'pass1':d1,'pass2':d2}
summary['improvement_vs_initial']=EXPECTED[MAPPING]-target(best)
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('LCDM_ULTRA_STENCIL_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('LCDM_ULTRA_STENCIL_COMPLETE',flush=True)
