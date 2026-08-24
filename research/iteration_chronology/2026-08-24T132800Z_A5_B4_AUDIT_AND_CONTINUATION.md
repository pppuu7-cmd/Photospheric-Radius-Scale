# RTK continuation checkpoint — 2026-08-24 13:28 UTC

## A5 historical LCDM interpretation audit

The preregistered exact old-to-new LCDM line profile completed with classification
`A5_LCDM_LINE_PROFILE_HISTORICAL_LOCAL_INTERPRETATION_AUDIT_REQUIRED`.

Both endpoints replay with zero error. Starting at the historical accepted-score point `S_eff=1049.966118347761`, the line already descends at `t=0.01` to `1049.9530692041817`, an exact improvement `0.013049143579337397 > 0.005`. At `t=0.05` the improvement is `0.029499863074988752`.

Audit of `research/state/current.json` identified the semantics mismatch: the recorded historical LCDM Hessian center has `Ob=0.04865764689799632`, while the accepted-score point has `Ob=0.04858764689799632`, exactly one frozen base `Ob` step (`0.00007`) apart. The state already describes the accepted score as `best_exact_stencil_within_recenter_tolerance`.

Therefore the historical exact score replay remains valid, but the accepted-score point must no longer be described as Hessian-certified. The historical positive-definite Hessian belongs to the neighboring recorded Hessian center.

Canonical audit:
`research/robustness/A5_HISTORICAL_LCDM_STATIONARITY_SEMANTICS_AUDIT_2026-08-24.md`.

Audit state:
`research/state/A5_historical_LCDM_audit_current.json`.

The new LCDM seed remains independently confirmed at `1049.400976604194`. Its base non-PD mode has already passed exact frozen rays with maximum improvement `0.0`; the mandatory independent half-scale Hessian remains unchanged.

A deterministic Actions router was added on `main` and triggered to dispatch the already-frozen A5 scale-0.5 stationarity workflow. This was an infrastructure-only repair; no science target, center, tolerance or score was changed.

At this checkpoint `research/robustness/A5_LCDM_B9_SEED_HALF_RESULT_v1.json` is still absent. This is pending execution/observability, not a scientific failure.

## B4 later-lineage recovery

The previous `B4_current.json` pointed to target-v2 half-eigenmode recentering, but repository/Actions audit recovered a scientifically later v3->v4 lineage that must not be discarded.

Recovered v4 half-scale original run:

- run `32587822698`;
- job `97066790347`, successful;
- artifact `9481647704`;
- digest `sha256:7598fc71ec7c4c9b459d0eb4e213329227c7ebe4857add18f4c64245caca7505`;
- source commit `5675204a78e0c84b0e926871adf03f999265f567`;
- center `S_eff=1050.5511025943172`;
- best exact `1050.5510527797987`;
- improvement `4.9814518433777266e-05 < 0.005`;
- Hessian non-PD;
- minimum eigenvalue `-4.7214683209037513e-05`.

Its prerequisite v4 base and base-ray chain was also recovered:

- base run `32565150038`, improvement `7.20729706245038e-05`, non-PD, min eig `-6.643686349509472e-05`;
- base ray run `32578063680`, max exact improvement `0.00020957288847966993 < 0.005`, classification `B4_RECENTER_V4_BASE_EIGENMODE_RAYS_NO_DESCENT_GT_0P005`.

Durable recovery file:
`research/robustness/B4_NEUTRINO_RTK_RECENTER_V4_HALF_RECOVERED_RESULT_v1.json`.

`research/state/B4_current.json` was advanced to this recovered v4 frontier.

## B4 next frozen gate

Before any new ray score, the recovered v4 half negative eigenmode was frozen at
`research/robustness/B4_NEUTRINO_RTK_RECENTER_V4_HALF_EIGENMODE_RAYS_TARGET_v1.json`.

- eigenvalue `-4.7214683209037513e-05`;
- full seven-dimensional eigenvector retained;
- amplitudes `[-4,-2,-1,-0.5,+0.5,+1,+2,+4]`;
- no clipping;
- center replay tolerance `2e-6`;
- recenter threshold `0.005`.

Worker:
`rtk/b4_neutrino_recenter_v4_half_eigenmode_rays.py`.

Workflow:
`main:.github/workflows/rtk-b4-recenter-v4-half-eigenmode-rays.yml`.

The gate was launched from `main`. At this checkpoint the persisted result file does not yet exist; this is pending, not FAIL.

## Conditional B4 quarter gate frozen before ray scores

A v4 quarter-scale target was preregistered before observing the new half-ray result:
`research/robustness/B4_NEUTRINO_RTK_RECENTER_V4_QUARTER_STATIONARITY_TARGET_v1.json`.

It may execute only if the persisted half-ray classification is exactly
`B4_RECENTER_V4_HALF_EIGENMODE_RAYS_NO_DESCENT_GT_0P005`
and the maximum exact ray improvement is `<=0.005`.

Quarter steps are exactly one quarter of the v4 base steps. A dedicated conditional worker/workflow and workflow-run router were added. The router dispatches quarter scale only after a persisted scientific no-descent result; workflow green alone is insufficient.

## Immediate frontier

1. A5 new LCDM independent half-scale Hessian.
2. A5 final replacement paired fresh-tree replay only after half PASS.
3. B4 v4 half negative-eigenmode exact rays.
4. B4 v4 quarter-scale Hessian only if those rays are no-descent.
5. In parallel, continue B5 survey/nonlinear RSD adequacy without mixing its claims with A5/B4.

## Interpretation guard

No result in this checkpoint proves a global minimum or authorizes sigma/Wilks, AIC/BIC, posterior or Bayes claims. B4 absolute scores belong to a different minimal-neutrino objective and cannot be compared directly with massless A5 scores.
