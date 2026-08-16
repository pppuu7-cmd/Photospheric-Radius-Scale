#!/usr/bin/env python3
"""Exact 2D Ob-ns scan around the t4 scale-0.5 orthogonal record.

All other cosmological parameters are fixed.  This is a navigation/localization
scan only; it is not a 7D stationarity certificate or profile likelihood.
"""
from pathlib import Path
import json, csv
import inference_core as core

CENTER={
 'lam':293868.81143246836,
 'h':0.6903899123316766,
 'Ob':0.046851744145772894,
 'Om':0.25313821169954864,
 'As':2.0752030803476467e-9,
 'ns':0.9644164163369503,
 'zre':7.00112905430964,
}
EXPECTED_EFF=1050.362361331656984
EXPECTED_K01=1050.375737633925155
# Half of the scale-0.5 stencil steps used to discover the center.
DOB=1.75e-5
DNS=8.75e-5
OFFSETS=[-2,-1,0,1,2]

rows=[]
best_eff=None; best_k01=None
for io in OFFSETS:
    for jn in OFFSETS:
        p=dict(CENTER)
        p['Ob']=CENTER['Ob']+io*DOB
        p['ns']=CENTER['ns']+jn*DNS
        core.CACHE.clear()
        r=core.evaluate('RTK',p)
        if not r.get('ok',False):
            raise RuntimeError(f'failed exact point io={io} jn={jn}: {r}')
        row={
          'i_Ob':io,'j_ns':jn,'Ob':p['Ob'],'ns':p['ns'],
          'score_eff':r['score'],'score_k01':r['score_k01'],
          'logL_planck':r['logL_planck'],'logL_high':r['logL_high'],
          'logL_lowT':r['logL_lowT'],'logL_lowE':r['logL_lowE'],
          'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],
          'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd']}
        rows.append(row)
        print('ORTHOGONAL_2D_POINT',json.dumps(row,sort_keys=True),flush=True)
        if io==0 and jn==0:
            if abs(row['score_eff']-EXPECTED_EFF)>1e-9 or abs(row['score_k01']-EXPECTED_K01)>1e-9:
                raise RuntimeError('center regression mismatch')
        if best_eff is None or row['score_eff']<best_eff['score_eff']: best_eff=row
        if best_k01 is None or row['score_k01']<best_k01['score_k01']: best_k01=row

out=Path('output/orthogonal_ob_ns_scan'); out.mkdir(parents=True,exist_ok=True)
with (out/'orthogonal_ob_ns_scan.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
summary={
 'stage':'orthogonal-Ob-ns-exact-localization',
 'center':CENTER,'delta_Ob':DOB,'delta_ns':DNS,'offsets':OFFSETS,
 'best_eff':best_eff,'best_k01':best_k01,
 'improvement_eff_from_center':EXPECTED_EFF-best_eff['score_eff'],
 'improvement_k01_from_center':EXPECTED_K01-best_k01['score_k01'],
 'exact_calls':len(rows),
 'scope':'2D exact navigation with all other parameters fixed; not stationarity/profile/significance.'}
(out/'orthogonal_ob_ns_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('ORTHOGONAL_2D_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('ORTHOGONAL_2D_COMPLETE',flush=True)
