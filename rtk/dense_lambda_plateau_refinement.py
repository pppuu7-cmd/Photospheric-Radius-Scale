#!/usr/bin/env python3
"""Refine the matched-ultra+dense RTK lambda plateau with fresh exact repeats.

For one lambda_D this evaluates the same nuisance center three times, clearing
all in-process memoization between evaluations.  The goal is to map the shallow
large-lambda profile and measure the deterministic numerical repeat floor before
any expensive recenter/Hessian decision.  This is not a nuisance reoptimization.
"""
from pathlib import Path
import json, math, sys

LAM=float(sys.argv[1])
if not (LAM>0 and math.isfinite(LAM)):
    raise SystemExit('lambda must be finite and positive')
sys.argv=['dense_lambda_plateau_refinement','planck_data']
import inference_core as L

CENTER={'lam':LAM,'h':0.6904831253428524,'Ob':0.046836300417955265,'Om':0.25300743080221694,
        'As':2.0837288833768707e-9,'ns':0.9643603115669437,'zre':7.21843542110055}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE='0.,0.25,0.30,0.34,0.36,0.37,0.38,0.39,0.40,0.42,0.47,0.49,0.50,0.51,0.52,0.53,0.55,0.57,0.59,0.60,0.61,0.62,0.63,0.65,0.70,0.75,1.0'
ULTRA={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7',
       'perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180',
       'k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2'}
orig=L.make_ini

def make_ini(model,p,tag):
    path=orig(model,p,tag); text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text:
        raise RuntimeError('production sparse z_pk line not found')
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

def one(rep):
    L.CACHE.clear()
    r=L.evaluate('RTK',dict(CENTER))
    if not r.get('ok'):
        raise RuntimeError(f'repeat {rep}: {r}')
    row={'repeat':rep,'lambda_D':LAM,'u_inv_lambda':1.0/LAM,
         'score_eff':float(r['score']),'score_k01':float(r['score_k01']),
         'chi2_BOSS_eff':float(r['chi2_BOSS_eff']),'chi2_BOSS_k01':float(r['chi2_BOSS_k01']),
         'chi2_SN':float(r['chi2_SN']),'logL_planck':float(r['logL_planck']),'rd':float(r['rd'])}
    cleanup(r.get('tag'))
    print('DENSE_LAMBDA_REPEAT',json.dumps(row,sort_keys=True),flush=True)
    return row

rows=[one(i) for i in range(1,4)]
eff=[r['score_eff'] for r in rows]; k01=[r['score_k01'] for r in rows]
summary={'stage':'dense-lambda-plateau-refinement','objective':'matched-ultra-linstep2+dense-BOSS',
         'lambda_D':LAM,'u_inv_lambda':1.0/LAM,'nuisance_center':CENTER,'repeats':rows,
         'mean_eff':sum(eff)/len(eff),'mean_k01':sum(k01)/len(k01),
         'spread_eff':max(eff)-min(eff),'spread_k01':max(k01)-min(k01),
         'warning':'Fresh-repeat fixed-nuisance profile only; not a global or nuisance-reoptimized likelihood.'}
out=Path('output/dense_lambda_plateau_refinement')/f'{LAM:.0f}'
out.mkdir(parents=True,exist_ok=True)
(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('DENSE_LAMBDA_REFINEMENT_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('DENSE_LAMBDA_REFINEMENT_COMPLETE',flush=True)
