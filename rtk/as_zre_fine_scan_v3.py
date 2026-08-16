#!/usr/bin/env python3
"""Third exact A_s-z_re localization around the 1050.22046 v2 boundary record.

All other parameters are fixed. The v2 map selected the +As,+z_re corner, so
this map extends further in both coordinates with the same fine spacings.
Navigation only; not a stationarity/profile/significance claim.
"""
from pathlib import Path
import json,csv
import inference_core as core
CENTER={'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,
        'Om':0.25313821169954864,'As':2.079203080347647e-9,'ns':0.9644164163369503,
        'zre':7.10612905430964}
EXPECTED_EFF=1050.2204635306726; EXPECTED_K01=1050.2343198896031
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
    rows.append(row); print('AS_ZRE_FINE_V3_POINT',json.dumps(row,sort_keys=True),flush=True)
    if ia==0 and jz==0:
      if abs(row['score_eff']-EXPECTED_EFF)>1e-9 or abs(row['score_k01']-EXPECTED_K01)>1e-9: raise RuntimeError(f'center mismatch {row}')
    if best_eff is None or row['score_eff']<best_eff['score_eff']: best_eff=row
    if best_k01 is None or row['score_k01']<best_k01['score_k01']: best_k01=row
lo=min(OFFSETS); hi=max(OFFSETS)
def on_boundary(r): return r['i_As'] in (lo,hi) or r['j_zre'] in (lo,hi)
out=Path('output/as_zre_fine_scan_v3'); out.mkdir(parents=True,exist_ok=True)
with (out/'as_zre_fine_scan_v3.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
summary={'stage':'As-zre-exact-fine-localization-v3','center':CENTER,'delta_As':DAS,'delta_zre':DZRE,'offsets':OFFSETS,
         'best_eff':best_eff,'best_k01':best_k01,'improvement_eff_from_center':EXPECTED_EFF-best_eff['score_eff'],
         'improvement_k01_from_center':EXPECTED_K01-best_k01['score_k01'],'best_eff_on_boundary':on_boundary(best_eff),
         'best_k01_on_boundary':on_boundary(best_k01),'exact_calls':len(rows),
         'scope':'2D exact navigation; all other parameters fixed; not stationarity/profile/significance.'}
(out/'as_zre_fine_summary_v3.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('AS_ZRE_FINE_V3_RESULT',json.dumps(summary,sort_keys=True),flush=True); print('AS_ZRE_FINE_V3_COMPLETE',flush=True)
