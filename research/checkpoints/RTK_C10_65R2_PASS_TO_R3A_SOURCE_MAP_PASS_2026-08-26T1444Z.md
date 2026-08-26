# RTK checkpoint — C10.65r2 PASS → C10.65r3a source-map PASS

UTC timestamp: 2026-08-26T14:44Z
Branch: `rtk-class-build`
Pinned CLASS upstream: `36cf283628c4a3330ec9fd3d84239bf775f77317`

## Closed in this iteration

### C10.65r2g — PASS_SCOPED
The dormant r2 first-RHS observer was isolated into a separately compiled `noinline,noclone` translation unit. This restored exact OFF-path numeric-text identity against the r1 control while preserving ON-path scientific parity. The key engineering conclusion is that the earlier OFF-path mismatch was code-generation/layout contamination, not a failure of the first-RHS equations.

### C10.65r2 — PASS_SCOPED
The original frozen 9×4 diagnostic first-RHS gate was rerun with the isolated r2g implementation after fixing only an input-generation bug (duplicate `c10_65r1_lambda_HL`/`c10_65r1_Mc` entries). No frozen threshold was changed.

Persisted result: `research/theory_results/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_RESULT_v1.json`.

Global checks:
- 9 completion points × 4 low-k onset anchors = 36 records.
- exact onset: PASS.
- all four anchors TCA-on: PASS.
- all outputs finite: PASS.
- exact dormant OFF-path SHA identity for all four k: PASS.
- max r1 projector regression relative = 0.
- max C vs independent local RHS relative = `2.0625432202795618e-10` ≤ frozen `5e-9`.
- max C vs detached parent RHS relative = `2.0625432202795618e-10` ≤ frozen `1e-6`.
- max B-prime actual-slip invariance relative = 0.
- max weighted photon-baryon slip cancellation normalized residual = `2.134955834845e-16` ≤ frozen `5e-13`.
- no `dy` write by r2 diagnostic: PASS.
- no production metric/RHS write by r2 diagnostic: PASS.

Interpretation remains strictly scoped: a completed-U1 first local RHS can be evaluated inside pinned CLASS at the conditional onset and agrees with independent/detached parents while remaining inert with respect to the actual integrator. This is not a state handoff and not time integration.

## Next frontier preflight

### C10.65r3a — PASS_SCOPED
Frozen target: `research/theory_targets/RTK_C10_65R3A_STATE_HANDOFF_SOURCE_MAP_TARGET_v1.json`.
Result: `research/theory_results/RTK_C10_65R3A_STATE_HANDOFF_SOURCE_MAP_RESULT_v1.json`.
Action run: `32982045014`.

The pinned implementation source map is now certified before any production write is added:
- Khronon state reuses `index_pt_delta_cdm` and `index_pt_theta_cdm`.
- stress tensor reads those same two slots.
- derivative callback writes those same two slots.
- Newtonian metric mapping is `phi_prime = -metric_continuity/3` and `psi = metric_euler/k2`.
- the integrator derivative callback owns `dy`.
- the integrator advances `y` in place.
- accepted-step output occurs after the RK generic-integrator call.
- no C10.65r3 production write exists yet.

## Next scientifically permitted step

Freeze C10.65r3b before implementation. It must be an opt-in, rollback-capable onset handoff experiment on a disposable state copy. The step prescription must be derived from the pinned integrator/timescale semantics and frozen before numerical execution. Required evidence must include exact OFF-path identity, explicit before/after state vectors, completed-U1 constraint residuals, and rollback identity. Do not expand to the full k grid or spectra before this short-step gate passes.

## Open physical gates / non-claims

- C9 radiative naturalness remains open.
- same-full-action primordial/background closure remains open.
- no microscopic derivation of the historical matching vector is claimed.
- no unique primordial growing mode is proven.
- massive-neutrino completion remains open.
- C10.65r2/r3a do not constitute spectra or likelihood evidence.
