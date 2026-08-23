#!/usr/bin/env python3
"""Resolution-audited tree-level power-counting proxy for the frozen RTK scalar.

This is NOT a partial-wave unitarity theorem.  It builds a dimensionless generic
non-resonant tree envelope from the exact reconstructed P(X) cubic/quartic
coefficients and the exact rational quadratic dispersion.  The mixed C(X)
vertices are included as a separately reported contribution.

External momentum y=k/M_K uses exact finite-k normalization Zrel=1+y^2 and
omega=c_a k/sqrt(1+y^2).  Define an absolute-value contact envelope and a
non-resonant exchange proxy V3^2/omega^2.  Resonant/forward denominators,
metric/U1/auxiliary exchange and loop effects are intentionally excluded.
"""
import json, math, time
import numpy as np

# Replay-certified matched-local RTK point.
h=0.691103719964454
OmegaK0=0.2522864064078236
lambdaD=219457.5727136581
gamma=0.05170371280716
MPC_M=3.0856775814913673e22
HBARC_EV_M=1.973269804e-7
INV_MPC_EV=HBARC_EV_M/MPC_M
MPL=2.435e27
T_CMB_K=2.7255
KB_EV_K=8.617333262e-5
H0=100.0*h/299792.458
mu=3.0*H0*math.sqrt(gamma)
mu_eV=mu*INV_MPC_EV
A0=OmegaK0/(6.0*gamma)
x0=A0*(2.0+lambdaD*A0)/(1.0+lambdaD*A0+math.sqrt(1.0+2.0*A0+lambdaD*A0*A0))


def state(z):
    x=x0*(1.0+z)**3
    s=math.hypot(1.0,math.sqrt(lambdaD)*x)
    r=x/s
    delta=1.0/(s*s)
    ca2=r*delta/(1.0+r)
    MK=mu_eV*(1.0+r)*s*math.sqrt(s)
    C3t=math.sqrt(2.0)*lambdaD*r/(4.0*MPL*mu_eV*delta**0.25)
    C3s=-math.sqrt(2.0)*(1.0+lambdaD*r**3)*delta**0.75/(4.0*MPL*mu_eV*(1.0+r)**2)
    C4t=lambdaD*(1.0+4.0*lambdaD*r*r)/(16.0*MPL**2*mu_eV**2*math.sqrt(delta))
    C4ts=-math.sqrt(delta)*(2.0*lambdaD**2*r**5+lambdaD*r**3+8.0*lambdaD*r*r+3.0*lambdaD*r-2.0)/(8.0*MPL**2*mu_eV**2*(1.0+r)**3)
    C4s=delta**1.5*(1.0+lambdaD*r**3)/(16.0*MPL**2*mu_eV**2*(1.0+r)**3)
    return dict(r=r,delta=delta,ca2=ca2,MK_eV=MK,C3t=C3t,C3s=C3s,C4t=C4t,C4ts=C4ts,C4s=C4s)


def scan_y(z,ny=2401,ymin=1e-5,ymax=1e5):
    st=state(z)
    y=np.logspace(math.log10(ymin),math.log10(ymax),ny)
    MK=st['MK_eV']; ca=math.sqrt(st['ca2'])
    k=y*MK; Z=1.0+y*y; omega=ca*k/np.sqrt(Z)
    # P(X) cubic absolute envelope after one Zrel^{-1/2} per external leg.
    V3pt=abs(st['C3t'])*omega**3/Z**1.5
    V3ps=abs(st['C3s'])*omega*k*k/Z**1.5
    # Exact low-k canonical mixed coefficient with finite-k external normalization.
    g3m=1.0/(math.sqrt(2.0)*MPL*MK**3)
    V3m=g3m*k*k*omega**3/Z**1.5
    exP=((V3pt+V3ps)/omega)**2
    exM=(V3m/omega)**2
    exTotal=((V3pt+V3ps+V3m)/omega)**2
    # P quartic contact absolute envelope.
    A4pt=abs(st['C4t'])*omega**4/Z**2
    A4pts=abs(st['C4ts'])*omega**2*k*k/Z**2
    A4ps=abs(st['C4s'])*k**4/Z**2
    A4P=A4pt+A4pts+A4ps
    g4m=1.0/(4.0*MPL**2*MK**4)
    A4M=g4m*(k**4*omega**2+3.0*k*k*omega**4)/Z**2
    total=exTotal+A4P+A4M
    i=int(np.nanargmax(total))
    return {
      'z':float(z),'y_at_max':float(y[i]),'proxy_max':float(total[i]),
      'exchange_total_at_max':float(exTotal[i]),'exchange_P_at_max':float(exP[i]),
      'exchange_mixed_at_max':float(exM[i]),'contact_P_at_max':float(A4P[i]),
      'contact_mixed_at_max':float(A4M[i]),'omega_at_max_eV':float(omega[i]),
      'k_at_max_eV':float(k[i]),'M_K_eV':MK,'c_a':ca,'delta':st['delta']
    }

start=time.time()
refs=[scan_y(z) for z in [0.0,1100.0,1.0e9,1.0e12,4.56e12,1.0e13]]
assert refs[2]['proxy_max']<1e-30
assert refs[3]['proxy_max']<1e-4
assert refs[4]['proxy_max']>0.5
assert refs[5]['proxy_max']>100.0

# Crossing of the proxy through unity. Logarithmic bisection in redshift.
lo,hi=1.0e12,1.0e13
assert scan_y(lo,ny=1601)['proxy_max']<1.0
assert scan_y(hi,ny=1601)['proxy_max']>1.0
for _ in range(70):
    mid=math.sqrt(lo*hi)
    if scan_y(mid,ny=1601)['proxy_max']<1.0: lo=mid
    else: hi=mid
zcross=math.sqrt(lo*hi)
cross=scan_y(zcross,ny=3201)
Tcross_eV=T_CMB_K*(1.0+zcross)*KB_EV_K

# y-resolution audit at the crossing.
audits=[]
for ny in [801,1601,3201,6401]:
    rr=scan_y(zcross,ny=ny)
    audits.append({'ny':ny,'proxy_max':rr['proxy_max'],'y_at_max':rr['y_at_max']})
fine=audits[-1]
max_rel=max(abs(a['proxy_max']-fine['proxy_max'])/fine['proxy_max'] for a in audits[:-1])

# Early asymptotic scaling audit: proxy should approach proportionality to
# (1+z)^9 in the DBI-edge regime, within finite-state corrections.
r1=scan_y(2.0e12,ny=1601)['proxy_max']
r2=scan_y(4.0e12,ny=1601)['proxy_max']
scaling_ratio=r2/r1
expected_ratio=((1.0+4.0e12)/(1.0+2.0e12))**9
scaling_rel=abs(scaling_ratio/expected_ratio-1.0)
assert scaling_rel<2e-3

out={
 'classification':'RTK_C9_RTK_SCALAR_PX_TREE_POWERCOUNT_SCAN_COMPLETE',
 'status_scope':'YELLOW_PROXY_CROSSES_ORDER_ONE_NEAR_EARLY_GEV_EPOCH_TRUE_UNITARITY_AND_FULL_EXCHANGE_PENDING',
 'frozen_point':{'h':h,'Omega_K0':OmegaK0,'lambda_D':lambdaD,'gamma':gamma,'x0':x0,'mu_K_Mpc_inv':mu},
 'proxy_definition':'A_proxy=(|V3_P|+|V3_mixed|)^2/omega^2 + absolute P(X) quartic contact envelope + mixed quartic contact envelope, with exact external Zrel=1+(k/M_K)^2 normalization; generic non-resonant power counting only',
 'reference_rows':refs,
 'crossing':{'z':zcross,'row':cross,'T_CMB_scaled_eV':Tcross_eV,'T_CMB_scaled_GeV':Tcross_eV/1e9},
 'resolution_audit':audits,
 'max_resolution_relative_difference':max_rel,
 'early_scaling':{'measured_ratio_proxy_4e12_over_2e12':scaling_ratio,'expected_(1+z)^9_ratio':expected_ratio,'relative_difference':scaling_rel},
 'interpretation':'The exact P(X)-sector tree power-counting envelope is fantastically small through CMB and BBN-like redshifts and becomes order unity only near the reported ultra-early crossing, with the maximum at k~O(M_K). The mixed C(X) vertices are separately tracked and are negligible in this proxy at the crossing. This identifies where a genuine amplitude/UV-completion calculation becomes mandatory; it is not itself a unitarity bound.',
 'non_claims':['not a partial-wave unitarity calculation','uses a generic non-resonant exchange denominator omega^2 and does not resolve channel poles','no metric/U1/auxiliary exchange','no loops or running','adiabatic T_CMB scaling is only a redshift conversion','does not prove validity above the crossing'],
 'next_gate':'derive explicit 2->2 channel Feynman rules with the anisotropic propagator, include s/t/u P(X) cubic exchange and contact interference, then add metric/U1/auxiliary exchange; use this proxy crossing as the preregistered high-resolution region rather than scanning all redshifts equally.',
 'elapsed_seconds':time.time()-start
}
open('c9_rtk_scalar_px_tree_powercount_scan_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps({'crossing':out['crossing'],'max_resolution_relative_difference':max_rel,'elapsed_seconds':out['elapsed_seconds']},sort_keys=True))
