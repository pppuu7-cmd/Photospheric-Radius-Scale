# RTK Stage 4D3 — checkpoint v5

## Current exact navigation record

The As-z_re v5 exact 5x5 map produced the first interior minimum in the v-series local two-dimensional scans:

- **S_eff = 1050.072580002519**
- **S_k01 = 1050.0869167499159**
- lambda_D = 293868.81143246836
- h = 0.6903899123316766
- Omega_b = 0.046851744145772894
- Omega_m = 0.25313821169954864
- A_s = 2.0832030803476467e-9
- n_s = 0.9644164163369503
- z_re = 7.21112905430964
- chi2_BOSS_eff = 7.559652229275825
- chi2_BOSS_k01 = 7.5739889766726245
- chi2_SN = 39.550891596423256
- logL_high = -291.9130833491661
- logL_lowE = -197.83170256862806
- logL_lowT = -11.736232170615892
- logL_planck = -501.48101808841
- r_d = 146.965527 Mpc

Improvement relative to the v4 center:

- Delta S_eff = **-0.0631196189729**
- Delta S_k01 = **-0.0629994473552**

Both `best_eff_on_boundary` and `best_k01_on_boundary` are false for the v5 grid. This is a local 2D navigation result, not yet a seven-dimensional stationary point or global best fit.

## Neighbor strict geometry at v4

The completed strict Stage4D3 scale=0.25 `eff` run around v4 independently demonstrated nonstationarity:

- max |base-scaled gradient| = 0.1444780234 > 0.03
- Hessian has two negative eigenvalues
- best exact stencil score = 1050.120415940173
- exact stencil improvement = 0.015283681319 > 0.005
- exact Newton proposal worsened the score

The best v4 strict-stencil point moved in the same A_s / z_re direction and is still above the v5 record. Thus v5 is the correct next strict center.

## Active strict-v5 stationarity

Workflow:

- `.github/workflows/rtk-stage4d3-as-zre-v5best-recenter-both.yml`
- commit `91e6395636a01a8e060e5d2f4bbe59a3e903a734`
- run `31935018530`

Six jobs are running in parallel: mappings `eff`, `k01` x scales 1.0, 0.5, 0.25. Acceptance gates remain:

- positive-definite Hessian
- max absolute base-scaled gradient <= 0.03
- no exact design-point improvement > 0.005
- no exact correlated Newton improvement > 0.005

Any exact improvement > 0.005 will trigger another recenter rather than a stationarity claim.

## Active v4 -> v5 numerical precision audit

Workflow:

- `.github/workflows/rtk-class-precision-v5best-pair.yml`
- commit `97955112e88ccea2c9c79f02a85928b53eea9462`
- run `31935040222`

The audit evaluates v4 and v5 at baseline, tight and provisional-ultra CLASS settings with strict 1e-9 baseline score regression. It tests whether the ~0.063 v4 -> v5 descent survives the same numerical tightening that previously validated the v2 -> v3 descent.

## LCDM matched-ultra control: timed-out Powell evidence

A two-start ultra-precision local Powell refinement was attempted for LCDM (`run 31919368067`). Both jobs were canceled by the 120-minute job timeout, not by a likelihood or CLASS failure.

Before timeout, the `k01` job found a common exact point that is better in both mappings than the old ultra fixed candidate:

- h = 0.6779337587382693
- Omega_b = 0.04872764689799632
- Omega_m = 0.26187225794495356
- A_s = 2.1094040998203598e-9
- n_s = 0.9649685632254442
- z_re = 7.8583129349509475
- **S_eff = 1050.2310656457898**
- **S_k01 = 1050.2326184302317**

Nearby exact z_re evaluations bracketed this one-dimensional direction:

- z_re = 7.8572462682 -> S_k01 = 1050.2350401185
- z_re = 7.8583129350 -> S_k01 = 1050.2326184302
- z_re = 7.8612751295 -> S_k01 = 1050.2368785873

The timed-out run therefore proves that the previously harvested LCDM point was not locally optimized on the provisional-ultra objective. It does **not** certify the above partial-best point as stationary.

## Replacement LCDM refinement

A deterministic checkpointed ultra stencil refinement has been launched to replace the slow Powell search:

- science code commit `430dd43c4c3c8adee3bbe2ae099836bd0c95b96d`
- workflow commit `36df66cb7e3c20d1089cc00bc715fb0e2a29cd6b`
- run `31935158052`

For each mapping it uses the common partial-best point above, a 13-point central axis stencil in six nuisance dimensions, one exact separable-quadratic proposal, then a half-scale recentered stencil and a second exact proposal. The summary and trace are checkpointed after every exact evaluation. This is still local numerical refinement, not global inference.

## Precision and likelihood status carried forward

✅ Official Planck R3.00 likelihood self-tests reproduced in Actions.

✅ Production inference uses exact IEEE-754 cache keys and modern `A_s` / `n_s` inputs through `prepare_inference_core.py`, with workflow grep gates.

✅ Pantheon covariance and analytic algebra audit passed independently.

✅ BOSS DR12 convention, data vector and covariance linear algebra are verified.

✅ Previous v2 -> v3 RTK descent is bit-repeatable and differential-precision robust: tight -> ultra changes Delta S by about 1e-4.

✅ Focused ultra ell-sampling tests show relative RTK descent stable within about 0.00123 across the tested corner.

❌ The v5 RTK point has not yet passed strict 7D stationarity.

❌ The v4 -> v5 descent has not yet completed its tight/ultra precision audit.

❌ Absolute CLASS production precision is not fully locked.

❌ Dense BOSS redshift-growth evaluation is not yet the production objective; sparse -> dense shifts chi2 by O(0.02-0.03).

❌ LCDM and RTK have not yet both been reoptimized on the same final converged objective.

❌ A finite lambda_D interior optimum versus the dust boundary is not established.

❌ No valid final AIC/BIC/Bayes-factor/significance/model-preference claim exists yet.

## Decision rule

Treat v5 as the current exact navigation center. Recenter immediately on any lower exact point improving the relevant score by more than 0.005. Only after strict local geometry, final precision locking, dense-BOSS production mapping and matched reoptimization of both models may score differences be interpreted as observational model comparison.
