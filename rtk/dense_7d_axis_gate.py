#!/usr/bin/env python3
"""Cheap exact 7D axis gate on the matched-ultra+dense RTK objective.

Evaluates the Round5 center plus +/- one base step in log(lambda_D), h, Ob,
Om, As, ns, and zre. One CLASS evaluation yields both eff and k01 scores.
This is a recenter gate before any expensive full 7D cross/Hessian stencil.
"""
from pathlib import Path
import csv, json, math, sys

sys.argv=['dense_7d_axis_gate','planck_data']
import inference_core as L

CENTER={'lam':217225.01601516694,'h':0.6904831253428524,'Ob':0.046836300417955265,
        'Om':0.25300743080221694,'As':2.0837288833768707e-9,
        'ns':0.9643603115669437,'zre':7.21843542110055}
BASE=[('loglam',0.05),('h',0.00035),('Ob',0.00007),('Om',0.00070),
      ('As',4.0e-12),('ns',0.00035),('zre',0.070)]
TOL=0.005
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE='0.,0.25,0.30,0.34,0.36,0.37,0.38,0.39,0.40,0.42,0.47,0.49,0.50,0.51,0.52,0.53,0.55,0.57,0.59,0.60,0.61,0.62,0.63,0.65,0.70,0.75,1.0'
ULTRA={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7',
       'perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180',
       'k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2'}
orig=L.make_ini

def make_ini(model,p,tag):
    path=orig(model,p,tag); text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text: raise RuntimeError('production sparse z_pk line not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text); f.write('\n# matched-ultra+dense 7D axis gate\n')
        for k,v in ULTRA.items(): f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini

def cleanup(tag):
    if not tag:return
    for p in L.OUT.glob(tag+'_*'):
        try:p.unlink()
        except OSError:pass
    for p in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:p.unlink()
        except OSError:pass

def ev(p,label,axis='',sign=0):
    L.CACHE.clear(); r=L.evaluate('RTK',dict(p))
    if not r.get('ok'): raise RuntimeError(f'{label}: {r}')
    row={'label':label,'axis':axis,'sign':sign,'score_eff':float(r['score']),
         'score_k01':float(r['score_k01']),'logL_planck':float(r['logL_planck']),
         'chi2_SN':float(r['chi2_SN']),'chi2_BOSS_eff':float(r['chi2_BOSS_eff']),
         'chi2_BOSS_k01':float(r['chi2_BOSS_k01']),'rd':float(r['rd']),**p}
    rows.append(row); cleanup(r.get('tag'))
    print('DENSE_7D_AXIS_POINT',json.dumps(row,sort_keys=True),flush=True)
    return row

rows=[]
center=ev(CENTER,'center')
for q,s in BASE:
    for sign in (-1,1):
        p=dict(CENTER)
        if q=='loglam': p['lam']=CENTER['lam']*math.exp(sign*s)
        else: p[q]=CENTER[q]+sign*s
        ev(p,f'{q}_{sign:+d}',q,sign)

axis_stats={}
for q,_ in BASE:
    minus=next(r for r in rows if r['axis']==q and r['sign']==-1)
    plus=next(r for r in rows if r['axis']==q and r['sign']==1)
    axis_stats[q]={}
    for m,key in [('eff','score_eff'),('k01','score_k01')]:
        s0=center[key]; sm=minus[key]; sp=plus[key]
        axis_stats[q][m]={'central_difference':(sp-sm)/2.0,
                          'diagonal_curvature':sp-2.0*s0+sm,
                          'minus_score':sm,'plus_score':sp}

best_eff=min(rows,key=lambda r:r['score_eff'])
best_k01=min(rows,key=lambda r:r['score_k01'])
imp_eff=center['score_eff']-best_eff['score_eff']
imp_k01=center['score_k01']-best_k01['score_k01']
summary={'stage':'dense-7d-axis-gate','objective':'matched-ultra-linstep2+dense-BOSS',
         'center':CENTER,'center_score_eff':center['score_eff'],'center_score_k01':center['score_k01'],
         'base_steps':dict(BASE),'points':len(rows),'axis_stats':axis_stats,
         'best_eff':best_eff,'best_k01':best_k01,
         'best_improvement_eff':imp_eff,'best_improvement_k01':imp_k01,
         'improvement_tolerance':TOL,
         'recenter_allowed_eff':bool(imp_eff>TOL),'recenter_allowed_k01':bool(imp_k01>TOL),
         'gate':'RECENTER' if max(imp_eff,imp_k01)>TOL else 'NO_RECENTER_AXIS_CLEAR',
         'warning':'Axis-only local exact gate; not a full Hessian, posterior, evidence, or global proof.'}
out=Path('output/dense_7d_axis_gate'); out.mkdir(parents=True,exist_ok=True)
(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
with (out/'points.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print('DENSE_7D_AXIS_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('DENSE_7D_AXIS_COMPLETE',flush=True)
