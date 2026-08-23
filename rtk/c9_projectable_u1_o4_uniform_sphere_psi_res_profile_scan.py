#!/usr/bin/env python3
"""Uniform-sphere real-space profile of the generalized finite-Mc O(4) potential.

This continues two already-certified results:
  (i) C(K,m): the isolated uniform-sphere single-resolvent O(4) source-shape
      convolution, with overall gravitational/source normalization stripped;
  (ii) on a1=1, delta h00(k)=S_res(k)/k^2 and Psi_res=-Delta^-1 S_res.

Set R=1, K=kR, m=M_c R, s=r/R.  With Fourier convention
  F(r)=1/(2pi^2) int_0^inf dk k^2 j0(kr) F(k),
the dimensionless stripped source profile C(K,m) gives
  Psi_hat(s,m) = 1/(2pi^2) int_0^inf dK C(K,m) j0(Ks),
  A_hat(s,m)   = -d Psi_hat/ds
               = 1/(2pi^2) int_0^inf dK K C(K,m) j1(Ks).

The hats denote shape functions only: the same overall G/rho/gamma/R powers
stripped in the parent convolution remain stripped here.  This is therefore a
source-specific generalized-PPN shape theorem, not an experimental bound.
"""
import json, math, time
import numpy as np
from numpy.polynomial.legendre import leggauss


def sphere_ff(x):
    x=np.asarray(x,dtype=float)
    out=np.empty_like(x)
    ax=np.abs(x)
    small=ax<1e-4
    xs=x[small]
    out[small]=1.0-xs*xs/10.0+xs**4/280.0-xs**6/15120.0
    y=x[~small]
    out[~small]=3.0*(np.sin(y)-y*np.cos(y))/(y**3)
    return out


def j0(x):
    x=np.asarray(x,dtype=float)
    out=np.empty_like(x)
    small=np.abs(x)<1e-4
    xs=x[small]
    out[small]=1-xs**2/6+xs**4/120-xs**6/5040
    y=x[~small]
    out[~small]=np.sin(y)/y
    return out


def j1(x):
    x=np.asarray(x,dtype=float)
    out=np.empty_like(x)
    small=np.abs(x)<1e-3
    xs=x[small]
    out[small]=xs/3-xs**3/30+xs**5/840-xs**7/45360
    y=x[~small]
    out[~small]=np.sin(y)/y**2-np.cos(y)/y
    return out


def Cshape(K,m,nq=650,nmu=32,qmin=2e-5,qmax=8e3):
    mu,w=leggauss(nmu)
    t=np.linspace(math.log(qmin),math.log(qmax),nq)
    Q=np.exp(t)
    SQ=sphere_ff(Q)
    vals=np.empty(nq)
    denomK=m*m+K*K
    for i,q in enumerate(Q):
        P2=np.maximum(K*K+q*q-2*K*q*mu,0.0)
        P=np.sqrt(P2)
        kernel=-(m*m)*(3*q*q-K*q*mu)/(denomK*(m*m+q*q))
        Ushape=sphere_ff(P)/(P2+m*m)
        vals[i]=q**3*SQ[i]*np.dot(w,kernel*Ushape)
    return float(2*math.pi*np.trapezoid(vals,t))


def build_C_grid(m,nK=260,Kmin=2e-3,Kmax=400,nq=650,nmu=32):
    tt=np.linspace(math.log(Kmin),math.log(Kmax),nK)
    Ks=np.exp(tt)
    C=np.array([Cshape(float(K),m,nq=nq,nmu=nmu) for K in Ks])
    return tt,Ks,C


def profiles_from_grid(tt,Ks,C,ss):
    # dK = K dt on the logarithmic grid.
    pref=1/(2*math.pi**2)
    out=[]
    for s in ss:
        psi=pref*np.trapezoid(Ks*C*j0(Ks*s),tt)
        acc=pref*np.trapezoid(Ks**2*C*j1(Ks*s),tt)
        out.append({'s_r_over_R':float(s),'Psi_hat':float(psi),'A_hat':float(acc)})
    return out

start=time.time()
ms=[0.01,0.1,1.0,10.0,100.0]
ss=[0.1,0.25,0.5,0.9,1.0,1.1,2.0,5.0]
rows=[]
for m in ms:
    tt,Ks,C=build_C_grid(m)
    prof=profiles_from_grid(tt,Ks,C,ss)
    rows.append({'m_McR':m,'profile':prof,
                 'C_grid_summary':{'Kmin':float(Ks[0]),'Kmax':float(Ks[-1]),'nK':len(Ks),
                                   'max_abs_C':float(np.max(np.abs(C)))}})

# Numerical derivative audit: -dPsi/ds should agree with A_hat.
deriv_audit=[]
for m in [0.1,1.0,10.0]:
    tt,Ks,C=build_C_grid(m,nK=300,nq=800,nmu=40)
    for s in [0.5,1.0,2.0]:
        h=2e-3*max(1,s)
        pm=profiles_from_grid(tt,Ks,C,[s-h,s,s+h])
        dpsi=(pm[2]['Psi_hat']-pm[0]['Psi_hat'])/(2*h)
        ah=pm[1]['A_hat']
        rel=abs((-dpsi)-ah)/max(1e-10,abs(ah))
        deriv_audit.append({'m':m,'s':s,'minus_numeric_dPsi_ds':float(-dpsi),'A_hat':float(ah),'relative':float(rel)})
assert max(a['relative'] for a in deriv_audit)<0.03

# Resolution / truncation audit at the most important transition m~1.
aud=[]
for config in [
    (180,450,26,200.0),
    (260,650,32,400.0),
    (360,900,48,700.0),
]:
    nK,nq,nmu,Kmax=config
    tt,Ks,C=build_C_grid(1.0,nK=nK,Kmax=Kmax,nq=nq,nmu=nmu)
    p=profiles_from_grid(tt,Ks,C,[0.5,1.0,2.0])
    aud.append({'nK':nK,'nq':nq,'nmu':nmu,'Kmax':Kmax,'profile':p})
fine=aud[-1]['profile']
max_conv=0.0
for A in aud[:-1]:
    for a,b in zip(A['profile'],fine):
        for key in ['Psi_hat','A_hat']:
            max_conv=max(max_conv,abs(a[key]-b[key])/max(1.0,abs(b[key])))
assert max_conv<0.08

# Local-parent disappearance: m->0 at fixed source size.  Use profile norms.
local=[]
for m in [1e-3,3e-3,1e-2]:
    tt,Ks,C=build_C_grid(m,nK=180,nq=450,nmu=28,Kmax=250)
    p=profiles_from_grid(tt,Ks,C,[0.5,1.0,2.0])
    norm=max(max(abs(x['Psi_hat']),abs(x['A_hat'])) for x in p)
    local.append({'m':m,'profile_norm':float(norm)})
assert local[0]['profile_norm'] < 0.25*local[-1]['profile_norm']

out={
 'classification':'RTK_C9_PROJECTABLE_U1_O4_UNIFORM_SPHERE_PSI_RES_PROFILE_COMPLETE',
 'status_scope':'GREEN_SOURCE_SPECIFIC_REAL_SPACE_SHAPE_PROFILE_OVERALL_NORMALIZATION_AND_FULL_PARENT_O4_OBSERVABLE_PENDING',
 'fourier_map':{
   'Psi_hat':'(1/2pi^2) integral dK C(K,m) j0(K s)',
   'A_hat':'(1/2pi^2) integral dK K C(K,m) j1(K s) = -dPsi_hat/ds'
 },
 'variables':'m=M_c R, s=r/R; R=1 in the dimensionless computation',
 'rows':rows,
 'derivative_audit':deriv_audit,
 'max_derivative_relative_error':max(a['relative'] for a in deriv_audit),
 'resolution_audit_m1':aud,
 'max_resolution_scaled_difference':max_conv,
 'local_parent_profile_norms':local,
 'interpretation':'The certified mode-mixing O4 source produces a definite nonlocal radial Psi_res and acceleration-shape profile for a uniform sphere. This is the first real-space source-specific generalized-PPN profile. The profile disappears toward the local-parent McR->0 limit. Its absolute amplitude is intentionally not interpreted until the stripped G/rho/gamma/R normalization is restored consistently with the full parent Eq.(6.17) source.',
 'non_claims':[
   'not a bound on beta, alpha2 or any experimental residual',
   'overall gravitational/source normalization remains stripped exactly as in the parent C(K,m) convolution audit',
   'not the sum of all parent/local O4 source terms',
   'uniform-density weak-field sphere only; no compact-object self-gravity or screening'
 ],
 'next_gate':'restore the full Eq.(6.17) source normalization and parent/local O4 terms for the same uniform sphere, then compare the resulting physical delta h00 and acceleration to the local-parent solution; only then test approximate degeneracy with a constant PPN parameter over a specified experiment.'
}
open('c9_projectable_u1_o4_uniform_sphere_psi_res_profile_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps({'max_derivative_relative_error':out['max_derivative_relative_error'],'max_resolution_scaled_difference':max_conv,'local':local,'elapsed_seconds':time.time()-start},sort_keys=True))
