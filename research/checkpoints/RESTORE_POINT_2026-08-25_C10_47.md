# RTK / DBI-Khronon restore point — C10.42 through C10.47

Date: 2026-08-25
Branch: `rtk-class-build`
Pinned upstream nonlocal CLASS: `36cf283628c4a3330ec9fd3d84239bf775f77317`

## Purpose

This restore point records the exact legacy-RT constraint-provenance investigation that followed C10.27. It is intentionally separate from the physically decisive completed-U1 coupled cosmology program. Do not reinterpret any legacy model=2 diagnostic below as a no-go for the final U1 completion.

## 1. Exact translated literature RT 00 residual

Literature metric convention:

`ds^2 = -(1+2 Psi_lit) dt^2 + a^2(1+2 Phi_lit) dx^2`

Pinned CLASS Newtonian convention:

`ds^2 = a^2[-(1+2 psi_CLASS)deta^2 + (1-2 phi_CLASS)dx^2]`

Map:

- `Psi_lit = psi_CLASS`
- `Phi_lit = -phi_CLASS`
- with `x=ln a`, `d/dx=(1/Hc)d/deta`, `Hc=aH`
- `V_lit = H0 V_code/a`
- `Z_lit = H0^2 Z_code`
- `h dV_lit/dx = V_code_prime/a^2 - Hc V_code/a^2`
- `rho_CLASS=(8 pi G/3)rho_phys`

The exact translated auxiliary bracket is

`B00 = dU - dVprime/a^2 + Hc*dV/a^2 + 2*psi*Vbgprime/a^2 - 2*Hc*psi*Vbg/a^2 + psi_prime*Vbg/a^2`.

The tested combined residual is

`R00 = Ccom + 2*k^2*phi/(3*a^2) + gamma*H0^2*B00 + 2*Hc*A0i/a^2`,

where

`Ccom = delta_rho_CLASS + 3*Hc*(rho+p)*theta_CLASS/k^2`.

C10.42 classification:

`C10_RT_00_TRANSLATION_ALGEBRA_REPRODUCES_EXISTING_ROUNDTRIP_RESIDUAL`.

Consequence: simple cosmic/conformal-time, V/Z, H0, scale-factor, metric-sign and CLASS-density normalization mistakes do not explain the mismatch.

Authoritative result:
`research/theory_results/RTK_C10_RT_LITERATURE_TO_FORK_00_TRANSLATION_RESULT_v1.json`.

## 2. What the pinned model=2 actually evolves

For model=2 the fork computes `psi` algebraically and `phi_prime` from its implemented 0i equation. It evolves six auxiliary phase-space coordinates:

- `deltaU`, `deltaUprime`
- `deltaV`, `deltaVprime`
- `deltaZ`, `deltaZprime`

The Newtonian IC block inherited from the old fork sets all six auxiliary perturbation ICs explicitly to zero after the ordinary GR-style matter/metric IC construction.

The visible model=2 metric equations are

`psi = phi + 3*gamma*H0^2*dZ - (9/2)*(a^2/k^2)*(rho+p)*sigma`,

`phi_prime = -Hc*psi + (3/2)*(a^2/k^2)*(rho+p)*theta + (3/2)*gamma*H0^2*(Hc*dZ - dZprime/2 + Vbg*psi/2 - dV/2)`.

The model=2 auxiliary derivatives in `source/perturbations.c` provide a linear ODE system. This linearity is the basis of C10.46 and C10.47.

## 3. C10.44 — start-time / initial first-integral audit

Frozen start thresholds were the CLASS defaults and two earlier starts:

- default: `0.0015`, `0.07`
- earlier_x2: `0.00075`, `0.035`
- earlier_x4: `0.000375`, `0.0175`

for `start_small_k_at_tau_c_over_tau_h` and `start_large_k_at_tau_h_over_tau_k`.

Result classification:

`C10_LEGACY_RT_00_INITIAL_FIRST_INTEGRAL_PROPAGATION_INCONCLUSIVE`.

Important quantitative pattern:

- production RTK earliest x4/default median |R00| ratio: about `0.49888`
- untouched upstream earliest x4/default ratio: about `0.45206`
- at `a=0.1`: x4/default about `1.00005` (RTK) and `1.00003` (upstream)
- at `a=0.5`: about `1.0158` in both trees

Thus earlier starts change the earliest residual but do not remove the late offset. A simple frozen initial-offset explanation is insufficient.

Authoritative result:
`research/theory_results/RTK_C10_LEGACY_RT_00_INITIAL_FIRST_INTEGRAL_PROPAGATION_RESULT_v1.json`.

## 4. C10.45 — matched GR numerical-floor control

Pinned model=0 GR was run on the same k ladder and matched diagnostic precision.

At `a=0.1`:

- median `|R_GR| = 1.995327746295745e-12`
- RT reference `|R_RT| = 2.970639971523458e-10`
- GR/RT `= 0.0067168279071949085`

At `a=0.5`:

- median `|R_GR| = 2.3495624118984335e-14`
- RT reference `|R_RT| = 2.774630373672167e-10`
- GR/RT `= 8.468019503400863e-05`

Classification:

`C10_LATE_SMALL_K_COMOVING_RESIDUAL_RT_SPECIFIC_AGAINST_GR_CONTROL_SCOPED`.

Consequence: the late RT offset is not a generic CLASS cancellation/interpolation floor under the matched control.

Authoritative result:
`research/theory_results/RTK_C10_GR_COMOVING_CONSTRAINT_FLOOR_CONTROL_RESULT_v1.json`.

## 5. C10.46 — single-direction exact initial projection

A disposable homogeneous auxiliary basis solution was generated with

- `deltaU_ini=1`
- `deltaUprime_ini=deltaV_ini=deltaVprime_ini=deltaZ_ini=deltaZprime_ini=0`

while the baseline retained the historical all-zero auxiliary perturbation ICs.

For each Fourier mode, because the system is linear,

`DeltaR_seed(t) = R_seed(t) - R_base(t)`

and the initial projection coefficient was fixed uniquely by

`alpha(k) = -R_base(t0)/DeltaR_seed(t0)`.

Then, with no further correction,

`R_projected(t) = R_base(t) + alpha(k)*DeltaR_seed(t)`.

This `alpha(k)` is not a model parameter or likelihood fit. It is the coordinate of the initial state on the tested `R00=0` hyperplane.

The projection was well conditioned. Example production RTK at `k=2e-6 /Mpc`:

- `alpha=-0.41125756261849694`
- baseline earliest `R10=1.1304507324257091e-9`
- unit-seed response `DeltaR10=2.748765822634541e-9`
- projected primary earliest `R10=0`
- independent cubic projected earliest residual `=-6.352521137089351e-13`

But the residual regenerated dynamically. Frozen binding ratios

`median_abs(R_projected)/median_abs(R_baseline)`

for `[upstream a=0.1, upstream a=0.5, RTK a=0.1, RTK a=0.5]` are

`[0.9997033023595985, 0.9565803211370325, 0.9996982193388055, 0.956500320981752]`.

Classification:

`C10_LEGACY_RT_00_RESIDUAL_REGENERATED_BY_IMPLEMENTED_MODEL2_EVOLUTION_SCOPED`.

Interpretation: one exact initial R00 projection along the deltaU homogeneous direction does not remain on the translated-R00 surface. This is stronger than the start-time audit, but it is still a legacy model=2 implementation diagnostic.

Authoritative target/result:

- `research/theory_targets/RTK_C10_LEGACY_RT_00_CONSTRAINT_PROJECTION_PROPAGATION_TARGET_v1.json`
- `research/theory_results/RTK_C10_LEGACY_RT_00_CONSTRAINT_PROJECTION_PROPAGATION_RESULT_v1.json`

## 6. C10.47 — full auxiliary covector invariance test

C10.46 uses only one auxiliary homogeneous direction. To avoid overclaiming, C10.47 spans the entire local six-direction auxiliary IC tangent basis:

`dU, dUp, dV, dVp, dZ, dZp`.

For each direction j:

`DeltaR_j(t)=R(seed_j,t)-R(base,t)`.

Define the initial response covector `r0_j=DeltaR_j(t0)` and late response covector `rt_j=DeltaR_j(t)`.

If the `R00=0` hyperplane is invariant under the linear implemented flow on this auxiliary tangent space, then necessarily

`rt = c(t) r0`

for some scalar c(t). Equivalently all pairwise minors must vanish:

`W_ij(t)=rt_i*r0_j-rt_j*r0_i=0`.

The binding statistic is the independently seed-rescaling-invariant normalized minor

`w_ij = |W_ij|/(|rt_i*r0_j|+|rt_j*r0_i|+tiny)`.

The test uses active pairs only, with a preregistered denominator floor, and compares 10-row quartic and 6-row cubic psi-prime estimators independently.

Frozen target:
`research/theory_targets/RTK_C10_LEGACY_RT_00_AUXILIARY_COVECTOR_PROPAGATION_TARGET_v1.json`.

Workflow:
`.github/workflows/rtk-c10-legacy-rt-00-auxiliary-covector-propagation.yml`.

At creation of this restore point the C10.47 result may still be pending. Its eventual authoritative result path is:
`research/theory_results/RTK_C10_LEGACY_RT_00_AUXILIARY_COVECTOR_PROPAGATION_RESULT_v1.json`.

## 7. C10.41 direct-native implementation certificate

The frozen direct-native `psi` and `phi_prime/0i` identity workflow exists at
`.github/workflows/rtk-c10-direct-native-model2-metric-identity.yml`.

It was retriggered on 2026-08-25 without changing the scientific target. Missing result artifact must be treated as infrastructure/pending, never as a scientific FAIL.

Expected result path:
`research/theory_results/RTK_C10_DIRECT_NATIVE_MODEL2_METRIC_IDENTITY_RESULT_v1.json`.

## 8. Scope theorem that must not be forgotten

C10.39 remains binding for interpretation: historical RT/RTK stress histories are functionals of the historical metric evolution. A detached completed-U1 replay on frozen legacy histories is not the self-consistent completed theory.

Therefore even if C10.47 shows that the translated literature-R00 hyperplane is non-invariant under this pinned legacy model=2 implementation, the physically decisive completion gate remains an opt-in coupled matter/Khronon + completed-U1 metric reintegration. Do not convert a legacy provenance result into a completed-U1 no-go.

## 9. Recovery procedure in a new chat

1. Read this restore point.
2. Read `research/checkpoints/RTK_MASTER_CHECKLIST.md` and run/inspect the checklist sync workflow if it lags persisted result files.
3. Inspect C10.47 result path first. If present, follow its frozen classification and thresholds exactly.
4. Inspect C10.41 result path. If absent, treat it as pending infrastructure and inspect/retrigger only the frozen workflow; do not alter the target.
5. Preserve C10.27, C10.38, C10.44, C10.45 and C10.46 as separate historical/scoped results; never overwrite a negative result with a later interpretation.
6. After legacy model=2 provenance is sufficiently localized, return priority to the self-consistent completed-U1 coupled Boltzmann architecture rather than fitting translation coefficients or immutable legacy source histories.
