#!/usr/bin/env python3
"""Deterministic numerical replay of the C10 action-level lapse-source ratio excess.

This is a diagnostic replay of an already-proved analytic ratio, not a blind
science-selection gate and not a likelihood-impact estimate.
"""
import json, math
from pathlib import Path

root=Path(__file__).resolve().parents[1]
target=json.load(open(root/'research/theory_targets/RTK_C10_SMIX_SOURCE_RATIO_IMPACT_REPLAY_TARGET_v1.json'))
state=json.load(open(root/'research/state/current.json'))
fr=state['final_replay_result']
assert fr['status']=='PASS'
assert abs(float(fr['rtk']['expected_score_eff'])-target['reference']['required_rtk_score'])<1e-12
p=fr['rtk']['params']

gamma=float(target['reference']['gamma_certified'])
h=float(p['h']); lam=float(p['lam']); OmK=float(p['Om'])
H0=100.0*h/299792.458
mu=3.0*H0*math.sqrt(gamma)
A=OmK/(6.0*gamma)
D=1.0+2.0*A+lam*A*A
rootD=math.sqrt(D)
x0=A*(2.0+lam*A)/(1.0+lam*A+rootD)

def row(z,kh):
    a=1.0/(1.0+z)
    x=x0/a**3
    s=math.hypot(1.0,math.sqrt(lam)*x)
    r=x/s
    Q=1.0+r
    MK=mu*Q*s*math.sqrt(s)
    kstar=a*MK
    kcom=kh*h
    R=(kcom/kstar)**2
    return {'z':z,'a':a,'k_h_Mpc':kh,'M_K_Mpc_inv':MK,'kstar_Mpc_inv':kstar,
            'R_excess_k2_over_MK2':R,'source_ratio_1_plus_R':1.0+R}

z0=row(0.0,0.24)
assert abs(z0['M_K_Mpc_inv']-target['reference']['required_MK_z0_Mpc_inv']) <= target['reference']['MK_z0_abs_tolerance']

boss=[]
for z in target['boss']['redshifts']:
    for kh in target['boss']['k_h_Mpc']:
        boss.append(row(float(z),float(kh)))

zspec=fr['objective']['dense_z_pk']
if isinstance(zspec,str):
    zgrid=[float(x) for x in zspec.split(',') if x.strip()]
else:
    zgrid=[float(x) for x in zspec]
technical=[row(z,float(target['technical_domain']['P_k_max_h_Mpc'])) for z in zgrid]

boss_max=max(boss,key=lambda r:r['R_excess_k2_over_MK2'])
technical_max=max(technical,key=lambda r:r['R_excess_k2_over_MK2'])
out={
  'classification':'C10_SMIX_SOURCE_RATIO_IMPACT_REPLAY_PASS',
  'status_scope':'GREEN_DETERMINISTIC_RATIO_REPLAY_NOT_OBSERVABLE_ERROR_ESTIMATE',
  'reference_params':p,
  'gamma':gamma,'mu_K_Mpc_inv':mu,'x0':x0,
  'z0_M_K_Mpc_inv':z0['M_K_Mpc_inv'],
  'boss_rows':boss,
  'boss_max':boss_max,
  'boss_max_percent_excess':100.0*boss_max['R_excess_k2_over_MK2'],
  'technical_Pkmax_rows':technical,
  'technical_max':technical_max,
  'technical_max_percent_excess':100.0*technical_max['R_excess_k2_over_MK2'],
  'interpretation':'On the historical replay-certified RTK point, the action-level lapse-source ratio excess is sub-percent across the actual frozen BOSS k-window at its three effective redshifts, while it can be order unity or larger at the technical high-k endpoint. This does not translate directly into likelihood error; the completed metric solver is required.',
  'non_claims':target['non_claims'],
  'target':'research/theory_targets/RTK_C10_SMIX_SOURCE_RATIO_IMPACT_REPLAY_TARGET_v1.json'
}
Path('c10_smix_source_ratio_impact_replay_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
