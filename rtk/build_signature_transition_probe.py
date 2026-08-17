#!/usr/bin/env python3
"""Probe the intrinsic RTK/LCDM linear-theory shape through k~k_star.

Shared cosmological parameters are fixed to the current RTK accepted center.
This is a theory diagnostic only; k above the nonlinear observational regime is
included solely to locate the linear-equation transition and must not be used
as a nonlinear-data prediction.
"""
import json, math, re
from pathlib import Path
import build_signature_atlas_pair as B

KPROBE=[0.01,0.05,0.1,0.2,0.5,0.75,1.0,1.5,2.0,3.0,4.0]
ZPROBE=[0.0,0.38,0.61,1.0]
B.K_TARGETS=KPROBE
B.PK_Z_TARGETS=ZPROBE
_old_interp=B.interp_pk

def strict_interp(rows,k):
    lo,hi=rows[0][0],rows[-1][0]
    if not (lo <= k <= hi):
        raise RuntimeError(f'k={k} outside exact P(k) output range [{lo},{hi}]')
    return _old_interp(rows,k)
B.interp_pk=strict_interp

S=B.STATE
KEYS=('As','Ob','Om','h','ns','zre')
shared={k:S['rtk']['accepted_center'][k] for k in KEYS}
lam=S['rtk']['accepted_center']['lam']


def parse_gamma(path):
    text=Path(path).read_text()
    m=re.search(r'RTK_LOG_GAMMA_ROOT[^\n]*gamma=([0-9eE+\-.]+)',text)
    if not m: raise RuntimeError('gamma root not found in RTK CLASS log')
    return float(m.group(1))


def khr_scales(gamma):
    h=shared['h']; Om=shared['Om']; c_km_s=299792.458
    H0=100.0*h/c_km_s
    mu=3.0*H0*math.sqrt(gamma)
    A=Om/(6.0*gamma)
    D=1.0+2.0*A+lam*A*A
    x0=A*(2.0+lam*A)/(1.0+lam*A+math.sqrt(D))
    out={}
    for z in ZPROBE:
        a=1.0/(1.0+z); x=x0/(a*a*a); s=math.hypot(1.0,math.sqrt(lam)*x)
        r=x/s; Q=1.0+r; ca2=r/(s*(s+x)); MK=mu*Q*s*math.sqrt(s); ks=a*MK
        out[str(z)]={'kstar_Mpc_inv':ks,'kstar_h_Mpc':ks/h,'ca2':ca2,
                     'cs2_over_ca2':{str(k):1.0/(1.0+(k/(ks/h))**2) for k in KPROBE}}
    return {'gamma':gamma,'mu_K_Mpc_inv':mu,'x0':x0,'by_z':out}


def main():
    rp=dict(shared);rp['lam']=lam
    lp=dict(shared);lp['lam']=0.0
    r=B.run_model('RTK',rp,'transition_rtk')
    l=B.run_model('LCDM',lp,'transition_lcdm')
    gamma=parse_gamma('signature_transition_rtk.log')
    payload={'status':'LINEAR_THEORY_TRANSITION_DIAGNOSTIC_NOT_NONLINEAR_PREDICTION',
             'objective':S['objective']['name'],'state_iteration':S.get('iteration'),
             'shared_parameters':shared,'lambda_D':lam,'k_probe_h_Mpc':KPROBE,
             'khronon_scales':khr_scales(gamma),
             'residual_rtk_over_lcdm_minus_one':B.build_residuals(r,l),
             'warning':'k above the linear observational regime is used only to locate the implemented RTK transition; no Halofit/N-body claim.'}
    p=Path('output/signature_atlas/transition_probe.json');p.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print('RTK_TRANSITION_SCALES',json.dumps(payload['khronon_scales'],sort_keys=True))
    print('RTK_TRANSITION_PK',json.dumps(payload['residual_rtk_over_lcdm_minus_one']['pk'],sort_keys=True))
    print('RTK_SIGNATURE_TRANSITION_COMPLETE')

if __name__=='__main__': main()
