#include "u1_elliptic_completion_shadow.h"

#include <assert.h>
#include <math.h>
#include <stdio.h>

static int close_rel(double a, double b, double tol) {
  double scale = fmax(1.0, fmax(fabs(a), fabs(b)));
  return fabs(a-b) <= tol*scale;
}

int main(void) {
  rtk_u1_shadow_params p = {1.001, 2.0, 1.0};
  rtk_u1_shadow_state s0, s1, s2;
  rtk_u1_shadow_params bad;
  double near_gr;

  assert(rtk_u1_shadow_validate(&p) == RTK_U1_SHADOW_OK);
  assert(close_rel(rtk_u1_shadow_h2_ratio(p.lambda_HL), 2.0/(3.0*p.lambda_HL-1.0), 1e-15));

  /* Exact homogeneous filter limit. */
  assert(rtk_u1_shadow_eval(&p, 1.0, 0.0, &s0) == RTK_U1_SHADOW_OK);
  assert(s0.k_phys == 0.0);
  assert(s0.q_over_h0 == 1.0);
  assert(s0.a1_eff == 0.0);
  assert(s0.a1_eff + s0.q_over_h0 == 1.0);

  /* k_phys=k_com/a and the analytic half-transfer point k_phys=M_c. */
  assert(rtk_u1_shadow_eval(&p, 0.5, 1.0, &s1) == RTK_U1_SHADOW_OK);
  assert(close_rel(s1.k_phys, 2.0, 1e-15));
  assert(close_rel(s1.q_over_h0, 0.5, 1e-15));
  assert(close_rel(s1.a1_eff, 0.5, 1e-15));
  assert(s1.a1_eff + s1.q_over_h0 == 1.0);

  /* Higher physical k approaches local-family-I recovery monotonically. */
  assert(rtk_u1_shadow_eval(&p, 1.0, 200.0, &s2) == RTK_U1_SHADOW_OK);
  assert(s2.a1_eff > s1.a1_eff);
  assert(s2.q_over_h0 < s1.q_over_h0);
  assert(s2.a1_eff > 0.9999);
  assert(s2.a1_eff + s2.q_over_h0 == 1.0);

  /* The lambda_HL->1+ homogeneous normalization is continuous. */
  near_gr = rtk_u1_shadow_h2_ratio(1.0 + 1e-9);
  assert(isfinite(near_gr));
  assert(fabs(near_gr-1.0) < 2e-9);

  /* Structural-domain validation is separate from lambda_D. */
  bad = p; bad.lambda_HL = 1.0;
  assert(rtk_u1_shadow_validate(&bad) == RTK_U1_SHADOW_UNPHYSICAL);
  bad = p; bad.M_c = 0.0;
  assert(rtk_u1_shadow_validate(&bad) == RTK_U1_SHADOW_UNPHYSICAL);
  bad = p; bad.eta0 = -1.0;
  assert(rtk_u1_shadow_validate(&bad) == RTK_U1_SHADOW_UNPHYSICAL);

  printf("RTK_ROUTE_B_U1_COMPLETION_SHADOW_INTERFACE_PASS\n");
  return 0;
}
