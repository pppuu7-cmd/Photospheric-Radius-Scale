#!/usr/bin/env python3
"""Conservative B9 physical-k margin against the RTK scalar P(X) tree cutoff.

The production likelihood runner fixes
  P_k_max_h/Mpc = 5.0
and the frozen RTK point has h=0.691103719964454.  We deliberately overextend
that full comoving envelope to every epoch 0<=z<=1e9 via
  k_phys,max(z)=5 h (1+z) Mpc^-1.
This is much more conservative than the actual low-z mPk outputs and CMB source
support, and is used only as a safety envelope.

For each z we recompute the single-channel P(X) l=0/l=2 tree partial-wave
cutoff from the exact RTK dispersion and DBI coefficients, then compare the
first crossing |g a_l|=1/2 with k_phys,max.  This gate does not promote the
single-channel cutoff to an all-sector EFT theorem.
"""
import json, math
import numpy as np

h=0.691103719964454
OmegaK0=0.2522864064078236
lambdaD=219457.5727136581
gamma=0.05170371280716
MPC_M=3.0856775814913673e22
HBARC_EV_M=1.973269804e-7
INV_MPC_EV=HBARC_EV_M/MPC_M
MPL=2.435e27
H0=100.0*h/299792.458
mu_mpc=3.0*H0*math.sqrt(gamma)
mu_eV=mu_mpc*INV_MPC_EV
A0=OmegaK0/(6.0*gamma)
x0=A0*(2.0+lambdaD*A0)/(1.0+lambdaD*A0+math.sqrt(1.0+2.0*A0+lambdaD*A0*A0))
KCOM_MAX_H_MPC=5.0
kcom_max_eV=KCOM_MAX_H_MPC*h*INV_MPC_EV


def state(z):
    x=x0*(1.0+z)**3
    s=math.hypot(1.0,math.sqrt(lambdaD)*x)
    r=x/s; d=1.0/(s*s)
    ca2=r*d/(1.0+r)
    MK=mu_eV*(1.0+r)*s*math.sqrt(s)
    C3t=math.sqrt(2.0)*lambdaD*r/(4.0*MPL*mu_eV*d**0.25)
    C3s=-math.sqrt(2.0)*(1.0+lambdaD*r**3)*d**0.75/(4.0*MPL*mu_eV*(1.0+r)**2)
    C4t=lambdaD*(1.0+4.0*lambdaD*r*r)/(16.0*MPL**2*mu_eV**2*math.sqrt(d))
    C4ts=-math.sqrt(d)*(2.0*lambdaD**2*r**5+lambdaD*r**3+8.0*lambdaD*r*r+3.0*lambdaD*r-2.0)/(8.0*MPL**2*mu_eV**2*(1.0+r)**3)
    C4s=d**1.5*(1.0+lambdaD*r**3)/(16.0*MPL**2*mu_eV**2*(1.0+r)**3)
    return ca2,MK,C3t,C3s,C4t,C4ts,C4s


def ga(z,y):
    ca2,MK,C3t,C3s,C4t,C4ts,C4s=state(z)
    ca=math.sqrt(ca2); Z=1+y*y; k=y*MK; w=ca*k/math.sqrt(Z)
    a0=(48*C4t*w**4-16*C4ts*k*k*w*w+(80/3)*C4s*k**4+8*(C3s*k*k-3*C3t*w*w)**2)/(32*math.pi*Z**2)
    a2=2*C4s*k**4/(15*math.pi*Z**2)
    g=Z**2.5/(2*ca**3)
    return g*a0,g*a2,k


def cutoff(z):
    lo=1e-50
    assert max(abs(ga(z,lo)[0]),abs(ga(z,lo)[1]))<0.5
    hi=lo
    for _ in range(110):
        hi*=10
        a0,a2,_=ga(z,hi)
        if max(abs(a0),abs(a2))>=0.5: break
    else: raise AssertionError('cutoff bracket failed')
    for _ in range(130):
        mid=math.sqrt(lo*hi)
        a0,a2,_=ga(z,mid)
        if max(abs(a0),abs(a2))<0.5: lo=mid
        else: hi=mid
    y=math.sqrt(lo*hi); a0,a2,k=ga(z,y)
    return {'k_unit_eV':k,'y':y,'g_a0':a0,'g_a2':a2}

# Dense in log(1+z), including exact endpoints and key observational epochs.
zs=sorted(set([0.0,1.0,10.0,100.0,1100.0,1e4,1e5,1e6,1e7,1e9]+[10.0**u-1.0 for u in np.linspace(0,9,181)]))
rows=[]
min_margin=(float('inf'),None)
last_kunit=0.0
monotonic_violations=0
for z in zs:
    c=cutoff(float(z))
    kphys=kcom_max_eV*(1.0+z)
    margin=c['k_unit_eV']/kphys
    if c['k_unit_eV'] < last_kunit*(1-2e-10): monotonic_violations+=1
    last_kunit=max(last_kunit,c['k_unit_eV'])
    row={'z':float(z),'k_phys_envelope_eV':kphys,'margin_kunit_over_kphys':margin,**c}
    rows.append(row)
    if margin<min_margin[0]: min_margin=(margin,row.copy())
assert monotonic_violations==0
assert min_margin[0] > 1e15

# Reproduce the early plateau analytically and compare the z=1e9 root.
kearly=(24.0*math.pi*MPL**2*mu_eV**2*math.sqrt(math.sqrt(lambdaD)+1.0)/(29.0*lambdaD))**0.25
r1e9=next(r for r in rows if r['z']==1e9)
assert abs(r1e9['k_unit_eV']/kearly-1)<3e-12

# Key rows kept compact in the primary result.
keyz=[0.0,1100.0,1e6,1e9]
keyrows=[]
for z in keyz:
    keyrows.append(min(rows,key=lambda r:abs(r['z']-z)))

out={
 'classification':'RTK_C9_RTK_SCALAR_UNITARITY_B9_K_WINDOW_PASS',
 'status_scope':'GREEN_B9_DECLARED_K_ENVELOPE_FAR_BELOW_SINGLE_CHANNEL_PX_TREE_CUTOFF_ALL_SECTOR_UV_PENDING',
 'pipeline_input':{
   'source':'rtk/joint_profile_runner.py production likelihood input',
   'P_k_max_h_per_Mpc':KCOM_MAX_H_MPC,
   'h':h,
   'comoving_k_envelope_eV':kcom_max_eV
 },
 'conservative_extension':'Treat the full configured 5 h/Mpc comoving envelope as present at every epoch through z=1e9, k_phys=k_com(1+z). This intentionally overstates the actual B9 physical-k demand.',
 'redshift_scan':{'z_min':0.0,'z_max':1e9,'points':len(rows),'parameterization':'dense uniform grid in log10(1+z), plus key epochs'},
 'cutoff_definition':'first positive momentum where max(|g a0|,|g a2|)=1/2 for the certified P(X)-only tree partial waves',
 'monotonic_kunit_violations_on_grid':monotonic_violations,
 'minimum_margin':min_margin[1],
 'key_rows':keyrows,
 'early_plateau_k_unit_eV':kearly,
 'interpretation':'Even under an intentionally excessive redshifting of the entire configured B9 k envelope to z=1e9, the physical momenta remain more than 10^15 below the single-channel P(X) tree partial-wave cutoff. The finite cutoff therefore does not threaten the momentum range explicitly requested by the B9 production pipeline over this conservative redshift window.',
 'B6_note':'B6 AlterBBN is a homogeneous expansion-history/nuclear-network gate using H(T); it has no perturbation Fourier-k demand to compare with this momentum cutoff.',
 'non_claims':[
   'does not certify all CLASS internal adaptive perturbation modes at arbitrarily early initialization times',
   'does not replace the missing mixed C(X), metric/U1/auxiliary, loop and inelastic unitarity analysis',
   'does not prove the EFT valid above the single-channel cutoff',
   'does not turn P_k_max_h/Mpc into a physical experimental resolution scale'
 ],
 'next_gate':'derive a UV-completion window for higher-spatial quadratic operators: keep corrections negligible over the certified B9 k envelope while forcing omega(k) to grow before the partial-wave phase-space cutoff.'
}
open('c9_rtk_scalar_unitarity_b9_k_window_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps({'minimum_margin':out['minimum_margin'],'key_rows':keyrows},sort_keys=True))
