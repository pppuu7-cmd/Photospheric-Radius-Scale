#!/usr/bin/env python3
"""Grouped CLASS precision sensitivity at old300k and current ray125 point."""
from pathlib import Path
import json
import inference_core as core

POINTS={
 'old300k': {'lam':300000.0,'h':0.6906430189065689,'Ob':0.046822913729452804,
             'Om':0.25278507230249403,'As':2.0695004530982282e-9,
             'ns':0.9644419669945631,'zre':6.8611290543096395},
 'ray125': {'lam':292355.6941224321,'h':0.6903266356879535,'Ob':0.04681520174985292,
            'Om':0.2532264965488123,'As':2.0766287371600014e-9,
            'ns':0.9646287786725471,'zre':7.03612905430964},
}
EXPECTED={'old300k':1050.610628798525,'ray125':1050.4444187294202}
GROUPS=[
 ('baseline',{}),
 ('background_thermo',{'tol_background_integration':'1e-3','tol_thermo_integration':'1e-3'}),
 ('perturbation',{'tol_perturb_integration':'1e-6','perturb_sampling_stepsize':'0.025'}),
 ('k_sampling',{'k_per_decade_for_pk':'30','k_per_decade_for_bao':'140','k_max_tau0_over_l_max':'3.5'}),
 ('ell_sampling',{'l_logstep':'1.04','l_linstep':'10'}),
 ('full_tight',{
   'tol_background_integration':'1e-3','tol_thermo_integration':'1e-3',
   'tol_perturb_integration':'1e-6','perturb_sampling_stepsize':'0.025',
   'k_per_decade_for_pk':'30','k_per_decade_for_bao':'140','k_max_tau0_over_l_max':'3.5',
   'l_logstep':'1.04','l_linstep':'10',
 }),
]
orig=core.make_ini; active={}
def make_ini(model,p,tag):
    path=orig(model,p,tag)
    if active:
        with Path(path).open('a') as f:
            f.write('\n# grouped precision audit\n')
            for k,v in active.items(): f.write(f'{k} = {v}\n')
    return path
core.make_ini=make_ini
rows=[]
for group,overrides in GROUPS:
    active.clear(); active.update(overrides)
    for name,p in POINTS.items():
        core.CACHE.clear(); r=core.evaluate('RTK',dict(p))
        if not r.get('ok',False): raise RuntimeError(f'{group}/{name}: {r}')
        row={'group':group,'point':name,'score_eff':r['score'],'score_k01':r['score_k01'],
             'logL_planck':r['logL_planck'],'logL_high':r['logL_high'],
             'logL_lowT':r['logL_lowT'],'logL_lowE':r['logL_lowE'],
             'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],
             'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd'],'overrides':dict(overrides)}
        rows.append(row); print('CLASS_PRECISION_GROUP_POINT',json.dumps(row,sort_keys=True),flush=True)
        if group=='baseline' and abs(r['score']-EXPECTED[name])>1e-9:
            raise RuntimeError(f'baseline regression {name}: {r["score"]} != {EXPECTED[name]}')
by={(r['group'],r['point']):r for r in rows}
comparisons=[]
for group,_ in GROUPS:
    a=by[(group,'old300k')]; b=by[(group,'ray125')]
    c={'group':group,
       'delta_eff_best_minus_old':b['score_eff']-a['score_eff'],
       'delta_k01_best_minus_old':b['score_k01']-a['score_k01'],
       'delta_planck_term_best_minus_old':-2*(b['logL_planck']-a['logL_planck']),
       'delta_high_term_best_minus_old':-2*(b['logL_high']-a['logL_high']),
       'delta_lowT_term_best_minus_old':-2*(b['logL_lowT']-a['logL_lowT']),
       'delta_lowE_term_best_minus_old':-2*(b['logL_lowE']-a['logL_lowE']),
       'delta_SN_best_minus_old':b['chi2_SN']-a['chi2_SN'],
       'delta_BOSS_eff_best_minus_old':b['chi2_BOSS_eff']-a['chi2_BOSS_eff']}
    comparisons.append(c); print('CLASS_PRECISION_GROUP_COMPARISON',json.dumps(c,sort_keys=True),flush=True)
base=by[('baseline','old300k')]
absolute_shifts=[]
for group,_ in GROUPS[1:]:
    r=by[(group,'old300k')]
    absolute_shifts.append({'group':group,'delta_eff_old300k_vs_baseline':r['score_eff']-base['score_eff'],
                            'delta_planck_term_old300k_vs_baseline':-2*(r['logL_planck']-base['logL_planck']),
                            'delta_high_term_old300k_vs_baseline':-2*(r['logL_high']-base['logL_high'])})
summary={'stage':'CLASS-grouped-precision-sensitivity','rows':rows,'comparisons':comparisons,
         'absolute_shifts_old300k':absolute_shifts,
         'scope':'Fixed-point grouped numerical sensitivity only; no optimization/significance.'}
out=Path('output/class_precision_groups'); out.mkdir(parents=True,exist_ok=True)
(out/'class_precision_groups_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('CLASS_PRECISION_GROUPS_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('CLASS_PRECISION_GROUPS_COMPLETE',flush=True)
