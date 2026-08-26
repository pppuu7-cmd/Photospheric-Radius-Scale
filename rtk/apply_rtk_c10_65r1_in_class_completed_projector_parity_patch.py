#!/usr/bin/env python3
"""C10.65r1: diagnostic-only C port of the completed-U1 onset projector.

Apply after C10.65r0 on a disposable pinned CLASS tree.  This patch NEVER writes
completed-U1 metric values into CLASS state, metric_continuity/metric_euler, or dy.
When c10_65r1_diag=1 it appends a shadow C evaluation of the already-certified
C10.65n finite-k algebraic seed plus the C10.65o radiation-shear closure.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
hdr=root/'include'/'background.h'
inc=root/'source'/'input.c'
pt=root/'source'/'perturbations.c'
hs=hdr.read_text(); ins=inc.read_text(); ps=pt.read_text()
marker='RTK_C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_V1'
if marker in ps:
    print('C10_65R1_PATCH_ALREADY_APPLIED')
    raise SystemExit(0)

# Runtime inputs are diagnostic-only and dormant by default.
if 'double c10_65r1_diag;' not in hs:
    needle='  double c10_65r0_diag;'
    pos=hs.find(needle)
    if pos<0: raise SystemExit('C10.65r1 requires r0 patch first')
    eol=hs.find('\n',pos)
    add=('  double c10_65r1_diag;/** C10.65r1 dormant projector parity flag */\n'
         '  double c10_65r1_lambda_HL;/** diagnostic completion lambda */\n'
         '  double c10_65r1_Mc;/** diagnostic completion mass in 1/Mpc */\n')
    hs=hs[:eol+1]+add+hs[eol+1:]

if 'pba->c10_65r1_diag = 0.;' not in ins:
    needle='pba->c10_65r0_diag = 0.;'
    pos=ins.find(needle)
    if pos<0: raise SystemExit('C10.65r1 default anchor missing')
    eol=ins.find('\n',pos)
    add=('  pba->c10_65r1_diag = 0.;\n'
         '  pba->c10_65r1_lambda_HL = 1.;\n'
         '  pba->c10_65r1_Mc = 1.;\n')
    ins=ins[:eol+1]+add+ins[eol+1:]

if 'class_read_double("c10_65r1_diag",pba->c10_65r1_diag);' not in ins:
    needle='class_read_double("c10_65r0_diag",pba->c10_65r0_diag);'
    pos=ins.find(needle)
    if pos<0: raise SystemExit('C10.65r1 parser anchor missing')
    eol=ins.find('\n',pos)
    add=('  class_read_double("c10_65r1_diag",pba->c10_65r1_diag);\n'
         '  class_read_double("c10_65r1_lambda_HL",pba->c10_65r1_lambda_HL);\n'
         '  class_read_double("c10_65r1_Mc",pba->c10_65r1_Mc);\n'
         '  class_test((pba->c10_65r1_diag != 0.) && (pba->c10_65r1_diag != 1.),errmsg,"c10_65r1_diag must be 0 or 1");\n'
         '  class_test((pba->c10_65r1_diag > 0.5) && !(pba->c10_65r1_lambda_HL > 1.),errmsg,"c10_65r1_lambda_HL must exceed 1 when r1 diagnostic is enabled");\n'
         '  class_test((pba->c10_65r1_diag > 0.5) && !(pba->c10_65r1_Mc > 0.),errmsg,"c10_65r1_Mc must be positive when r1 diagnostic is enabled");\n')
    ins=ins[:eol+1]+add+ins[eol+1:]

cond='(pba->model == 2.) && (pba->c10_65r1_diag > 0.5)'
title_anchor='      class_store_columntitle(ppt->scalar_titles,"c10_65r0_tca_flag",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));'
if title_anchor not in ps: raise SystemExit('C10.65r1 title anchor missing; apply r0 first')
titles=f'''
      /* {marker}: shadow C metric evaluation only; no integration feedback. */
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_W_khr",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_Db",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_Dg",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_DA",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_delta_mu_pref",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_Qpref",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_psi_pref",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_psi_pref_prime",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_phi_pref",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_B_pref",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_B_den",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_V_N",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_Psi_N",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_Phi_N",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_sigma_g_over_k2",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r1_shear_feedback_den",{cond});'''
ps=ps.replace(title_anchor,title_anchor+titles,1)

# Unique r0 data tail.  We append r1 AFTER r0 so the analyzer can consume the
# exact local environment and the C projector outputs as adjacent diagnostics.
data_anchor='''        class_store_double(dataptr,(double)ppw->approx[ppw->index_ap_tca],_TRUE_,storeidx);
      }'''
# r0 is the last block after c10.65e, therefore choose the final occurrence.
pos=ps.rfind(data_anchor)
if pos<0: raise SystemExit('C10.65r1 r0 data anchor missing')
end=pos+len(data_anchor)
block=r'''
      if ((pba->model == 2.) && (pba->c10_65r1_diag > 0.5)) {
        /* Historical/pre-EFT matching control: frozen by C10.65m, not predicted here. */
        const double r1_J = -3.;
        const double r1_A2 = -1120.906563855608;
        const double r1_C2 = -1.314425482950032;
        const double r1_Sur = 298.90841588141416;
        const double r1_Eth = 2.;
        const double r1_Pcal = 1.;
        double r1_a=pvecback[pba->index_bg_a];
        double r1_H=r1_a*pvecback[pba->index_bg_H];
        double r1_rhob=pvecback[pba->index_bg_rho_b];
        double r1_rhog=pvecback[pba->index_bg_rho_g];
        double r1_rhour=pvecback[pba->index_bg_rho_ur];
        double r1_R=(4./3.)*r1_rhog/r1_rhob;
        double r1_cb2=ppw->pvecthermo[pth->index_th_cb2];
        double r1_dk=ppw->pvecthermo[pth->index_th_dkappa];
        double r1_ddk=ppw->pvecthermo[pth->index_th_ddkappa];
        double r1_tau,r1_dtau;
        double r1_x=k*k,r1_L=-k*k;
        double r1_lam=pba->c10_65r1_lambda_HL,r1_Mc=pba->c10_65r1_Mc;
        double r1_rr=r1_lam-1.,r1_D=3.*r1_lam-1.;
        khr_params r1_kp={pba->H0,pba->gnl,pba->lambda_D,pba->Omega0_cdm};
        khr_closure r1_kc; khr_state r1_kb; int r1_kstat;
        double r1_Wk,r1_W0,r1_C0,r1_W,r1_Db,r1_Dg,r1_h,r1_ph,r1_muhat;
        double r1_K,r1_a1,r1_Kp,r1_W0p,r1_DA,r1_DAp,r1_psi,r1_dm,r1_Ctarget,r1_Q;
        double r1_qpref,r1_q0pref,r1_hpA,r1_hpB,r1_psipA,r1_psipB,r1_lapse;
        double r1_phiA,r1_phiB,r1_shift,r1_Bden,r1_Brhs,r1_B,r1_psip,r1_phi,r1_Vpref,r1_VN,r1_Psi;
        double r1_Wg,r1_Wur,r1_delta_b,r1_delta_g,r1_thpA,r1_c,r1_s1,r1_pref,r1_sec;
        double r1_sgA,r1_sgPhi,r1_PiA,r1_PiPhi,r1_feedback,r1_Phi,r1_sg;
        class_test(!(r1_H>0.) || !(r1_rhob>0.) || !(r1_rhog>0.) || !(r1_rhour>0.) || !(r1_dk>0.),error_message,"C10.65r1 invalid local environment");
        r1_tau=1./r1_dk; r1_dtau=-r1_ddk*r1_tau*r1_tau;
        r1_kstat=khr_closure_from_params(&r1_kp,&r1_kc);
        class_test(r1_kstat != KHR_OK,error_message,"C10.65r1 Khronon closure failed: %s",khr_status_string(r1_kstat));
        r1_kstat=khr_background(&r1_kp,&r1_kc,r1_a/pba->a_today,k,&r1_kb);
        class_test(r1_kstat != KHR_OK,error_message,"C10.65r1 Khronon background failed: %s",khr_status_string(r1_kstat));
        r1_Wk=(r1_kb.rho8piG+r1_kb.p8piG)/3.;
        r1_W0=r1_rhob+(4./3.)*(r1_rhog+r1_rhour);
        r1_C0=(4./9.)*(r1_rhog+r1_rhour);
        r1_W=r1_W0+r1_Wk;
        r1_Db=r1_J+r1_A2*r1_x; r1_Dg=(4./3.)*r1_Db;
        r1_h=r1_W0*r1_Db; r1_ph=r1_C0*r1_Db; r1_muhat=r1_W*r1_Db;
        r1_K=-1.5*r1_a*r1_a/(r1_x+r1_a*r1_a*r1_Mc*r1_Mc);
        r1_a1=r1_x/(r1_x+r1_a*r1_a*r1_Mc*r1_Mc);
        r1_Kp=2.*r1_H*r1_a1*r1_K;
        r1_W0p=-3.*r1_H*(r1_W0+r1_C0);
        r1_DA=1.-3.*r1_K*r1_W0;
        r1_DAp=-3.*(r1_Kp*r1_W0+r1_K*r1_W0p);
        r1_psi=r1_K*r1_h/r1_DA;
        r1_dm=r1_muhat+3.*r1_W*r1_psi;
        r1_Ctarget=r1_C2*r1_x;
        r1_Q=(r1_Ctarget-3.*r1_a*r1_a*r1_dm)/(3.*r1_H);
        r1_qpref=r1_Q/(3.*r1_a); r1_q0pref=(r1_W0/r1_W)*r1_qpref;
        r1_hpA=-3.*r1_H*(r1_h+r1_ph)-(r1_x/r1_a)*r1_q0pref;
        r1_hpB=-r1_x*r1_W0;
        r1_psipA=(r1_Kp*r1_h+r1_K*r1_hpA-r1_DAp*r1_psi)/r1_DA;
        r1_psipB=r1_K*r1_hpB/r1_DA;
        r1_lapse=r1_rr*r1_Eth*r1_L-2.*r1_D*r1_H*r1_H;
        class_test(r1_lapse == 0.,error_message,"C10.65r1 lapse denominator vanished");
        r1_phiA=(-3.*r1_a*r1_a*r1_rr*r1_dm-r1_D*r1_H*r1_Q+2.*r1_D*r1_H*r1_psipA+2.*r1_rr*r1_Pcal*r1_L*r1_psi)/r1_lapse;
        r1_phiB=(2.*r1_D*r1_H*r1_psipB)/r1_lapse;
        r1_shift=r1_rr*r1_L;
        r1_Bden=r1_shift+r1_D*(r1_psipB+r1_H*r1_phiB);
        class_test(r1_Bden == 0.,error_message,"C10.65r1 B denominator vanished");
        r1_Brhs=r1_Q-r1_D*(r1_psipA+r1_H*r1_phiA);
        r1_B=r1_Brhs/r1_Bden;
        r1_psip=r1_psipA+r1_psipB*r1_B; r1_phi=r1_phiA+r1_phiB*r1_B;
        r1_Vpref=r1_qpref/(r1_a*r1_W); r1_VN=r1_Vpref+r1_B; r1_Psi=r1_psi-r1_H*r1_B;
        /* C10.65o source-locked compromise_CLASS radiation-shear closure. */
        r1_Wg=(4./3.)*r1_rhog; r1_Wur=(4./3.)*r1_rhour;
        r1_delta_b=r1_Db+3.*r1_Psi; r1_delta_g=r1_Dg+4.*r1_Psi;
        r1_thpA=(-r1_H*r1_VN+r1_cb2*r1_delta_b+r1_R*r1_delta_g/4.)/(1.+r1_R);
        r1_c=(16./45.)*r1_tau; r1_s1=r1_c*r1_VN;
        r1_pref=1.-(11./6.)*r1_dtau; r1_sec=(11./6.)*r1_tau*r1_c;
        r1_sgA=r1_pref*r1_s1-r1_sec*r1_thpA; r1_sgPhi=-r1_sec;
        r1_PiA=1.5*(r1_Wg*r1_sgA+r1_Wur*r1_Sur); r1_PiPhi=1.5*r1_Wg*r1_sgPhi;
        r1_feedback=1.+3.*r1_a*r1_a*r1_PiPhi;
        class_test(fabs(r1_feedback)<1.e-14,error_message,"C10.65r1 radiation shear feedback denominator vanished");
        r1_Phi=(r1_Psi-3.*r1_a*r1_a*r1_PiA)/r1_feedback;
        r1_sg=r1_sgA+r1_sgPhi*r1_Phi;
        class_test(!isfinite(r1_Wk)||!isfinite(r1_Db)||!isfinite(r1_DA)||!isfinite(r1_dm)||!isfinite(r1_Q)||!isfinite(r1_psi)||!isfinite(r1_psip)||!isfinite(r1_phi)||!isfinite(r1_B)||!isfinite(r1_VN)||!isfinite(r1_Psi)||!isfinite(r1_Phi)||!isfinite(r1_sg),error_message,"C10.65r1 non-finite shadow projector output");
        class_store_double(dataptr,r1_Wk,_TRUE_,storeidx);
        class_store_double(dataptr,r1_Db,_TRUE_,storeidx);
        class_store_double(dataptr,r1_Dg,_TRUE_,storeidx);
        class_store_double(dataptr,r1_DA,_TRUE_,storeidx);
        class_store_double(dataptr,r1_dm,_TRUE_,storeidx);
        class_store_double(dataptr,r1_Q,_TRUE_,storeidx);
        class_store_double(dataptr,r1_psi,_TRUE_,storeidx);
        class_store_double(dataptr,r1_psip,_TRUE_,storeidx);
        class_store_double(dataptr,r1_phi,_TRUE_,storeidx);
        class_store_double(dataptr,r1_B,_TRUE_,storeidx);
        class_store_double(dataptr,r1_Bden,_TRUE_,storeidx);
        class_store_double(dataptr,r1_VN,_TRUE_,storeidx);
        class_store_double(dataptr,r1_Psi,_TRUE_,storeidx);
        class_store_double(dataptr,r1_Phi,_TRUE_,storeidx);
        class_store_double(dataptr,r1_sg,_TRUE_,storeidx);
        class_store_double(dataptr,r1_feedback,_TRUE_,storeidx);
      }'''
ps=ps[:end]+block+ps[end:]

hdr.write_text(hs); inc.write_text(ins); pt.write_text(ps)
print('C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_PATCH_APPLIED')
