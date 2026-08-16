#!/usr/bin/env python3
from pathlib import Path
import json
import inference_core as core
P={'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,'Om':0.25313821169954864,'As':2.080703080347647e-9,'ns':0.9644164163369503,'zre':7.14112905430964}
rows=[]
for i in range(5):
    core.CACHE.clear(); r=core.evaluate('RTK',dict(P))
    if not r.get('ok',False): raise RuntimeError(r)
    row={'repeat':i,'score_eff':float(r['score']),'score_k01':float(r['score_k01']),'chi2_BOSS_eff':float(r['chi2_BOSS_eff']),'chi2_BOSS_k01':float(r['chi2_BOSS_k01']),'logL_planck':float(r['logL_planck']),'rd':float(r['rd'])}
    rows.append(row); print('V3_REPEAT_POINT',json.dumps(row,sort_keys=True),flush=True)
def spread(k):
    v=[r[k] for r in rows]; return max(v)-min(v)
summary={'stage':'v3-fixed-point-repeatability','repeats':len(rows),'rows':rows,'spread_eff':spread('score_eff'),'spread_k01':spread('score_k01'),'spread_boss_eff':spread('chi2_BOSS_eff'),'spread_boss_k01':spread('chi2_BOSS_k01'),'spread_planck':spread('logL_planck'),'spread_rd':spread('rd'),'scientific_tolerance':0.005}
out=Path('output/k01_repeatability_v3'); out.mkdir(parents=True,exist_ok=True)
(out/'k01_repeatability_v3_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('V3_REPEAT_RESULT',json.dumps(summary,sort_keys=True),flush=True); print('V3_REPEAT_COMPLETE',flush=True)
