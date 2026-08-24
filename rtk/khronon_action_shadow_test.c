#include "khronon_action_shadow.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>

static int close_rel(double a,double b,double tol){
  double s=fmax(1.0,fmax(fabs(a),fabs(b)));
  return fabs(a-b)<=tol*s;
}

static void production_formula(const khr_action_shadow_bg *bg,
                               const khr_action_shadow_state *y,
                               const khr_action_shadow_metric *m,
                               khr_action_shadow_out *o){
  double onepw=1.0+bg->w, k2=bg->k*bg->k, entropy=bg->cs2-bg->ca2;
  o->delta_prime=-onepw*(y->theta-3.0*m->phi_prime)-3.0*bg->Hc*(bg->cs2-bg->w)*y->delta
                 -9.0*bg->Hc*bg->Hc*onepw*entropy*y->theta/k2;
  o->theta_prime=-bg->Hc*(1.0-3.0*bg->cs2)*y->theta+k2*(bg->cs2*y->delta/onepw+m->psi);
  o->delta_p_over_rho=bg->cs2*y->delta+3.0*bg->Hc*onepw*entropy*y->theta/k2;
  o->momentum_over_rho=onepw*y->theta;
}

int main(void){
  khr_action_shadow_bg bg={-0.05,2.0e-8,2.0e-8,0.12,3.0e-4};
  khr_action_shadow_state y={0.08,1.5e-3};
  khr_action_shadow_metric m={2.0e-5,-3.0e-7};
  khr_action_shadow_out a,p;
  assert(khr_action_shadow_eval(&bg,&y,&m,&a)==0);
  production_formula(&bg,&y,&m,&p);
  assert(close_rel(a.delta_prime,p.delta_prime,1e-14));
  assert(close_rel(a.theta_prime,p.theta_prime,1e-14));
  assert(close_rel(a.delta_p_over_rho,p.delta_p_over_rho,1e-14));

  bg.cs2=3.0e-9;
  assert(khr_action_shadow_eval(&bg,&y,&m,&a)==0);
  production_formula(&bg,&y,&m,&p);
  {
    double dc=bg.cs2-bg.ca2, onepw=1.0+bg.w, k2=bg.k*bg.k;
    double expected_d=-3.0*bg.Hc*dc*(y.delta+3.0*bg.Hc*onepw*y.theta/k2);
    double expected_t=3.0*bg.Hc*dc*y.theta;
    assert(close_rel(p.delta_prime-a.delta_prime,expected_d,1e-14));
    assert(close_rel(p.theta_prime-a.theta_prime,expected_t,1e-14));
    assert(close_rel(a.delta_p_over_rho,bg.cs2*y.delta,1e-14));
  }
  assert(khr_action_shadow_eval(NULL,&y,&m,&a)!=0);
  bg.ca2=-1.0;
  assert(khr_action_shadow_eval(&bg,&y,&m,&a)!=0);
  puts("C10_ACTION_FLUID_SHADOW_INTERFACE_PASS");
  return 0;
}
