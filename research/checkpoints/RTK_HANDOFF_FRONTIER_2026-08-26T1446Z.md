# RTK handoff frontier — 2026-08-26T14:46Z

Authoritative repo/branch: `pppuu7-cmd/Photospheric-Radius-Scale` / `rtk-class-build`.
Pinned CLASS upstream SHA: `36cf283628c4a3330ec9fd3d84239bf775f77317`.

## Closed parent

`C10.65r2` is closed scoped on the full 3x3 completion grid x four exact low-k onset anchors. OFF path is numeric-text SHA identical; worst independent/detached RHS relative discrepancy is `2.0625432202795618e-10`; weighted photon+baryon cancellation residual is `2.134955834845e-16`; no production dy/metric write is present.

## Handoff ownership preflights

### C10.65r3a — PASS scoped

Persisted result: `research/theory_results/RTK_C10_65R3A_STATE_HANDOFF_SOURCE_MAP_RESULT_v1.json`.

Certified facts:
- model=2 Newtonian Khronon evolution reuses the genuine integrated CLASS slots `index_pt_delta_cdm` and `index_pt_theta_cdm`;
- stress tensor reads those same slots;
- derivative callback owns `dy`, while the generic integrator advances `y` in place;
- metric mappings are algebraic (`phi_prime=-metric_continuity/3`, `psi=metric_euler/k^2`);
- no r3 production state write existed at this preflight.

### C10.65s0 — PASS scoped, supplemental architecture certification

Persisted result: `research/theory_results/RTK_C10_65S0_INTEGRATION_SAFE_HANDOFF_ARCHITECTURE_RESULT_v1.json`.

Certified facts:
- `perturb_solve()` integrates piecewise intervals of uniform approximation state;
- each interval calls `perturb_vector_init()` before `generic_evolver`;
- metric constraint quantities are not independent integrated state;
- an arbitrary exact `a_on` cannot be implemented as an ordinary RHS side effect;
- the safe architecture is: convert exact persisted `a_on` to deterministic `tau_on`, split the containing approximation interval without changing approximation flags/criteria, call normal `perturb_vector_init`, then perform a single opt-in write to the two genuine integrated carrier slots before the post-handoff evolver starts.

The `s0` label is not a competing research branch. It is an architecture supplement to the already-established `r3` handoff line. Continue canonical numbering with `r3b`.

## Frozen next gate: C10.65r3b

Target: `research/theory_targets/RTK_C10_65R3B_EXACT_ONSET_INTERVAL_SPLIT_HANDOFF_CANARY_TARGET_v1.json`.

Domain: first persisted completion point x `k={1e-5,3e-5,1e-4,3e-4} Mpc^-1`, exact `a_on=0.0002203229136467`.

Required architecture:
1. opt-in flag default OFF;
2. exact OFF rollback SHA identity;
3. deterministic `tau_on` derived from the pinned background;
4. explicit interval split at `tau_on`, with unchanged approximation flags on both sides;
5. handoff only after `perturb_vector_init` and before `generic_evolver`;
6. write only `delta_cdm/theta_cdm` integrated carrier state;
7. no metric/shift/TCA/collision/approximation mutation and no state write inside RHS callbacks;
8. first post-handoff RHS parity against unchanged C10.65r2 thresholds;
9. frozen short-step fraction `1e-4` of local `perturb_timescale`, all-finite state, max fractional state change `0.05`, and completed-U1 residual growth-factor canary `<=10`;
10. no spectra or likelihood claim.

Historical matching-vector values remain phenomenological control only. A pass of r3b will be only a local handoff/short-step canary, not primordial derivation or long-time stability.

## Global open lines unchanged

C9 radiative naturalness; same-full-action background/primordial/gravity normalization; massive-neutrino completion; B9 stationarity/Hessian + paired LCDM; broader C7 PPN/positivity/matter-coupling completion; microscopic UV/pre-EFT derivation of the matching vector.
