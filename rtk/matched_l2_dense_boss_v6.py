#!/usr/bin/env python3
"""Matched-ultra l=2 sparse->dense BOSS audit at the current v6 Newton center.

Only z_pk changes. The RTK point is the strict-v5 k01-scale-0.5 Newton candidate
used as the v6 strict center. LCDM is the current matched-ultra partial control.
Fixed-point numerical audit only; not model selection.
"""
from pathlib import Path
import json
import inference_core as L

POINTS={
 'rtk_v6':('RTK',{'lam':287930.95430552866,'h':0.6904668858782219,'Ob':0.046835996338062985,'Om':0.2530185206833107,'As':2.0836316905673827e-9,'ns':0.9644013704702473,'zre':7.218930610576525}),
 'lcdm_partial':('LCDM',{'lam':0.0,'h':0.6779337587382693,'Ob':0.04872764689799632,'Om':0.26187225794495356,'As':2.1094040998203598e-9,'ns':0.9649685632254442,'zre':7.8583129349509475}),
}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE='0.,0.25,0.30,0.34,0.36,0.37,0.38,0.39,0.40,0.42,0.47,0.49,0.50,0.51,0.52,0.53,0.55,0.57,0.59,0.60,0.61,0.62,0.63,0.65,0.70,0.75,1.0'
ULTRA={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180','k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2'}
mode='sparse';orig=L.make_ini

def make_ini(model,p,tag):
    path=orig(model,p,tag)
    text=Path(path).read_text(); needle='z_pk = '+SPARSE
    if needle not in text: raise RuntimeError('production sparse z_pk line not found')
    if mode=='dense': text=text.replace(needle,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text);f.write('\n# matched-ultra l2 overrides\n')
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
        rows.append(row);print('V6_DENSE_BOSS_POINT',json.dumps(row,sort_keys=True),flush=True)
by={(r['mode'],r['point']):r for r in rows}
changes={}
for name in POINTS:
    a=by[('sparse',name)];b=by[('dense',name)]
    changes[name]={'delta_score_eff':b['score_eff']-a['score_eff'],'delta_score_k01':b['score_k01']-a['score_k01'],'delta_BOSS_eff':b['chi2_BOSS_eff']-a['chi2_BOSS_eff'],'delta_BOSS_k01':b['chi2_BOSS_k01']-a['chi2_BOSS_k01'],'delta_planck':b['logL_planck']-a['logL_planck'],'delta_SN':b['chi2_SN']-a['chi2_SN'],'delta_rd':b['rd']-a['rd']}
comparison={}
for m in ('sparse','dense'):
    r=by[(m,'rtk_v6')];d=by[(m,'lcdm_partial')]
    comparison[m]={'delta_eff_rtk_minus_lcdm':r['score_eff']-d['score_eff'],'delta_k01_rtk_minus_lcdm':r['score_k01']-d['score_k01']}
summary={'stage':'v6-matched-ultra-l2-sparse-dense-BOSS','scope':'fixed-point numerical audit only','ultra_overrides':ULTRA,'z_pk_sparse':SPARSE,'z_pk_dense':DENSE,'rows':rows,'dense_minus_sparse':changes,'fixed_point_rtk_minus_lcdm':comparison}
out=Path('output/matched_l2_dense_boss_v6');out.mkdir(parents=True,exist_ok=True);(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('V6_DENSE_BOSS_RESULT',json.dumps(summary,sort_keys=True),flush=True);print('V6_DENSE_BOSS_COMPLETE',flush=True)
