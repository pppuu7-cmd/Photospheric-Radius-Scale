#!/usr/bin/env python3
from pathlib import Path
import json
import inference_core as core
POINTS={
 'previous':{'p':{'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,'Om':0.25313821169954864,'As':2.078203080347647e-9,'ns':0.9644164163369503,'zre':7.07112905430964},'eff':1050.2553996957809,'k01':1050.2691358734728},
 'v2best':{'p':{'lam':293868.81143246836,'h':0.6903899123316766,'Ob':0.046851744145772894,'Om':0.25313821169954864,'As':2.079203080347647e-9,'ns':0.9644164163369503,'zre':7.10612905430964},'eff':1050.2204635306726,'k01':1050.2343198896031},
}
LEVELS=[('baseline',{}),('tight',{'tol_background_integration':'1e-3','tol_thermo_integration':'1e-3','tol_perturb_integration':'1e-6','perturb_sampling_stepsize':'0.025','k_per_decade_for_pk':'30','k_per_decade_for_bao':'140','k_max_tau0_over_l_max':'3.5','l_logstep':'1.04','l_linstep':'10'}),('ultra',{'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180','k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'5'})]
orig=core.make_ini; active={}
def make_ini(model,p,tag):
    path=orig(model,p,tag)
    if active:
        with Path(path).open('a') as f:
            f.write('\n# As-zre v2 record precision overrides\n')
            for k,v in active.items(): f.write(f'{k} = {v}\n')
    return path
core.make_ini=make_ini
rows=[]
for level,ov in LEVELS:
    active.clear(); active.update(ov)
    for name,spec in POINTS.items():
        core.CACHE.clear(); r=core.evaluate('RTK',dict(spec['p']))
        if not r.get('ok',False): raise RuntimeError(f'{level}/{name}: {r}')
        row={'level':level,'point':name,'score_eff':r['score'],'score_k01':r['score_k01'],'logL_planck':r['logL_planck'],'logL_high':r['logL_high'],'logL_lowT':r['logL_lowT'],'logL_lowE':r['logL_lowE'],'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd']}
        rows.append(row); print('V2BEST_PRECISION_POINT',json.dumps(row,sort_keys=True),flush=True)
        if level=='baseline':
            if abs(row['score_eff']-spec['eff'])>1e-9 or abs(row['score_k01']-spec['k01'])>1e-9: raise RuntimeError(f'baseline regression {name}: {row}')
by={(r['level'],r['point']):r for r in rows}; comps=[]
for level,_ in LEVELS:
    a=by[(level,'previous')]; b=by[(level,'v2best')]
    c={'level':level,'delta_eff':b['score_eff']-a['score_eff'],'delta_k01':b['score_k01']-a['score_k01'],'delta_planck_term':-2*(b['logL_planck']-a['logL_planck']),'delta_high_term':-2*(b['logL_high']-a['logL_high']),'delta_lowT_term':-2*(b['logL_lowT']-a['logL_lowT']),'delta_lowE_term':-2*(b['logL_lowE']-a['logL_lowE']),'delta_SN':b['chi2_SN']-a['chi2_SN'],'delta_BOSS_eff':b['chi2_BOSS_eff']-a['chi2_BOSS_eff'],'delta_BOSS_k01':b['chi2_BOSS_k01']-a['chi2_BOSS_k01']}
    comps.append(c); print('V2BEST_PRECISION_COMPARISON',json.dumps(c,sort_keys=True),flush=True)
for i in range(1,len(comps)):
    comps[i]['change_delta_eff_vs_previous_level']=comps[i]['delta_eff']-comps[i-1]['delta_eff']; comps[i]['change_delta_k01_vs_previous_level']=comps[i]['delta_k01']-comps[i-1]['delta_k01']
out=Path('output/class_precision_v2best_pair'); out.mkdir(parents=True,exist_ok=True)
summary={'stage':'As-zre-v2best-differential-precision','rows':rows,'comparisons':comps,'scope':'fixed-point numerical audit only'}
(out/'class_precision_v2best_pair_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('V2BEST_PRECISION_RESULT',json.dumps(summary,sort_keys=True),flush=True); print('V2BEST_PRECISION_COMPLETE',flush=True)
