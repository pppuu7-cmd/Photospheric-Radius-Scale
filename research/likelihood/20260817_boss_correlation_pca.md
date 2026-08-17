# Additive PCA decomposition of the BOSS correlated RTK-LCDM gap

Status: **exact linear-algebra diagnostic of the published 9x9 covariance; not a model-selection statistic**.

Inputs are the validated current-point BOSS residuals from workflow `32055604273` and the repository covariance `final_consensus_covtot_dM_Hz_fsig.txt`.

## Method

Let `D = diag(sqrt(C_ii))`, `R = D^-1 C D^-1` be the dimensionless correlation matrix, and `z = D^-1 (prediction-data)` the standardized residual vector. Diagonalize

`R = V diag(lambda_a) V^T`.

Then the BOSS chi-square decomposes exactly and additively as

`chi2 = sum_a q_a^2`, with `q_a = (V_a^T z)/sqrt(lambda_a)`.

Unlike leave-one-block-out diagnostics, the PCA-mode contributions are orthogonal and sum exactly to the full chi-square. Eigenvector signs are conventional; only relative loadings and q_a^2 matter.

The calculation reproduces
- RTK chi2 = `7.61217220343068`,
- LCDM chi2 = `6.72761359439515`,
- delta = `+0.88455860903553`.

## Dominant delta modes

| mode | corr eigenvalue | q_RTK | q_LCDM | delta(q^2), RTK-LCDM |
|---:|---:|---:|---:|---:|
| 5 | 1.10870 | -0.95795 | -0.15016 | **+0.89512** |
| 4 | 0.63004 | -1.67737 | -1.48307 | **+0.61407** |
| 7 | 1.43214 | -0.60998 | -0.82379 | **-0.30654** |
| 2 | 0.41966 | +1.66021 | +1.60709 | +0.17355 |
| 0 | 0.21127 | -0.58227 | -0.70845 | -0.16286 |
| 6 | 1.32942 | +0.49225 | +0.63458 | -0.16038 |
| 8 | 2.94785 | -0.32227 | -0.50485 | -0.15101 |
| 1 | 0.30147 | -0.16104 | -0.27023 | -0.04709 |
| 3 | 0.61944 | +0.20351 | +0.10818 | +0.02971 |

The compensating positive/negative mode deltas sum to `+0.8845586`.

## Dominant mode 5

Largest standardized-observable loadings (one arbitrary sign convention):

- `fσ8(z=0.51)`: -0.495
- `fσ8(z=0.61)`: -0.447
- `D_M(z=0.51)`: +0.415
- `D_M(z=0.38)`: +0.411
- `fσ8(z=0.38)`: -0.349

This single orthogonal mode contributes
- RTK: `0.91767` to chi2,
- LCDM: only `0.02255`,
- delta: **`+0.89512`**.

Thus essentially the entire net BOSS penalty can be traced to a correlated **geometry-versus-growth consistency direction**, not to a single transverse-distance point. RTK moves D_M closer to the data but simultaneously predicts larger growth, especially at z=0.51--0.61; the BOSS covariance is sensitive to that relation.

## Secondary mode 4

Largest loadings:
- `H(z=0.38)`: -0.660
- `D_M(z=0.61)`: -0.444
- `H(z=0.61)`: +0.427
- `D_M(z=0.38)`: +0.291
- `fσ8(z=0.51)`: +0.193

It adds another `+0.6141` delta chi2, but several other orthogonal modes favor RTK and partially cancel it, leaving the observed total +0.8846.

## Scientific interpretation

The most useful next physics target is therefore not simply lowering all BOSS residuals. The current RTK sector must reproduce the observed relation between:

1. transverse distance evolution D_M(z),
2. radial expansion H(z), and
3. late-time growth fσ8(z).

The present RTK point already improves D_M, so an indiscriminate geometry retuning could make the physically important correlation mode worse. Future parameter/physics diagnostics should monitor this PCA mode explicitly.

This is still based on the compressed BOSS fσ8 observable. A survey-window/template-aware RTK RSD likelihood remains required for publication-strength inference with scale-dependent growth.
