#include <math.h>
#include <stddef.h>
#include "c10_65s2_kernel.h"

/* C10.65s2: pure current-state kernel.  No file/history reads, no onset seed
   constants, and no CLASS state mutation live in this translation unit. */

typedef struct { double v,d; } s2d;
static s2d D(double v,double d){ s2d z={v,d}; return z; }
static s2d C(double v){ return D(v,0.); }
static s2d add(s2d a,s2d b){ return D(a.v+b.v,a.d+b.d); }
static s2d sub(s2d a,s2d b){ return D(a.v-b.v,a.d-b.d); }
static s2d mul(s2d a,s2d b){ return D(a.v*b.v,a.d*b.v+a.v*b.d); }
static s2d divd(s2d a,s2d b){ double q=a.v/b.v; return D(q,(a.d-q*b.d)/b.v); }
static s2d scale(double s,s2d a){ return D(s*a.v,s*a.d); }

static double max2(double a,double b){ return a>b?a:b; }
static double rel(double a,double b){ return fabs(a-b)/max2(max2(fabs(a),fabs(b)),1e-300); }
static double n2(double r,double a,double b){ return fabs(r)/max2(max2(fabs(a),fabs(b)),1e-300); }
static double n3(double r,double a,double b,double c){ return fabs(r)/max2(max2(max2(fabs(a),fabs(b)),fabs(c)),1e-300); }
static double n6(double r,double a,double b,double c,double d,double e,double f){
  double m=max2(fabs(a),fabs(b)); m=max2(m,fabs(c)); m=max2(m,fabs(d)); m=max2(m,fabs(e)); m=max2(m,fabs(f));
  return fabs(r)/max2(m,1e-300);
}

static s2d dae_B_dual(double k,double lam,double Mc,
                      s2d a,s2d H,s2d rb,s2d rg,s2d ru,s2d rk,s2d pk,
                      s2d Db,s2d Dg,s2d Dur,s2d J,s2d q0,s2d thetaN){
  const double x=k*k,Lk=-x,r=lam-1.,DD=3.*lam-1.;
  s2d Wg=scale(4./3.,rg),Wu=scale(4./3.,ru),W0=add(rb,add(Wg,Wu)),Wk=add(rk,pk),W=add(W0,Wk);
  s2d h=add(mul(rb,Db),add(mul(rg,Dg),mul(ru,Dur)));
  s2d ph=scale(1./3.,add(mul(rg,Dg),mul(ru,Dur)));
  s2d aa=mul(a,a),denf=add(C(x),scale(Mc*Mc,aa));
  s2d K=scale(-1.5,divd(aa,denf)),a1=divd(C(x),denf),Kp=scale(2.,mul(H,mul(a1,K)));
  s2d W0p=add(scale(-3.,mul(H,rb)),scale(-4.,mul(H,add(Wg,Wu))));
  s2d DA=sub(C(1.),scale(3.,mul(K,W0)));
  s2d DAp=scale(-3.,add(mul(Kp,W0),mul(K,W0p)));
  s2d psi=divd(mul(K,h),DA);
  s2d hp=add(scale(-3.,mul(H,add(h,ph))),scale(-x,mul(divd(C(1.),a),q0)));
  s2d psip=divd(sub(add(mul(Kp,h),mul(K,hp)),mul(DAp,psi)),DA);
  s2d dm=add(h,add(scale(3.,mul(W,psi)),mul(Wk,J)));
  s2d Q0=scale(3.,mul(a,add(q0,scale(1./x,mul(a,mul(Wk,thetaN))))));
  s2d Xt=scale(3.,mul(aa,W));
  s2d lapse=add(C(r*2.*Lk),scale(-2.*DD,mul(H,H)));
  s2d A11=lapse,A12=scale(-DD,mul(H,Xt)),A21=scale(DD,H),A22=add(C(r*Lk),Xt);
  s2d b1=C(0.);
  b1=add(b1,scale(-3.*r,mul(aa,dm)));
  b1=add(b1,scale(-DD,mul(H,Q0)));
  b1=add(b1,scale(2.*DD,mul(H,psip)));
  b1=add(b1,scale(2.*r*Lk,psi));
  s2d b2=sub(Q0,scale(DD,psip));
  s2d det=sub(mul(A11,A22),mul(A12,A21));
  return divd(sub(mul(A11,b2),mul(b1,A21)),det);
}

int rtk_c10_65s2_current_state(const rtk_c10_65s2_input *in,
                               rtk_c10_65s2_output *o){
  double k,x,Lk,r,DD,Wg,Wu,W0,Wk,W;
  double Db,Dg,Dur,h,ph,denf,K,a1,Kp,W0p,DA,DAp,psi,q0,hp,psip;
  double dm0,Q0,X0,Xt,Bnum,Bden,B,dm,Qpref,lapse,Hrhs,phi,PsiRec;
  double R,c,theta0p,pref,sec,sigmaA,sigmaPhi,PiA,PiPhi,feedback,Phi,sg,Pi,tres;
  double J,deltaPref,thetaPref,thetaPrefP,deltaPrefP;
  double rbp,Wgp,Wup,agg_bg,agg_pb,agg_ur,M0,M0p,ap,q0p;
  double f0,f1,cB,iden,Bp,PsiNp,metric_cont,metric_euler,App,F,Fp,slip1,shear1,thetaCommon,shear1p,slip;
  double tbp,tgp,tup,thetaNP,deltaNP,bpiece,gpiece;
  double Ares,Hres,Mleft,Mq,Mgrav,Mres;
  s2d z0,z1;
  int finite_ok;

  if (in==NULL || o==NULL) return 1;
  k=in->k; x=k*k; if (!(x>0.)) return 2;
  if (!(in->a>0.) || !(in->Mc>0.) || !(in->lambda_HL>1.)) return 3;
  if (!(in->rb>0.) || !(in->rg>0.) || !(in->ru>0.) || !(in->tau_c>0.)) return 4;
  if (!(1.+in->w_khr>0.)) return 5;

  Lk=-x; r=in->lambda_HL-1.; DD=3.*in->lambda_HL-1.;
  Wg=(4./3.)*in->rg; Wu=(4./3.)*in->ru; W0=in->rb+Wg+Wu; Wk=in->rk+in->pk; W=W0+Wk;
  Db=in->delta_b-3.*in->PsiN; Dg=in->delta_g-4.*in->PsiN; Dur=in->delta_ur-4.*in->PsiN;
  h=in->rb*Db+in->rg*Dg+in->ru*Dur;
  ph=(in->rg*Dg+in->ru*Dur)/3.;
  denf=x+in->a*in->a*in->Mc*in->Mc; if (!(denf>0.)) return 6;
  K=-1.5*in->a*in->a/denf; a1=x/denf; Kp=2.*in->H*a1*K;
  W0p=-3.*in->H*in->rb-4.*in->H*(Wg+Wu);
  DA=1.-3.*K*W0; if (DA==0.) return 7;
  DAp=-3.*(Kp*W0+K*W0p);
  psi=K*h/DA;
  q0=in->a*(in->rb*in->theta_b+Wg*in->theta_g+Wu*in->theta_ur)/x;
  hp=-3.*in->H*(h+ph)-(x/in->a)*q0;
  psip=(Kp*h+K*hp-DAp*psi)/DA;
  dm0=h+3.*W0*psi+in->rk*in->delta_khr_N;
  Q0=3.*in->a*(q0+in->a*Wk*in->theta_khr_N/x);
  X0=3.*in->a*in->a*W0; Xt=3.*in->a*in->a*W;
  Bnum=2.*Lk*(Q0-DD*psip)+3.*DD*in->H*in->H*Q0+3.*DD*in->H*in->a*in->a*dm0-2.*DD*Lk*in->H*psi;
  Bden=r*2.*Lk*Lk-2.*DD*Lk*in->H*in->H+2.*Lk*Xt+3.*DD*in->H*in->H*X0;
  if (Bden==0.) return 8;
  B=Bnum/Bden;
  dm=dm0+3.*in->H*Wk*B;
  Qpref=Q0-Xt*B;
  lapse=r*2.*Lk-2.*DD*in->H*in->H; if (lapse==0.) return 9;
  Hrhs=-3.*in->a*in->a*r*dm-DD*in->H*Qpref+2.*DD*in->H*psip+2.*r*Lk*psi;
  phi=Hrhs/lapse;
  PsiRec=psi-in->H*B;

  Ares=DA*psi-K*h;
  Hres=lapse*phi-Hrhs;
  Mleft=r*Lk*B; Mq=Qpref; Mgrav=DD*(psip+in->H*phi); Mres=Mleft-Mq+Mgrav;

  R=Wg/in->rb;
  c=(16./45.)*in->tau_c;
  theta0p=(-in->H*in->theta_b+x*(in->cb2*in->delta_b+R*in->delta_g/4.))/(1.+R);
  pref=1.-(11./6.)*in->dtau_c; sec=(11./6.)*in->tau_c*c;
  sigmaA=pref*c*in->theta_g-sec*theta0p; sigmaPhi=-sec*x;
  PiA=1.5*(Wg*sigmaA+Wu*in->sigma_ur)/x; PiPhi=1.5*Wg*sigmaPhi/x;
  feedback=1.+3.*in->a*in->a*PiPhi; if (feedback==0.) return 10;
  Phi=(PsiRec-3.*in->a*in->a*PiA)/feedback;
  sg=sigmaA+sigmaPhi*Phi;
  Pi=1.5*(Wg*sg+Wu*in->sigma_ur)/x;
  tres=Phi-(PsiRec-3.*in->a*in->a*Pi);

  J=in->delta_khr_N/(1.+in->w_khr)-3.*in->PsiN;
  deltaPref=(1.+in->w_khr)*(J+3.*psi);
  thetaPref=in->theta_khr_N-x*B;
  thetaPrefP=-in->H*(1.-3.*in->ca2_khr)*thetaPref+x*(in->cs2_khr*deltaPref/(1.+in->w_khr)+phi);
  deltaPrefP=-(1.+in->w_khr)*(thetaPref+x*B-3.*psip)-3.*in->H*(in->ca2_khr-in->w_khr)*deltaPref;

  rbp=-3.*in->H*in->rb; Wgp=-4.*in->H*Wg; Wup=-4.*in->H*Wu;
  agg_bg=rbp*in->theta_b+Wgp*in->theta_g+Wup*in->theta_ur;
  agg_pb=in->rb*(-in->H*in->theta_b+x*(in->cb2*in->delta_b+R*(in->delta_g/4.-sg))+(1.+R)*x*Phi);
  agg_ur=Wu*x*(in->delta_ur/4.-in->sigma_ur+Phi);
  M0=in->rb*in->theta_b+Wg*in->theta_g+Wu*in->theta_ur;
  M0p=agg_bg+agg_pb+agg_ur; ap=in->a*in->H; q0p=(ap*M0+in->a*M0p)/x;

  z0=dae_B_dual(k,in->lambda_HL,in->Mc,
      D(in->a,ap),D(in->H,in->Hprime),D(in->rb,rbp),D(in->rg,-4.*in->H*in->rg),D(in->ru,-4.*in->H*in->ru),
      D(in->rk,-3.*in->H*Wk),D(in->pk,in->ca2_khr*(-3.*in->H*Wk)),
      D(Db,-in->theta_b),D(Dg,-(4./3.)*in->theta_g),D(Dur,-(4./3.)*in->theta_ur),D(J,-in->theta_khr_N),D(q0,q0p),D(in->theta_khr_N,thetaPrefP));
  z1=dae_B_dual(k,in->lambda_HL,in->Mc,
      D(in->a,ap),D(in->H,in->Hprime),D(in->rb,rbp),D(in->rg,-4.*in->H*in->rg),D(in->ru,-4.*in->H*in->ru),
      D(in->rk,-3.*in->H*Wk),D(in->pk,in->ca2_khr*(-3.*in->H*Wk)),
      D(Db,-in->theta_b),D(Dg,-(4./3.)*in->theta_g),D(Dur,-(4./3.)*in->theta_ur),D(J,-in->theta_khr_N),D(q0,q0p),D(in->theta_khr_N,thetaPrefP+x));
  f0=z0.d; f1=z1.d; cB=f1-f0; iden=1.-cB; if (iden==0.) return 11;
  Bp=f0/iden;
  PsiNp=psip-in->Hprime*B-in->H*Bp;

  metric_cont=-3.*PsiNp; metric_euler=x*Phi; App=in->Hprime+in->H*in->H;
  F=in->tau_c/(1.+R);
  Fp=in->dtau_c/(1.+R)+in->tau_c*in->H*R/((1.+R)*(1.+R));
  slip1=(in->dtau_c/in->tau_c-2.*in->H/(1.+R))*(in->theta_b-in->theta_g)
       +F*(-App*in->theta_b+x*(-in->H*in->delta_g/2.+in->cb2*(-in->theta_b-metric_cont)
       -(1./3.)*(-in->theta_g-metric_cont))-in->H*metric_euler);
  shear1=(16./45.)*in->tau_c*in->theta_g;
  thetaCommon=theta0p+metric_euler;
  shear1p=(16./45.)*(in->tau_c*thetaCommon+in->dtau_c*in->theta_g);
  slip=(1.-2.*in->H*F)*slip1+F*x*(2.*in->H*shear1+shear1p-(1./3.-in->cb2)*(F*thetaCommon+2.*Fp*in->theta_b));
  tbp=(-in->H*in->theta_b+x*(in->cb2*in->delta_b+R*(in->delta_g/4.-sg))+R*slip)/(1.+R)+metric_euler;
  tgp=-(tbp+in->H*in->theta_b-in->cb2*x*in->delta_b)/R+x*(in->delta_g/4.-sg)+(1.+R)/R*metric_euler;
  tup=x*(in->delta_ur/4.-in->sigma_ur)+metric_euler;
  thetaNP=thetaPrefP+x*Bp;
  deltaNP=-3.*in->H*(in->ca2_khr-in->w_khr)*in->delta_khr_N-(1.+in->w_khr)*in->theta_khr_N+3.*(1.+in->w_khr)*PsiNp;
  bpiece=in->rb*R/(1.+R)*slip; gpiece=Wg*(-1./(1.+R))*slip;

  finite_ok=isfinite(B)&&isfinite(Bp)&&isfinite(psi)&&isfinite(psip)&&isfinite(phi)&&isfinite(PsiRec)&&isfinite(PsiNp)&&isfinite(Phi)&&isfinite(sg)&&isfinite(slip)&&isfinite(deltaNP)&&isfinite(thetaNP)&&isfinite(iden);
  if (!finite_ok) return 12;

  o->B=B; o->B_prime=Bp; o->psi_pref=psi; o->psi_pref_prime=psip; o->phi_pref=phi;
  o->Psi_N_reconstructed=PsiRec; o->Psi_N_prime=PsiNp; o->Phi_N=Phi;
  o->sigma_g=sg; o->tca_slip=slip;
  o->theta_b_prime=tbp; o->theta_g_prime=tgp; o->theta_ur_prime=tup;
  o->delta_khr_pref_prime=deltaPrefP; o->theta_khr_pref_prime=thetaPrefP;
  o->delta_khr_N_prime=deltaNP; o->theta_khr_N_prime=thetaNP;
  o->metric_continuity=metric_cont; o->metric_euler=metric_euler;
  o->Bprime_affine_f0=f0; o->Bprime_affine_coefficient=cB; o->Bprime_implicit_denominator=iden;
  o->weighted_slip_cancel=fabs(bpiece+gpiece)/max2(max2(fabs(bpiece),fabs(gpiece)),1e-300);
  o->A_residual=Ares; o->A_residual_normalized=n2(Ares,DA*psi,K*h);
  o->Hamiltonian_residual=Hres; o->Hamiltonian_residual_normalized=n6(Hres,lapse*phi,-3.*in->a*in->a*r*dm,-DD*in->H*Qpref,2.*DD*in->H*psip,2.*r*Lk*psi,0.);
  o->momentum_residual=Mres; o->momentum_residual_normalized=n3(Mres,Mleft,Mq,Mgrav);
  o->traceless_residual=tres; o->traceless_residual_normalized=n3(tres,Phi,PsiRec,3.*in->a*in->a*Pi);
  o->Psi_reconstruction_relative=rel(PsiRec,in->PsiN);
  o->feedback_denominator=feedback;
  return 0;
}
