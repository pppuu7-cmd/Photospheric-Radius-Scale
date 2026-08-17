#!/usr/bin/env python3
"""One-shot matched-ultra+dense RTK evaluation for inter-runner reproducibility."""
from pathlib import Path
import json, math, os, sys
LAM=float(sys.argv[1]); REP=str(sys.argv[2])
if not (LAM>0 and math.isfinite(LAM)): raise SystemExit('bad lambda')
sys.argv=['dense_lambda_crossrunner_probe','planck_data']
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
    if 'z_pk = '+SPARSE not in text: raise RuntimeError('sparse z_pk not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text); f.write('\n# matched-ultra+dense crossrunner probe\n')
        for k,v in ULTRA.items(): f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini
L.CACHE.clear(); r=L.evaluate('RTK',dict(CENTER))
if not r.get('ok'): raise RuntimeError(r)
row={'stage':'dense-lambda-crossrunner','replica':REP,'lambda_D':LAM,'u_inv_lambda':1.0/LAM,
     'score_eff':float(r['score']),'score_k01':float(r['score_k01']),
     'chi2_BOSS_eff':float(r['chi2_BOSS_eff']),'chi2_BOSS_k01':float(r['chi2_BOSS_k01']),
     'chi2_SN':float(r['chi2_SN']),'logL_planck':float(r['logL_planck']),'rd':float(r['rd']),
     'runner_name':os.environ.get('RUNNER_NAME',''),'runner_arch':os.environ.get('RUNNER_ARCH',''),
     'objective':'matched-ultra-linstep2+dense-BOSS'}
out=Path('output/dense_lambda_crossrunner')/f'{LAM:.0f}'/REP; out.mkdir(parents=True,exist_ok=True)
(out/'result.json').write_text(json.dumps(row,indent=2,sort_keys=True)+'\n')
print('DENSE_LAMBDA_CROSSRUNNER_RESULT',json.dumps(row,sort_keys=True),flush=True)
print('DENSE_LAMBDA_CROSSRUNNER_COMPLETE',flush=True)
