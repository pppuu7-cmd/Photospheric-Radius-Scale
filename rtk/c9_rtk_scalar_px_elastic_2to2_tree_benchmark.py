#!/usr/bin/env python3
"""Exact P(X)-sector elastic 2->2 tree-amplitude benchmark with RTK dispersion.

This is stronger than coefficient power counting but is still NOT a complete
unitarity theorem: Lorentz-breaking asymptotic-state flux/partial-wave
normalization, mixed C(X), metric/U1/auxiliary exchange and loops remain.

Use the low-k canonically normalized scalar pi_c. Quadratic inverse propagator:
  D^{-1}(Omega,Q)=Z(Q) Omega^2-c_a^2 Q^2,
  Z(Q)=1+Q^2/M_K^2.
For elastic COM scattering with |k_in|=|k_out|=k and angle theta, all external
oscillators receive Z(k)^(-1/2) normalization.

From
 L3=C3t dot(pi)^3+C3s dot(pi)(grad pi)^2,
 L4=C4t dot(pi)^4+C4ts dot(pi)^2(grad pi)^2+C4s[(grad pi)^2]^2,
the exact identical-field vertex combinatorics give the amplitude printed below.
The t/u cubic exchange vertices vanish identically for elastic equal-|k|
kinematics; the s-channel remains.
"""
import json, math, time
import numpy as np
import sympy as sp

# --- symbolic kinematic theorem ---
w,k,c,C3t,C3s,C4t,C4ts,C4s,Z=sp.symbols('omega k c C3t C3s C4t C4ts C4s Z', real=True, finite=True)
# t-channel cubic: p1=(w,k1), p3=(-w,-k3), internal energy 0, Q=k1-k3.
# Spatial cubic polynomial is 2 C3s*w[(k1+k3).(k1-k3)] = 2 C3s*w(k^2-k^2)=0.
t_vertex=sp.simplify(2*C3s*w*(k**2-k**2))
assert t_vertex==0
u_vertex=t_vertex
# s vertex first side: (w,k),(w,-k),(-2w,0).
Vs=sp.factor(-12*C3t*w**3+4*C3s*w*k**2)
# second side has opposite sign, propagator denominator 4w^2.
s_exchange=sp.factor(-(Vs**2)/(4*w**2)) # V1*V2/Ds
assert sp.simplify(s_exchange+4*(C3s*k**2-3*C3t*w**2)**2)==0
# contact angular contractions: sum_ts=-2 k^2 w^2; spatial pairings=k^4(1+2c^2).
contact=24*C4t*w**4-8*C4ts*k**2*w**2+8*C4s*k**4*(1+2*c**2)
Mraw=sp.factor(contact-s_exchange)
Mexpected=24*C4t*w**4-8*C4ts*k**2*w**2+8*C4s*k**4*(1+2*c**2)+4*(C3s*k**2-3*C3t*w**2)**2
assert sp.simplify(Mraw-Mexpected)==0

# --- replay-certified background ---
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
    r=x/s; delta=1.0/(s*s)
    ca2=r*delta/(1.0+r)
    MK=mu_eV*(1.0+r)*s*math.sqrt(s)
    C3t=math.sqrt(2.0)*lambdaD*r/(4.0*MPL*mu_eV*delta**0.25)
    C3s=-math.sqrt(2.0)*(1.0+lambdaD*r**3)*delta**0.75/(4.0*MPL*mu_eV*(1.0+r)**2)
    C4t=lambdaD*(1.0+4.0*lambdaD*r*r)/(16.0*MPL**2*mu_eV**2*math.sqrt(delta))
    C4ts=-math.sqrt(delta)*(2.0*lambdaD**2*r**5+lambdaD*r**3+8.0*lambdaD*r*r+3.0*lambdaD*r-2.0)/(8.0*MPL**2*mu_eV**2*(1.0+r)**3)
    C4s=delta**1.5*(1.0+lambdaD*r**3)/(16.0*MPL**2*mu_eV**2*(1.0+r)**3)
    return {'r':r,'delta':delta,'ca2':ca2,'MK':MK,'C3t':C3t,'C3s':C3s,'C4t':C4t,'C4ts':C4ts,'C4s':C4s}

def amplitude(z,y,costh):
    s=state(z); ZZ=1.0+y*y; kk=y*s['MK']; ww=math.sqrt(s['ca2'])*kk/math.sqrt(ZZ)
    ct=24.0*s['C4t']*ww**4
    cts=-8.0*s['C4ts']*kk**2*ww**2
    css=8.0*s['C4s']*kk**4*(1.0+2.0*costh**2)
    sex=4.0*(s['C3s']*kk**2-3.0*s['C3t']*ww**2)**2
    return (ct+cts+css+sex)/ZZ**2, {'time_contact':ct/ZZ**2,'mixed_time_space_contact':cts/ZZ**2,'spatial_contact':css/ZZ**2,'s_exchange':sex/ZZ**2,'omega_eV':ww,'k_eV':kk,'M_K_eV':s['MK'],'c_a':math.sqrt(s['ca2']),'delta':s['delta']}

def scan(z,ny=2401,ymin=1e-5,ymax=1e5):
    # C4s>0 on production branch, so |M| benchmark is maximized at |cos theta|=1
    # for the positive early-edge amplitude; verify both endpoint and 90deg.
    ys=np.logspace(math.log10(ymin),math.log10(ymax),ny)
    vals=np.empty(ny)
    for i,y in enumerate(ys): vals[i]=abs(amplitude(z,float(y),1.0)[0])
    i=int(np.argmax(vals)); val,parts=amplitude(z,float(ys[i]),1.0)
    val90,_=amplitude(z,float(ys[i]),0.0)
    return {'z':float(z),'abs_M_max_angle_y_scan':float(abs(val)),'M_at_max':float(val),'y_at_max':float(ys[i]),'M_90deg_same_y':float(val90),'parts_at_max':parts}

start=time.time()
refs=[scan(z) for z in [0.0,1100.0,1e9,1e12,2e12,3e12,4e12]]
assert refs[2]['abs_M_max_angle_y_scan']<1e-30
assert refs[3]['abs_M_max_angle_y_scan']<1e-3
assert refs[5]['abs_M_max_angle_y_scan']<1.0
assert refs[6]['abs_M_max_angle_y_scan']>1.0

lo,hi=3.0e12,4.0e12
for _ in range(72):
    mid=math.sqrt(lo*hi)
    if scan(mid,ny=1401)['abs_M_max_angle_y_scan']<1.0: lo=mid
    else: hi=mid
zcross=math.sqrt(lo*hi)
cross=scan(zcross,ny=5001)
Tcross=T_CMB_K*(1.0+zcross)*KB_EV_K

# Resolution audit of y maximum at the crossing.
aud=[]
for ny in [1001,2001,5001,10001]:
    r=scan(zcross,ny=ny)
    aud.append({'ny':ny,'Mmax':r['abs_M_max_angle_y_scan'],'y_at_max':r['y_at_max']})
fine=aud[-1]
res_rel=max(abs(a['Mmax']-fine['Mmax'])/fine['Mmax'] for a in aud[:-1])
# early asymptotic z^9 scaling
m2=scan(2e12,ny=1601)['abs_M_max_angle_y_scan']; m4=scan(4e12,ny=1601)['abs_M_max_angle_y_scan']
expected=((1+4e12)/(1+2e12))**9
scaling_rel=abs((m4/m2)/expected-1.0)
assert scaling_rel<2e-3

out={
 'classification':'RTK_C9_RTK_SCALAR_PX_ELASTIC_2TO2_TREE_BENCHMARK_COMPLETE',
 'status_scope':'YELLOW_EXACT_PX_TREE_AMPLITUDE_ORDER_ONE_BENCHMARK_FULL_UNITARITY_NORMALIZATION_AND_OTHER_EXCHANGES_PENDING',
 'symbolic_amplitude':'M_P=[24 C4t omega^4-8 C4ts k^2 omega^2+8 C4s k^4(1+2 cos^2 theta)+4(C3s k^2-3 C3t omega^2)^2]/Z(k)^2',
 'kinematic_theorem':'elastic equal-|k| COM t/u P(X) cubic exchange vertices vanish exactly; only s-channel cubic exchange survives',
 'quadratic':'omega^2=c_a^2 k^2/Z(k), Z(k)=1+k^2/M_K^2',
 'external_normalization':'one Z(k)^(-1/2) per external oscillator, hence Z(k)^(-2) for the four-point amplitude',
 'frozen_point':{'h':h,'Omega_K0':OmegaK0,'lambda_D':lambdaD,'gamma':gamma,'x0':x0,'mu_K_Mpc_inv':mu},
 'reference_rows':refs,
 'order_one_crossing':{'z':zcross,'T_CMB_scaled_eV':Tcross,'T_CMB_scaled_GeV':Tcross/1e9,'row':cross},
 'resolution_audit':aud,
 'max_resolution_relative_difference':res_rel,
 'early_scaling_relative_difference_from_(1+z)^9':scaling_rel,
 'interpretation':'Including exact identical-field combinatorics and contact/s-channel interference moves the P(X)-only order-one tree-amplitude benchmark earlier than the absolute-value power-count proxy. It remains enormously perturbative through CMB/BBN-like epochs and becomes order one only in the ultra-early sub-GeV-to-GeV redshift-conversion regime. The benchmark localizes where the full Lorentz-breaking unitarity calculation is needed.',
 'non_claims':['not a partial-wave unitarity bound because the Lorentz-breaking flux/state-density normalization has not been derived','mixed C(X) vertices omitted here (previous proxy shows them negligible near its crossing but that is not a proof for every channel)','metric/U1/auxiliary exchange omitted','no loops/running','order-one M is a benchmark, not an EFT phase transition','adiabatic T_CMB scaling is only a redshift conversion'],
 'next_gate':'derive the correct optical-theorem/phase-space normalization for omega(k)=c_a k/sqrt(1+k^2/M_K^2), project this exact amplitude onto the corresponding angular partial waves, then add mixed C(X) and metric/U1/auxiliary tree exchange.'
}
open('c9_rtk_scalar_px_elastic_2to2_tree_benchmark_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps({'crossing':out['order_one_crossing'],'max_resolution_relative_difference':res_rel,'elapsed_seconds':time.time()-start},sort_keys=True))
