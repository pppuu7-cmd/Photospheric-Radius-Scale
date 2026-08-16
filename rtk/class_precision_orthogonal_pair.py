#!/usr/bin/env python3
"""Minimal differential CLASS precision audit: old300k vs orthogonal exact record."""
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
 'orthogonal': {
   'p': {'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,
         'Om':0.25313821169954864,'As':2.0752030803476467e-9,
         'ns':0.9644164163369503,'zre':7.00112905430964},
   'expected_eff':1050.362361331656984,'expected_k01':1050.375737633925155,
 },
}
LEVELS=[
 ('baseline',{}),
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
orig=core.make_ini; active={}
def make_ini(model,p,tag):
    path=orig(model,p,tag)
    if active:
        with Path(path).open('a') as f:
            f.write('\n# orthogonal differential precision overrides\n')
            for k,v in active.items(): f.write(f'{k} = {v}\n')
    return path
core.make_ini=make_ini
rows=[]
for level,overrides in LEVELS:
    active.clear(); active.update(overrides)
    for name,spec in POINTS.items():
        core.CACHE.clear(); r=core.evaluate('RTK',dict(spec['p']))
        if not r.get('ok',False): raise RuntimeError(f'{level}/{name}: {r}')
        row={'level':level,'point':name,'score_eff':r['score'],'score_k01':r['score_k01'],
             'logL_planck':r['logL_planck'],'logL_high':r['logL_high'],
             'logL_lowT':r['logL_lowT'],'logL_lowE':r['logL_lowE'],
             'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],
             'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd'],'overrides':dict(overrides)}
        rows.append(row); print('CLASS_ORTHOGONAL_PAIR_POINT',json.dumps(row,sort_keys=True),flush=True)
        if level=='baseline':
            for k,e in [('score_eff',spec['expected_eff']),('score_k01',spec['expected_k01'])]:
                if abs(row[k]-e)>1e-9: raise RuntimeError(f'baseline regression {name}/{k}: {row[k]} vs {e}')
by={(r['level'],r['point']):r for r in rows}
comparisons=[]
for level,_ in LEVELS:
    a=by[(level,'old300k')]; b=by[(level,'orthogonal')]
    c={'level':level,
       'delta_eff_orthogonal_minus_old':b['score_eff']-a['score_eff'],
       'delta_k01_orthogonal_minus_old':b['score_k01']-a['score_k01'],
       'delta_planck_term':-2*(b['logL_planck']-a['logL_planck']),
       'delta_high_term':-2*(b['logL_high']-a['logL_high']),
       'delta_lowT_term':-2*(b['logL_lowT']-a['logL_lowT']),
       'delta_lowE_term':-2*(b['logL_lowE']-a['logL_lowE']),
       'delta_SN':b['chi2_SN']-a['chi2_SN'],
       'delta_BOSS_eff':b['chi2_BOSS_eff']-a['chi2_BOSS_eff'],
       'delta_BOSS_k01':b['chi2_BOSS_k01']-a['chi2_BOSS_k01']}
    comparisons.append(c); print('CLASS_ORTHOGONAL_PAIR_COMPARISON',json.dumps(c,sort_keys=True),flush=True)
for i in range(1,len(comparisons)):
    comparisons[i]['change_delta_eff_vs_previous_level']=comparisons[i]['delta_eff_orthogonal_minus_old']-comparisons[i-1]['delta_eff_orthogonal_minus_old']
    comparisons[i]['change_delta_k01_vs_previous_level']=comparisons[i]['delta_k01_orthogonal_minus_old']-comparisons[i-1]['delta_k01_orthogonal_minus_old']
summary={'stage':'CLASS-orthogonal-record-pair-precision','points':POINTS,'rows':rows,'comparisons':comparisons,
         'scope':'Fixed-point numerical differential audit only; no optimization or statistical inference.'}
out=Path('output/class_precision_orthogonal_pair'); out.mkdir(parents=True,exist_ok=True)
(out/'class_precision_orthogonal_pair_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('CLASS_ORTHOGONAL_PAIR_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('CLASS_ORTHOGONAL_PAIR_COMPLETE',flush=True)
