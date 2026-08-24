#!/usr/bin/env python3
import json, math
from pathlib import Path

root=Path(__file__).resolve().parents[1]
t=json.load(open(root/'research/theory_targets/RTK_C10_FLRW_MISMATCH_COEFFICIENT_REPLAY_TARGET_v1.json'))
s=json.load(open(root/'research/state/current.json'))
fr=s['final_replay_result']; p=fr['rtk']['params']
assert fr['status']=='PASS'
assert abs(float(fr['rtk']['expected_score_eff'])-t['reference']['required_score'])<1e-12
h=float(p['h']); lam=float(p['lam']); Om=float(p['Om']); gamma=float(t['reference']['gamma'])
H0=100*h/299792.458; mu=3*H0*math.sqrt(gamma)
A0=Om/(6*gamma); D=1+2*A0+lam*A0*A0; rootD=math.sqrt(D)
x0=A0*(2+lam*A0)/(1+lam*A0+rootD)

def evalrow(z,kh):
    a=1/(1+z); x=x0/a**3; ss=math.hypot(1,math.sqrt(lam)*x); r=x/ss; Q=1+r
    ca=r/(ss*(ss+x)); MK=mu*Q*ss*math.sqrt(ss); kstar=a*MK
    R=(kh*h/kstar)**2; cs=ca/(1+R); eps=3*abs(ca-cs)
    return {'z':z,'k_h_Mpc':kh,'c_a_sq':ca,'c_s_sq':cs,'R':R,'epsilon_theta_over_H':eps,
            'M_K_Mpc_inv':MK,'kstar_Mpc_inv':kstar}

z0=evalrow(0.0,0.24)
assert abs(z0['M_K_Mpc_inv']-t['reference']['required_MK_z0_Mpc_inv'])<1e-12
boss=[evalrow(float(z),float(t['boss']['k_h_Mpc_max'])) for z in t['boss']['redshifts']]
zspec=fr['objective']['dense_z_pk']; zgrid=[float(x) for x in zspec.split(',') if x.strip()] if isinstance(zspec,str) else list(map(float,zspec))
technical=[evalrow(z,float(t['technical']['P_k_max_h_Mpc'])) for z in zgrid]
bmax=max(boss,key=lambda x:x['epsilon_theta_over_H']); tmax=max(technical,key=lambda x:x['epsilon_theta_over_H'])
out={
 'classification':'C10_FLRW_MISMATCH_COEFFICIENT_REPLAY_PASS',
 'status_scope':'GREEN_DETERMINISTIC_COEFFICIENT_REPLAY_NOT_OBSERVABLE_ERROR',
 'boss_rows':boss,'boss_max':bmax,
 'technical_rows':technical,'technical_max':tmax,
 'boss_max_epsilon_theta_over_H':bmax['epsilon_theta_over_H'],
 'technical_max_epsilon_theta_over_H':tmax['epsilon_theta_over_H'],
 'interpretation':'The exact-action vs production Euler-friction difference is coefficient-suppressed by the extremely small adiabatic sound speed. On the historical RTK point, the coefficient 3|c_a^2-c_s^2| is tiny on both the BOSS window and the full dense technical endpoint, although this alone does not bound the state-dependent density-equation residual or an observable error.',
 'non_claims':t['non_claims'],
 'target':'research/theory_targets/RTK_C10_FLRW_MISMATCH_COEFFICIENT_REPLAY_TARGET_v1.json'
}
Path('c10_flrw_mismatch_coefficient_replay_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
