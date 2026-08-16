#!/usr/bin/env python3
"""Absolute/matched convergence check for CLASS l_linstep=2 -> 1.
Fixed-point numerical audit only.  Evaluates RTK v5 and the current LCDM ultra
control at identical ultra settings, changing only l_linstep.
"""
from pathlib import Path
import json
import inference_core as L
POINTS={
 'rtk_v5':('RTK',{'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,'Om':0.25313821169954864,'As':2.0832030803476467e-9,'ns':0.9644164163369503,'zre':7.21112905430964}),
 'lcdm_partial':('LCDM',{'lam':0.0,'h':0.6779337587382693,'Ob':0.04872764689799632,'Om':0.26187225794495356,'As':2.1094040998203598e-9,'ns':0.9649685632254442,'zre':7.8583129349509475}),
}
BASE={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180','k_max_tau0_over_l_max':'4.0','l_logstep':'1.02'}
linstep='2';orig=L.make_ini
def make_ini(model,p,tag):
    path=orig(model,p,tag)
    with Path(path).open('a') as f:
        f.write('\n# matched l_linstep convergence audit\n')
        for k,v in BASE.items():f.write(f'{k} = {v}\n')
        f.write(f'l_linstep = {linstep}\n')
    return path
L.make_ini=make_ini
rows=[]
for ls in ('2','1'):
    linstep=ls
    for name,(model,p) in POINTS.items():
        L.CACHE.clear();r=L.evaluate(model,dict(p))
        if not r.get('ok'):raise RuntimeError(f'l{ls}/{name}: {r}')
        row={'l_linstep':int(ls),'point':name,'model':model,'score_eff':r['score'],'score_k01':r['score_k01'],'logL_planck':r['logL_planck'],'logL_high':r['logL_high'],'logL_lowE':r['logL_lowE'],'logL_lowT':r['logL_lowT'],'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd']}
        rows.append(row);print('LINSTEP21_POINT',json.dumps(row,sort_keys=True),flush=True)
by={(r['l_linstep'],r['point']):r for r in rows}
changes={}
for name in POINTS:
    a=by[(2,name)];b=by[(1,name)]
    changes[name]={'delta_eff_l1_minus_l2':b['score_eff']-a['score_eff'],'delta_k01_l1_minus_l2':b['score_k01']-a['score_k01'],'delta_planck_term':-2*(b['logL_planck']-a['logL_planck']),'delta_BOSS_eff':b['chi2_BOSS_eff']-a['chi2_BOSS_eff'],'delta_BOSS_k01':b['chi2_BOSS_k01']-a['chi2_BOSS_k01'],'delta_SN':b['chi2_SN']-a['chi2_SN']}
comparison={}
for ls in (2,1):
    r=by[(ls,'rtk_v5')];d=by[(ls,'lcdm_partial')]
    comparison[str(ls)]={'delta_eff_rtk_minus_lcdm':r['score_eff']-d['score_eff'],'delta_k01_rtk_minus_lcdm':r['score_k01']-d['score_k01']}
comparison['change_l1_minus_l2']={'eff':comparison['1']['delta_eff_rtk_minus_lcdm']-comparison['2']['delta_eff_rtk_minus_lcdm'],'k01':comparison['1']['delta_k01_rtk_minus_lcdm']-comparison['2']['delta_k01_rtk_minus_lcdm']}
summary={'stage':'matched-linstep-2-to-1-convergence','scope':'fixed-point numerical convergence only','base_ultra_overrides':BASE,'rows':rows,'l1_minus_l2':changes,'matched_rtk_minus_lcdm':comparison,'scientific_tolerance':0.005}
out=Path('output/matched_linstep21');out.mkdir(parents=True,exist_ok=True);(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('LINSTEP21_RESULT',json.dumps(summary,sort_keys=True),flush=True);print('LINSTEP21_COMPLETE',flush=True)
