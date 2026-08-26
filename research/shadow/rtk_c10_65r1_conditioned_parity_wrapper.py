#!/usr/bin/env python3
"""Run the frozen C10.65r1 analyzer with an algebraically conditioned local projector.

This overrides only local_project().  All frozen thresholds, parent comparisons,
OFF-path SHA checks and classifications remain those of the frozen r1 analyzer.
"""
from pathlib import Path
import importlib.util

p=Path(__file__).with_name('rtk_c10_65r1_in_class_completed_projector_parity.py')
spec=importlib.util.spec_from_file_location('r1base',p)
base=importlib.util.module_from_spec(spec); spec.loader.exec_module(base)

def conditioned_local_project(r,lam,Mc):
    J=-3.; A2=-1120.906563855608; C2=-1.314425482950032; Sur=298.90841588141416; Eth=2.; Pcal=1.
    a=r['c10_65r0_a']; H=r['c10_65r0_Hc']; rhob=r['c10_65r0_rho_b']; rhog=r['c10_65r0_rho_g']; rhour=r['c10_65r0_rho_ur']
    R=r['c10_65r0_R']; cb2=r['c10_65r0_cb2']; tau=r['c10_65r0_tau_c']; dtau=r['c10_65r0_dtau_c']; Wk=r['c10_65r1_W_khr']; k=r['c10_k_Mpc_inv']
    x=k*k; L=-x; rr=lam-1.; D=3.*lam-1.; Db=J+A2*x; Dg=4./3.*Db
    W0=rhob+4./3.*(rhog+rhour); C0=4./9.*(rhog+rhour); W=W0+Wk; h=W0*Db; ph=C0*Db; muhat=W*Db
    K=-1.5*a*a/(x+a*a*Mc*Mc); a1=x/(x+a*a*Mc*Mc); Kp=2.*H*a1*K; W0p=-3.*H*(W0+C0)
    DA=1.-3.*K*W0; DAp=-3.*(Kp*W0+K*W0p); psi=K*h/DA; dm=muhat+3.*W*psi
    Q=(C2*x-3.*a*a*dm)/(3.*H); qpref=Q/(3.*a); q0pref=(W0/W)*qpref
    hpA=-3.*H*(h+ph)-(x/a)*q0pref; hpB=-x*W0
    psipA=(Kp*h+K*hpA-DAp*psi)/DA; psipB=K*hpB/DA
    lapse=rr*Eth*L-2.*D*H*H
    # Keep phiA/phiB only as exact split diagnostics; B is solved from the
    # algebraically reduced, cancellation-free form used by the conditioned C block.
    phiA=(-3.*a*a*rr*dm-D*H*Q+2.*D*H*psipA+2.*rr*Pcal*L*psi)/lapse
    phiB=(2.*D*H*psipB)/lapse
    Bden=rr*L*(1.+D*Eth*psipB/lapse)
    Brhs=(rr/lapse)*(Eth*L*(Q-D*psipA)+3.*D*H*H*Q+3.*D*H*a*a*dm-2.*D*H*Pcal*L*psi)
    B=Brhs/Bden
    psip=psipA+psipB*B
    phi=(-3.*a*a*rr*dm-D*H*Q+2.*D*H*psip+2.*rr*Pcal*L*psi)/lapse
    Vpref=qpref/(a*W); VN=Vpref+B; Psi=psi-H*B
    Wg=4./3.*rhog; Wur=4./3.*rhour; db=Db+3.*Psi; dg=Dg+4.*Psi
    thpA=(-H*VN+cb2*db+R*dg/4.)/(1.+R); c=16./45.*tau; s1=c*VN; pref=1.-11./6.*dtau; sec=11./6.*tau*c
    sgA=pref*s1-sec*thpA; sgPhi=-sec; PiA=1.5*(Wg*sgA+Wur*Sur); PiPhi=1.5*Wg*sgPhi
    feedback=1.+3.*a*a*PiPhi; Phi=(Psi-3.*a*a*PiA)/feedback; sg=sgA+sgPhi*Phi
    return {'c10_65r1_W_khr':Wk,'c10_65r1_Db':Db,'c10_65r1_Dg':Dg,'c10_65r1_DA':DA,'c10_65r1_delta_mu_pref':dm,'c10_65r1_Qpref':Q,'c10_65r1_psi_pref':psi,'c10_65r1_psi_pref_prime':psip,'c10_65r1_phi_pref':phi,'c10_65r1_B_pref':B,'c10_65r1_B_den':Bden,'c10_65r1_V_N':VN,'c10_65r1_Psi_N':Psi,'c10_65r1_Phi_N':Phi,'c10_65r1_sigma_g_over_k2':sg,'c10_65r1_shear_feedback_den':feedback}

base.local_project=conditioned_local_project
if __name__=='__main__': base.main()
