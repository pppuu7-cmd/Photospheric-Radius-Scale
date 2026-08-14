#include "khronon_perturbations.h"
#include <math.h>
#include <stddef.h>

static int finite4(double a,double b,double c,double d){return isfinite(a)&&isfinite(b)&&isfinite(c)&&isfinite(d);}

int khr_perturb_derivs_newtonian(const khr_state *bg,const khr_pert_state *y,const khr_metric_sources *m,khr_pert_derivs *dy){
  double onepw,k2,entropy;
  if(!bg||!y||!m||!dy) return KHR_BAD_INPUT;
  if(!finite4(bg->w,bg->ca2,bg->cs2,bg->k)||!finite4(y->delta,y->theta,m->Hc,m->psi)||!isfinite(m->phi_prime)||bg->k<=0.0||m->Hc<0.0) return KHR_BAD_INPUT;
  onepw=1.0+bg->w; if(!(onepw>0.0)) return KHR_UNPHYSICAL;
  k2=bg->k*bg->k; entropy=bg->cs2-bg->ca2;
  dy->delta_prime=-onepw*(y->theta-3.0*m->phi_prime)-3.0*m->Hc*(bg->cs2-bg->w)*y->delta-9.0*m->Hc*m->Hc*onepw*entropy*y->theta/k2;
  dy->theta_prime=-m->Hc*(1.0-3.0*bg->cs2)*y->theta+k2*(bg->cs2*y->delta/onepw+m->psi);
  return (isfinite(dy->delta_prime)&&isfinite(dy->theta_prime))?KHR_OK:KHR_NONFINITE;
}

int khr_class_sources_newtonian(const khr_state *bg,const khr_pert_state *y,double Hc,khr_class_sources *s){
  double onepw,k2,pb;
  if(!bg||!y||!s||!isfinite(Hc)||Hc<0.0||!isfinite(y->delta)||!isfinite(y->theta)||bg->k<=0.0) return KHR_BAD_INPUT;
  onepw=1.0+bg->w; if(!(onepw>0.0)) return KHR_UNPHYSICAL; k2=bg->k*bg->k;
  pb=bg->cs2*y->delta+3.0*Hc*onepw*(bg->cs2-bg->ca2)*y->theta/k2;
  s->rho_class=bg->rho8piG/3.0; s->p_class=bg->p8piG/3.0; s->delta_rho_class=s->rho_class*y->delta; s->delta_p_class=s->rho_class*pb;
  s->momentum_class=(s->rho_class+s->p_class)*y->theta; s->shear_class=0.0; s->w=bg->w; s->ca2=bg->ca2; s->cs2=bg->cs2; s->k_star=bg->k_star;
  return finite4(s->rho_class,s->p_class,s->delta_rho_class,s->delta_p_class)&&isfinite(s->momentum_class)?KHR_OK:KHR_NONFINITE;
}

int khr_sync_to_newtonian(double w,double Hc,double k,double alpha,const khr_pert_state *sync,khr_pert_state *n){
  if(!sync||!n||!finite4(w,Hc,k,alpha)||!isfinite(sync->delta)||!isfinite(sync->theta)||k<0.0) return KHR_BAD_INPUT;
  n->delta=sync->delta-3.0*(1.0+w)*Hc*alpha; n->theta=sync->theta+k*k*alpha; return (isfinite(n->delta)&&isfinite(n->theta))?KHR_OK:KHR_NONFINITE;
}
int khr_newtonian_to_sync(double w,double Hc,double k,double alpha,const khr_pert_state *n,khr_pert_state *sync){
  if(!n||!sync||!finite4(w,Hc,k,alpha)||!isfinite(n->delta)||!isfinite(n->theta)||k<0.0) return KHR_BAD_INPUT;
  sync->delta=n->delta+3.0*(1.0+w)*Hc*alpha; sync->theta=n->theta-k*k*alpha; return (isfinite(sync->delta)&&isfinite(sync->theta))?KHR_OK:KHR_NONFINITE;
}
double khr_delta_adiabatic_from_photon(double w,double dg){return (!isfinite(w)||!isfinite(dg))?NAN:0.75*(1.0+w)*dg;}
