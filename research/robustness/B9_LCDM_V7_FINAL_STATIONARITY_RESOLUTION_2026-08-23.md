# B9 LCDM v7 final local-stationarity resolution — 2026-08-23

Status: **GREEN under the frozen B9 v7 local-stationarity protocol**.

This memo closes the preregistered B9 LCDM v7 local stationarity chain. It does not claim a global minimum, posterior preference, significance, AIC/BIC result, or Bayes evidence.

## Frozen center

- h = 0.6803133881531521
- Ob = 0.048406958808714234
- Om = 0.25869220161756795
- As = 2.099031119902081e-09
- ns = 0.9662859140870312
- zre = 7.684806125603674
- lam = 0.0

Objective: `matched-ultra-linstep2+dense-BOSS+PlanckR3-lensing-v1`.
Production mapping: `eff`.
Frozen numerical tolerance for exact descent: `0.005`.

## Why a half-scale audit was required

The v7 base replay had exact improvement zero but a soft negative Hessian eigenvalue, so the frozen decision tree did not permit an immediate minimum claim. Exact eigenmode rays were then tested on the unchanged v7 center and found no descent larger than `0.005`; the best ray was worse than the center. The preregistered response was therefore an independent half-scale Hessian on the same center, not a v8 recenter.

## Half-scale result

GitHub Actions run: `32657629806`.
Job: `97238783899`.
Artifact:
- id `9499099343`
- name `rtk-b9-lcdm-recenter-v7-half-scale-stationarity`
- digest `sha256:0b4fd505094e4d0884f9b2ddeea93f1f0efe2cb70baf2901c63d4544bdcaa9e9`

Exact results:

- stencil scale = `0.5`
- center replay absolute error = `0.0`
- `S_center = 1058.2173424114785`
- `best_exact_S = 1058.2173424114785`
- exact best improvement = `0.0`
- best label = `center`
- Hessian positive definite = `true`
- eigenvalues in scaled coordinates:
  - `0.0005663251859819669`
  - `0.005060400282264203`
  - `0.020337739329173366`
  - `0.05812909855191392`
  - `0.7767230890379992`
  - `1.7939571590117493`

The k01 companion mapping is also positive definite, with minimum eigenvalue `0.0005703516304846819` and zero exact improvement at the same center.

Workflow classification:

`B9_LCDM_V7_HALF_SCALE_STATIONARITY_RESOLUTION_PASS`

## Decision

The frozen B9 v7 decision rule is satisfied:

1. center unchanged from the frozen v7 target;
2. exact replay error is zero;
3. no half-scale exact point improves the center by more than `0.005` (actual improvement zero);
4. half-scale Hessian is positive definite;
5. prior exact eigenmode-ray audit found no descent above threshold;
6. runtime, CLASS, Pantheon and Planck R3 provenance locks passed.

Therefore the previously soft negative base-stencil mode is resolved as a stencil-scale instability rather than a reproducible descent direction under the frozen protocol.

## Scientific scope

This closes **local numerical stationarity of the B9 LCDM v7 reference under the frozen objective and tested scales**.

It does not establish:

- global optimality;
- a likelihood-ratio significance between LCDM and RTK;
- posterior/Bayesian evidence;
- validity of the later projectable U(1) completion in CLASS;
- equality of the phenomenological B9 `lam` parameter and `lambda_HL` (they are distinct).

The next numerical architecture task is not another B9 v7 recenter. It is to introduce `lambda_HL` and the completed matter-filter architecture explicitly into a same-action cosmological implementation before interpreting projectable-U(1) observational viability.
