#!/usr/bin/env python3
"""Fifth exact A_s-z_re navigation map around the v4 boundary record.

v4 selected the upper A_s and z_re corner. This map extends both coordinates
upward with the established fine spacings. All other parameters are fixed.
Navigation only; not a stationarity/profile/model-selection calculation.
"""
from pathlib import Path
import json,csv
import inference_core as core
CENTER={'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,
        'Om':0.25313821169954864,'As':2.082203080347647e-9,'ns':0.9644164163369503,
        'zre':7.17612905430964}
EXPECTED_EFF=1050.135699621492
EXPECTED_K01=1050.149916197271
CENTER_REG_TOL=1e-6
DAS=5.0e-13; DZRE=0.0175; OFFSETS=[-1,0,1,2,3]
rows=[]; best_eff=None; best_k01=None
for ia in OFFSETS:
  for jz in OFFSETS:
    p=dict(CENTER); p['As']=CENTER['As']+ia*DAS; p['zre']=CENTER['zre']+jz*DZRE
    core.CACHE.clear(); r=core.evaluate('RTK',p)
    if not r.get('ok',False): raise RuntimeError(f'failed {ia=} {jz=}: {r}')
    row={'i_As':ia,'j_zre':jz,'As':p['As'],'zre':p['zre'],'score_eff':r['score'],'score_k01':r['score_k01'],
         'logL_planck':r['logL_planck'],'logL_high':r['logL_high'],'logL_lowT':r['logL_lowT'],'logL_lowE':r['logL_lowE'],
         'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd']}
    rows.append(row); print('AS_ZRE_FINE_V5_POINT',json.dumps(row,sort_keys=True),flush=True)
    if ia==0 and jz==0:
      de=row['score_eff']-EXPECTED_EFF; dk=row['score_k01']-EXPECTED_K01
      print('AS_ZRE_FINE_V5_CENTER_REGRESSION',json.dumps({'delta_eff':de,'delta_k01':dk,'tol':CENTER_REG_TOL},sort_keys=True),flush=True)
      if abs(de)>CENTER_REG_TOL or abs(dk)>CENTER_REG_TOL: raise RuntimeError(f'center mismatch {row}')
    if best_eff is None or row['score_eff']<best_eff['score_eff']: best_eff=row
    if best_k01 is None or row['score_k01']<best_k01['score_k01']: best_k01=row
lo=min(OFFSETS); hi=max(OFFSETS)
def on_boundary(r): return r['i_As'] in (lo,hi) or r['j_zre'] in (lo,hi)
out=Path('output/as_zre_fine_scan_v5'); out.mkdir(parents=True,exist_ok=True)
with (out/'as_zre_fine_scan_v5.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
summary={'stage':'As-zre-exact-fine-localization-v5','center':CENTER,'center_regression_tolerance':CENTER_REG_TOL,
         'delta_As':DAS,'delta_zre':DZRE,'offsets':OFFSETS,'best_eff':best_eff,'best_k01':best_k01,
         'improvement_eff_from_center':EXPECTED_EFF-best_eff['score_eff'],
         'improvement_k01_from_center':EXPECTED_K01-best_k01['score_k01'],
         'best_eff_on_boundary':on_boundary(best_eff),'best_k01_on_boundary':on_boundary(best_k01),
         'exact_calls':len(rows),'scope':'2D exact navigation only; all other parameters fixed; not stationarity/profile/significance.'}
(out/'as_zre_fine_summary_v5.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('AS_ZRE_FINE_V5_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('AS_ZRE_FINE_V5_COMPLETE',flush=True)
