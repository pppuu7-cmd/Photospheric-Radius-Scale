#ifndef KHRONON_PERTURBATIONS_H
#define KHRONON_PERTURBATIONS_H

#include "khronon_background.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct { double delta; double theta; } khr_pert_state;
typedef struct { double Hc; double phi_prime; double psi; } khr_metric_sources;
typedef struct { double delta_prime; double theta_prime; } khr_pert_derivs;
typedef struct {
  double rho_class, p_class, delta_rho_class, delta_p_class;
  double momentum_class, shear_class, w, ca2, cs2, k_star;
} khr_class_sources;

int khr_perturb_derivs_newtonian(const khr_state *bg,const khr_pert_state *y,const khr_metric_sources *metric,khr_pert_derivs *dy);
int khr_class_sources_newtonian(const khr_state *bg,const khr_pert_state *y,double Hc,khr_class_sources *src);
int khr_sync_to_newtonian(double w,double Hc,double k,double alpha,const khr_pert_state *sync,khr_pert_state *newtonian);
int khr_newtonian_to_sync(double w,double Hc,double k,double alpha,const khr_pert_state *newtonian,khr_pert_state *sync);
double khr_delta_adiabatic_from_photon(double w,double delta_gamma);

#ifdef __cplusplus
}
#endif
#endif
