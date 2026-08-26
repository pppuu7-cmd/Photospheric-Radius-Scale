#ifndef RTK_C10_65S2_KERNEL_H
#define RTK_C10_65S2_KERNEL_H

typedef struct {
  double k,a,H,Hprime;
  double rb,rg,ru,rk,pk;
  double lambda_HL,Mc;
  double cb2,tau_c,dtau_c;
  double PsiN;
  double delta_b,theta_b,delta_g,theta_g,delta_ur,theta_ur,sigma_ur;
  double delta_khr_N,theta_khr_N;
  double w_khr,ca2_khr,cs2_khr;
} rtk_c10_65s2_input;

typedef struct {
  double B,B_prime;
  double psi_pref,psi_pref_prime,phi_pref;
  double Psi_N_reconstructed,Psi_N_prime,Phi_N;
  double sigma_g,tca_slip;
  double theta_b_prime,theta_g_prime,theta_ur_prime;
  double delta_khr_pref_prime,theta_khr_pref_prime;
  double delta_khr_N_prime,theta_khr_N_prime;
  double metric_continuity,metric_euler;
  double Bprime_affine_f0,Bprime_affine_coefficient,Bprime_implicit_denominator;
  double weighted_slip_cancel;
  double A_residual,A_residual_normalized;
  double Hamiltonian_residual,Hamiltonian_residual_normalized;
  double momentum_residual,momentum_residual_normalized;
  double traceless_residual,traceless_residual_normalized;
  double Psi_reconstruction_relative;
  double feedback_denominator;
} rtk_c10_65s2_output;

int rtk_c10_65s2_current_state(const rtk_c10_65s2_input *in,
                               rtk_c10_65s2_output *out);

#endif
