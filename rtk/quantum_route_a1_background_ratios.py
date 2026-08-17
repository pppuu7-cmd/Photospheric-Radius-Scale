#!/usr/bin/env python3
"""Evaluate long-wave P(X) interaction ratios for the DBI-Khronon background.

Inputs are the physical closure parameters used by khronon_background.c.
This is a conditional Route-A1/P(X) diagnostic, not a full RTK cutoff theorem.
"""
import argparse, json, math

p=argparse.ArgumentParser()
p.add_argument('--gamma',type=float,required=True)
p.add_argument('--lambda-D',dest='lam',type=float,required=True)
p.add_argument('--Omega-K0',dest='Om',type=float,required=True)
p.add_argument('--H0',type=float,required=True,help='CLASS H0 in 1/Mpc')
a=p.parse_args()
if not (a.gamma>0 and a.lam>0 and a.Om>0 and a.H0>0):
    raise SystemExit('positive parameters required')

A=a.Om/(6*a.gamma)
D=1+2*A+a.lam*A*A
x0=A*(2+a.lam*A)/(1+a.lam*A+math.sqrt(D))
mu=3*a.H0*math.sqrt(a.gamma)

def vals(scale):
    x=x0/scale**3
    s=math.hypot(1.0,math.sqrt(a.lam)*x)
    r=x/s
    t=x/(s+1.0)
    G=2*mu*mu*(x*(1+t)+r*t)
    ca2=r/(s*(s+x))
    K=G/ca2
    # c2=-(K-G)/2 exactly.
    c2_over_K=-0.5*(1-G/K)
    # c1/K=[(d ln K/d ln x)/(2 ca2)-1]/3.
    # Evaluate d ln K/d ln x with a symmetric log derivative; the exact
    # thermodynamic identity has already been proved symbolically in CI.
    eps=1e-5
    def kval(xx):
        ss=math.hypot(1.0,math.sqrt(a.lam)*xx)
        rr=xx/ss; tt=xx/(ss+1.0)
        GG=2*mu*mu*(xx*(1+tt)+rr*tt)
        cc=rr/(ss*(ss+xx))
        return GG/cc
    kp=kval(x*math.exp(eps)); km=kval(x*math.exp(-eps))
    dlnK=(math.log(kp)-math.log(km))/(2*eps)
    c1_over_K=(dlnK/(2*ca2)-1)/3
    rho=2*mu*mu*x*(1+t); pr=2*mu*mu*r*t
    w=pr/rho
    Q=1+r
    MK=mu*Q*s*math.sqrt(s)
    return {'a':scale,'z':1/scale-1,'x':x,'w':w,'ca2':ca2,
            'c1_over_K':c1_over_K,'c2_over_K':c2_over_K,
            'M_K_over_H0':MK/a.H0,'dbi_margin':1/(s*s)}

scales=[1.0,0.8,0.67,0.5,1/3,0.2,0.1,0.01,0.001]
rows=[vals(s) for s in scales]
out={'classification':'RTK_ROUTE_A1_BACKGROUND_RATIOS_COMPLETE',
     'gamma':a.gamma,'lambda_D':a.lam,'Omega_K0':a.Om,'H0_class':a.H0,
     'x0':x0,'mu_over_H0':mu/a.H0,'rows':rows,
     'interpretation_boundary':{
       'D3_longwave_only':True,
       'c3_c4_known':False,
       'full_strong_coupling_cutoff_known':False,
       'M_K_is_not_declared_cutoff':True}}
print('RTK_ROUTE_A1_BACKGROUND_RATIOS_COMPLETE',json.dumps(out,sort_keys=True))
