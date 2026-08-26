# RTK C10.65s1 PASS -> C10.65s2a source-lock PASS checkpoint

UTC: 2026-08-26T17:30Z  
Branch: `rtk-class-build`

## Recovered frontier

C10.65s1 is already closed as `C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_PASS_SCOPED` from GitHub Actions. The frozen next production canary is `research/theory_targets/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_TARGET_v1.json`.

The current s2 contract is explicit that ordinary photon/baryon/UR/metric scalar coordinates must enter only through CLASS initialization ownership (`perturb_initial_conditions` / `perturb_vector_init`). After vector initialization the only certified carrier writes are the Khronon/CDM slots `delta_cdm` and `theta_cdm`. Legacy model=2 `dU/dV/dZ` perturbation auxiliaries are forbidden as completed-U1 boundary data.

## C10.65s2a frozen and executed

Target: `research/theory_targets/RTK_C10_65S2A_PRODUCTION_CANARY_SOURCE_LOCK_PREFLIGHT_TARGET_v1.json`  
Analyzer: `research/shadow/rtk_c10_65s2a_production_canary_source_lock_preflight.py`  
Workflow: `.github/workflows/rtk-c10-65s2a-production-canary-source-lock-preflight.yml`  
GitHub Actions run: `32994439241`  
Pinned CLASS upstream: `36cf283628c4a3330ec9fd3d84239bf775f77317`

Classification: `C10_65S2A_PRODUCTION_CANARY_SOURCE_LOCK_PREFLIGHT_PASS_SCOPED`.

All frozen preflight checks passed: parent classifications, frozen s2 status, exact one-point x four-anchor domain alignment, exact `a_on`, finite completed state, finite certified first RHS, legacy nlde exclusion, required pinned source anchors, and absence of any s2 production patch during the preflight.

The strongest numerical cross-check in the handoff manifest reconstructs completed `Phi_N` independently from the certified r2 production metric Euler source, `Phi_N = metric_euler/k^2`, and compares it to the s1 completed-state constraint value. Maximum relative discrepancy over the four anchors is `4.4377881598529706e-13`, versus the pre-frozen `5e-9` bound.

The Action persisted `research/theory_results/RTK_C10_65S2A_PRODUCTION_CANARY_SOURCE_LOCK_PREFLIGHT_RESULT_v1.json` with `threshold_changed=false` and immutable run provenance. Result commit at the time of this checkpoint: `00f76817d436e42673458dd05d4b8fcbd368afd8`.

## Interpretation

This is a scoped implementation/source-lock PASS only. It does not write completed-U1 quantities into the production metric or RHS, does not mutate the integrated state, and does not execute an accepted integrator step. Therefore C10.65s2 remains OPEN.

## Exact next frontier

Implement the already frozen C10.65s2 canary on the single frozen completion point x four exact low-k anchors:

1. opt-in direct start at certified `a_on` using the source-locked initialization path;
2. initialize ordinary photon/baryon/UR/metric state through `perturb_initial_conditions` / `perturb_vector_init` only;
3. exclude legacy model=2 nlde `dU/dV/dZ` coordinates from completed-U1 physical state/feedback;
4. preserve only the two certified Khronon carrier slots after vector initialization;
5. route completed metric/projector and first RHS into the actual production derivative path;
6. require first production RHS parity against C10.65r2 at the inherited frozen `5e-9` relative threshold;
7. preserve exact OFF numeric-text SHA identity on all four anchors;
8. capture state and preferred A/Hamiltonian/momentum residuals before and after exactly one accepted post-handoff integrator step per anchor;
9. require finiteness only for s2 constraint-drift diagnostics; do not derive a post-hoc stability tolerance from the same run.

Only after s2 PASS may a separate finite-short-interval stability target be frozen.

## Physical gates intentionally unchanged

C9 radiative naturalness remains open. Same-full-action primordial/background closure remains open. Massive-neutrino completion, broader C7/B9 and spectra/likelihood interpretation remain outside the claim of s2a. No DSIR material was used or written.
