#!/usr/bin/env python3
"""Matched-ultra l=2 sparse->dense BOSS audit using the prepared production core.

Only the CLASS z_pk sampling used to reconstruct growth observables is changed
between sparse and dense modes.  Planck, Pantheon, BAO convention, covariance,
physics parameters, P_k_max=5 and all other CLASS precision settings are held
fixed.  This is a fixed-point numerical-systematics audit, not an optimization
or model-selection calculation.
"""
from pathlib import Path
import json
import inference_core as L

POINTS={
 'rtk_v5':('RTK',{'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,'Om':0.25313821169954864,'As':2.0832030803476467e-9,'ns':0.9644164163369503,'zre':7.21112905430964}),
 'lcdm_partial':('LCDM',{'lam':0.0,'h':0.6779337587382693,'Ob':0.04872764689799632,'Om':0.26187225794495356,'As':2.1094040998203598e-9,'ns':0.9649685632254442,'zre':7.8583129349509475}),
}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE='0.,0.25,0.30,0.34,0.36,0.37,0.38,0.39,0.40,0.42,0.47,0.49,0.50,0.51,0.52,0.53,0.55,0.57,0.59,0.60,0.61,0.62,0.63,0.65,0.70,0.75,1.0'
ULTRA={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180','k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2'}
mode='sparse'
orig=L.make_ini

def make_ini(model,p,tag):
    path=orig(model,p,tag)
    text=Path(path).read_text()
    needle='z_pk = '+SPARSE
    if needle not in text:
        raise RuntimeError('production sparse z_pk line not found')
    if mode=='dense':
        text=text.replace(needle,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text)
        f.write('\n# matched-ultra l2 precision overrides\n')
        for k,v in ULTRA.items():f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini

rows=[]
for m in ('sparse','dense'):
    mode=m
    for name,(model,p) in POINTS.items():
        L.CACHE.clear();r=L.evaluate(model,dict(p))
        if not r.get('ok'):raise RuntimeError(f'{m}/{name}: {r}')
        row={'mode':m,'point':name,'model':model,'score_eff':r['score'],'score_k01':r['score_k01'],'logL_planck':r['logL_planck'],'logL_high':r['logL_high'],'logL_lowT':r['logL_lowT'],'logL_lowE':r['logL_lowE'],'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd']}
        rows.append(row);print('MATCHED_DENSE_BOSS_POINT',json.dumps(row,sort_keys=True),flush=True)
by={(r['mode'],r['point']):r for r in rows}
changes={}
for name in POINTS:
    a=by[('sparse',name)];b=by[('dense',name)]
    changes[name]={'delta_score_eff_dense_minus_sparse':b['score_eff']-a['score_eff'],'delta_score_k01_dense_minus_sparse':b['score_k01']-a['score_k01'],'delta_BOSS_eff':b['chi2_BOSS_eff']-a['chi2_BOSS_eff'],'delta_BOSS_k01':b['chi2_BOSS_k01']-a['chi2_BOSS_k01'],'delta_planck':b['logL_planck']-a['logL_planck'],'delta_SN':b['chi2_SN']-a['chi2_SN'],'delta_rd':b['rd']-a['rd']}
comparison={}
for m in ('sparse','dense'):
    r=by[(m,'rtk_v5')];d=by[(m,'lcdm_partial')]
    comparison[m]={'delta_eff_rtk_minus_lcdm':r['score_eff']-d['score_eff'],'delta_k01_rtk_minus_lcdm':r['score_k01']-d['score_k01']}
summary={'stage':'matched-ultra-l2-sparse-dense-BOSS-fixed-point-audit','scope':'numerical fixed-point audit only; neither point is a final matched optimum','z_pk_sparse':SPARSE,'z_pk_dense':DENSE,'p_k_max_h_mpc':5.0,'ultra_overrides':ULTRA,'rows':rows,'dense_minus_sparse':changes,'fixed_point_rtk_minus_lcdm':comparison}
out=Path('output/matched_l2_dense_boss_pair');out.mkdir(parents=True,exist_ok=True);(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('MATCHED_DENSE_BOSS_RESULT',json.dumps(summary,sort_keys=True),flush=True);print('MATCHED_DENSE_BOSS_COMPLETE',flush=True)
