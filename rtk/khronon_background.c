#include "khronon_background.h"

#include <float.h>
#include <math.h>

static int finite_positive(double x) { return isfinite(x) && x > 0.0; }

const char *khr_status_string(int status) {
  switch (status) {
    case KHR_OK: return "OK";
    case KHR_BAD_INPUT: return "BAD_INPUT";
    case KHR_NONFINITE: return "NONFINITE";
    case KHR_UNPHYSICAL: return "UNPHYSICAL";
    default: return "UNKNOWN";
  }
}

int khr_closure_from_params(const khr_params *p, khr_closure *c) {
  double A, D, rootD, x0;
  if (p == NULL || c == NULL) return KHR_BAD_INPUT;
  if (!finite_positive(p->H0) || !finite_positive(p->gamma) ||
      !finite_positive(p->lambda_D) || !finite_positive(p->Omega_K0)) return KHR_BAD_INPUT;
  c->mu_K = 3.0 * p->H0 * sqrt(p->gamma);
  if (!finite_positive(c->mu_K)) return KHR_NONFINITE;
  A = p->Omega_K0 / (6.0 * p->gamma);
  if (!finite_positive(A)) return KHR_NONFINITE;
  if (fabs(p->lambda_D - 1.0) < 64.0 * DBL_EPSILON) {
    x0 = A * (A + 2.0) / (2.0 * (A + 1.0));
  } else {
    D = 1.0 + 2.0 * A + p->lambda_D * A * A;
    if (!(D > 0.0) || !isfinite(D)) return KHR_NONFINITE;
    rootD = sqrt(D);
    x0 = A * (2.0 + p->lambda_D * A) /
         (1.0 + p->lambda_D * A + rootD);
  }
  if (!finite_positive(x0)) return KHR_UNPHYSICAL;
  c->x0 = x0;
  return KHR_OK;
}

double khr_x0_normalization_residual(const khr_params *p, const khr_closure *c) {
  double s, t, lhs, rhs, scale;
  if (p == NULL || c == NULL || !finite_positive(c->x0)) return NAN;
  s = hypot(1.0, sqrt(p->lambda_D) * c->x0);
  t = c->x0 / (s + 1.0);
  lhs = 2.0 * c->mu_K * c->mu_K * (c->x0 + c->x0 * t);
  rhs = 3.0 * p->H0 * p->H0 * p->Omega_K0;
  scale = fmax(fabs(lhs), fabs(rhs));
  if (scale == 0.0) return 0.0;
  return (lhs - rhs) / scale;
}

int khr_background(const khr_params *p, const khr_closure *c, double a, double k, khr_state *out) {
  double sqrt_lambda, y, s, r, t, Q, mu2, rho8, p8, w, ca2, MK, kstar, cs2, ratio;
  if (p == NULL || c == NULL || out == NULL) return KHR_BAD_INPUT;
  if (!finite_positive(a) || !isfinite(k) || k < 0.0 ||
      !finite_positive(c->mu_K) || !finite_positive(c->x0)) return KHR_BAD_INPUT;
  out->a = a; out->k = k; out->x = c->x0 / (a*a*a);
  if (!finite_positive(out->x)) return KHR_NONFINITE;
  sqrt_lambda = sqrt(p->lambda_D); y = sqrt_lambda * out->x;
  s = hypot(1.0, y); r = out->x / s; t = out->x / (s + 1.0); Q = 1.0 + r;
  mu2 = c->mu_K * c->mu_K;
  rho8 = 2.0 * mu2 * out->x * (1.0 + t); p8 = 2.0 * mu2 * r * t; w = p8 / rho8;
  ca2 = r / (s * (s + out->x));
  MK = c->mu_K * Q * s * sqrt(s); kstar = a * MK;
  if (k == 0.0) cs2 = ca2;
  else if (kstar == 0.0) cs2 = 0.0;
  else { ratio = k / kstar; cs2 = (!isfinite(ratio) || ratio > sqrt(DBL_MAX)) ? 0.0 : ca2/(1.0+ratio*ratio); }
  out->s=s; out->r=r; out->t=t; out->Q=Q; out->rho8piG=rho8; out->p8piG=p8;
  out->w=w; out->ca2=ca2; out->M_K=MK; out->k_star=kstar; out->cs2=cs2; out->dbi_margin=1.0/(s*s);
  if (!isfinite(s)||!isfinite(r)||!isfinite(t)||!isfinite(Q)||!isfinite(rho8)||!isfinite(p8)||
      !isfinite(w)||!isfinite(ca2)||!isfinite(MK)||!isfinite(kstar)||!isfinite(cs2)||!isfinite(out->dbi_margin)) return KHR_NONFINITE;
  if (!(Q>0.0)||!(rho8>0.0)||p8<0.0||ca2<0.0||cs2<0.0||cs2>ca2*(1.0+64.0*DBL_EPSILON)||!(out->dbi_margin>0.0)) return KHR_UNPHYSICAL;
  return KHR_OK;
}
