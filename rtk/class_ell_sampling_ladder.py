#!/usr/bin/env python3
"""Targeted CLASS ell-sampling convergence: old300k vs orthogonal record.

Defaults in dirian/class_public/nonlocal are l_logstep=1.12, l_linstep=40.
Only these two transfer-function sampling controls are varied here.
"""
from pathlib import Path
import json
import inference_core as core

POINTS={
 'old300k': {'lam':300000.0,'h':0.6906430189065689,'Ob':0.046822913729452804,
             'Om':0.25278507230249403,'As':2.0695004530982282e-9,
             'ns':0.9644419669945631,'zre':6.8611290543096395},
 'orthogonal': {'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,
                'Om':0.25313821169954864,'As':2.0752030803476467e-9,
                'ns':0.9644164163369503,'zre':7.00112905430964},
}
EXPECTED={'old300k':1050.610628798525,'orthogonal':1050.362361331656984}
LEVELS=[
 ('default_1.12_40',{}),
 ('ell_1.08_30',{'l_logstep':'1.08','l_linstep':'30'}),
 ('ell_1.06_20',{'l_logstep':'1.06','l_linstep':'20'}),
 ('ell_1.04_10',{'l_logstep':'1.04','l_linstep':'10'}),
 ('ell_1.02_5',{'l_logstep':'1.02','l_linstep':'5'}),
 ('ell_1.01_3',{'l_logstep':'1.01','l_linstep':'3'}),
]
orig=core.make_ini; active={}
def make_ini(model,p,tag):
    path=orig(model,p,tag)
    if active:
        with Path(path).open('a') as f:
            f.write('\n# targeted ell-sampling audit\n')
            for k,v in active.items(): f.write(f'{k} = {v}\n')
    return path
core.make_ini=make_ini
rows=[]
for level,overrides in LEVELS:
    active.clear(); active.update(overrides)
    for name,p in POINTS.items():
        core.CACHE.clear(); r=core.evaluate('RTK',dict(p))
        if not r.get('ok',False): raise RuntimeError(f'{level}/{name}: {r}')
        row={'level':level,'point':name,'score_eff':r['score'],'score_k01':r['score_k01'],
             'logL_planck':r['logL_planck'],'logL_high':r['logL_high'],
             'logL_lowT':r['logL_lowT'],'logL_lowE':r['logL_lowE'],
             'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],
             'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd'],'overrides':dict(overrides)}
        rows.append(row); print('ELL_LADDER_POINT',json.dumps(row,sort_keys=True),flush=True)
        if level=='default_1.12_40' and abs(r['score']-EXPECTED[name])>1e-9:
            raise RuntimeError(f'baseline regression {name}: {r["score"]} vs {EXPECTED[name]}')
by={(r['level'],r['point']):r for r in rows}
comparisons=[]
prev=None
for level,_ in LEVELS:
    a=by[(level,'old300k')]; b=by[(level,'orthogonal')]
    c={'level':level,
       'old300k_eff':a['score_eff'],'orthogonal_eff':b['score_eff'],
       'delta_eff_orthogonal_minus_old':b['score_eff']-a['score_eff'],
       'delta_k01_orthogonal_minus_old':b['score_k01']-a['score_k01'],
       'old300k_high_term':-2*a['logL_high'],
       'orthogonal_high_term':-2*b['logL_high']}
    if prev is not None:
        c['change_old300k_eff_vs_previous']=a['score_eff']-prev['old300k_eff']
        c['change_orthogonal_eff_vs_previous']=b['score_eff']-prev['orthogonal_eff']
        c['change_delta_eff_vs_previous']=(b['score_eff']-a['score_eff'])-prev['delta_eff_orthogonal_minus_old']
    comparisons.append(c); prev=c
    print('ELL_LADDER_COMPARISON',json.dumps(c,sort_keys=True),flush=True)
summary={'stage':'CLASS-ell-sampling-ladder','defaults':{'l_logstep':1.12,'l_linstep':40},
         'rows':rows,'comparisons':comparisons,
         'scope':'Fixed-point ell-sampling numerical convergence only; no optimization/statistical inference.'}
out=Path('output/class_ell_sampling_ladder'); out.mkdir(parents=True,exist_ok=True)
(out/'class_ell_sampling_ladder_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('ELL_LADDER_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('ELL_LADDER_COMPLETE',flush=True)
