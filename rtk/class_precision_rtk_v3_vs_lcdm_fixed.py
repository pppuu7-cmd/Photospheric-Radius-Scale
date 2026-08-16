#!/usr/bin/env python3
"""Matched fixed-point numerical comparison of the RTK v3 navigation record
against both harvested exact-float LCDM local candidates.

This is deliberately NOT a model-selection calculation: none of the points is
reoptimized at tight/ultra precision here, and LCDM Stage4C is start-sensitive.
The purpose is only to test whether the raw baseline crossing survives applying
the same CLASS precision settings to both models.
"""
from pathlib import Path
import json
import inference_core as core
EFF_REG_TOL=1e-9
K01_REG_TOL=1e-4
POINTS={
 'rtk_v3':('RTK',{'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,'Om':0.25313821169954864,'As':2.080703080347647e-9,'ns':0.9644164163369503,'zre':7.14112905430964}),
 'lcdm_eff_candidate':('LCDM',{'lam':0.0,'h':0.6780618719300789,'Ob':0.04876205689548621,'Om':0.26191636161657555,'As':2.1105202470513124e-9,'ns':0.9651623965474088,'zre':7.8629952806182}),
 'lcdm_k01_candidate':('LCDM',{'lam':0.0,'h':0.6780117522107563,'Ob':0.04876857444980584,'Om':0.26197634862058367,'As':2.110543499612126e-9,'ns':0.9650407210966931,'zre':7.8639924801075285}),
}
EXPECTED_BASELINE={
 'rtk_v3':(1050.1486476532043,1050.1627089601635),
 'lcdm_eff_candidate':(1050.1661952170557,1050.1684126165533),
 'lcdm_k01_candidate':(1050.1867256061544,1050.1889036368575),
}
LEVELS=[
 ('baseline',{}),
 ('tight',{'tol_background_integration':'1e-3','tol_thermo_integration':'1e-3','tol_perturb_integration':'1e-6','perturb_sampling_stepsize':'0.025','k_per_decade_for_pk':'30','k_per_decade_for_bao':'140','k_max_tau0_over_l_max':'3.5','l_logstep':'1.04','l_linstep':'10'}),
 ('ultra',{'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180','k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'5'}),
]
orig=core.make_ini; active={}
def make_ini(model,p,tag):
    path=orig(model,p,tag)
    if active:
        with Path(path).open('a') as f:
            f.write('\n# matched RTK/LCDM fixed-point precision overrides\n')
            for k,v in active.items(): f.write(f'{k} = {v}\n')
    return path
core.make_ini=make_ini
rows=[]; regression=[]
for level,ov in LEVELS:
    active.clear(); active.update(ov)
    for name,(model,p) in POINTS.items():
        core.CACHE.clear(); r=core.evaluate(model,dict(p))
        if not r.get('ok',False): raise RuntimeError(f'{level}/{name}: {r}')
        row={'level':level,'point':name,'model':model,'score_eff':r['score'],'score_k01':r['score_k01'],'logL_planck':r['logL_planck'],'logL_high':r['logL_high'],'logL_lowT':r['logL_lowT'],'logL_lowE':r['logL_lowE'],'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd']}
        rows.append(row); print('MATCHED_FIXED_POINT',json.dumps(row,sort_keys=True),flush=True)
        if level=='baseline':
            ee,ek=EXPECTED_BASELINE[name]; de=row['score_eff']-ee; dk=row['score_k01']-ek
            reg={'point':name,'delta_eff':de,'delta_k01':dk,'eff_tol':EFF_REG_TOL,'k01_tol':K01_REG_TOL}
            regression.append(reg); print('MATCHED_BASELINE_REGRESSION',json.dumps(reg,sort_keys=True),flush=True)
            if abs(de)>EFF_REG_TOL or abs(dk)>K01_REG_TOL: raise RuntimeError(f'baseline regression {name}: {row}; {reg}')
by={(r['level'],r['point']):r for r in rows}; comparisons=[]
for level,_ in LEVELS:
    r=by[(level,'rtk_v3')]
    le=by[(level,'lcdm_eff_candidate')]
    lk=by[(level,'lcdm_k01_candidate')]
    best_lcdm_eff=min((le,lk),key=lambda x:x['score_eff'])
    best_lcdm_k01=min((le,lk),key=lambda x:x['score_k01'])
    c={'level':level,
       'best_lcdm_eff_point':best_lcdm_eff['point'],'best_lcdm_eff':best_lcdm_eff['score_eff'],
       'rtk_eff':r['score_eff'],'delta_eff_rtk_minus_best_fixed_lcdm':r['score_eff']-best_lcdm_eff['score_eff'],
       'best_lcdm_k01_point':best_lcdm_k01['point'],'best_lcdm_k01':best_lcdm_k01['score_k01'],
       'rtk_k01':r['score_k01'],'delta_k01_rtk_minus_best_fixed_lcdm':r['score_k01']-best_lcdm_k01['score_k01']}
    comparisons.append(c); print('MATCHED_FIXED_COMPARISON',json.dumps(c,sort_keys=True),flush=True)
out=Path('output/class_precision_rtk_v3_vs_lcdm_fixed'); out.mkdir(parents=True,exist_ok=True)
summary={'stage':'matched-fixed-point-RTK-v3-vs-LCDM','rows':rows,'baseline_regression':regression,'regression_tolerances':{'eff':EFF_REG_TOL,'k01':K01_REG_TOL},'comparisons':comparisons,
         'scope':'Fixed-point numerical comparison only. No point is reoptimized at tight/ultra; not AIC/BIC/evidence/model preference.'}
(out/'matched_fixed_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('MATCHED_FIXED_RESULT',json.dumps(summary,sort_keys=True),flush=True); print('MATCHED_FIXED_COMPLETE',flush=True)
