# A5 matched-objective cross-basin live recovery methodology

Status: **CANONICAL ACTIVE A5 REOPENING DOCUMENT**  
Updated: `2026-08-24T08:43:00Z`  
Live state: `research/state/A5_cross_basin_current.json`  
Historical autonomous state: `research/state/current.json`

## 1. What changed and what did not

The original A5 matched objective has **not changed**:

`S_A5 = matched-ultra-linstep2+dense-BOSS`

with production mapping `eff` and objective fingerprint

`754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`.

The historical fresh-tree replay-certified local pair remains numerically correct at its exact centers:

- LCDM `S_A5 = 1049.966118347761`;
- RTK `S_A5 = 1050.249912429787`;
- historical local `Delta S_A5 = +0.2837940820259064` (`RTK-LCDM`).

What changed is the **best-known basin status**. B9 reoptimization exposed an LCDM point with much lower baseline score. An independently preregistered baseline-only fresh-tree four-point audit subsequently reproduced that lower score exactly, so it is no longer permissible to treat the historical LCDM point as the best known basin without testing the new point's stationarity.

## 2. Confirmed independent cross-basin result

Canonical result:

`research/robustness/A5_B9_CROSS_BASIN_REPLAY_RESULT_v1.json`

Classification:

`A5_B9_CROSS_BASIN_REPLAY_PASS_NEW_LCDM_SEED_CONFIRMED`

All four target scores replayed with absolute error `0.0` in one common fresh pinned environment:

| point | `S_A5,eff` |
|---|---:|
| historical LCDM | `1049.966118347761` |
| historical RTK | `1050.249912429787` |
| B9-derived LCDM seed | `1049.400976604194` |
| B9-derived RTK seed | `1050.2560245726381` |

The new LCDM seed improves the historical LCDM score by

`I_LCDM = 1049.966118347761 - 1049.400976604194 = 0.5651417435669828`.

The frozen exact-recenter threshold is

`T_recenter = 0.005`.

Hence

`I_LCDM / T_recenter ~= 113.03`.

This is far above numerical recenter tolerance and is therefore a material cross-basin discovery, not a tolerance-level fluctuation.

## 3. Why the historical certificate remains true

A positive-definite local Hessian and recenter-clear exact stencil prove a local statement around a tested center. They do not prove uniqueness of the basin or global optimality.

Therefore the correct logical update is:

1. preserve the historical A5 LCDM local certificate at its old center;
2. remove the stronger interpretation that it is the best currently known LCDM basin;
3. require the new lower seed to pass the same controlled stationarity/reproducibility chain before replacing the reference point;
4. only then re-freeze the paired A5 difference.

No historical artifact is deleted or retroactively rewritten.

## 4. Component origin of the new LCDM improvement

At the historical LCDM A5 center:

- `logL_planck = -501.74128295952414`;
- `chi2_SN = 39.7559388343177`;
- `chi2_BOSS_eff = 6.727613594395151`.

At the independently replayed B9-derived LCDM seed:

- `logL_planck = -501.7107533611436`;
- `chi2_SN = 39.6159823431352`;
- `chi2_BOSS_eff = 6.363487538771697`.

Since the baseline score contribution from Planck is `-2 logL_planck`, the improvements are approximately:

- Planck: `0.06105919676108` (`10.8%` of total improvement);
- Pantheon: `0.1399564911825` (`24.8%`);
- BOSS: `0.364126055623454` (`64.4%`).

All three improve simultaneously. Therefore the lower A5 score cannot be dismissed as a simple trade of baseline goodness-of-fit against the standalone B9 lensing likelihood.

## 5. Parameter displacement from historical LCDM center

Historical LCDM:

- `h = 0.6782837587382693`;
- `Omega_b = 0.04858764689799632`;
- `Omega_m = 0.2611722579449536`;
- `A_s = 2.1054040998203598e-09`;
- `n_s = 0.9653185632254442`;
- `z_re = 7.788312934950947`.

New lower seed:

- `h = 0.6803133881531521`;
- `Omega_b = 0.048406958808714234`;
- `Omega_m = 0.25869220161756795`;
- `A_s = 2.099031119902081e-09`;
- `n_s = 0.9662859140870312`;
- `z_re = 7.684806125603674`.

The displacement is therefore a coherent multi-parameter move rather than a one-coordinate numerical perturbation.

## 6. Frozen stationarity geometry for the new seed

Target frozen before the independent cross-basin result:

`research/robustness/A5_LCDM_B9_SEED_STATIONARITY_TARGET_v1.json`.

Center is exactly the independently replayed lower seed.

Normalized axes:

`[h, Omega_b, Omega_m, A_s, n_s, z_re]`.

Base physical steps:

- `delta h = 0.00035`;
- `delta Omega_b = 0.00007`;
- `delta Omega_m = 0.0007`;
- `delta A_s = 4e-12`;
- `delta n_s = 0.00035`;
- `delta z_re = 0.07`.

At a requested stencil scale `q`, each step is multiplied by `q`.

The exact finite-difference definitions in normalized coordinates are

`g_i = [S(+e_i)-S(-e_i)]/2`,

`H_ii = S(+e_i)-2S(0)+S(-e_i)`,

`H_ij = [S(+e_i+e_j)-S(+e_i-e_j)-S(-e_i+e_j)+S(-e_i-e_j)]/4`.

The worker evaluates both production `eff` and companion `k01` Newton candidates exactly before selecting the best exact production point.

Define

`I_exact = S_center - min_exact S`.

The frozen decision threshold remains

`I_exact <= 0.005`.

## 7. Mandatory decision tree

### Base scale `q=1`

- if `I_exact > 0.005`: **mandatory recenter** to the exact best point, freeze a new target, then repeat base scale;
- if `I_exact <= 0.005` and Hessian is positive definite: run independent half-scale `q=0.5` at exactly the same center;
- if `I_exact <= 0.005` and Hessian is not positive definite: freeze exact eigenmode-ray target from the reproduced non-PD mode(s) before any scale fallback.

### Exact ray gate when required

Use the frozen normalized eigenvector(s) and explicitly preregistered amplitudes. Do not clip a ray into another point. If any exact ray improves by more than `0.005`, recenter is mandatory. If no exact ray does, proceed only according to the preregistered scale-resolution rule.

### Half scale `q=0.5`

A strong local certificate at an unchanged center requires:

- exact improvement `<=0.005`;
- positive-definite half-scale Hessian;
- consistency with the prior base/ray decision path.

Only then may the point advance to a separate independent fresh-tree baseline replay before replacing the historical A5 reference.

## 8. Existing B9-stencil reuse diagnostic — navigation only

The old B9-v7 stationarity artifacts contain exact `S_base_eff` at every B9 stencil point, so the lensing term can be ignored and a baseline Hessian reconstructed from those already-computed values.

This does **not** replace the independent A5 stationarity gate; it is only a prediction of what that gate may see.

### Reconstructed base scale

B9 source run `32601673857`, artifact `9483908098`:

- baseline center `1049.4009766041925`;
- best exact improvement over inherited points `0.0`;
- reconstructed minimum eigenvalue `-0.0024673415362139557`;
- reconstructed Hessian non-PD.

The corresponding approximate baseline normalized gradient is

`[-0.03868037464428653, +0.019149290754967296, -0.02691399037712472, -0.051116057802687465, -0.01316179040577481, +0.0417316825233911]`.

### Reconstructed half scale

B9 source run `32657629806`, artifact `9499099343`:

- baseline center `1049.400976604194`;
- best inherited exact score `1049.4008066153126`;
- improvement `0.00016998888145280944`, far below `0.005`;
- reconstructed Hessian PD;
- minimum eigenvalue `0.00018344795941211117`.

Reconstructed half-scale eigenvalues:

`[0.00018344795941211117, 0.004874018351865473, 0.01911856410563944, 0.0577979220536735, 0.7608069713161205, 1.7771793363901567]`.

The base-nonPD / half-PD pattern is similar to the already resolved B9-v7 stencil-scale instability, but the independent baseline calculation must decide the A5 gate.

## 9. Consequence for paired A5 and A6

At the two independently replayed cross-seeds the raw baseline difference is

`Delta S_A5,cross-seed = 1050.2560245726381 - 1049.400976604194 = +0.8550479684440688`.

This is **not yet a frozen paired result**, because the new LCDM seed is not yet stationarity-certified and the historical RTK point remains the certified RTK reference.

Therefore:

- historical `Delta S_A5=+0.2837940820259064` remains a historical local-pair result;
- it is no longer the current best-known final pair;
- historical AIC derived from it is conditional on that historical pair;
- no new AIC/BIC/Bayes/significance value should be reported until A5 is re-frozen from currently certified reference points.

## 10. Recovery checklist after total chat loss

1. Read `research/state/README.md`.
2. Read `research/state/A5_cross_basin_current.json`.
3. Read this file.
4. Read `research/robustness/A5_B9_CROSS_BASIN_REPLAY_RESULT_v1.json`.
5. Inspect whether `research/robustness/A5_LCDM_B9_SEED_BASE_RESULT_v1.json` exists.
6. If it exists, follow its exact frozen decision classification; do not infer from workflow color alone.
7. If a recenter target/ray result/half result exists, follow the newest frozen target in chronological order.
8. Do not modify `research/state/current.json` accepted A5 pair until the full replacement-candidate chain including independent replay has passed.
9. After replacement certification, re-freeze the matched pair and only then refresh A6 statistics.

## 11. Non-claims

This cross-basin discovery does not prove a global LCDM minimum, does not falsify the RTK model, does not establish a significance level, and does not by itself compare Bayesian evidences. It corrects the best-known local-search frontier under one unchanged frozen objective.
