#!/usr/bin/env python3
"""C10.61 detached dual-interface ODE/DAE architecture smoke test.

This is deliberately synthetic.  It tests the coupling architecture only:
ordinary barotropic matter is evolved in a curvature-dressed physical-metric
basis, the neutral action fluid is evolved in preferred variables, and the U1
metric variables are projected algebraically on every RHS call.  No B/chi
variable belongs to the integrated state.
"""
from __future__ import annotations
import json, math

# Frozen synthetic controls (not a physical parameter point).
H=0.1
a0=0.7
k=0.5
lam=1.2
Eth=2.0
Mc=0.4
Pcal=0.1
alpha1=0.01
wo=1.0/3.0
wk=0.05
ca2k=wk
cs2k=0.03
rhoo0=0.04
rhok0=0.02
T=2.0
steps=1000

r=lam-1.0
D=3.0*lam-1.0
L=-(k*k)


def background(t):
    a=a0*math.exp(H*t)
    rhoo=rhoo0*math.exp(-3.0*H*(1.0+wo)*t)
    rhok=rhok0*math.exp(-3.0*H*(1.0+wk)*t)
    Wo=(1.0+wo)*rhoo
    Co=wo*Wo
    Wk=(1.0+wk)*rhok
    Wop=-3.0*H*(1.0+wo)*Wo
    return a,rhoo,rhok,Wo,Co,Wk,Wop


def algebra(t,y):
    Do,thetao,deltak,thetak=y
    a,rhoo,rhok,Wo,Co,Wk,Wop=background(t)

    a1=k*k/(k*k+a*a*Mc*Mc)
    K=1.5*a*a*a1/L
    Kp=2.0*H*a1*K

    # Ordinary physical-interface dressed A/density source.
    hhat=rhoo*Do
    p0hat=wo*rhoo*Do
    qoN=a*Wo*thetao/(k*k)
    hhatp=-3.0*H*(hhat+p0hat)-(k*k/a)*qoN
    DA=1.0-3.0*K*Wo
    DAp=-3.0*(Kp*Wo+K*Wop)
    psi=K*hhat/DA
    psip=(Kp*hhat+K*hhatp-DAp*psi)/DA

    # Preferred ordinary sources after exact dressed-source identities.
    dmo_pref=hhat+3.0*Wo*psi
    dpo_pref=p0hat+3.0*Co*psi

    # Neutral action-fluid preferred sources.
    dmk_pref=rhok*deltak
    dpk_pref=rhok*cs2k*deltak
    qk_pref=a*Wk*thetak/(k*k)

    # q_o,pref=q_o,N-a W_o B makes Hamiltonian+momentum a coupled 2x2
    # algebraic solve.  Do not divide by the partial momentum coefficient.
    qbase=qoN+qk_pref
    dm_pref=dmo_pref+dmk_pref
    dp_pref=dpo_pref+dpk_pref
    Qbase=3.0*a*qbase
    X=3.0*a*a*Wo
    lapse_den=r*Eth*L-2.0*D*H*H

    a11=D*H
    a12=r*L+X
    a21=lapse_den
    a22=-D*H*X
    b1=Qbase-D*psip
    b2=(-3.0*a*a*r*dm_pref-D*H*Qbase+2.0*D*H*psip
        +2.0*r*Pcal*L*psi)
    det=a11*a22-a12*a21
    if (not math.isfinite(det)) or det == 0.0:
        raise RuntimeError('dual-interface algebraic determinant vanished/nonfinite')
    phi=(b1*a22-a12*b2)/det
    B=(a11*b2-b1*a21)/det

    qo_pref=qoN-a*Wo*B
    q_pref=qo_pref+qk_pref
    Qpref=3.0*a*q_pref

    # Physical Newtonian potentials for the ordinary interface.
    PsiN=psi-H*B
    PhiN=(1.0-Pcal)*phi+psi+alpha1*L*psi-H*B

    # Reconstruct ordinary physical density and check dressed transforms.
    deltao=Do+3.0*(1.0+wo)*PsiN
    dmuoN=rhoo*deltao
    dpoN=wo*dmuoN
    muhat=dmuoN-3.0*Wo*PsiN
    phat=dpoN-3.0*Co*PsiN

    # Algebraic constraint residuals.
    Ares=DA*psi-K*hhat
    Mres=r*L*B-(Qpref-D*(psip+H*phi))
    Hrhs=(-3.0*a*a*r*dm_pref-D*H*Qpref+2.0*D*H*psip
          +2.0*r*Pcal*L*psi)
    Hres=lapse_den*phi-Hrhs

    source_res=max(
        abs(muhat-hhat),
        abs(phat-p0hat),
        abs(dmo_pref-(muhat+3.0*Wo*psi)),
        abs(dpo_pref-(phat+3.0*Co*psi)),
        abs(qo_pref-(qoN-a*Wo*B)),
    )

    vals=(psi,psip,phi,B,PhiN,PsiN,dm_pref,dp_pref,q_pref,DA,det)
    if not all(math.isfinite(x) for x in vals):
        raise RuntimeError('nonfinite algebraic output')

    return {
        'a':a,'rhoo':rhoo,'rhok':rhok,'Wo':Wo,'Wk':Wk,
        'psi':psi,'psip':psip,'phi':phi,'B':B,'PhiN':PhiN,'PsiN':PsiN,
        'deltao':deltao,'DA':DA,'det':det,
        'Ares':Ares,'Mres':Mres,'Hres':Hres,'source_res':source_res,
    }


def rhs(t,y):
    Do,thetao,deltak,thetak=y
    z=algebra(t,y)
    # Ordinary constant-w barotropic physical fluid in curvature-dressed basis.
    Dop=-(1.0+wo)*thetao
    thetaop=(-H*(1.0-3.0*wo)*thetao
             +k*k*(wo/(1.0+wo)*z['deltao']+z['PhiN']))
    # Neutral action fluid in preferred variables (C10.59).
    deltakp=(-(1.0+wk)*(thetak+k*k*z['B']-3.0*z['psip'])
              -3.0*H*(ca2k-wk)*deltak)
    thetakp=(-H*(1.0-3.0*ca2k)*thetak
             +k*k*(cs2k*deltak/(1.0+wk)+z['phi']))
    out=(Dop,thetaop,deltakp,thetakp)
    if not all(math.isfinite(x) for x in out):
        raise RuntimeError('nonfinite ODE RHS')
    return out


def add(y,scale,kvec):
    return tuple(yi+scale*ki for yi,ki in zip(y,kvec))


def run():
    y=(1.0e-4,2.0e-5,8.0e-5,1.0e-5)
    dt=T/steps
    t=0.0
    max_constraint=0.0
    max_source=0.0
    min_abs_det=float('inf')
    min_DA=float('inf')
    max_abs_state=0.0
    max_abs_alg=0.0
    samples=[]
    for n in range(steps):
        k1=rhs(t,y)
        k2v=rhs(t+0.5*dt,add(y,0.5*dt,k1))
        k3=rhs(t+0.5*dt,add(y,0.5*dt,k2v))
        k4=rhs(t+dt,add(y,dt,k3))
        y=tuple(yi+dt*(u+2*v+2*w+x)/6.0 for yi,u,v,w,x in zip(y,k1,k2v,k3,k4))
        t += dt
        z=algebra(t,y)
        max_constraint=max(max_constraint,abs(z['Ares']),abs(z['Mres']),abs(z['Hres']))
        max_source=max(max_source,z['source_res'])
        min_abs_det=min(min_abs_det,abs(z['det']))
        min_DA=min(min_DA,z['DA'])
        max_abs_state=max(max_abs_state,max(abs(v) for v in y))
        max_abs_alg=max(max_abs_alg,abs(z['psi']),abs(z['psip']),abs(z['phi']),abs(z['B']),abs(z['PhiN']),abs(z['PsiN']))
        if n in (0,steps//4,steps//2,3*steps//4,steps-1):
            samples.append({'t':t,'state':list(y),'psi_pref':z['psi'],'phi_pref':z['phi'],'B':z['B'],'Phi_N':z['PhiN'],'Psi_N':z['PsiN'],'det':z['det'],'D_A':z['DA']})

    assert max_constraint < 1e-11
    assert max_source < 1e-11
    assert min_abs_det > 1e-5
    assert min_DA > 1.0
    assert all(math.isfinite(v) for v in y)

    return {
      'schema':'RTK_C10_DUAL_INTERFACE_DAE_PROTOTYPE_RESULT_v1',
      'classification':'C10_DUAL_INTERFACE_DAE_PROTOTYPE_PASS_SCOPED',
      'integrated_state':['D_o','theta_o','delta_khr_pref','theta_khr_pref'],
      'integrated_B_or_chi':False,
      'synthetic_controls':{
        'H':H,'a0':a0,'k':k,'lambda_hl':lam,'E_th':Eth,'M_c':Mc,
        'Pcal':Pcal,'alpha1':alpha1,'w_o':wo,'w_khr':wk,
        'ca2_khr':ca2k,'cs2_khr':cs2k,'rho_o0':rhoo0,'rho_khr0':rhok0,
        'interval':[0.0,T],'rk4_steps':steps,
        'guard':'architecture smoke-test only; these are not selected physical completion parameters'
      },
      'diagnostics':{
        'max_abs_A_H_M_constraint_residual':max_constraint,
        'max_abs_dressed_source_identity_residual':max_source,
        'min_abs_coupled_phi_B_determinant':min_abs_det,
        'min_D_A':min_DA,
        'max_abs_integrated_state':max_abs_state,
        'max_abs_algebraic_metric_state':max_abs_alg,
        'all_finite':True
      },
      'architecture':{
        'ordinary':'curvature-dressed physical density + physical velocity; physical Phi_N/Psi_N from algebraic projection',
        'neutral':'preferred action-fluid delta/theta with k^2 B continuity advection',
        'gravity':'dressed A solve + differentiated A + coupled Hamiltonian/momentum 2x2 solve on every RHS call',
        'partial_momentum_division':'forbidden/not used',
        'temporal_chi_state':'absent'
      },
      'samples':samples,
      'next_gate':'physical finite-onset memory-loss/growing-mode test after freezing a diagnostic completion-parameter protocol; do not infer attractor behavior from this synthetic run',
      'non_claims':['not a physical adiabatic IC result','not a parameter selection','not CLASS','not full photon/UR hierarchy','not exact k=0','not spectra or likelihood evidence']
    }

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
