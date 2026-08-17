#!/usr/bin/env python3
"""Fixed-center minimal-neutrino robustness check for RTK and LCDM.

This does NOT alter the frozen matched objective/minimum protocol.  It evaluates
both accepted centers in one pinned environment under three neutrino baselines:
  1) frozen massless baseline (N_ncdm=0, N_ur=3.046),
  2) one 0.06 eV species added at fixed dark coordinate,
  3) one 0.06 eV species while subtracting Omega_nu from Om so today's
     non-baryonic matter density is approximately held fixed.

The legacy pinned CLASS explanatory.ini states that T_ncdm=0.71611 gives
m/omega=93.14 eV and recommends N_ur=2.0328 for one massive neutrino when
matching early N_eff=3.046.
"""
from pathlib import Path
import copy, json, math, os

os.environ.setdefault('CLIPY_NOJAX','1')
import inference_core as L

STATE=json.loads(Path('../research/state/current.json').read_text())
DENSE=STATE['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
ORIG=L.make_ini

RTK=dict(STATE['rtk']['accepted_center'])
LCDM=dict(STATE['lcdm']['accepted_center'])


def patch_common(text):
    if 'z_pk = '+SPARSE not in text:
        raise RuntimeError('expected sparse z_pk baseline not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    return text+'\n'+''.join(f'{k} = {v}\n' for k,v in ULTRA.items())


def make_mode(mode):
    def make_ini(model,p,tag):
        path=ORIG(model,p,tag)
        text=patch_common(Path(path).read_text())
        if mode=='massless':
            if 'N_ur = 3.046' not in text or 'N_ncdm = 0' not in text:
                raise RuntimeError('frozen neutrino baseline not found')
        else:
            if 'N_ur = 3.046' not in text or 'N_ncdm = 0' not in text:
                raise RuntimeError('baseline neutrino lines not found')
            text=text.replace('N_ur = 3.046','N_ur = 2.0328',1)
            text=text.replace('N_ncdm = 0','N_ncdm = 1\nm_ncdm = 0.06\nT_ncdm = 0.71611\ndeg_ncdm = 1.0',1)
        Path(path).write_text(text)
        return path
    return make_ini


def omega_nu(h):
    return (0.06/93.14)/(h*h)


def evaluate_mode(mode,model,center):
    p=copy.deepcopy(center)
    omnu=omega_nu(float(p['h'])) if mode!='massless' else 0.0
    if mode=='mnu006_fixed_total_nonbaryonic':
        p['Om']=float(p['Om'])-omnu
        if not p['Om']>0: raise RuntimeError('Om became non-positive')
    L.CACHE.clear()
    L.make_ini=make_mode(mode)
    r=L.evaluate(model,p)
    if not r.get('ok'):
        raise RuntimeError(f'{mode} {model} failed: {r}')
    return {
      'mode':mode,'model':model,'input_params':p,'Omega_nu_today':omnu,
      'score_eff':float(r['score']),'score_k01':float(r['score_k01']),
      'logL_planck':float(r['logL_planck']),'chi2_SN':float(r['chi2_SN']),
      'chi2_BOSS_eff':float(r['chi2_BOSS_eff']),'chi2_BOSS_k01':float(r['chi2_BOSS_k01']),
      'rd':float(r['rd']),'z_drag':float(r['z_drag'])
    }

modes=['massless','mnu006_additive','mnu006_fixed_total_nonbaryonic']
rows=[]
for mode in modes:
    for model,center in [('RTK',RTK),('LCDM',LCDM)]:
        rows.append(evaluate_mode(mode,model,center))
        print('RTK_NEUTRINO_ROBUSTNESS_POINT',json.dumps(rows[-1],sort_keys=True),flush=True)

by={(r['mode'],r['model']):r for r in rows}
summary={'classification':'RTK_NEUTRINO_FIXED_CENTER_ROBUSTNESS_COMPLETE',
         'objective':STATE['objective']['name'],
         'state_iteration':STATE.get('iteration'),
         'frozen_production_unchanged':True,
         'mnu_eV':0.06,'massive_N_ur':2.0328,'T_ncdm':0.71611,'deg_ncdm':1.0,
         'rows':rows,'comparisons':{}}
for mode in modes:
    rr=by[(mode,'RTK')]; ll=by[(mode,'LCDM')]
    summary['comparisons'][mode]={
      'fixed_center_delta_S_eff_RTK_minus_LCDM':rr['score_eff']-ll['score_eff'],
      'fixed_center_delta_S_k01_RTK_minus_LCDM':rr['score_k01']-ll['score_k01'],
      'RTK_delta_from_massless_eff':rr['score_eff']-by[('massless','RTK')]['score_eff'],
      'LCDM_delta_from_massless_eff':ll['score_eff']-by[('massless','LCDM')]['score_eff']}
summary['warning']='Robustness-only fixed-center diagnostic; no reoptimization, no replacement of the frozen production objective, no model-selection significance.'
Path('../neutrino_mass_robustness_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('RTK_NEUTRINO_FIXED_CENTER_ROBUSTNESS_COMPLETE',json.dumps(summary,sort_keys=True),flush=True)
