#include <math.h>
#include "background.h"
#include "thermodynamics.h"
#include "perturbations.h"
#include "khronon_background.h"
#include "rtk_c10_65r2_observer.h"

/* Keep the dual algebra in this translation unit.  There is deliberately no
 * LTO in the pinned CLASS Makefile, and the public entry point is noinline and
 * noclone, so this code cannot be folded into perturb_print_variables(). */
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

#if defined(__GNUC__)
__attribute__((noinline,noclone))
#endif
void rtk_c10_65r2_observe(struct background *pba,
                          struct thermo *pth,
                          struct perturb_workspace *ppw,
                          double k,
                          double *dataptr,
                          int *storeidx)
{
  /* Dormant path: no output mutation and no heavy arithmetic. */
  if ((pba->model != 2.) || !(pba->c10_65r1_diag > 0.5) || !(pba->c10_65r2_diag > 0.5)) return;

  /* The immediately preceding 16 doubles are the already materialized r1
   * projector row.  Reading them here prevents any r1 temporary in the caller
   * from acquiring a diagnostic-only extended live range. */
  const double *r1=dataptr+(*storeidx)-16;
  const double r1_Wk=r1[0];
  const double r1_Db=r1[1],r1_Dg=r1[2];
  const double r1_psi=r1[6],r1_psip=r1[7],r1_phi=r1[8],r1_B=r1[9];
  const double r1_VN=r1[11],r1_Psi=r1[12],r1_Phi=r1[13],r1_sg=r1[14];
  const double r1_Sur=298.90841588141416;
  const double r1_a=ppw->pvecback[pba->index_bg_a];
  const double r1_H=r1_a*ppw->pvecback[pba->index_bg_H];
  const double r1_rhob=ppw->pvecback[pba->index_bg_rho_b];
  const double r1_rhog=ppw->pvecback[pba->index_bg_rho_g];
  const double r1_rhour=ppw->pvecback[pba->index_bg_rho_ur];
  const double r1_R=(4./3.)*r1_rhog/r1_rhob;
  const double r1_cb2=ppw->pvecthermo[pth->index_th_cb2];
  const double r1_dk=ppw->pvecthermo[pth->index_th_dkappa];
  const double r1_ddk=ppw->pvecthermo[pth->index_th_ddkappa];
  const double r1_tau=1./r1_dk;
  const double r1_dtau=-r1_ddk*r1_tau*r1_tau;
  const double r1_x=k*k;
  const double r1_lam=pba->c10_65r1_lambda_HL,r1_Mc=pba->c10_65r1_Mc;
  const double r1_Vpref=r1_VN-r1_B;
  const double r1_c=(16./45.)*r1_tau;

  khr_params r1_kp={pba->H0,pba->gnl,pba->lambda_D,pba->Omega0_cdm};
  khr_closure r1_kc; khr_state r1_kb;
  int st=khr_closure_from_params(&r1_kp,&r1_kc);
  if (st==KHR_OK) st=khr_background(&r1_kp,&r1_kc,r1_a/pba->a_today,k,&r1_kb);
  if (st!=KHR_OK) {
    int i; for(i=0;i<13;i++) dataptr[(*storeidx)++]=NAN;
    return;
  }

  {
    const double r2_Hp=r1_a*r1_a*ppw->pvecback[pba->index_bg_H]*ppw->pvecback[pba->index_bg_H]
      +r1_a*ppw->pvecback[pba->index_bg_H_prime];
    const double r2_rk=r1_kb.rho8piG/3.,r2_pk=r1_kb.p8piG/3.;
    const double r2_Wk=r2_rk+r2_pk,r2_Wg=(4./3.)*r1_rhog;
    const double r2_db=r1_Db+3.*r1_Psi,r2_dg=r1_Dg+4.*r1_Psi,r2_du=r1_Dg+4.*r1_Psi;
    const double r2_thb=r1_x*r1_VN,r2_thg=r2_thb,r2_thur=r2_thb;
    const double r2_dk=r1_Db+3.*(1.+r1_kb.w)*r1_psi;
    const double r2_thk=r1_x*r1_Vpref;
    const double r2_Dbp=-r2_thb,r2_Dgp=-(4./3.)*r2_thg,r2_Durp=-(4./3.)*r2_thur;
    const double r2_thbp0=(-r1_H*r2_thb+r1_x*(r1_cb2*r2_db+r1_R*(r2_dg/4.-r1_x*r1_sg)))/(1.+r1_R)+r1_x*r1_Phi;
    const double r2_thgp0=-(r2_thbp0+r1_H*r2_thb-r1_cb2*r1_x*r2_db)/r1_R
      +r1_x*(r2_dg/4.-r1_x*r1_sg)+(1.+r1_R)/r1_R*r1_x*r1_Phi;
    const double r2_thurp=r1_x*(r2_du/4.-r1_x*r1_Sur)+r1_x*r1_Phi;
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
    const double r2_thbp=(-r1_H*r2_thb+r1_x*(r1_cb2*r2_db+r1_R*(r2_dg/4.-r1_x*r1_sg))+r1_R*r2_slip)/(1.+r1_R)+r1_x*r1_Phi;
    const double r2_thgp=-(r2_thbp+r1_H*r2_thb-r1_cb2*r1_x*r2_db)/r1_R
      +r1_x*(r2_dg/4.-r1_x*r1_sg)+(1.+r1_R)/r1_R*r1_x*r1_Phi;
    r2dual r2_Ba=rtk_c10_65r2_general_B(r1_lam,r1_Mc,k,
      r2D(r1_a,r1_a*r1_H),r2D(r1_H,r2_Hp),
      r2D(r1_rhob,-3.*r1_H*r1_rhob),r2D(r1_rhog,-4.*r1_H*r1_rhog),r2D(r1_rhour,-4.*r1_H*r1_rhour),
      r2D(r2_rk,-3.*r1_H*r2_Wk),r2D(r2_pk,r1_kb.ca2*(-3.*r1_H*r2_Wk)),
      r2D(r1_Db,r2_Dbp),r2D(r1_Dg,r2_Dgp),r2D(r1_Dg,r2_Durp),
      r2D(r2_thb,r2_thbp),r2D(r2_thg,r2_thgp),r2D(r2_thur,r2_thurp),r2D(r2_dk,r2_dkp),r2D(r2_thk,r2_thkp));
    const double r2_bp=r1_rhob*r1_R/(1.+r1_R)*r2_slip;
    const double r2_gp=r2_Wg*(-1./(1.+r1_R))*r2_slip;
    const double r2_cancel=fabs(r2_bp+r2_gp)/fmax(fmax(fabs(r2_bp),fabs(r2_gp)),1.e-300);
    const double out[13]={r2_B0.v,r2_B0.d,r2_Ba.d,r2_Psip,-3.*r2_Psip,r1_x*r1_Phi,r2_slip,
                          r2_thbp,r2_thgp,r2_thurp,r2_dkp,r2_thkp,r2_cancel};
    int i; for(i=0;i<13;i++) dataptr[(*storeidx)++]=out[i];
  }
}
