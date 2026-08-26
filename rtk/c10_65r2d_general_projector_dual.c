#include <math.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { double v,d; } dual;
static inline dual C(double v){ dual x={v,0.}; return x; }
static inline dual D(double v,double d){ dual x={v,d}; return x; }
static inline dual add(dual a,dual b){ return D(a.v+b.v,a.d+b.d); }
static inline dual sub(dual a,dual b){ return D(a.v-b.v,a.d-b.d); }
static inline dual mul(dual a,dual b){ return D(a.v*b.v,a.d*b.v+a.v*b.d); }
static inline dual divd(dual a,dual b){ double q=a.v/b.v; return D(q,(a.d-q*b.d)/b.v); }
static inline dual scale(double s,dual a){ return D(s*a.v,s*a.d); }

/* C10.65r2d: IEEE-754 double forward-directional implementation of the
 * C10.65r2c general cancellation-reduced off-manifold projector.  This file is
 * a standalone numerical port preflight.  It intentionally contains no C2 and
 * introduces no matching/boundary datum. */
static dual projector_B(
  double lam,double Mc,double k,
  dual a,dual H,dual rb,dual rg,dual ru,dual rk,dual pk,
  dual Db,dual Dg,dual Dur,dual thb,dual thg,dual thur,dual dk,dual thk)
{
  const double x=k*k, L=-x, rr=lam-1., DD=3.*lam-1., E=2., P=1.;
  dual Wg=scale(4./3.,rg), Wu=scale(4./3.,ru);
  dual W0=add(rb,add(Wg,Wu));
  dual Wk=add(rk,pk);
  dual h=add(mul(rb,Db),add(mul(rg,Dg),mul(ru,Dur)));
  dual ph=scale(1./3.,add(mul(rg,Dg),mul(ru,Dur)));
  dual mom0=add(mul(rb,thb),add(mul(Wg,thg),mul(Wu,thur)));
  dual q0N=scale(1./x,mul(a,mom0));
  dual aa=mul(a,a);
  dual kden=add(C(x),scale(Mc*Mc,aa));
  dual K=scale(-1.5,divd(aa,kden));
  dual a1=divd(C(x),kden);
  dual Kp=scale(2.,mul(H,mul(a1,K)));
  dual W0p=add(scale(-3.,mul(H,rb)),scale(-4.,mul(H,add(Wg,Wu))));
  dual DA=sub(C(1.),scale(3.,mul(K,W0)));
  dual DAp=scale(-3.,add(mul(Kp,W0),mul(K,W0p)));
  dual psi=divd(mul(K,h),DA);
  dual hp=add(scale(-3.,mul(H,add(h,ph))),scale(-x,mul(divd(C(1.),a),q0N)));
  dual psip=divd(sub(add(mul(Kp,h),mul(K,hp)),mul(DAp,psi)),DA);
  dual dm=add(h,add(scale(3.,mul(W0,psi)),mul(rk,dk)));
  dual qk=scale(1./x,mul(a,mul(Wk,thk)));
  dual Q=scale(3.,mul(a,add(q0N,qk)));
  dual X0=scale(3.,mul(aa,W0));
  dual num=C(0.), den=C(0.);
  num=add(num,scale(E*L,sub(Q,scale(DD,psip))));
  num=add(num,scale(3.*DD,mul(mul(H,H),Q)));
  num=add(num,scale(3.*DD,mul(H,mul(aa,dm))));
  num=add(num,scale(-2.*DD*P*L,mul(H,psi)));
  den=add(den,C(rr*E*L*L));
  den=add(den,scale(-2.*DD*L,mul(H,H)));
  den=add(den,scale(E*L,X0));
  den=add(den,scale(3.*DD,mul(mul(H,H),X0)));
  return divd(num,den);
}

int main(void){
  double lam,Mc,k;
  double bv[7],bd[7],zv[8],zd[8];
  while (scanf("%lf %lf %lf",&lam,&Mc,&k)==3) {
    int i;
    for(i=0;i<7;i++) if(scanf("%lf",&bv[i])!=1) return 2;
    for(i=0;i<7;i++) if(scanf("%lf",&bd[i])!=1) return 2;
    for(i=0;i<8;i++) if(scanf("%lf",&zv[i])!=1) return 2;
    for(i=0;i<8;i++) if(scanf("%lf",&zd[i])!=1) return 2;
    dual B=projector_B(lam,Mc,k,
      D(bv[0],bd[0]),D(bv[1],bd[1]),D(bv[2],bd[2]),D(bv[3],bd[3]),D(bv[4],bd[4]),D(bv[5],bd[5]),D(bv[6],bd[6]),
      D(zv[0],zd[0]),D(zv[1],zd[1]),D(zv[2],zd[2]),D(zv[3],zd[3]),D(zv[4],zd[4]),D(zv[5],zd[5]),D(zv[6],zd[6]),D(zv[7],zd[7]));
    if(!isfinite(B.v)||!isfinite(B.d)) return 3;
    printf("%.17e %.17e\n",B.v,B.d);
  }
  return 0;
}
