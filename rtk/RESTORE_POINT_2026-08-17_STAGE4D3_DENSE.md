# RTK research restoration point — Stage 4D3 dense objective

Checkpoint date: 2026-08-17 (MSK)
Repository: pppuu7-cmd/Photospheric-Radius-Scale
Primary working branch: `rtk-class-build`

## 1. Purpose

This file is the recovery/manual continuation point for the RTK cosmology research. If the chat/session is lost, start from this document, inspect the two active GitHub Actions runs below, and continue according to the decision tree in section 8. Do not silently replace the objective, center, tolerances, or likelihood harness.

## 2. Current scientific frontier

The current production comparison is the **matched-ultra + dense-BOSS objective**. Sparse-objective Stage4D3 results are historical validation only and must not be compared numerically as if they were the same objective.

Current contemporaneous dense control known at checkpoint:

- LCDM local center: `S_eff = 1050.242749509221`.
- RTK best reproducible sampled dense point around the broad large-lambda plateau: `S_eff ~= 1050.424570865017` at `lambda_D = 1e7`.
- Therefore the provisional dense raw-fit gap is `Delta S_eff = S_RTK - S_LCDM ~= +0.1818213558` (RTK worse). This is **not final** until both models have matched local stationarity certification.
- The earlier sparse Round5 RTK value `S_eff = 1050.0338294787382` belongs to the old/sparser objective and must not be used as the dense comparison score.

## 3. Frozen RTK center used by current dense local gate

```
lambda_D = 217225.01601516694
h        = 0.6904831253428524
Ob       = 0.046836300417955265
Om       = 0.25300743080221694
As       = 2.0837288833768707e-9
ns       = 0.9643603115669437
zre      = 7.21843542110055
```

Base finite-difference scales:

```
log(lambda_D): 0.05
h:             0.00035
Ob:            0.00007
Om:            0.00070
As:            4.0e-12
ns:            0.00035
zre:           0.070
```

Recenter/improvement tolerance: `0.005` in S.

## 4. Frozen dense numerical objective

Dense BOSS redshift grid:

```
0.,0.25,0.30,0.34,0.36,0.37,0.38,0.39,0.40,0.42,0.47,0.49,0.50,0.51,0.52,0.53,0.55,0.57,0.59,0.60,0.61,0.62,0.63,0.65,0.70,0.75,1.0
```

Ultra CLASS overrides:

```
tol_background_integration = 3e-4
tol_thermo_integration = 3e-4
tol_perturb_integration = 3e-7
perturb_sampling_stepsize = 0.0125
k_per_decade_for_pk = 40
k_per_decade_for_bao = 180
k_max_tau0_over_l_max = 4.0
l_logstep = 1.02
l_linstep = 2
```

Likelihood dependencies/harness used by current workflows:

- official Planck baseline R3.00 archive;
- `clipy-like==0.15`;
- Pantheon repository cloned into CLASS tree;
- BOSS files under `rtk/data/`;
- exact-float cache-safe inference core; do not restore the old `round(float(p[k]),12)` cache key behavior.

## 5. Important historical Stage4D3 result

The Round5 ultrafine 7D stationarity run on the earlier objective completed successfully as a computation. For the `eff` mapping:

- center `S = 1050.0338294787382`;
- exact likelihood calls = 100;
- all seven Hessian eigenvalues positive;
- best exact sampled S including Newton remained the center;
- Newton trust point worsened to `S = 1050.057732406676`;
- best exact improvement from center = 0;
- formal stationarity failed only because `max_abs_gradient_base_scaled = 0.1433449781` exceeded gradient tolerance 0.03.

Interpretation: this supported **no recenter** but motivated independent exact directional/local checks rather than declaring a proof from a noisy finite-difference gradient.

Relevant historical workflow run: `31978330116` (`RTK Stage 4D3 Round5 ultrafine 7D stationarity`).

## 6. Active computations at checkpoint

### A. RTK dense 7D axis gate

Workflow run ID: `31985345036`
Job ID: `95259287035`
Status at checkpoint: `in_progress`
Current step: `Run exact dense 7D axis gate`

Source script: `rtk/dense_7d_axis_gate.py`

The gate evaluates the frozen center and +/- one base step along all seven coordinates. One RTK CLASS evaluation produces both `eff` and `k01` scores. It writes:

- `output/dense_7d_axis_gate/summary.json`
- `output/dense_7d_axis_gate/points.csv`

Decision variable:

- if either mapping has exact improvement `> 0.005`, recenter is allowed/required before a full Hessian;
- otherwise gate should be `NO_RECENTER_AXIS_CLEAR` and the full dense RTK 7D Hessian should be launched around the frozen center.

### B. LCDM dense 6D stationarity/Hessian

Workflow run ID: `31985735749`
Job ID: `95260337088`
Status at checkpoint: `in_progress`
Current step: `Run exact dense LCDM 6D Hessian`

Purpose: obtain a matched local stationarity/Hessian certification for LCDM on the same dense production objective, so the RTK-vs-LCDM comparison is symmetric.

## 7. Prepared next RTK code

A full dense RTK 7D stationarity/Hessian script has already been prepared on `rtk-class-build`:

- file: `rtk/dense_rtk_7d_stationarity.py`
- preparation commit: `42bd8e28110777124e61ae51b15934787de30da0`

**Do not launch it blindly.** First resolve run `31985345036`. If the axis gate finds an improvement greater than 0.005, recenter first and run the Hessian around the new center. If the axis gate is clear, launch the full Hessian around the frozen center above.

Earlier useful commits in the same research chain:

- `45a175c3770e002de07680aea5bf2a16c837c583` — exact Stage4D3 correlated-ray gate code.
- `08d364dc486fdb09004c44d5cc33ba1935e83c33` — correlated-ray workflow addition on main at that stage.

## 8. Mandatory recovery/continuation decision tree

When resuming:

1. Query run `31985345036` and run `31985735749` first. Do not assume their checkpoint statuses are still current.
2. If RTK axis run is still running, inspect LCDM status and do other non-conflicting preparation only. Do not change the production objective.
3. If RTK axis run completed:
   - download/read its artifact and `summary.json`;
   - record `center_score_eff`, `center_score_k01`, best scores, improvements, best parameters, and gate;
   - if `max(best_improvement_eff, best_improvement_k01) > 0.005`, RECENTER to the exact improving point relevant to the production mapping, revalidate center exactly, then run full dense 7D stationarity there;
   - otherwise launch the prepared full dense RTK 7D stationarity/Hessian at the frozen center.
4. If LCDM Hessian completed, record exact center S, gradient, Hessian eigenvalues/PD status, Newton/trust result, best exact point, and stationarity gates. Do not call LCDM certified if its formal gates fail without investigating why.
5. Once both RTK and LCDM have matched dense stationary/local-minimum results, recompute the contemporaneous raw-fit gap using those final exact center/minimum scores only.
6. Only after the matched minima are frozen should model-selection quantities (AIC/BIC or a separately justified evidence calculation) be discussed. Raw Delta-S alone is not model evidence.
7. Preserve `eff` and `k01` mapping labels separately. Do not mix their scores.
8. Keep warnings explicit: local Hessian/stationarity is not a global posterior, significance, evidence, or observational proof.

## 9. What is closed vs open at checkpoint

Closed / established:

- CLASS RTK patch/build path works.
- exact likelihood harness works with official Planck baseline + Pantheon + BOSS.
- cache-key rounding bug was removed for exact finite differences.
- sparse Stage4D3 7D Hessian was positive definite locally.
- sparse Stage4D3 center beat all exact stencil/Newton points tested there.
- large-lambda RTK dense behavior is a reproducible plateau; the sampled move from ~217k to 1e7 was below the 0.005 recenter threshold.
- dense LCDM local axis poll had its center best among +/-axis points available before this checkpoint.

Open / must not be overstated:

- RTK dense 7D axis gate is not yet resolved at this checkpoint.
- RTK dense full 7D Hessian has not yet been run at the final accepted dense center.
- LCDM dense full 6D Hessian is still running at this checkpoint.
- final matched RTK-vs-LCDM minimum gap is not yet certified.
- no final AIC/BIC/evidence/significance conclusion.
- no global observational proof.

## 10. Fast recovery commands/concepts for a new assistant

The new assistant should use the GitHub connector, not web search, for repository state. Start by fetching jobs/artifacts/logs for the two run IDs in section 6. Repository full name is exactly:

`pppuu7-cmd/Photospheric-Radius-Scale`

Primary branch for RTK research code:

`rtk-class-build`

Useful files to inspect first:

- `rtk/dense_7d_axis_gate.py`
- `rtk/dense_rtk_7d_stationarity.py`
- `rtk/stage4d3_joint_stationarity.py`
- `rtk/stage4d3_correlated_ray.py`
- `rtk/joint_profile_runner.py`
- `rtk/prepare_inference_core.py`

Do not infer a result merely from workflow conclusion. Read the scientific JSON/log result and distinguish computational success from a scientific PASS/FAIL gate.

## 11. One-paragraph handoff prompt

> Continue the RTK Stage4D3 dense-production research from `rtk/RESTORE_POINT_2026-08-17_STAGE4D3_DENSE.md` in `pppuu7-cmd/Photospheric-Radius-Scale`. First query GitHub Actions runs 31985345036 (RTK dense 7D axis gate) and 31985735749 (LCDM dense 6D Hessian), then follow section 8 exactly. Preserve the matched-ultra+dense objective and 0.005 recenter threshold. Do not compare the old sparse S=1050.033829... directly with dense LCDM. If RTK axis is clear, launch the prepared dense 7D Hessian; if it finds >0.005 exact improvement, recenter first. Continue autonomously and report closed items with green checks and unresolved items with red marks.
