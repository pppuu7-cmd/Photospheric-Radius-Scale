#include "khronon_action_shadow.h"
#include <math.h>
#include <stddef.h>

int khr_action_shadow_eval(const khr_action_shadow_bg *bg,
                           const khr_action_shadow_state *y,
                           const khr_action_shadow_metric *m,
                           khr_action_shadow_out *out) {
  double onepw, k2;
  if (!bg || !y || !m || !out) return 1;
  if (!isfinite(bg->w) || !isfinite(bg->ca2) || !isfinite(bg->cs2) ||
      !isfinite(bg->k) || !isfinite(bg->Hc) || !isfinite(y->delta) ||
      !isfinite(y->theta) || !isfinite(m->psi) || !isfinite(m->phi_prime)) return 1;
  if (bg->k <= 0.0 || bg->Hc < 0.0 || bg->ca2 < 0.0 || bg->cs2 < 0.0 || bg->cs2 > bg->ca2) return 2;
  onepw=1.0+bg->w;
  if (!(onepw>0.0)) return 2;
  k2=bg->k*bg->k;
  out->delta_prime=-onepw*(y->theta-3.0*m->phi_prime)-3.0*bg->Hc*(bg->ca2-bg->w)*y->delta;
  out->theta_prime=-bg->Hc*(1.0-3.0*bg->ca2)*y->theta+k2*(bg->cs2*y->delta/onepw+m->psi);
  out->delta_p_over_rho=bg->cs2*y->delta;
  out->momentum_over_rho=onepw*y->theta;
  return (isfinite(out->delta_prime)&&isfinite(out->theta_prime)&&
          isfinite(out->delta_p_over_rho)&&isfinite(out->momentum_over_rho)) ? 0 : 3;
}
