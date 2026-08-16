#!/usr/bin/env python3
"""Regression smoke test for inference_core_final.py.

The expected scores come from the independent matched-ultra-l2 sparse/dense
BOSS audit run 31935495651.  Reproduction at 1e-9 confirms the builder creates
the same dense-z_pk, l_linstep=2 numerical objective.
"""
import json
import inference_core_final as L

POINTS={
 'rtk_v5':('RTK',{'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,'Om':0.25313821169954864,'As':2.0832030803476467e-9,'ns':0.9644164163369503,'zre':7.21112905430964},1050.4343922976,1050.4346133759982),
 'lcdm_partial':('LCDM',{'lam':0.0,'h':0.6779337587382693,'Ob':0.04872764689799632,'Om':0.26187225794495356,'As':2.1094040998203598e-9,'ns':0.9649685632254442,'zre':7.8583129349509475},1050.2427495092431,1050.242795989815),
}
rows=[]
for name,(model,p,ee,ek) in POINTS.items():
    L.CACHE.clear();r=L.evaluate(model,dict(p))
    if not r.get('ok'):raise RuntimeError(f'{name}: {r}')
    row={'point':name,'model':model,'score_eff':r['score'],'score_k01':r['score_k01'],'delta_eff':r['score']-ee,'delta_k01':r['score_k01']-ek,'expected_eff':ee,'expected_k01':ek,'logL_planck':r['logL_planck'],'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd']}
    rows.append(row);print('FINAL_OBJECTIVE_SMOKE_POINT',json.dumps(row,sort_keys=True),flush=True)
    if abs(row['delta_eff'])>1e-9 or abs(row['delta_k01'])>1e-9:
        raise RuntimeError(f'final-objective regression failed: {row}')
print('FINAL_OBJECTIVE_SMOKE_RESULT',json.dumps({'rows':rows,'tolerance':1e-9,'scope':'numerical objective regression only'},sort_keys=True),flush=True)
print('FINAL_OBJECTIVE_SMOKE_PASS',flush=True)
