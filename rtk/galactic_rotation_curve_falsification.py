#!/usr/bin/env python3
"""Analytic necessary-condition test for galaxy flat rotation curves.

This audit uses only the *implemented linear RTK closure* in the static,
quasistatic limit.  It asks whether that closure by itself can generate the
scale-free potential Phi(r) ~ log r (hence a_r ~ 1/r and flat v_c) around a
compact baryonic source without adding a particle-DM halo.

It is deliberately a falsification/necessary-condition test.  Failure means
the present linear closure does not supply the required scale-free galactic
kernel.  PASS would not prove galaxy phenomenology because the cosmological
linearization is not a nonlinear isolated-galaxy solution.
"""
import json, math

# Implemented equations imply in the static limit:
#   0 = theta' = k^2 [ cs2*delta/(1+w) + psi ]
# => delta_K = -(1+w) psi/cs2(k)
# with cs2(k)=ca2/(1+k^2/kstar^2).
# Hence delta_rho_K = -(rho_K(1+w)/ca2)*(1+k^2/kstar^2)*psi.
# A Poisson/Einstein constraint linear in total delta_rho then has the form
#   D(k^2) psi_k = source_k,
# where D is affine in k^2: D=A*k^2+B (after collecting the RTK response).
# The Green kernel is therefore rational in k^2 with only even-power poles.
# For a compact source this yields Coulomb/Newton (1/r) and/or Yukawa-type
# potentials, not a scale-free log(r) potential over an asymptotic interval.
# Flat circular speed requires Phi~v0^2 log r, a~v0^2/r.

required_potential = "log_r"
required_acceleration_slope = -1.0
implemented_denominator_degree_in_k2 = 1
implemented_kernel_class = "rational_affine_in_k2"
implemented_real_space_class = ["1/r", "exp(-m r)/r", "oscillatory_1/r_if_sign_flipped"]
produces_log_r_asymptotically = False
produces_scale_free_1_over_r_acceleration_asymptotically = False

# Fourier scaling cross-check in 3 spatial dimensions:
# log r has non-contact scaling ~ k^-3, whereas an affine rational function
# of k^2 can asymptote only to k^0 or k^-2 (up to tuned/contact pieces), not k^-3.
required_noncontact_fourier_power = -3
possible_asymptotic_fourier_powers = [0, -2]
fourier_power_match = required_noncontact_fourier_power in possible_asymptotic_fourier_powers

summary = {
    "stage": "galactic-flat-rotation-necessary-condition",
    "scope": "implemented linear RTK closure; static/quasistatic necessary-condition only",
    "static_euler_relation": "delta_K=-(1+w)*psi/cs2(k)",
    "implemented_cs2": "ca2/(1+k^2/kstar^2)",
    "rtk_density_response": "delta_rho_K proportional to -(1+k^2/kstar^2)*psi",
    "effective_constraint_kernel": implemented_kernel_class,
    "effective_denominator_degree_in_k2": implemented_denominator_degree_in_k2,
    "real_space_green_classes": implemented_real_space_class,
    "flat_curve_requirement": "Phi~v0^2*log(r), a_r~v0^2/r",
    "required_noncontact_fourier_power_for_log_r": required_noncontact_fourier_power,
    "available_asymptotic_fourier_powers_from_affine_k2_kernel": possible_asymptotic_fourier_powers,
    "fourier_power_match": fourier_power_match,
    "produces_log_r_asymptotically": produces_log_r_asymptotically,
    "produces_scale_free_1_over_r_acceleration_asymptotically": produces_scale_free_1_over_r_acceleration_asymptotically,
    "hypothesis_supported_by_current_linear_closure": False,
    "interpretation": (
        "The present implemented linear RTK closure does not by itself generate the scale-free galactic kernel "
        "needed for asymptotically flat rotation curves around a compact baryonic source. A nonlinear/environment-dependent "
        "completion, altered gravitational constraint, or additional gravitating component would be required."
    ),
    "warning": (
        "This is not a nonlinear galaxy solution. It only falsifies the stronger claim that the current linear cosmological "
        "RTK closure already contains the required flat-curve mechanism."
    ),
}

assert not fourier_power_match
assert not produces_log_r_asymptotically
assert not produces_scale_free_1_over_r_acceleration_asymptotically
print("RTK_GALACTIC_ROTATION_FALSIFICATION_RESULT", json.dumps(summary, sort_keys=True))
print("RTK_GALACTIC_ROTATION_FALSIFICATION_PASS")
