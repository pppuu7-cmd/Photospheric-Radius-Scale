#!/usr/bin/env python3
"""C10.65r2 diagnostic-only first-RHS port for pinned CLASS.

Apply after the C10.65r1 patch and its conditioned-B stabilizer.  The inserted
code only appends scalar-output diagnostics.  It does not alter the integrator,
production metric sources, approximation switching, collision coefficients, or
any physical RHS used by CLASS.

B' is obtained by forward directional automatic differentiation of the general
off-manifold cancellation-safe projector certified by C10.65r2c/r2d.  The
historical fixed-C2 onset specialization is retained only by r1 for the onset
value/regression and is never differentiated here.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
hdr=root/'include'/'background.h'
inc=root/'source'/'input.c'
pt=root/'source'/'perturbations.c'
hs=hdr.read_text(); ins=inc.read_text(); ps=pt.read_text()
marker='RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_V1'
if marker in ps:
    print('C10_65R2_PATCH_ALREADY_APPLIED')
    raise SystemExit(0)
if 'RTK_C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_V1' not in ps:
    raise SystemExit('C10.65r2 requires r1 patch first')

# Dormant runtime switch.
if 'double c10_65r2_diag;' not in hs:
    needle='  double c10_65r1_Mc;'
    pos=hs.find(needle)
    if pos<0: raise SystemExit('C10.65r2 background anchor missing')
    eol=hs.find('\n',pos)
    hs=hs[:eol+1]+'  double c10_65r2_diag;/** C10.65r2 dormant first-RHS diagnostic flag */\n'+hs[eol+1:]
if 'pba->c10_65r2_diag = 0.;' not in ins:
    needle='  pba->c10_65r1_Mc = 1.;'
    pos=ins.find(needle)
    if pos<0: raise SystemExit('C10.65r2 default anchor missing')
    eol=ins.find('\n',pos)
    ins=ins[:eol+1]+'  pba->c10_65r2_diag = 0.;\n'+ins[eol+1:]
if 'class_read_double("c10_65r2_diag",pba->c10_65r2_diag);' not in ins:
    needle='  class_read_double("c10_65r1_Mc",pba->c10_65r1_Mc);'
    pos=ins.find(needle)
    if pos<0: raise SystemExit('C10.65r2 parser anchor missing')
    eol=ins.find('\n',pos)
    add=('  class_read_double("c10_65r2_diag",pba->c10_65r2_diag);\n'
         '  class_test((pba->c10_65r2_diag != 0.) && (pba->c10_65r2_diag != 1.),errmsg,"c10_65r2_diag must be 0 or 1");\n'
         '  class_test((pba->c10_65r2_diag > 0.5) && !(pba->c10_65r1_diag > 0.5),errmsg,"c10_65r2_diag requires c10_65r1_diag=1");\n')
    ins=ins[:eol+1]+add+ins[eol+1:]

# File-scope forward-dual implementation: exact double port of r2d.
inc_anchor='#include "perturbations.h"'
if inc_anchor not in ps: raise SystemExit('C10.65r2 include anchor missing')
dual_code=r'''

/* RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_V1: read-only forward dual. */
typedef struct { double v,d; } r2dual;
static inline r2dual r2D(double v,double d){ r2dual z={v,d}; return z; }
static inline r2dual r2C(double v){ return r2D(v,0.); }
static inline r2dual r2add(r2dual a,r2dual b){ return r2D(a.v+b.v,a.d+b.d); }
static inline r2dual r2sub(r2dual a,r2dual b){ return r2D(a.v-b.v,a.d-b.d); }
static inline r2dual r2mul(r2dual a,r2dual b){ return r2D(a.v*b.v,a.d*b.v+a.v*b.d); }
static inline r2dual r2div(r2dual a,r2dual b){ double q=a.v/b.v; return r2D(q,(a.d-q*b.d)/b.v); }
static inline r2dual r2scale(double s,r2dual a){ return r2D(s*a.v,s*a.d); }
static r2dual rtk_c10_65r2_general_B(
  double lam,double Mc,double k,
  r2dual a,r2dual H,r2dual rb,r2dual rg,r2dual ru,r2dual rk,r2dual pk,
  r2dual Db,r2dual Dg,r2dual Dur,r2dual thb,r2dual thg,r2dual thur,r2dual dk,r2dual thk)
{
  const double x=k*k,L=-x,rr=lam-1.,DD=3.*lam-1.,E=2.,P=1.;
  r2dual Wg=r2scale(4./3.,rg),Wu=r2scale(4./3.,ru);
  r2dual W0=r2add(rb,r2add(Wg,Wu)),Wk=r2add(rk,pk);
  r2dual h=r2add(r2mul(rb,Db),r2add(r2mul(rg,Dg),r2mul(ru,Dur)));
  r2dual ph=r2scale(1./3.,r2add(r2mul(rg,Dg),r2mul(ru,Dur)));
  r2dual mom0=r2add(r2mul(rb,thb),r2add(r2mul(Wg,thg),r2mul(Wu,thur)));
  r2dual q0N=r2scale(1./x,r2mul(a,mom0));
  r2dual aa=r2mul(a,a),kden=r2add(r2C(x),r2scale(Mc*Mc,aa));
  r2dual K=r2scale(-1.5,r2div(aa,kden));
  r2dual a1=r2div(r2C(x),kden),Kp=r2scale(2.,r2mul(H,r2mul(a1,K)));
  r2dual W0p=r2add(r2scale(-3.,r2mul(H,rb)),r2scale(-4.,r2mul(H,r2add(Wg,Wu))));
  r2dual DA=r2sub(r2C(1.),r2scale(3.,r2mul(K,W0)));
  r2dual DAp=r2scale(-3.,r2add(r2mul(Kp,W0),r2mul(K,W0p)));
  r2dual psi=r2div(r2mul(K,h),DA);
  r2dual hp=r2add(r2scale(-3.,r2mul(H,r2add(h,ph))),r2scale(-x,r2mul(r2div(r2C(1.),a),q0N)));
  r2dual psip=r2div(r2sub(r2add(r2mul(Kp,h),r2mul(K,hp)),r2mul(DAp,psi)),DA);
  r2dual dm=r2add(h,r2add(r2scale(3.,r2mul(W0,psi)),r2mul(rk,dk)));
  r2dual qk=r2scale(1./x,r2mul(a,r2mul(Wk,thk)));
  r2dual Q=r2scale(3.,r2mul(a,r2add(q0N,qk)));
  r2dual X0=r2scale(3.,r2mul(aa,W0));
  r2dual num=r2C(0.),den=r2C(0.);
  num=r2add(num,r2scale(E*L,r2sub(Q,r2scale(DD,psip))));
  num=r2add(num,r2scale(3.*DD,r2mul(r2mul(H,H),Q)));
  num=r2add(num,r2scale(3.*DD,r2mul(H,r2mul(aa,dm))));
  num=r2add(num,r2scale(-2.*DD*P*L,r2mul(H,psi)));
  den=r2add(den,r2C(rr*E*L*L));
  den=r2add(den,r2scale(-2.*DD*L,r2mul(H,H)));
  den=r2add(den,r2scale(E*L,X0));
  den=r2add(den,r2scale(3.*DD,r2mul(r2mul(H,H),X0)));
  return r2div(num,den);
}
'''
ps=ps.replace(inc_anchor,inc_anchor+dual_code,1)

# Output titles. These columns only exist when both r1 and r2 diagnostics are enabled.
cond='(pba->model == 2.) && (pba->c10_65r1_diag > 0.5) && (pba->c10_65r2_diag > 0.5)'
title_anchor='      class_store_columntitle(ppt->scalar_titles,"c10_65r1_shear_feedback_den",(pba->model == 2.) && (pba->c10_65r1_diag > 0.5));'
if title_anchor not in ps: raise SystemExit('C10.65r2 r1 title anchor missing')
titles=f'''
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_B_general",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_B_prime",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_B_prime_actual",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_Psi_N_prime",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_metric_continuity_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_metric_euler_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_tca_slip_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_theta_b_prime_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_theta_g_prime_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_theta_ur_prime_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_delta_khr_prime_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_theta_khr_prime_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_weighted_slip_cancel",{cond});'''
ps=ps.replace(title_anchor,title_anchor+titles,1)

# Insert inside the already-read-only r1 block after full shear/Phi closure.
data_anchor='        r1_sg=r1_sgA+r1_sgPhi*r1_Phi;'
if ps.count(data_anchor)!=1: raise SystemExit(f'C10.65r2 expected one r1 data anchor, found {ps.count(data_anchor)}')
block=r'''
        if (pba->c10_65r2_diag > 0.5) {
          const double r2_Hp=r1_a*r1_a*pvecback[pba->index_bg_H]*pvecback[pba->index_bg_H]
            +r1_a*pvecback[pba->index_bg_H_prime];
          const double r2_rk=r1_kb.rho8piG/3.,r2_pk=r1_kb.p8piG/3.;
          const double r2_Wk=r2_rk+r2_pk,r2_Wg=(4./3.)*r1_rhog;
          const double r2_db=r1_Db+3.*r1_Psi,r2_dg=r1_Dg+4.*r1_Psi,r2_du=r1_Dg+4.*r1_Psi;
          const double r2_thb=r1_x*r1_VN,r2_thg=r2_thb,r2_thur=r2_thb;
          const double r2_dk=r1_Db+3.*(1.+r1_kb.w)*r1_psi;
          const double r2_thk=r1_x*r1_Vpref;
          const double r2_Dbp=-r2_thb,r2_Dgp=-(4./3.)*r2_thg,r2_Durp=-(4./3.)*r2_thur;
          const double r2_thbp0=(-r1_H*r2_thb+r1_x*(r1_cb2*r2_db+r1_R*(r2_dg/4.-r1_sg)))/(1.+r1_R)+r1_x*r1_Phi;
          const double r2_thgp0=-(r2_thbp0+r1_H*r2_thb-r1_cb2*r1_x*r2_db)/r1_R
            +r1_x*(r2_dg/4.-r1_sg)+(1.+r1_R)/r1_R*r1_x*r1_Phi;
          const double r2_thurp=r1_x*(r2_du/4.-r1_Sur)+r1_x*r1_Phi;
          const double r2_dkp=-(1.+r1_kb.w)*(r2_thk+r1_x*r1_B-3.*r1_psip)
            -3.*r1_H*(r1_kb.ca2-r1_kb.w)*r2_dk;
          const double r2_thkp=-r1_H*(1.-3.*r1_kb.ca2)*r2_thk
            +r1_x*(r1_kb.cs2*r2_dk/(1.+r1_kb.w)+r1_phi);
          r2dual r2_B0=rtk_c10_65r2_general_B(r1_lam,r1_Mc,k,
            r2D(r1_a,r1_a*r1_H),r2D(r1_H,r2_Hp),
            r2D(r1_rhob,-3.*r1_H*r1_rhob),r2D(r1_rhog,-4.*r1_H*r1_rhog),r2D(r1_rhour,-4.*r1_H*r1_rhour),
            r2D(r2_rk,-3.*r1_H*r2_Wk),r2D(r2_pk,r1_kb.ca2*(-3.*r1_H*r2_Wk)),
            r2D(r1_Db,r2_Dbp),r2D(r1_Dg,r2_Dgp),r2D(r1_Dg,r2_Durp),
            r2D(r2_thb,r2_thbp0),r2D(r2_thg,r2_thgp0),r2D(r2_thur,r2_thurp),r2D(r2_dk,r2_dkp),r2D(r2_thk,r2_thkp));
          const double r2_Psip=r1_psip-r2_Hp*r1_B-r1_H*r2_B0.d;
          const double r2_mc=-3.*r2_Psip;
          const double r2_App=r2_Hp+r1_H*r1_H;
          const double r2_F=r1_tau/(1.+r1_R);
          const double r2_Fp=r1_dtau/(1.+r1_R)+r1_tau*r1_H*r1_R/((1.+r1_R)*(1.+r1_R));
          const double r2_sg1=r1_c*r2_thg;
          const double r2_sgp=(16./45.)*(r1_tau*r2_thgp0+r1_dtau*r2_thg);
          const double r2_first=(r1_dtau/r1_tau-2.*r1_H/(1.+r1_R))*(r2_thb-r2_thg)
            +r2_F*(-r2_App*r2_thb+r1_x*(-r1_H*r2_dg/2.+r1_cb2*(-r2_thb-r2_mc)
            -(1./3.)*(-r2_thg-r2_mc))-r1_H*r1_x*r1_Phi);
          const double r2_slip=(1.-2.*r1_H*r2_F)*r2_first+r2_F*r1_x*(2.*r1_H*r2_sg1+r2_sgp
            -(1./3.-r1_cb2)*(r2_F*r2_thgp0+2.*r2_Fp*r2_thb));
          const double r2_thbp=(-r1_H*r2_thb+r1_x*(r1_cb2*r2_db+r1_R*(r2_dg/4.-r1_sg))+r1_R*r2_slip)/(1.+r1_R)+r1_x*r1_Phi;
          const double r2_thgp=-(r2_thbp+r1_H*r2_thb-r1_cb2*r1_x*r2_db)/r1_R
            +r1_x*(r2_dg/4.-r1_sg)+(1.+r1_R)/r1_R*r1_x*r1_Phi;
          r2dual r2_Ba=rtk_c10_65r2_general_B(r1_lam,r1_Mc,k,
            r2D(r1_a,r1_a*r1_H),r2D(r1_H,r2_Hp),
            r2D(r1_rhob,-3.*r1_H*r1_rhob),r2D(r1_rhog,-4.*r1_H*r1_rhog),r2D(r1_rhour,-4.*r1_H*r1_rhour),
            r2D(r2_rk,-3.*r1_H*r2_Wk),r2D(r2_pk,r1_kb.ca2*(-3.*r1_H*r2_Wk)),
            r2D(r1_Db,r2_Dbp),r2D(r1_Dg,r2_Dgp),r2D(r1_Dg,r2_Durp),
            r2D(r2_thb,r2_thbp),r2D(r2_thg,r2_thgp),r2D(r2_thur,r2_thurp),r2D(r2_dk,r2_dkp),r2D(r2_thk,r2_thkp));
          const double r2_bp=r1_rhob*r1_R/(1.+r1_R)*r2_slip;
          const double r2_gp=r2_Wg*(-1./(1.+r1_R))*r2_slip;
          const double r2_cancel=fabs(r2_bp+r2_gp)/MAX(MAX(fabs(r2_bp),fabs(r2_gp)),1.e-300);
          class_test(!isfinite(r2_B0.v)||!isfinite(r2_B0.d)||!isfinite(r2_Ba.d)||!isfinite(r2_Psip)||!isfinite(r2_slip)
            ||!isfinite(r2_thbp)||!isfinite(r2_thgp)||!isfinite(r2_thurp)||!isfinite(r2_dkp)||!isfinite(r2_thkp),error_message,"C10.65r2 non-finite shadow first RHS");
          class_store_double(dataptr,r2_B0.v,_TRUE_,storeidx);
          class_store_double(dataptr,r2_B0.d,_TRUE_,storeidx);
          class_store_double(dataptr,r2_Ba.d,_TRUE_,storeidx);
          class_store_double(dataptr,r2_Psip,_TRUE_,storeidx);
          class_store_double(dataptr,-3.*r2_Psip,_TRUE_,storeidx);
          class_store_double(dataptr,r1_x*r1_Phi,_TRUE_,storeidx);
          class_store_double(dataptr,r2_slip,_TRUE_,storeidx);
          class_store_double(dataptr,r2_thbp,_TRUE_,storeidx);
          class_store_double(dataptr,r2_thgp,_TRUE_,storeidx);
          class_store_double(dataptr,r2_thurp,_TRUE_,storeidx);
          class_store_double(dataptr,r2_dkp,_TRUE_,storeidx);
          class_store_double(dataptr,r2_thkp,_TRUE_,storeidx);
          class_store_double(dataptr,r2_cancel,_TRUE_,storeidx);
        }
'''
ps=ps.replace(data_anchor,data_anchor+block,1)

hdr.write_text(hs); inc.write_text(ins); pt.write_text(ps)
print('C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PATCH_APPLIED')
