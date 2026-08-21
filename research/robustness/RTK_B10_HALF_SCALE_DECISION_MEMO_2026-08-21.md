# RTK B10 half-scale decision memo

Date: 2026-08-21
Status: **decision logic frozen before half-scale artifact interpretation**

## Purpose

This memo prevents post-result reinterpretation of the B10 lambda-tail identifiability gate. It does not declare the half-scale run successful and does not close B10 by itself.

Canonical preregistered protocol: `research/robustness/B10_LAMBDA_TAIL_IDENTIFIABILITY_PROTOCOL_v1.md` on `rtk-class-build`.

## Frozen finite point

Frozen finite-lambda local RTK score:

`S_finite = 1050.249912429787`.

This is the accepted local massless dense-objective RTK score. B10 asks whether the profiled large-lambda dust-like tail is numerically distinguishable from it on the same frozen objective.

## T2 profile-artifact audit

The T3 anchors come from the preregistered paired 6D fixed-lambda profiling run `32244330691`, not directly from the fixed-shared T1 reconnaissance.

### Factor 64

Source artifact id: `9364651941`.

- fixed lambda: `14045284.653674118`;
- exact shared-parameter start score: `1050.249062546245`;
- Powell endpoint objective: `1050.252766957277`;
- optimizer success: `true`;
- normalized endpoint coordinates: approximately `[-0.001268, +0.001078, +0.000446, +0.002111, +0.001460, +0.008128]`;
- retained best exact score: `1050.249062546245`;
- `profile_improvement = 0.0`.

The optimizer endpoint is interior and worse than the exact start. The pipeline therefore correctly retained the exact start as the best profiled point.

### Factor 16384

Source artifact id: `9363646458`.

- fixed lambda: `3595592871.3405743`;
- exact shared-parameter start score: `1050.2490169939647`;
- Powell endpoint objective: `1050.2529335888485`;
- optimizer success: `true`;
- normalized endpoint coordinates: approximately `[-0.001264, +0.001076, +0.000444, +0.002109, +0.001456, +0.008127]`;
- retained best exact score: `1050.2490169939647`;
- `profile_improvement = 0.0`.

Again, the optimizer endpoint is interior and worse than the exact start.

### Interpretation of `profile_improvement=0`

This value does **not** mean that T2 skipped nuisance-parameter profiling. Forty-nine exact requests were made for each tail anchor and Powell terminated successfully. It means the profiling search did not find a shared-parameter displacement with a lower exact objective than the frozen shared RTK start.

The B10 tail similarity is therefore not a boundary-hit artifact of the T2 optimizer. T3 stationarity certification is still mandatory because a successful optimizer endpoint or retained exact start is not by itself a local-minimum proof.

## Already completed T3 base-stencil anchors

Factor 64:

- `lambda_D = 14045284.653674118`;
- `S_tail,64 = 1050.249062546245`;
- exact base-stencil improvement = 0;
- Hessian positive definite;
- minimum eigenvalue approximately `0.046675`.

Factor 16384:

- `lambda_D = 3595592871.3405743`;
- `S_tail,16384 = 1050.2490169939647`;
- exact base-stencil improvement = 0;
- Hessian positive definite;
- minimum eigenvalue approximately `0.046707`.

## Frozen finite-versus-tail differences

Using `Delta_tail = S_tail - S_finite`:

- factor 64: `Delta_tail = -0.0008498835418322415`;
- factor 16384: `Delta_tail = -0.0008954358222581504`.

Both absolute differences are far below the preregistered B10 numerical-identifiability tolerance

`0.005`.

The slightly lower tail score is not large enough to trigger the protocol branch `S_tail < S_finite - 0.005`.

## Mechanical decision after half-scale validation

The half-scale run is not an optional extra. It is the local stationarity confirmation required before the tail anchors may be used in the final B10 statement.

For each anchor, require:

1. center replay agrees with the frozen T2/base target within the workflow tolerance;
2. no exact half-scale stencil point improves the center by more than `0.005`;
3. the half-scale Hessian remains positive definite and qualitatively consistent with the base stencil;
4. no runtime/provenance lock fails.

Then apply the following decision without changing thresholds:

### Case A — both tail anchors pass half-scale stationarity

The best stationarity-certified preregistered tail score differs from the finite score by much less than `0.005`. Therefore the protocol classification is

`LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`.

This means only that, after profiling the six other cosmological parameters and within the frozen local/tail protocol, the finite lambda solution is not numerically separated from the preregistered large-lambda tail at the `0.005` raw-objective resolution convention.

It is not a confidence interval, posterior statement, Bayes factor, global-minimum theorem, or proof that lambda is mathematically redundant.

### Case B — either half-scale anchor finds improvement > 0.005

Do not use that anchor for the final finite-versus-tail statement. B10 remains open and the improved point becomes a mandatory recenter target under a new frozen local-stationarity step.

### Case C — Hessian becomes indefinite without a >0.005 coordinate improvement

B10 remains open. Run exact rays along the negative/near-zero eigenmodes before any identifiability claim.

### Case D — provenance/runtime/replay mismatch

Classify as infrastructure/protocol failure only; make no scientific B10 inference.

## Scope

This memo freezes interpretation only. It does not assert that the currently running or recently launched half-scale jobs have passed. Their artifacts must be inspected before changing B10 status in `research/RESEARCH_LEDGER.md`.
