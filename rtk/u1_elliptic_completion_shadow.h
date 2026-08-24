#ifndef RTK_U1_ELLIPTIC_COMPLETION_SHADOW_H
#define RTK_U1_ELLIPTIC_COMPLETION_SHADOW_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
  double lambda_HL;
  double M_c;
  double eta0;
} rtk_u1_shadow_params;

typedef struct {
  double a;
  double k_com;
  double k_phys;
  double q_over_h0;
  double a1_eff;
  double h2_ratio;
} rtk_u1_shadow_state;

enum {
  RTK_U1_SHADOW_OK = 0,
  RTK_U1_SHADOW_BAD_INPUT = 1,
  RTK_U1_SHADOW_NONFINITE = 2,
  RTK_U1_SHADOW_UNPHYSICAL = 3
};

int rtk_u1_shadow_validate(const rtk_u1_shadow_params *p);
double rtk_u1_shadow_h2_ratio(double lambda_HL);
int rtk_u1_shadow_eval(const rtk_u1_shadow_params *p,
                       double a,
                       double k_com,
                       rtk_u1_shadow_state *out);
const char *rtk_u1_shadow_status_string(int status);

#ifdef __cplusplus
}
#endif

#endif
