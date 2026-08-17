#include "khronon_background.h"
#include "khronon_perturbations.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>

static void near(double a,double b,double tol){
  double s=fmax(1.0,fmax(fabs(a),fabs(b)));
  assert(fabs(a-b)<=tol*s);
}

int main(void){
  const double lambdas[]={1.0,10.0,1e2,1e4,2e5,1e7};
  const double avec[]={1e-3,1e-2,1e-1,1.0};
  double previous_w=INFINITY, previous_ca2=INFINITY;
  for(size_t il=0;il<sizeof(lambdas)/sizeof(lambdas[0]);++il){
    khr_params p={1.0,1e-4,lambdas[il],0.25};
    khr_closure c;
    assert(khr_closure_from_params(&p,&c)==KHR_OK);
    assert(isfinite(c.mu_K)&&c.mu_K>0.0&&isfinite(c.x0)&&c.x0>0.0);
    assert(fabs(khr_x0_normalization_residual(&p,&c))<5e-13);
    for(size_t ia=0;ia<sizeof(avec)/sizeof(avec[0]);++ia){
      khr_state b0,bk;
      assert(khr_background(&p,&c,avec[ia],0.0,&b0)==KHR_OK);
      assert(khr_background(&p,&c,avec[ia],0.2,&bk)==KHR_OK);
      assert(b0.rho8piG>0.0&&b0.p8piG>=0.0);
      assert(b0.w>=0.0&&b0.w<1.0);
      assert(b0.ca2>=0.0&&b0.ca2<1.0);
      assert(bk.cs2>=0.0&&bk.cs2<=bk.ca2*(1.0+1e-12));
      assert(b0.dbi_margin>0.0&&b0.dbi_margin<=1.0);
    }
    khr_state today;
    assert(khr_background(&p,&c,1.0,0.0,&today)==KHR_OK);
    if(il>0){
      assert(today.w<previous_w);
      assert(today.ca2<previous_ca2);
    }
    previous_w=today.w; previous_ca2=today.ca2;
  }

  /* Large-lambda implementation must approach a dust-like present-day limit. */
  {
    khr_params p={1.0,1e-4,1e7,0.25}; khr_closure c; khr_state b;
    assert(khr_closure_from_params(&p,&c)==KHR_OK);
    assert(khr_background(&p,&c,1.0,0.1,&b)==KHR_OK);
    assert(b.w<1e-8);
    assert(b.ca2<1e-12);
    assert(b.cs2<=b.ca2);
  }

  /* Gauge transforms must be exact inverses for the implemented fluid variables. */
  {
    khr_pert_state s={0.031,-0.017},n,r;
    assert(khr_sync_to_newtonian(0.02,0.11,0.7,-0.03,&s,&n)==KHR_OK);
    assert(khr_newtonian_to_sync(0.02,0.11,0.7,-0.03,&n,&r)==KHR_OK);
    near(s.delta,r.delta,5e-15); near(s.theta,r.theta,5e-15);
    near(khr_delta_adiabatic_from_photon(0.02,0.4),0.75*1.02*0.4,5e-15);
  }

  /* CLASS-source normalization must preserve rho/3 and p/3 conventions. */
  {
    khr_params p={1.0,1e-4,2e5,0.25}; khr_closure c; khr_state b;
    khr_pert_state y={0.02,-0.01}; khr_class_sources src;
    assert(khr_closure_from_params(&p,&c)==KHR_OK);
    assert(khr_background(&p,&c,0.8,0.15,&b)==KHR_OK);
    assert(khr_class_sources_newtonian(&b,&y,0.09,&src)==KHR_OK);
    near(src.rho_class,b.rho8piG/3.0,5e-15);
    near(src.p_class,b.p8piG/3.0,5e-15);
    near(src.delta_rho_class,src.rho_class*y.delta,5e-15);
    near(src.momentum_class,(src.rho_class+src.p_class)*y.theta,5e-15);
  }

  puts("RTK_KHRONON_REGRESSION_PASS");
  return 0;
}
