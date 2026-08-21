# RTK B10 final preregistered lambda-tail identifiability result

Date: 2026-08-21
Status: **B10 CLOSED under protocol v1**
Classification: `LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`

## Scope

This result answers only the preregistered B10 question on the frozen local dense objective: after profiling the six non-lambda cosmological parameters, is the finite RTK `lambda_D` solution numerically separated from the preregistered large-lambda dust-like tail at the raw-objective resolution convention `0.005`?

It is not a confidence interval, posterior statement, Bayes factor, significance result, proof of global optimality, or proof that `lambda_D` is mathematically redundant.

Canonical protocol: `rtk-class-build:research/robustness/B10_LAMBDA_TAIL_IDENTIFIABILITY_PROTOCOL_v1.md`.
Frozen pre-interpretation memo: `research/robustness/RTK_B10_HALF_SCALE_DECISION_MEMO_2026-08-21.md`.

## Frozen finite reference

`S_finite = 1050.249912429787`.

## Tail anchors and T3 base certification

Base-stencil source run: `32252288173`.

### Factor 64

- `lambda_D = 14045284.653674118`
- `S_tail,64 = 1050.249062546245`
- exact base-stencil improvement: `0.0`
- base Hessian: positive definite
- base eigenvalues:
  - `0.04667495962`
  - `0.08851486`
  - `0.12516730`
  - `0.30092733`
  - `3.13822775`
  - `7.39300329`

### Factor 16384

- `lambda_D = 3595592871.3405743`
- `S_tail,16384 = 1050.2490169939647`
- exact base-stencil improvement: `0.0`
- base Hessian: positive definite
- base eigenvalues:
  - `0.04670707814`
  - `0.08852800`
  - `0.12535199`
  - `0.30088074`
  - `3.13831437`
  - `7.39311551`

## Independent half-scale validation

Workflow run: `32482153752`.
Head SHA: `6dfd19e0a70fcd7d853a9454cc9de6147e3d7322`.

### Factor 64 half-scale

Artifact:

- id `9450288661`
- name `rtk-b10-t3-half-stationarity-f64`
- digest `sha256:f7f2d67b4770ab611e77f523b2ac2715f1b0c58c1aec685e9f745b454f520ef5`

Results:

- stencil scale `0.5`
- center replay `1050.249062546245`, exact match to frozen anchor
- best exact score `1050.249062546245`
- exact improvement `0.0`
- Hessian positive definite
- half-scale eigenvalues:
  - `0.02212379149449256`
  - `0.04889094765131189`
  - `0.08490211199460815`
  - `0.11765997434982825`
  - `0.8140506519916093`
  - `1.8756053901397773`

Absolute base↔half corresponding-eigenvector overlaps are approximately:

`[0.9149, 0.9039, 0.9809, 0.9719, 0.9992, 0.9998]`.

### Factor 16384 half-scale

Artifact:

- id `9450372881`
- name `rtk-b10-t3-half-stationarity-f16384`
- digest `sha256:1f5e57fc7b60d9d6f87535561b1c45403632933ca674e189a5be6ee220517d08`

Results:

- stencil scale `0.5`
- center replay `1050.2490169939647`, exact match to frozen anchor
- best exact score `1050.2490169939647`
- exact improvement `0.0`
- Hessian positive definite
- half-scale eigenvalues:
  - `0.02218809597516494`
  - `0.048961810498290737`
  - `0.08492486532682854`
  - `0.11763520918114409`
  - `0.81407236073415`
  - `1.8756223119237942`

Absolute base↔half corresponding-eigenvector overlaps are approximately:

`[0.9141, 0.9030, 0.9808, 0.9718, 0.9992, 0.9998]`.

## Stationarity decision

Both anchors satisfy the frozen validation rule:

1. center replay agrees with the frozen anchor;
2. no exact half-scale point improves the center by more than `0.005` — in fact the exact improvement is zero at both anchors;
3. the half-scale Hessian remains positive definite;
4. the eigenmode structure remains qualitatively aligned with the base stencil;
5. runtime/provenance locks passed and both workflow jobs completed successfully.

Therefore both preregistered tail anchors are stationarity-certified for the B10 finite-versus-tail classification.

## Final finite-versus-tail comparison

Define

`Delta_tail = S_tail - S_finite`.

Factor 64:

`Delta_tail,64 = -0.0008498835418322415`.

Factor 16384:

`Delta_tail,16384 = -0.0008954358222581504`.

The best stationarity-certified preregistered tail score is factor 16384, and

`|Delta_tail,best| = 0.0008954358222581504 < 0.005`.

The tail score is slightly lower numerically, but not by enough to enter the protocol branch `S_tail < S_finite - 0.005`.

Hence, mechanically applying the preregistered classification rule:

`LAMBDA_NOT_NUMERICALLY_IDENTIFIABLE_AGAINST_PREREGISTERED_DUST_TAIL_AT_0P005`.

## Interpretation

Within this frozen local/profile/tail protocol, the finite `lambda_D` solution is not numerically separated from the tested large-lambda dust-like tail at the `0.005` raw-objective resolution convention.

This does not show that the tail is globally preferred. It also does not imply a statistical confidence interval on `lambda_D`; the `0.005` threshold is a preregistered numerical-identifiability convention, not a Wilks/sigma threshold.

B10 protocol v1 is therefore closed.
