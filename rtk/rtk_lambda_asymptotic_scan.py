#!/usr/bin/env python3
"""Conditional high-lambda exact likelihood scan around the recovered RTK basin.

All non-lambda parameters are fixed to the artifact-verified Stage 4C.1 k01
best point. This is a direction diagnostic only, not a profiled likelihood or
constraint on lambda_D.
"""
from pathlib import Path
import csv, json, sys
import inference_core as L

P0={'h':0.6876415412107025,'Ob':0.04713370853636241,
    'Om':0.2563078649786827,'As':2.052560909053839e-9,
    'ns':0.9627323451269592,'zre':6.35470443812342}
LAM=[1000.,1877.1636529486852,3253.599566504292,5000.,8000.,15000.,30000.,100000.]
out=Path('output/lambda_asymptotic');out.mkdir(parents=True,exist_ok=True)
rows=[]
for lam in LAM:
    p=dict(P0);p['lam']=lam
    r=L.evaluate('RTK',p)
    if not r.get('ok'):raise RuntimeError((lam,r))
    row={'lambda_D':lam,'score_eff':r['score'],'score_k01':r['score_k01'],
         'logL_planck':r['logL_planck'],'chi2_SN':r['chi2_SN'],
         'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],
         'rd':r['rd']}
    rows.append(row);print('LAMBDA_SCAN',row,flush=True)
with (out/'lambda_asymptotic_scan.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary={'scope':'conditional_exact_scan_not_profiled_constraint','fixed_params':P0,
         'rows':rows,'best_eff':min(rows,key=lambda x:x['score_eff']),
         'best_k01':min(rows,key=lambda x:x['score_k01']),
         'warning':'Non-lambda parameters are fixed. A monotonic trend is diagnostic only and must be confirmed by profiled optimization.'}
(out/'lambda_asymptotic_scan.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('ASYMPTOTIC_SCAN_PASS',flush=True)
