#!/usr/bin/env python3
"""Checkpointed low-budget exact LCDM local refinement at matched ultra CLASS precision.

Local numerical control only; not a global fit or posterior. The previous v1
stopped because it compared a fresh exact center against an older harvested
Powell value and treated a *lower* fresh score as a regression failure.  This
version freezes the fresh exact center reproduced by both mappings in run
31935158052 and only rejects a genuine mismatch of that objective.
"""
from pathlib import Path
import csv, json, math, sys
import numpy as np
import inference_core as L

MAPPING=(sys.argv[2] if len(sys.argv)>2 else 'eff').lower()
if MAPPING not in ('eff','k01'): raise SystemExit('mapping must be eff or k01')
CENTER={'lam':0.0,'h':0.6779337587382693,'Ob':0.04872764689799632,'Om':0.26187225794495356,
        'As':2.1094040998203598e-9,'ns':0.9649685632254442,'zre':7.8583129349509475}
# Fresh exact matched-ultra reproduction from failed-v1 run 31935158052.
EXPECTED={'eff':1050.2269760031668,'k01':1050.2285287876086}
AXES=['h','Ob','Om','As','ns','zre']
STEP={'h':4e-5,'Ob':4e-6,'Om':2e-5,'As':4e-13,'ns':2e-5,'zre':1.5e-3}
ULTRA={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7',
       'perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180',
       'k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2'}
OUT=Path('output/lcdm_ultra_stencil_refine_v2')/MAPPING; OUT.mkdir(parents=True,exist_ok=True)
TRACE=OUT/'trace.csv'; SUMMARY=OUT/'summary.json'; ROWS=[]; CACHE={}
orig=L.make_ini
def make_ini(model,p,tag):
    path=orig(model,p,tag)
    with Path(path).open('a') as f:
        f.write('\n# matched ultra precision overrides\n')
        for k,v in ULTRA.items(): f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini
def target(r): return float(r['score'] if MAPPING=='eff' else r['score_k01'])
def key(p): return tuple(float(p[k]).hex() for k in AXES)
def cleanup(tag):
    if not tag:return
    for q in L.OUT.glob(tag+'_*'):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:q.unlink()
        except OSError:pass
def persist(status='running'):
    valid=[r for r in CACHE.values() if r.get('ok')]; best=min(valid,key=target) if valid else None
    s={'stage':'lcdm-ultra-stencil-refine-v2','status':status,'scope':'local_exact_control_not_global',
       'mapping':MAPPING,'ultra_overrides':ULTRA,'initial_center':CENTER,'initial_expected':EXPECTED[MAPPING],
       'base_steps':STEP,'exact_calls':int(L.COUNTER),'unique_points':len(CACHE),
       'best_S':target(best) if best else None,'best_params':best.get('params') if best else None,
       'best_components':({q:best.get(q) for q in ('score','score_k01','logL_planck','logL_high','logL_lowT','logL_lowE','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')} if best else None)}
    SUMMARY.write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
    if ROWS:
        fields=[]
        for r in ROWS:
            for k in r:
                if k not in fields: fields.append(k)
        with TRACE.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(ROWS)
    return s
def ev(p,label):
    p=dict(p);p['lam']=0.0;k=key(p)
    if k in CACHE:return CACHE[k]
    try:r=L.evaluate('LCDM',p)
    except Exception as e:r={'ok':False,'reason':repr(e)}
    if not r.get('ok'):
        rr={'ok':False,'reason':r.get('reason',str(r)),'params':p};CACHE[k]=rr;persist('evaluation_failure');return rr
    rr=dict(r);rr['params']=p;CACHE[k]=rr
    row={'label':label,'target':target(rr),**{a:p[a] for a in AXES}}
    for q in ('score','score_k01','logL_planck','logL_high','logL_lowT','logL_lowE','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):row[q]=rr.get(q)
    ROWS.append(row);cleanup(rr.get('tag'));persist();print('LCDM_STENCIL_POINT',json.dumps(row,sort_keys=True),flush=True);return rr
def poll(c,steps,label):
    rc=ev(c,label+'_center'); vals={}
    for a in AXES:
        vals[a]={0:(c[a],target(rc))}
        for sg in (-1,1):
            p=dict(c);p[a]=c[a]+sg*steps[a];r=ev(p,f'{label}_{a}_{sg:+d}')
            if r.get('ok'):vals[a][sg]=(p[a],target(r))
    return vals
def proposal(c,steps,vals,lim=.8):
    p=dict(c);diag={}
    for a in AXES:
        fm,f0,fp=vals[a][-1][1],vals[a][0][1],vals[a][1][1];g=(fp-fm)/2;h=fp-2*f0+fm
        x=float(np.clip(-g/h,-lim,lim)) if h>0 and math.isfinite(h) else float(min([(-1,fm),(0,f0),(1,fp)],key=lambda z:z[1])[0])
        p[a]=c[a]+x*steps[a];diag[a]={'g_step':g,'h_step':h,'x_norm':x}
    return p,diag
r0=ev(CENTER,'initial')
if not r0.get('ok'):raise SystemExit('initial failed')
reg=target(r0)-EXPECTED[MAPPING];print('LCDM_STENCIL_CENTER_REGRESSION_V2',MAPPING,reg,flush=True)
if abs(reg)>1e-6:raise SystemExit(f'fresh center objective mismatch: {reg}')
v1=poll(CENTER,STEP,'s1');p1,d1=proposal(CENTER,STEP,v1);ev(p1,'quad1')
best1=min([r for r in CACHE.values() if r.get('ok')],key=target);c2=dict(best1['params']);step2={a:.5*STEP[a] for a in AXES}
v2=poll(c2,step2,'s2');p2,d2=proposal(c2,step2,v2);ev(p2,'quad2')
best=min([r for r in CACHE.values() if r.get('ok')],key=target);s=persist('complete');s['quadratic_diagnostics']={'pass1':d1,'pass2':d2};s['improvement_vs_fresh_initial']=EXPECTED[MAPPING]-target(best);SUMMARY.write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
print('LCDM_ULTRA_STENCIL_V2_RESULT',json.dumps(s,sort_keys=True),flush=True);print('LCDM_ULTRA_STENCIL_V2_COMPLETE',flush=True)
