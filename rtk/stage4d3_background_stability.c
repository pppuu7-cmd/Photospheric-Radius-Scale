#include "khronon_background.h"

#include <float.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static int fail_count = 0;
static long long state_count = 0;
static double max_norm_resid = 0.0;
static double max_margin_identity = 0.0;
static double min_margin = DBL_MAX;
static double min_ca2 = DBL_MAX;
static double max_cs_over_ca = 0.0;

static void check(int ok, const char *what, double lam, double gamma,
                  double Om, double a, double k) {
  if (!ok) {
    ++fail_count;
    if (fail_count <= 20) {
      fprintf(stderr,
              "FAIL %s lambda=%.17g gamma=%.17g Om=%.17g a=%.17g k=%.17g\n",
              what, lam, gamma, Om, a, k);
    }
  }
}

int main(void) {
  const double lambdas[] = {1e3, 3e3, 1e4, 1.5e4, 2e4, 2.5e4, 2.75e4,
                            3e4, 3.25e4, 3.5e4, 4e4, 6e4, 8e4, 1e5,
                            1e6, 1e8};
  const double gammas[] = {1e-4, 1e-3, 1e-2, 3e-2, 5e-2, 8e-2, 0.2, 1.0};
  const double oms[] = {0.20, 0.23, 0.25, 0.253, 0.28, 0.32};
  const double kvals[] = {0.0, 1e-5, 1e-3, 0.1, 1.0, 10.0, 1e3};
  const int na = 49;
  size_t il, ig, io, ik;
  int ia;

  for (il = 0; il < sizeof(lambdas)/sizeof(lambdas[0]); ++il) {
    for (ig = 0; ig < sizeof(gammas)/sizeof(gammas[0]); ++ig) {
      for (io = 0; io < sizeof(oms)/sizeof(oms[0]); ++io) {
        khr_params p;
        khr_closure c;
        int st;
        double norm;
        p.H0 = 2.25e-4; /* arbitrary positive CLASS-like inverse-Mpc scale */
        p.gamma = gammas[ig];
        p.lambda_D = lambdas[il];
        p.Omega_K0 = oms[io];
        st = khr_closure_from_params(&p, &c);
        check(st == KHR_OK, "closure", p.lambda_D, p.gamma, p.Omega_K0, 1.0, 0.0);
        if (st != KHR_OK) continue;
        norm = fabs(khr_x0_normalization_residual(&p, &c));
        if (norm > max_norm_resid) max_norm_resid = norm;
        check(isfinite(norm) && norm < 5e-13, "normalization", p.lambda_D, p.gamma, p.Omega_K0, 1.0, 0.0);
        check(c.x0 > 0.0 && isfinite(c.x0), "x0_positive", p.lambda_D, p.gamma, p.Omega_K0, 1.0, 0.0);
        check(c.mu_K > 0.0 && isfinite(c.mu_K), "mu_positive", p.lambda_D, p.gamma, p.Omega_K0, 1.0, 0.0);

        for (ia = 0; ia < na; ++ia) {
          /* a = 10^[-10,0], including radiation era well before recombination. */
          double loga = -10.0 + 10.0 * ((double)ia / (double)(na - 1));
          double a = pow(10.0, loga);
          for (ik = 0; ik < sizeof(kvals)/sizeof(kvals[0]); ++ik) {
            khr_state s;
            double identity, csratio;
            st = khr_background(&p, &c, a, kvals[ik], &s);
            ++state_count;
            check(st == KHR_OK, "background", p.lambda_D, p.gamma, p.Omega_K0, a, kvals[ik]);
            if (st != KHR_OK) continue;
            check(s.x > 0.0 && s.s >= 1.0 && s.r > 0.0 && s.t > 0.0 && s.Q > 1.0,
                  "positive_kinematics", p.lambda_D, p.gamma, p.Omega_K0, a, kvals[ik]);
            check(s.rho8piG > 0.0 && s.p8piG >= 0.0 && s.w >= 0.0,
                  "positive_stress", p.lambda_D, p.gamma, p.Omega_K0, a, kvals[ik]);
            check(s.ca2 >= 0.0 && s.ca2 < 1.0,
                  "ca2_range", p.lambda_D, p.gamma, p.Omega_K0, a, kvals[ik]);
            check(s.cs2 >= 0.0 && s.cs2 <= s.ca2 * (1.0 + 1e-12),
                  "cs2_range", p.lambda_D, p.gamma, p.Omega_K0, a, kvals[ik]);
            check(s.M_K > 0.0 && s.k_star > 0.0,
                  "positive_scales", p.lambda_D, p.gamma, p.Omega_K0, a, kvals[ik]);
            check(s.dbi_margin > 0.0 && s.dbi_margin <= 1.0,
                  "dbi_margin", p.lambda_D, p.gamma, p.Omega_K0, a, kvals[ik]);

            /* Stable exact branch identity: margin * s^2 == 1. */
            identity = fabs(s.dbi_margin * s.s * s.s - 1.0);
            if (identity > max_margin_identity) max_margin_identity = identity;
            check(identity < 2e-12, "branch_identity", p.lambda_D, p.gamma, p.Omega_K0, a, kvals[ik]);

            if (s.dbi_margin < min_margin) min_margin = s.dbi_margin;
            if (s.ca2 < min_ca2) min_ca2 = s.ca2;
            csratio = (s.ca2 > 0.0) ? s.cs2 / s.ca2 : 0.0;
            if (csratio > max_cs_over_ca) max_cs_over_ca = csratio;
          }
        }
      }
    }
  }

  printf("STAGE4D3_STABILITY_STATES %lld\n", state_count);
  printf("STAGE4D3_STABILITY_MAX_NORM_RESID %.17g\n", max_norm_resid);
  printf("STAGE4D3_STABILITY_MAX_BRANCH_IDENTITY %.17g\n", max_margin_identity);
  printf("STAGE4D3_STABILITY_MIN_MARGIN %.17g\n", min_margin);
  printf("STAGE4D3_STABILITY_MIN_CA2 %.17g\n", min_ca2);
  printf("STAGE4D3_STABILITY_MAX_CS_OVER_CA %.17g\n", max_cs_over_ca);
  if (fail_count != 0) {
    printf("STAGE4D3_STABILITY_FAIL %d\n", fail_count);
    return 1;
  }
  printf("STAGE4D3_STABILITY_PASS\n");
  return 0;
}
