#!/usr/bin/env python3
"""Matched-ultra+dense-BOSS screening profile toward the RTK dust boundary.

For one fixed lambda_D, evaluate the current Round5 nuisance center plus a
symmetric one-step poll in each of the six nuisance coordinates.  This is a
screening profile: it can falsify a claimed finite minimum if a large-lambda
point improves, but it is not a fully reoptimized boundary likelihood.
"""
from pathlib import Path
import json, math, sys
import inference_core as L

LAM=float(sys.argv[1])
if not (LAM>0 and math.isfinite(LAM)): raise SystemExit('lambda must be finite and positive')
CENTER={'lam':LAM,'h':0.6904831253428524,'Ob':0.046836300417955265,'Om':0.25300743080221694,
        'As':2.0837288833768707e-9,'ns':0.9643603115669437,'zre':7.21843542110055}
STEPS={'h':0.00070,'Ob':0.00014,'Om':0.00140,'As':8e-12,'ns':0.00070,'zre':0.14}
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
        f.write(text); f.write('\n# frozen-candidate matched-ultra+dense overrides\n')
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

def ev(p,label):
    L.CACHE.clear(); r=L.evaluate('RTK',dict(p))
    if not r.get('ok'): raise RuntimeError(f'{label}: {r}')
    row={'label':label,'lambda_D':LAM,'u_inv_lambda':1.0/LAM,
         'score_eff':r['score'],'score_k01':r['score_k01'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],
         'chi2_BOSS_k01':r['chi2_BOSS_k01'],'chi2_SN':r['chi2_SN'],'logL_planck':r['logL_planck'],'rd':r['rd'],**p}
    cleanup(r.get('tag')); rows.append(row)
    print('DENSE_DUST_POLL_POINT',json.dumps(row,sort_keys=True),flush=True)

rows=[]; ev(CENTER,'center')
for q,s in STEPS.items():
    for sign in (-1,1):
        p=dict(CENTER); p[q]+=sign*s; ev(p,f'{q}_{sign:+d}')
best_eff=min(rows,key=lambda r:r['score_eff']); best_k01=min(rows,key=lambda r:r['score_k01'])
summary={'stage':'dense-dust-boundary-nuisance-poll','lambda_D':LAM,'u_inv_lambda':1.0/LAM,
         'objective':'matched-ultra-linstep2+dense-BOSS','nuisance_center':CENTER,'nuisance_steps':STEPS,
         'best_eff':best_eff,'best_k01':best_k01,'rows':rows,
         'warning':'Screening fixed-lambda nuisance poll only; not a full nuisance reoptimization or global model comparison.'}
out=Path('output/dense_dust_boundary_poll')/f'{LAM:.0f}'; out.mkdir(parents=True,exist_ok=True)
(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('DENSE_DUST_POLL_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('DENSE_DUST_POLL_COMPLETE',flush=True)
