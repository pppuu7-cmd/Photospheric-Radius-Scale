#!/usr/bin/env python3
"""Cross-grid audit of CLASS ell-sampling controls.

Separates l_logstep from l_linstep near the dense regime. Two fixed RTK points
are compared so both absolute and differential numerical convergence can be
assessed. No optimization or statistical inference is performed.
"""
from pathlib import Path
import json
import inference_core as core

POINTS={
 'old300k': {'lam':300000.0,'h':0.6906430189065689,'Ob':0.046822913729452804,
             'Om':0.25278507230249403,'As':2.0695004530982282e-9,
             'ns':0.9644419669945631,'zre':6.8611290543096395},
 'orthogonal': {'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,
                'Om':0.25313821169954864,'As':2.0752030803476467e-9,
                'ns':0.9644164163369503,'zre':7.00112905430964},
}
# Cross rather than diagonal: isolate each control near the dense regime.
COMBOS=[
 ('l104_n10','1.04','10'),('l104_n5','1.04','5'),('l104_n3','1.04','3'),
 ('l102_n10','1.02','10'),('l102_n5','1.02','5'),('l102_n3','1.02','3'),
 ('l101_n10','1.01','10'),('l101_n5','1.01','5'),('l101_n3','1.01','3'),
]
orig=core.make_ini; active={}
def make_ini(model,p,tag):
    path=orig(model,p,tag)
    with Path(path).open('a') as f:
        f.write('\n# ell-sampling cross-grid overrides\n')
        for k,v in active.items(): f.write(f'{k} = {v}\n')
    return path
core.make_ini=make_ini
rows=[]
for label,llog,llin in COMBOS:
    active.clear(); active.update({'l_logstep':llog,'l_linstep':llin})
    for name,p in POINTS.items():
        core.CACHE.clear(); r=core.evaluate('RTK',dict(p))
        if not r.get('ok',False): raise RuntimeError(f'{label}/{name}: {r}')
        row={'label':label,'l_logstep':float(llog),'l_linstep':int(llin),'point':name,
             'score_eff':r['score'],'score_k01':r['score_k01'],'logL_high':r['logL_high'],
             'logL_planck':r['logL_planck'],'chi2_SN':r['chi2_SN'],
             'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd']}
        rows.append(row); print('ELL_CROSSGRID_POINT',json.dumps(row,sort_keys=True),flush=True)
by={(r['label'],r['point']):r for r in rows}; comps=[]
for label,llog,llin in COMBOS:
    a=by[(label,'old300k')]; b=by[(label,'orthogonal')]
    c={'label':label,'l_logstep':float(llog),'l_linstep':int(llin),
       'old300k_eff':a['score_eff'],'orthogonal_eff':b['score_eff'],
       'delta_eff':b['score_eff']-a['score_eff'],
       'delta_k01':b['score_k01']-a['score_k01'],
       'old_high_term':-2*a['logL_high'],'orthogonal_high_term':-2*b['logL_high']}
    comps.append(c); print('ELL_CROSSGRID_COMPARISON',json.dumps(c,sort_keys=True),flush=True)
summary={'stage':'CLASS-ell-sampling-crossgrid','rows':rows,'comparisons':comps,
 'scope':'Fixed-point numerical convergence audit only; no optimization/statistical inference.'}
out=Path('output/class_ell_sampling_crossgrid'); out.mkdir(parents=True,exist_ok=True)
(out/'class_ell_sampling_crossgrid_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('ELL_CROSSGRID_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('ELL_CROSSGRID_COMPLETE',flush=True)
