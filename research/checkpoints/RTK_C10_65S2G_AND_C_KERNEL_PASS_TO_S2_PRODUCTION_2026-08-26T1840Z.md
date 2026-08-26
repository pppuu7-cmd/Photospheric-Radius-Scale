# RTK C10.65s2 detached production-kernel checkpoint

UTC checkpoint: 2026-08-26T18:40Z
Branch: `rtk-class-build`
Scope: RTK only; do not mix with DSIR.

## Frozen production target

`research/theory_targets/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_TARGET_v1.json` remains `FROZEN_BEFORE_IMPLEMENTATION` with the inherited first-production-RHS relative tolerance `5e-9`, exact dormant OFF rollback, one completion point x four exact low-k anchors, and exactly one accepted post-handoff step per anchor.

## Historical s2e failure preserved

`C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_FAIL_SCOPED` is not relabelled.  Its originally frozen `|implicit denominator| > 0.9` guard failed because the exact scalar feedback denominator is about `0.69574`.  C10.65s2f independently proved that this is the expected enthalpy-fraction DAE coupling and that the scalar implicit solve is well-conditioned under its separately pre-frozen criterion:

- min |denominator| = 0.6957396985465041
- max scalar amplification = 1.437319161302909

## C10.65s2g

`C10_65S2G_PRODUCTION_KERNEL_PREFLIGHT_PASS_SCOPED` remains valid and preserves the failed s2e parent classification.

On the frozen one-point x four-anchor domain:

- max Khronon Newtonian density-RHS disagreement vs s2b = 1.039080201200683e-12
- max Khronon Newtonian velocity-RHS disagreement vs s2b = 1.3562898777804596e-12
- max inherited non-conditioning s2e parity quantity = 1.106601882510684e-9 < 5e-9
- all required runtime stage quantities are function arguments
- no onset literals, history/file reads, matching seed constants, or production patch are consumed by the detached dynamic kernel.

## Standalone C current-state kernel parity

The first C-kernel parity Action (`33000387362`) failed before any parity residual was evaluated because the analyzer incorrectly looked for `psi_pref` inside the s2e record schema.  This was an analyzer schema-routing bug only.

The analyzer was fixed without changing formulas or thresholds: each C output is now compared to the gate that originally certified it:

- s2c for B, psi_pref, psi_pref_prime, phi_pref, Psi_N
- s2d for Phi_N, sigma_g, feedback denominator
- s2e for B_prime, Psi_N_prime, TCA slip and the first ordinary/Khronon RHS values.

GitHub Actions run `33000737462` then passed and persisted:

`C10_65S2_C_KERNEL_PARITY_PASS_SCOPED`

Results over all 36 onset states:

- compile and all C return codes: PASS
- record count 36: PASS
- all outputs finite: PASS
- max physical relative disagreement = 1.8226998336680743e-9 < frozen 5e-9
- max implicit relative disagreement = 2.748370320251458e-12 < 5e-11
- inherited conditioning: PASS

Important component maxima:

- B = 0
- psi_pref = 0
- psi_pref_prime = 0
- phi_pref = 0
- Psi_N = 0
- Phi_N = 0
- sigma_g = 0
- B_prime = 1.2012191872349758e-12
- Psi_N_prime = 7.348776990898599e-13
- metric_continuity = 7.348776990898599e-13
- metric_euler = 0
- delta_khr_N_prime = 7.348819480345878e-13
- theta_khr_N_prime = 9.539075698220527e-13
- TCA slip = 1.8226998336680743e-9 (largest physical parity error, still inside frozen 5e-9)
- weighted photon-baryon slip cancellation = 0

Provenance for the passing run is persisted in `research/theory_results/RTK_C10_65S2_C_KERNEL_PARITY_AUDIT_RESULT_v1.json`, run id `33000737462`, with `threshold_changed=false`.

## Exact frontier

All detached/current-state prerequisites needed before mutation are now available:

- C10.65r2: PASS_SCOPED
- C10.65s0: PASS_SCOPED
- C10.65s1: PASS_SCOPED
- C10.65s2a: PASS_SCOPED
- C10.65s2b: PASS_SCOPED
- C10.65s2c: PASS_SCOPED
- C10.65s2d: PASS_SCOPED
- C10.65s2e: FAIL_SCOPED (historical frozen conditioning guard; preserved)
- C10.65s2f: PASS_SCOPED (separate conditioning audit)
- C10.65s2g: PASS_SCOPED
- standalone C current-state kernel parity: PASS_SCOPED

The next allowed scientific step is therefore the already-frozen **C10.65s2 direct-onset one-accepted-step production canary** in disposable pinned CLASS.

Implementation restrictions remain exactly those frozen by s2:

1. default `c10_65s2_canary=0` must preserve exact OFF numeric-text SHA identity;
2. ordinary photon/baryon/UR/metric initialization remains owned by `perturb_initial_conditions` / `perturb_vector_init`;
3. only `index_pt_delta_cdm` and `index_pt_theta_cdm` may receive the explicit post-vector Khronon handoff writes;
4. legacy dU/dV/dZ auxiliaries are not completed-U1 physical state;
5. no adaptive RHS callback may mutate integrated state except normal `dy` evaluation;
6. current-state metric/RHS coefficients must be sourced at each production RHS stage rather than frozen at onset;
7. capture first production RHS before the step and compare to the certified chain with the unchanged 5e-9 threshold;
8. execute exactly one accepted post-handoff step for each of the four anchors;
9. capture before/after state plus raw and normalized preferred A/H/momentum residuals;
10. constraint drift in s2 is measurement-only; do not set a post-hoc stability threshold from the same run.

Fundamental non-claims remain unchanged: this does not close radiative naturalness, same-full-action primordial/background closure, microscopic UV matching, massive-neutrino completion, finite-time stability, spectra or likelihood evidence.
