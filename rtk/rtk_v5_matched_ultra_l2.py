#!/usr/bin/env python3
"""Evaluate RTK v4/v5 fixed points on the exact matched-ultra l_linstep=2 objective.
Numerical fixed-point audit only; not an optimization or model-selection result.
"""
from pathlib import Path
import json
import inference_core as L

POINTS={
 'v4':{'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,'Om':0.25313821169954864,'As':2.082203080347647e-9,'ns':0.9644164163369503,'zre':7.17612905430964},
 'v5':{'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,'Om':0.25313821169954864,'As':2.0832030803476467e-9,'ns':0.9644164163369503,'zre':7.21112905430964},
}
ULTRA={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180','k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2'}
orig=L.make_ini
def make_ini(model,p,tag):
    path=orig(model,p,tag)
    with Path(path).open('a') as f:
        f.write('\n# matched ultra l2 audit\n')
        for k,v in ULTRA.items():f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini
rows=[]
for name,p in POINTS.items():
    L.CACHE.clear();r=L.evaluate('RTK',dict(p))
    if not r.get('ok'):raise RuntimeError(r)
    row={'point':name,'score_eff':r['score'],'score_k01':r['score_k01'],'logL_planck':r['logL_planck'],'logL_high':r['logL_high'],'logL_lowE':r['logL_lowE'],'logL_lowT':r['logL_lowT'],'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd']}
    rows.append(row);print('RTK_V5_MATCHED_L2_POINT',json.dumps(row,sort_keys=True),flush=True)
a,b=rows
comparison={'delta_eff_v5_minus_v4':b['score_eff']-a['score_eff'],'delta_k01_v5_minus_v4':b['score_k01']-a['score_k01'],'delta_planck_term':-2*(b['logL_planck']-a['logL_planck']),'delta_BOSS_eff':b['chi2_BOSS_eff']-a['chi2_BOSS_eff'],'delta_BOSS_k01':b['chi2_BOSS_k01']-a['chi2_BOSS_k01'],'delta_SN':b['chi2_SN']-a['chi2_SN']}
summary={'stage':'rtk-v5-matched-ultra-l2','scope':'fixed-point numerical audit only','ultra_overrides':ULTRA,'rows':rows,'comparison':comparison}
out=Path('output/rtk_v5_matched_ultra_l2');out.mkdir(parents=True,exist_ok=True);(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('RTK_V5_MATCHED_L2_RESULT',json.dumps(summary,sort_keys=True),flush=True);print('RTK_V5_MATCHED_L2_COMPLETE',flush=True)
