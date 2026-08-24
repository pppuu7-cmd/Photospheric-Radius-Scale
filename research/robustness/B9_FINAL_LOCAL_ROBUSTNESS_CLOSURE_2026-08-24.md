# B9 Planck standalone-lensing robustness — final local closure

Date: 2026-08-24
Status: **CLOSED under the frozen local B9 protocol**

## Frozen objective

`S_B9(theta) = S_A5(theta) - 2 log L_lensing(theta)`

with objective name

`matched-ultra-linstep2+dense-BOSS+PlanckR3-lensing-v1`,

production mapping `eff`, standalone Planck R3 lensing product

`baseline/plc_3.0/lensing/smicadx12_Dec5_ftl_mv2_ndclpp_p_teb_consext8.clik_lensing`.

Frozen protocol: `research/robustness/B9_PAIRED_REOPTIMIZATION_TARGET_v1.json`.

## LCDM local stationarity

Final v7 center:

- `h=0.6803133881531521`
- `Ob=0.048406958808714234`
- `Om=0.25869220161756795`
- `As=2.099031119902081e-09`
- `ns=0.9662859140870312`
- `zre=7.684806125603674`
- `lam=0`

Final local B9 score:

`S_B9,LCDM = 1058.2173424114785`.

The v7 base stencil was exact-recenter-clear but had one soft negative curvature mode. Frozen exact eigenmode rays found no descent above `0.005`; the independent half-scale audit reproduced the center, gave zero exact improvement, and was positive definite with minimum eigenvalue `0.0005663251859819669`. This resolves the base negative mode as a stencil-scale numerical instability under the frozen protocol, not as a reproducible descent direction.

Canonical LCDM resolution: `research/robustness/B9_LCDM_V7_FINAL_STATIONARITY_RESOLUTION_2026-08-23.md`.

## RTK local stationarity

Final recentered RTK point:

- `As=2.0874265764520984e-09`
- `Ob=0.04679404670223316`
- `Om=0.2522369962493503`
- `h=0.6911169559022905`
- `lam=792605.2167661682`
- `ns=0.9645439945136476`
- `zre=7.329291125785135`

Final local B9 score:

`S_B9,RTK = 1059.2719553175134`.

Base-scale result:

- exact best improvement `0.0`;
- positive-definite Hessian;
- minimum eigenvalue `0.0005825694006286208`.

Independent half-scale result:

- center replay error `0.0`;
- exact best improvement `0.0`;
- positive-definite Hessian;
- minimum eigenvalue `0.00035275631994283977`.

Independent fresh-tree certification then passed:

- workflow run `32704596153`;
- center score `1059.2719553175134`;
- cross-run replay absolute error `0.0`;
- best exact improvement `0.0`;
- positive-definite Hessian;
- minimum eigenvalue `0.0005825694001738223`;
- classification `B9_RTK_INDEPENDENT_FRESH_TREE_CERTIFICATION_PASS`.

Canonical fresh-tree result: `research/robustness/B9_RTK_FRESH_TREE_CERTIFICATION_RESULT_v1.json`.

## Final paired fresh-environment replay

The paired replay target was frozen before the RTK fresh-tree result was inspected:

`research/robustness/B9_FINAL_PAIRED_REPLAY_TARGET_v1.json`.

Final exact paired replay:

- `S_LCDM = 1058.2173424114785`;
- `S_RTK = 1059.2719553175134`;
- LCDM replay absolute error `0.0`;
- RTK replay absolute error `0.0`;
- `Delta S_B9 = S_RTK-S_LCDM = +1.0546129060348903`;
- delta replay absolute error `9.769962616701378e-15`, well below the frozen `4e-6` tolerance;
- classification `B9_FINAL_PAIRED_EXACT_REPLAY_PASS`.

Canonical paired result: `research/robustness/B9_FINAL_PAIRED_REPLAY_RESULT_v1.json`.

## Decomposition and the A5 cross-basin discovery

At the final B9 centers:

- RTK baseline component `S_A5=1050.2560245726381`;
- LCDM baseline component `S_A5=1049.400976604194`;
- baseline difference `+0.8550479684440688`;
- direct standalone-lensing contribution difference `+0.1995649375908215` (rounding at the last digits depends on subtraction order).

Thus most of the final local B9 gap arises from the different baseline objective values at the B9-reoptimized centers, not from the direct standalone-lensing term alone.

The LCDM B9 center was independently replayed under the unchanged baseline A5 objective and was confirmed to improve on the historical A5 LCDM local point by `0.5651417435669828`. This spawned the separate A5 cross-basin stationarity chain. That chain must not be folded back into B9 retroactively.

## Closure statement

B9 is closed only in the following scope:

> Under the frozen local matched B9 objective and locked numerical environment, the final locally stationarity-certified RTK and LCDM centers reproduce independently, and the final paired local raw-objective difference is `Delta S_B9=+1.0546129060348903`.

This is **not** a claim of global minima, frequentist significance, Wilks/sigma preference, AIC/BIC preference, posterior odds, Bayes evidence, nonlinear lensing completeness, or validity of a later fixed-action completion.

The phenomenological B9 `lambda_D` coordinate remains distinct from later theory parameters such as `lambda_HL`.
