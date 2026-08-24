#ifndef KHRONON_ACTION_SHADOW_H
#define KHRONON_ACTION_SHADOW_H

typedef struct {
  double w, ca2, cs2, k, Hc;
} khr_action_shadow_bg;

typedef struct {
  double delta, theta;
} khr_action_shadow_state;

typedef struct {
  double psi, phi_prime;
} khr_action_shadow_metric;

typedef struct {
  double delta_prime, theta_prime;
  double delta_p_over_rho;
  double momentum_over_rho;
} khr_action_shadow_out;

int khr_action_shadow_eval(const khr_action_shadow_bg *bg,
                           const khr_action_shadow_state *y,
                           const khr_action_shadow_metric *m,
                           khr_action_shadow_out *out);

#endif
