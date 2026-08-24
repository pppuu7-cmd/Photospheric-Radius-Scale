# B9 Planck-lensing live recovery methodology

Status: **CANONICAL B9 CONTINUATION DOCUMENT**  
Updated: `2026-08-24T08:01:00Z`  
Live machine-readable B9 state: `research/state/B9_current.json`  
Global autonomous state remains: `research/state/current.json`

## 1. Purpose

This document is the shortest safe path for continuing B9 after total chat loss. It records the frozen objective, formulas, certified subgates, current centers, exact decision rules, and the single next gate. Historical chat statements must not override the frozen files cited below.

B9 tests robustness of the already-frozen matched cosmology to adding the standalone Planck 2018/R3 lensing likelihood. It is a robustness branch and does not mutate the A1-A5 baseline objective.

## 2. Frozen objective and score

Baseline matched score:

`S_A5(theta) = matched-ultra-linstep2+dense-BOSS`.

B9 adds exactly the preregistered standalone Planck R3 lensing likelihood:

`S_B9(theta) = S_A5(theta) - 2 ln L_lensing(theta)`.

This is implemented point-by-point in `rtk/b9_rtk_stationarity_hessian.py`: the production dense score is evaluated first, the lensed CLASS spectra are mapped into the frozen Planck lensing vector, and then `S_B9_eff = S_base_eff - 2*logL_lensing`.

For a paired local comparison after both model centers are independently certified:

`Delta S_B9 = S_B9(RTK) - S_B9(LCDM)`.

A positive value means the RTK local center has the larger raw objective on this frozen likelihood. It is **not** automatically a significance, sigma value, AIC/BIC result, posterior preference, or Bayes factor.

Frozen protocol: `research/robustness/B9_PAIRED_REOPTIMIZATION_TARGET_v1.json`.

## 3. Parameterization used by the RTK stationarity stencil

The RTK Hessian uses dimensionless local coordinates `y_i` around the frozen center.

For ordinary parameters `p_i`:

`p_i(y_i) = p_i,0 + y_i * delta_i`.

For the strictly positive RTK scale parameter:

`lambda_D(y_lambda) = lambda_D,0 * exp(y_lambda * delta_loglambda)`.

Thus the Hessian is tested in a controlled normalized geometry rather than by mixing raw dimensional parameter scales.

The production RTK axes are:

`[log(lambda_D), h, Omega_b, Omega_m, A_s, n_s, z_re]`.

## 4. Exact finite-difference quantities

At normalized center `y=0`, with unit stencil displacement along each normalized axis, the worker computes

`g_i ~= [S(+e_i) - S(-e_i)] / 2`,

`H_ii ~= S(+e_i) - 2 S(0) + S(-e_i)`,

and for `i != j`,

`H_ij ~= [S(+e_i+e_j) - S(+e_i-e_j) - S(-e_i+e_j) + S(-e_i-e_j)] / 4`.

These are Hessian entries in normalized `y` coordinates. The script also computes a pseudoinverse Newton proposal, evaluates that point exactly, and only then selects the best objective from **all exact points** evaluated for both mappings.

Define

`I_exact = S_center - min_exact S`.

The frozen recenter/descent tolerance is

`I_exact <= 0.005`.

A local B9 stencil is accepted only if this exact-improvement gate is satisfied and every Hessian eigenvalue is above the frozen positive-definite threshold. Workflow success alone is not a scientific pass.

## 5. Multiscale and fresh-tree logic

The preregistered stationarity chain is:

1. exact base stencil at scale `1.0`;
2. exact independent half-scale stencil at scale `0.5` at the **same center**;
3. if both are recenter-clear and positive definite, run an independent fresh-tree base-scale audit;
4. fresh-tree audit must rebuild the pinned CLASS tree, restore the frozen RTK modifications, use the pinned Pantheon commit, reinstall the locked likelihood stack, freshly download Planck R3 and verify its SHA256;
5. only after the fresh-tree score reproduces the frozen center within `2e-6`, exact improvement is `<=0.005`, and the Hessian is positive definite may the RTK B9 local-stationarity gate be certified.

If any condition fails, do not average runs, loosen thresholds, or silently recenter. Preserve the failed condition as a distinct reproducibility/stationarity result and diagnose it under a new preregistered gate.

## 6. LCDM B9 status — closed local stationarity subgate

Frozen LCDM v7 center:

- `h = 0.6803133881531521`
- `Omega_b = 0.048406958808714234`
- `Omega_m = 0.25869220161756795`
- `A_s = 2.099031119902081e-09`
- `n_s = 0.9662859140870312`
- `z_re = 7.684806125603674`
- `lambda_D = 0`

Certified local score:

`S_B9,LCDM = 1058.2173424114785`.

The base stencil had a soft negative numerical eigenmode. The preregistered exact eigenmode-ray audit found no descent above `0.005`; the independent half-scale audit then reproduced the same center, found zero exact improvement, and a positive-definite Hessian with minimum eigenvalue `0.0005663251859819669`. Therefore the soft base-scale mode is classified as a stencil-scale instability, not a reproducible descent direction, under the frozen v7 protocol.

Canonical result: `research/robustness/B9_LCDM_V7_FINAL_STATIONARITY_RESOLUTION_2026-08-23.md`.

This closes local numerical stationarity only. It does not prove global optimality.

## 7. RTK B9 status — base and half closed, fresh-tree active

Frozen RTK recentered point:

- `A_s = 2.0874265764520984e-09`
- `Omega_b = 0.04679404670223316`
- `Omega_m = 0.2522369962493503`
- `h = 0.6911169559022905`
- `lambda_D = 792605.2167661682`
- `n_s = 0.9645439945136476`
- `z_re = 7.329291125785135`

Center score:

`S_B9,RTK = 1059.2719553175134`.

Base-scale result:

- exact best improvement `0.0`;
- Hessian positive definite;
- minimum eigenvalue `0.0005825694006286208`.

Half-scale result at the exact same center:

- center replay absolute error `0.0`;
- exact best improvement `0.0`;
- Hessian positive definite;
- minimum eigenvalue `0.00035275631994283977`.

Canonical decisions:

- `research/robustness/B9_RTK_RECENTER_BASE_DECISION_v1.json`
- `research/robustness/B9_RTK_RECENTER_HALF_DECISION_v1.json`

Therefore the only missing RTK local-stationarity gate is the independent fresh-tree certification.

## 8. Provisional paired number — DO NOT freeze yet

Using the two current locally certified/recentered score values,

`Delta S_B9,provisional = 1059.2719553175134 - 1058.2173424114785 = +1.0546129060349`.

This number is stored only as a navigation/checkpoint quantity. It must not be promoted to the final B9 paired local difference until the RTK independent fresh-tree gate passes and a final independent paired exact replay verifies both certified centers under the same frozen B9 objective.

## 9. Active gate launched 2026-08-24

The preregistered workflow was restored unchanged to the current `rtk-class-build` lineage:

- workflow: `.github/workflows/rtk-b9-rtk-recenter-fresh-tree.yml`
- restore commit: `7369e6703f7448bd7c32c85d67be47dd969ff003`
- trigger: `.github/rtk-b9-rtk-recenter-fresh-tree-trigger.txt`
- trigger commit: `f1101bb060e83484e5a1e6cb8c4282a3c2f50009`

Required PASS conditions are exactly:

1. `abs(S_fresh_center - 1059.2719553175134) <= 2e-6`;
2. `S_fresh_center - min_exact(S_fresh_points) <= 0.005`;
3. fresh base-scale RTK Hessian is positive definite.

The workflow uploads the full exact-point stencil, summary, log, environment freeze and provenance even on failure.

## 10. Next decision tree

If fresh-tree **PASS**:

1. persist run ID, job ID, artifact ID/digest and exact certification JSON in `research/robustness/`;
2. update `research/state/B9_current.json`;
3. launch one independent paired exact replay of the frozen LCDM-v7 and RTK certified centers under the same B9 objective;
4. require each center replay error `<=2e-6` and verify the objective/product/provenance fingerprints;
5. freeze `Delta S_B9` only after this paired replay passes;
6. update the closure matrix and chronology.

If fresh-tree **FAIL**:

- replay mismatch -> reproducibility failure; diagnose tree/environment/product provenance;
- exact descent `>0.005` -> RTK center is not certified; preregister a recenter and repeat the multiscale chain;
- non-PD Hessian -> run the frozen exact eigenmode-ray diagnostic before deciding whether the mode is physical descent or stencil instability;
- infrastructure failure -> retry identically; never count it as scientific falsification.

## 11. Recovery checklist for a new chat

1. Read `research/state/B9_current.json` first for B9.
2. Read this file.
3. Inspect the active/latest `rtk-b9-rtk-recenter-fresh-tree` Actions run and its artifact.
4. Read the three frozen decision sources listed above; do not repeat base or half RTK stencils, and do not repeat LCDM v7 stationarity unless a new protocol explicitly invalidates them.
5. Apply the decision tree in section 10.
6. Record every new run/result with UTC timestamp, exact run/artifact provenance, formulas/thresholds, and non-claims.

## 12. Interpretation guards

Nothing in B9 by itself establishes global model preference, a Bayes factor, a Wilks/sigma significance, a fully nonlinear lensing prediction, or validity of the later projectable-U(1) completion in CLASS. The phenomenological B9 `lambda_D` coordinate is also not to be silently identified with later `lambda_HL` theory parameters.


## 13. RTK independent fresh-tree result — automatic record

<!-- B9_RTK_FRESH_TREE_RESULT:AUTO -->

The preregistered RTK independent fresh-tree certification passed. Canonical result: `research/robustness/B9_RTK_FRESH_TREE_CERTIFICATION_RESULT_v1.json`.

- run `32704596153`
- fresh center `S_B9 = 1059.2719553175134`
- cross-run replay absolute error `0.0`
- exact best improvement `0.0`
- fresh Hessian minimum eigenvalue `0.0005825694001738223`
- positive definite `True`

The next gate remains the previously preregistered final paired exact replay.


## 13. Final paired replay — automatic closure record

<!-- B9_FINAL_PAIRED_RESULT:AUTO -->

The preregistered final paired fresh-tree replay passed. Canonical result: `research/robustness/B9_FINAL_PAIRED_REPLAY_RESULT_v1.json`.

- `S_B9,LCDM = 1058.2173424114785`
- `S_B9,RTK = 1059.2719553175134`
- `Delta S_B9 = 1.0546129060348903` (`RTK-LCDM`)
- LCDM replay error `0.0`
- RTK replay error `0.0`
- paired-delta replay error `9.769962616701378e-15`

This closes the **local matched B9 Planck-lensing robustness chain only**. It is not global optimality, significance, AIC/BIC, posterior preference or Bayes evidence.
