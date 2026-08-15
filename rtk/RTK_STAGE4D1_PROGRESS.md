# RT+DBI-Khronon — Stage 4D1 progress

## Scope

Stage 4D1 profiles the exact objective

`S = -2 ln L_Planck + chi2_Pantheon + chi2_BOSS`

at fixed `lambda_D`, reoptimizing the remaining six cosmological parameters. Two BOSS/RSD mappings are retained: `eff` and `k01`. All results below are local profile candidates, not a global posterior, confidence interval, significance, or Bayesian evidence.

Reference stationarity-checked local LCDM candidates:

- `S_LCDM,eff = 1050.17772999`
- `S_LCDM,k01 = 1050.15993541`

## Completed 14-point raw profile

Workflow `31856275702` completed all seven lambda values for both mappings. The corrected aggregate workflow `31898432252` succeeded after exact artifact-directory validation was fixed.

### eff raw profile

| lambda_D | raw S_eff |
|---:|---:|
| 1e3 | 1054.57485623 |
| 3e3 | 1052.05582877 |
| 1e4 | 1051.79468469 |
| 3e4 | 1051.60923103 |
| 1e5 | 1051.53717674 |
| 1e6 | 1051.55985695 |
| 1e8 | 1051.32449549 |

### k01 raw profile

| lambda_D | raw S_k01 |
|---:|---:|
| 1e3 | 1052.99098948 |
| 3e3 | 1052.01395410 |
| 1e4 | 1051.78242627 |
| 3e4 | 1051.72035633 |
| 1e5 | 1051.60600015 |
| 1e6 | 1051.51907405 |
| 1e8 | 1051.24650973 |

At raw Stage-4D1 optimizer accuracy both mappings look approximately monotonic toward large lambda. This raw conclusion is **not** reliable at the sub-unit level because tighter searches have already found a substantially deeper finite-lambda basin.

## Tight eff refinement

### lambda_D = 30000

Five-start tight Powell plus exact polls reached

- `S_eff = 1051.0755927897148`
- `S_k01 = 1051.0835197820677` at the same parameters,
- `h = 0.6905802910391277`,
- `Omega_b = 0.04684163640622535`,
- `Omega_K0 = 0.2529201285589534`,
- `A_s = 2.0630563560740213e-9`,
- `n_s = 0.9640474757333444`,
- `z_reio = 6.6839724497605335`,
- `r_d = 146.965498 Mpc`.

No parameter-box boundary was hit. Relative to the stable local LCDM eff candidate, this gives `Delta S_eff=+0.89786280`.

The independent 73-point exact fixed-lambda check (workflow `31898477269`) reproduced the center exactly and showed that the point is inside a **locally convex** basin: all six normalized-Hessian eigenvalues are positive,

`0.04668, 0.05988, 0.09514, 0.31004, 3.08656, 7.37635`.

However the center is not yet stationary. The largest normalized finite-difference gradient component is about `0.1472`, dominated by the correlated amplitude/reionization direction. A stencil cross-step increasing both `A_s` and `z_reio` found the current best exact point

- `S_eff = 1051.026338142692`,
- `S_k01 = 1051.035699794882`,
- `A_s = 2.0670563560740213e-9`,
- `z_reio = 6.753972449760534`,
- all other six-parameter coordinates unchanged from the tight center.

This improves the tight center by `0.04925465` and gives the current best exact conditional difference

`Delta S_eff(3e4) = +0.84860815`

relative to the stationarity-checked local LCDM eff candidate. A clipped Newton diagnostic also improved the center, to `S_eff=1051.04126124`, but not as much as the exact cross-step. Therefore `lambda_D=3e4` remains an **unconverged but locally convex** finite-lambda candidate.

### lambda_D = 100000

Tight Powell reached

- `S_eff = 1051.1778474864889`,
- `S_k01 = 1051.1887989863240`,
- `h = 0.6901873895028806`,
- `Omega_b = 0.04688758336412194`,
- `Omega_K0 = 0.253421603515163`,
- `A_s = 2.062306350250812e-9`,
- `n_s = 0.9638955372522343`,
- `z_reio = 6.647719070471404`,
- `r_d = 146.943558 Mpc`.

The exact 73-point stationarity check (workflow `31898491296`) found no stencil point that improves this center. Its normalized Hessian is positive definite with eigenvalues

`0.04381, 0.09288, 0.11346, 0.33251, 3.07095, 7.37725`.

The formal central finite-difference gradient is still non-negligible (`max |g_y| ~= 0.2205`) and the clipped Newton extrapolation worsens the exact objective by about `0.0941`. This means the local surface is non-quadratic at the chosen stencil scale; the point is a stable finite-stencil candidate, but a smaller-trust-region optimizer is still required for a stronger stationarity statement.

Relative to the stable local LCDM eff candidate, `Delta S_eff(1e5)=+1.00011750`.

## Component origin of the finite-lambda improvement

Comparing the tight `lambda_D=3e4` center with the raw `lambda_D=1e8` eff point, the finite point improves the total objective by about `0.24890`. This improvement is driven almost entirely by the Planck primary-CMB term:

- Planck contribution to Delta objective (`3e4 - 1e8`): `-0.28093`,
- Pantheon: `+0.01765`,
- BOSS eff: `+0.01438`,
- total: `-0.24890`.

Thus the present hint of a finite-lambda basin is **not** being created by the approximate RSD mapping. Individual Planck lowT/lowE/high-l components are being audited separately before physical interpretation of the CMB improvement.

## Consequence for the raw large-lambda interpretation

The raw `lambda_D=1e8` points are

- `S_eff = 1051.32449549`,
- `S_k01 = 1051.24650973`.

The finite `3e4` basin is already lower than these raw high-lambda objectives, but this is not yet an equal-depth comparison. Large-lambda points must receive the same tight/trust-region optimization before the lambda profile can be classified.

## Equal-depth numerical validation now running

1. Symmetric five-start tight refinement workflow `31898624907`:
   - `eff @ 1e8`,
   - `k01 @ 1e8`,
   - `k01 @ 3e4`,
   - `k01 @ 1e5`.
2. Independent bounded COBYQA trust-region workflow `31898756573` for both mappings at `3e4`, `1e5`, and `1e8`.
3. Exact repeated-evaluation diagnostic to measure the numerical noise floor of CLASS+Planck at the deep RTK and LCDM points.

The purpose is to separate true profile structure from optimizer-family bias and numerical noise.

## Large-lambda analytic coordinate

For fixed positive `A=Omega_K0/(6 gamma)` and `delta_D=1/lambda_D`, the exact normalized Khronon density has no `O(lambda_D^-1/2)` correction:

`x(1+t) = A/a^3 - (a^3-1)/a^3 * lambda_D^-1 + O(lambda_D^-3/2)`.

Thus the leading background departure from dust is naturally linear in `delta_D=1/lambda_D`, while `c_a^2 ~ lambda_D^-3/2` and `k_* ~ lambda_D^3/4`.

If equal-depth optimization ultimately minimizes at `delta_D=0`, boundary-aware inference is required. If a stable interior finite-lambda minimum survives, an interior profile/posterior analysis becomes appropriate. Nominal Delta-S crossings must not be called confidence limits before numerical stationarity and statistical calibration are established.

## Immediate next decision

Do not launch production MCMC yet. First compare the finite basin and large-lambda tail with the same numerical optimization depth and an independent optimizer family. If the `~3e4` basin survives, build a dense refined fixed-lambda grid around it and then reparameterize the final profile in `delta_D=1/lambda_D`. If the large-lambda tail drops below it, revert to the dust-boundary interpretation.
