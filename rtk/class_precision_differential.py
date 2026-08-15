#!/usr/bin/env python3
"""Differential CLASS-precision audit across exact RTK descent points.

Absolute likelihood values can move when CLASS precision changes. The primary
scientific question here is whether *relative* score improvements converge as
CLASS precision is tightened. No optimization is performed.
"""
from pathlib import Path
import json
import inference_core as core

POINTS={
  'old300k': {
    'p': {'lam':300000.0,'h':0.6906430189065689,'Ob':0.046822913729452804,
          'Om':0.25278507230249403,'As':2.0695004530982282e-9,
          'ns':0.9644419669945631,'zre':6.8611290543096395},
    'expected_eff':1050.610628798525,'expected_k01':1050.623296036079,
  },
  'newton05': {
    'p': {'lam':298455.3134754306,'h':0.6905797422628458,'Ob':0.04682137133353283,
          'Om':0.2528733571517577,'As':2.070926109910583e-9,
          'ns':0.9644793293301599,'zre':6.89612905430964},
    'expected_eff':1050.5562518398717,'expected_k01':1050.5691351225128,
  },
  'ray_t4': {
    'p': {'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046816744145772894,
          'Om':0.25313821169954864,'As':2.0752030803476467e-9,
          'ns':0.9645914163369503,'zre':7.00112905430964},
    'expected_eff':1050.453791769174,'expected_k01':1050.4673245097958,
  },
  'ray125': {
    'p': {'lam':292355.6941224321,'h':0.6903266356879535,'Ob':0.04681520174985292,
          'Om':0.2532264965488123,'As':2.0766287371600014e-9,
          'ns':0.9646287786725471,'zre':7.03612905430964},
    'expected_eff':1050.4444187294202,'expected_k01':1050.4581685583998,
  },
}

LEVELS=[
 ('baseline',{}),
 ('medium',{
   'tol_background_integration':'3e-3','tol_thermo_integration':'3e-3',
   'tol_perturb_integration':'3e-6','perturb_sampling_stepsize':'0.05',
   'k_per_decade_for_pk':'20','k_per_decade_for_bao':'100',
   'k_max_tau0_over_l_max':'3.0','l_logstep':'1.08','l_linstep':'20',
 }),
 ('tight',{
   'tol_background_integration':'1e-3','tol_thermo_integration':'1e-3',
   'tol_perturb_integration':'1e-6','perturb_sampling_stepsize':'0.025',
   'k_per_decade_for_pk':'30','k_per_decade_for_bao':'140',
   'k_max_tau0_over_l_max':'3.5','l_logstep':'1.04','l_linstep':'10',
 }),
 ('ultra',{
   'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4',
   'tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125',
   'k_per_decade_for_pk':'40','k_per_decade_for_bao':'180',
   'k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'5',
 }),
]

orig_make_ini=core.make_ini
_active={}
def audited_make_ini(model,p,tag):
    path=orig_make_ini(model,p,tag)
    if _active:
        with Path(path).open('a') as f:
            f.write('\n# Differential CLASS precision audit overrides\n')
            for k,v in _active.items(): f.write(f'{k} = {v}\n')
    return path
core.make_ini=audited_make_ini

rows=[]
for level,overrides in LEVELS:
    _active.clear(); _active.update(overrides)
    for name,spec in POINTS.items():
        core.CACHE.clear()
        r=core.evaluate('RTK',dict(spec['p']))
        if not r.get('ok',False): raise RuntimeError(f'{level}/{name} failed: {r}')
        row={
          'level':level,'point':name,'overrides':dict(overrides),
          'score_eff':r['score'],'score_k01':r['score_k01'],'rd':r['rd'],
          'logL_lowT':r['logL_lowT'],'logL_lowE':r['logL_lowE'],
          'logL_high':r['logL_high'],'logL_planck':r['logL_planck'],
          'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],
          'chi2_BOSS_k01':r['chi2_BOSS_k01'],
        }
        rows.append(row)
        print('CLASS_DIFF_POINT',json.dumps(row,sort_keys=True),flush=True)
        if level=='baseline':
            for key,expected in [('score_eff',spec['expected_eff']),('score_k01',spec['expected_k01'])]:
                if abs(row[key]-expected)>1e-9:
                    raise RuntimeError(f'baseline regression {name}/{key}: {row[key]} vs {expected}')

by={(r['level'],r['point']):r for r in rows}
comparisons=[]
for level,_ in LEVELS:
    old=by[(level,'old300k')]; n=by[(level,'newton05')]
    t=by[(level,'ray_t4')]; b=by[(level,'ray125')]
    c={
      'level':level,
      'delta_eff_best_minus_old300k':b['score_eff']-old['score_eff'],
      'delta_k01_best_minus_old300k':b['score_k01']-old['score_k01'],
      'delta_eff_best_minus_t4':b['score_eff']-t['score_eff'],
      'delta_k01_best_minus_t4':b['score_k01']-t['score_k01'],
      'delta_eff_t4_minus_old300k':t['score_eff']-old['score_eff'],
      'delta_k01_t4_minus_old300k':t['score_k01']-old['score_k01'],
      'delta_eff_newton_minus_old300k':n['score_eff']-old['score_eff'],
      'delta_k01_newton_minus_old300k':n['score_k01']-old['score_k01'],
      'delta_planck_term_best_minus_old300k':-2*(b['logL_planck']-old['logL_planck']),
      'delta_SN_best_minus_old300k':b['chi2_SN']-old['chi2_SN'],
      'delta_BOSS_eff_best_minus_old300k':b['chi2_BOSS_eff']-old['chi2_BOSS_eff'],
      'delta_BOSS_k01_best_minus_old300k':b['chi2_BOSS_k01']-old['chi2_BOSS_k01'],
    }
    comparisons.append(c)
    print('CLASS_DIFF_COMPARISON',json.dumps(c,sort_keys=True),flush=True)

for i in range(1,len(comparisons)):
    a,b=comparisons[i-1],comparisons[i]
    b['change_delta_eff_best_vs_previous_precision']=b['delta_eff_best_minus_old300k']-a['delta_eff_best_minus_old300k']
    b['change_delta_k01_best_vs_previous_precision']=b['delta_k01_best_minus_old300k']-a['delta_k01_best_minus_old300k']

summary={
 'stage':'CLASS-differential-precision-audit-current-best',
 'points':POINTS,'levels':rows,'comparisons':comparisons,
 'scope':'Fixed-point differential precision only; no optimization, posterior, interval or significance claim.',
}
out=Path('output/class_precision_differential'); out.mkdir(parents=True,exist_ok=True)
(out/'class_precision_differential_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('CLASS_DIFFERENTIAL_PRECISION_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('CLASS_DIFFERENTIAL_PRECISION_COMPLETE',flush=True)
