#include "u1_elliptic_completion_shadow.h"

#include <math.h>
#include <stddef.h>

static int finite_positive(double x) {
  return isfinite(x) && x > 0.0;
}

const char *rtk_u1_shadow_status_string(int status) {
  switch (status) {
    case RTK_U1_SHADOW_OK: return "OK";
    case RTK_U1_SHADOW_BAD_INPUT: return "BAD_INPUT";
    case RTK_U1_SHADOW_NONFINITE: return "NONFINITE";
    case RTK_U1_SHADOW_UNPHYSICAL: return "UNPHYSICAL";
    default: return "UNKNOWN";
  }
}

int rtk_u1_shadow_validate(const rtk_u1_shadow_params *p) {
  if (p == NULL) return RTK_U1_SHADOW_BAD_INPUT;
  if (!isfinite(p->lambda_HL) || !(p->lambda_HL > 1.0)) return RTK_U1_SHADOW_UNPHYSICAL;
  if (!finite_positive(p->M_c) || !finite_positive(p->eta0)) return RTK_U1_SHADOW_UNPHYSICAL;
  return RTK_U1_SHADOW_OK;
}

double rtk_u1_shadow_h2_ratio(double lambda_HL) {
  double denom;
  if (!isfinite(lambda_HL) || !(lambda_HL > 1.0)) return NAN;
  denom = 3.0 * lambda_HL - 1.0;
  if (!finite_positive(denom)) return NAN;
  return 2.0 / denom;
}

int rtk_u1_shadow_eval(const rtk_u1_shadow_params *p,
                       double a,
                       double k_com,
                       rtk_u1_shadow_state *out) {
  double k_phys, hyp, q_over_h0, a1_eff, h2_ratio;
  int status;

  if (out == NULL) return RTK_U1_SHADOW_BAD_INPUT;
  status = rtk_u1_shadow_validate(p);
  if (status != RTK_U1_SHADOW_OK) return status;
  if (!finite_positive(a) || !isfinite(k_com) || k_com < 0.0) return RTK_U1_SHADOW_BAD_INPUT;

  k_phys = k_com / a;
  if (!isfinite(k_phys) || k_phys < 0.0) return RTK_U1_SHADOW_NONFINITE;

  /* Stable realization of Q/H0=M_c^2/(M_c^2+k_phys^2). */
  hyp = hypot(p->M_c, k_phys);
  if (!finite_positive(hyp)) return RTK_U1_SHADOW_NONFINITE;
  q_over_h0 = p->M_c / hyp;
  q_over_h0 *= q_over_h0;
  a1_eff = 1.0 - q_over_h0;
  h2_ratio = rtk_u1_shadow_h2_ratio(p->lambda_HL);

  if (!isfinite(q_over_h0) || !isfinite(a1_eff) || !isfinite(h2_ratio)) return RTK_U1_SHADOW_NONFINITE;
  if (q_over_h0 < 0.0 || q_over_h0 > 1.0 || a1_eff < 0.0 || a1_eff > 1.0) return RTK_U1_SHADOW_UNPHYSICAL;

  out->a = a;
  out->k_com = k_com;
  out->k_phys = k_phys;
  out->q_over_h0 = q_over_h0;
  out->a1_eff = a1_eff;
  out->h2_ratio = h2_ratio;
  return RTK_U1_SHADOW_OK;
}
