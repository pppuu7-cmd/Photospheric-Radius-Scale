#!/usr/bin/env python3
"""Focused CLASS ell-sampling convergence at otherwise-ultra precision.

The broad cross-grid showed differential RTK descent robust but absolute scores
still varying at O(1e-2). Here all non-ell precision controls are fixed to the
ultra settings and only l_logstep/l_linstep are refined. Two fixed RTK points
(old300k and the current As-zre v2 navigation record) are evaluated.
"""
from pathlib import Path
import json
import inference_core as core

POINTS={
 'old300k': {'lam':300000.0,'h':0.6906430189065689,'Ob':0.046822913729452804,
             'Om':0.25278507230249403,'As':2.0695004530982282e-9,
             'ns':0.9644419669945631,'zre':6.8611290543096395},
 'v2best': {'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,
            'Om':0.25313821169954864,'As':2.079203080347647e-9,
            'ns':0.9644164163369503,'zre':7.10612905430964},
}
BASE={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4',
      'tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125',
      'k_per_decade_for_pk':'40','k_per_decade_for_bao':'180',
      'k_max_tau0_over_l_max':'4.0'}
COMBOS=[
 ('l102_n5','1.02','5'),('l102_n3','1.02','3'),('l102_n2','1.02','2'),
 ('l101_n5','1.01','5'),('l101_n3','1.01','3'),('l101_n2','1.01','2'),
 ('l1005_n5','1.005','5'),('l1005_n3','1.005','3'),('l1005_n2','1.005','2'),
]
orig=core.make_ini; active={}
def make_ini(model,p,tag):
    path=orig(model,p,tag)
    with Path(path).open('a') as f:
        f.write('\n# ultra precision + focused ell corner overrides\n')
        for k,v in active.items(): f.write(f'{k} = {v}\n')
    return path
core.make_ini=make_ini
rows=[]
for label,llog,llin in COMBOS:
    active.clear(); active.update(BASE); active.update({'l_logstep':llog,'l_linstep':llin})
    for name,p in POINTS.items():
        core.CACHE.clear(); r=core.evaluate('RTK',dict(p))
        if not r.get('ok',False): raise RuntimeError(f'{label}/{name}: {r}')
        row={'label':label,'l_logstep':float(llog),'l_linstep':int(llin),'point':name,
             'score_eff':r['score'],'score_k01':r['score_k01'],'logL_high':r['logL_high'],
             'logL_planck':r['logL_planck'],'chi2_SN':r['chi2_SN'],
             'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd']}
        rows.append(row); print('ULTRA_ELL_CORNER_POINT',json.dumps(row,sort_keys=True),flush=True)
by={(r['label'],r['point']):r for r in rows}; comps=[]
for label,llog,llin in COMBOS:
    a=by[(label,'old300k')]; b=by[(label,'v2best')]
    c={'label':label,'l_logstep':float(llog),'l_linstep':int(llin),
       'old300k_eff':a['score_eff'],'v2best_eff':b['score_eff'],
       'delta_eff':b['score_eff']-a['score_eff'],
       'delta_k01':b['score_k01']-a['score_k01'],
       'old_high_term':-2*a['logL_high'],'v2best_high_term':-2*b['logL_high']}
    comps.append(c); print('ULTRA_ELL_CORNER_COMPARISON',json.dumps(c,sort_keys=True),flush=True)
summary={'stage':'CLASS-ultra-ell-focused-corner','base_overrides':BASE,'rows':rows,'comparisons':comps,
         'scope':'Fixed-point numerical convergence audit only; no optimization/statistical inference.'}
out=Path('output/class_precision_ultra_ell_corner'); out.mkdir(parents=True,exist_ok=True)
(out/'class_precision_ultra_ell_corner_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('ULTRA_ELL_CORNER_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('ULTRA_ELL_CORNER_COMPLETE',flush=True)
