#ifndef KHRONON_BACKGROUND_H
#define KHRONON_BACKGROUND_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
  double H0;
  double gamma;
  double lambda_D;
  double Omega_K0;
} khr_params;

typedef struct {
  double mu_K;
  double x0;
} khr_closure;

typedef struct {
  double a;
  double k;
  double x;
  double s;
  double r;
  double t;
  double Q;
  double rho8piG;
  double p8piG;
  double w;
  double ca2;
  double M_K;
  double k_star;
  double cs2;
  double dbi_margin;
} khr_state;

enum { KHR_OK=0, KHR_BAD_INPUT=1, KHR_NONFINITE=2, KHR_UNPHYSICAL=3 };

int khr_closure_from_params(const khr_params *p, khr_closure *c);
int khr_background(const khr_params *p, const khr_closure *c, double a, double k, khr_state *out);
double khr_x0_normalization_residual(const khr_params *p, const khr_closure *c);
const char *khr_status_string(int status);

#ifdef __cplusplus
}
#endif
#endif
