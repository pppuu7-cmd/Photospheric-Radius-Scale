#!/usr/bin/env python3
"""Matched ultra l=2 sparse->dense BOSS audit at the Round5 common center.

Only z_pk changes. This quantifies numerical sensitivity of both BOSS mappings
at the exact current Stage4D3 center; it is not a model-selection claim.
"""
from pathlib import Path
import json
import inference_core as L

P={'lam':217225.01601516694,'h':0.6904831253428524,'Ob':0.046836300417955265,
   'Om':0.25300743080221694,'As':2.0837288833768707e-9,
   'ns':0.9643603115669437,'zre':7.21843542110055}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE='0.,0.25,0.30,0.34,0.36,0.37,0.38,0.39,0.40,0.42,0.47,0.49,0.50,0.51,0.52,0.53,0.55,0.57,0.59,0.60,0.61,0.62,0.63,0.65,0.70,0.75,1.0'
ULTRA={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4',
       'tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125',
       'k_per_decade_for_pk':'40','k_per_decade_for_bao':'180',
       'k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2'}
mode='sparse'; orig=L.make_ini

def make_ini(model,p,tag):
    path=orig(model,p,tag); text=Path(path).read_text(); needle='z_pk = '+SPARSE
    if needle not in text: raise RuntimeError('production sparse z_pk line not found')
    if mode=='dense': text=text.replace(needle,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text); f.write('\n# Round5 matched-ultra l2 overrides\n')
        for k,v in ULTRA.items(): f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini
rows=[]
for m in ('sparse','dense'):
    mode=m; L.CACHE.clear(); r=L.evaluate('RTK',dict(P))
    if not r.get('ok'): raise RuntimeError(f'{m}: {r}')
    row={'mode':m,'score_eff':r['score'],'score_k01':r['score_k01'],
         'logL_planck':r['logL_planck'],'chi2_SN':r['chi2_SN'],
         'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd']}
    rows.append(row); print('ROUND5_DENSE_BOSS_POINT',json.dumps(row,sort_keys=True),flush=True)
a,b=rows
change={'delta_score_eff':b['score_eff']-a['score_eff'],
        'delta_score_k01':b['score_k01']-a['score_k01'],
        'delta_BOSS_eff':b['chi2_BOSS_eff']-a['chi2_BOSS_eff'],
        'delta_BOSS_k01':b['chi2_BOSS_k01']-a['chi2_BOSS_k01'],
        'delta_planck':b['logL_planck']-a['logL_planck'],
        'delta_SN':b['chi2_SN']-a['chi2_SN'],'delta_rd':b['rd']-a['rd']}
summary={'stage':'round5-current-center-matched-ultra-l2-sparse-dense-BOSS',
         'scope':'fixed-point numerical audit only','center':P,'ultra_overrides':ULTRA,
         'z_pk_sparse':SPARSE,'z_pk_dense':DENSE,'rows':rows,'dense_minus_sparse':change}
out=Path('output/matched_l2_dense_boss_round5'); out.mkdir(parents=True,exist_ok=True)
(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('ROUND5_DENSE_BOSS_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('ROUND5_DENSE_BOSS_COMPLETE',flush=True)
