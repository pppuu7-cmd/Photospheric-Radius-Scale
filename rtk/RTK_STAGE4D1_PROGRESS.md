# RT+DBI-Khronon — Stage 4D1 progress

## Status

Stage 4D1 is an exact fixed-`lambda_D` local profile grid. For each declared `lambda_D`, the other six cosmological parameters are reoptimized against the same CLASS + Planck + Pantheon + BOSS objective used in Stage 4C. These are local fixed-lambda profile candidates, not a global profile likelihood, posterior, confidence interval, or Bayesian evidence.

Active workflow run: `31856275702` (`RTK Stage 4D1 lambda profile`). It contains 14 jobs: seven `lambda_D` values for each of the `eff` and `k01` BOSS/RSD mappings.

## Important correction to the earlier asymptotic interpretation

The earlier dedicated large-lambda Stage 4C candidate at `lambda_D=1e8` had `S_eff=1051.91604846` and `S_k01=1051.78660426`. Stage 4D1 uses three deterministic optimizer starts at every fixed lambda and has found a substantially deeper `eff` basin. The old `S_eff=1051.91605` must therefore not be used as the asymptotic profile reference.

## Completed raw `eff` profile points

Reference stationarity-checked local LCDM candidate: `S_LCDM,eff=1050.17772999`.

| lambda_D | raw Stage-4D1 S_eff | Delta S vs local LCDM | boundary hit | Stage-4D1 poll improvement |
|---:|---:|---:|---|---:|
| 1e3 | 1054.57486 | +4.39713 | no | 0 |
| 3e3 | 1052.0558287744 | +1.87810 | no | 0 |
| 1e4 | 1051.7946846876 | +1.61695 | no | 0 |
| 3e4 | 1051.6092310268 | +1.43150 | no | 0.0018556 |
| 1e5 | **1051.5371767423** | **+1.35945** | no | **0** |
| 1e6 | 1051.5598569515 | +1.38213 | no | 0.0049113 |

The raw completed grid has a shallow finite-lambda dip at `lambda_D=1e5`. However, the independent 73-point check at `3e4` demonstrates that the raw Stage-4D1 optimizer/poll accuracy is not yet sufficient to classify a dip at the `Delta S~0.01-0.05` level. Tight refinements are therefore required before a preferred finite lambda is claimed.

### Current raw best completed eff candidate: lambda_D = 100000

Artifact: `rtk-stage4d1-eff-100000`, artifact id `9239499318`.

- `S_eff = 1051.5371767423296`
- `h = 0.6896156938454194`
- `Omega_b = 0.046969011141089693`
- `Omega_K0 = 0.25414311872101175`
- `A_s = 2.0602067886760265e-9`
- `n_s = 0.9633856082218082`
- `z_reio = 6.568446193824527`
- `log L_Planck = -502.33569200248445`
- `chi2_SN = 39.496147992968844`
- `chi2_BOSS_eff = 7.369644744392044`
- `r_d = 146.903945 Mpc`
- no parameter-box boundary hit
- independent Stage 4D1 coordinate poll improvement: `0`
- exact likelihood calls: `228`

Relative to the stationarity-checked local LCDM candidate, the raw difference is `Delta S_eff(1e5)=+1.35944675`.

## Independent exact check at lambda_D = 30000

The corrected Stage 4D0 fixed-lambda workflow (run `31857396800`) completed the physical 73-point symmetric stencil and exact Newton diagnostic. The raw Stage-4D1 center reproduced at

`S_center = 1051.6092310268014`.

It was **not stationary** at the requested numerical precision:

- `max_abs_gradient_y = 0.37904065`,
- Hessian in normalized coordinates was not positive definite (two negative eigenvalues),
- clipped exact Newton diagnostic found `S_newton = 1051.5536376413036`,
- exact improvement from the raw Stage-4D1 center: `0.0555933855`.

The improved exact point is

- `h = 0.6898347623963937`,
- `Omega_b = 0.046919618346436466`,
- `Omega_K0 = 0.2536493197461319`,
- `A_s = 2.060369176646841e-9`,
- `n_s = 0.9631793974885859`,
- `z_reio = 6.591837261867912`.

This gives an improved conditional difference `Delta S_eff(3e4) ~= +1.37591`, only about `0.01646` above the raw `1e5` candidate. Therefore the finite-lambda dip is currently unresolved at the required optimization precision.

## Tight refinement now running

A new dedicated `stage4d1_tight_refine.py` uses a smaller trust box, tighter Powell tolerances, five deterministic correlated starts and two exact coordinate-poll radii. It is being run for `lambda_D=30000` from the exact Newton-improved point and for `lambda_D=100000` from the current raw best point. Workflow: `RTK Stage 4D1 tight eff refinement`, run `31857823623`.

A separate 73-point stationarity/Hessian check is also running directly at the raw `lambda_D=100000` candidate: run `31857719173`.

## Why multi-start coverage matters

At several completed Stage 4D1 points a correlated optimizer start found a much deeper objective than the center or opposite start. This confirms a multi-basin likelihood surface and means single-basin/asymptotic fits are insufficient for the profile.

## Large-lambda analytic coordinate

At fixed `A=Omega_K0/(6 gamma)`, with `epsilon_D=lambda_D^(-1/2)`, the normalized density has a first-order cancellation:

`x(1+t) = A/a^3 - (a^3-1)/a^3 * epsilon_D^2 + O(epsilon_D^3)`.

Hence the leading density and equation-of-state departure from dust is naturally parameterized by `delta_D=1/lambda_D`, while `c_a^2` starts at `lambda_D^(-3/2)`. The Stage 4D1 aggregator records both `epsilon_D` and `delta_D`; high-lambda fits are diagnostics only and are not confidence constructions.

## Remaining Stage 4D1 / Stage 4D2 work

The new `eff,1e8` point and the full `k01` sequence are still running/queued. After all 14 jobs finish, the automatic aggregate workflow will assemble the profile and check boundary hits. A Stage-4D2 interpretation scaffold has also been added: it works in the physical coordinate `delta_D=1/lambda_D >= 0`, distinguishes an interior sampled minimum from a dust-boundary minimum, and deliberately reports threshold crossings only as shape diagnostics until stationarity and boundary-aware coverage/posterior calibration are complete.

No confidence interval, significance or Bayesian evidence should be inferred from the current raw/tight profile until those checks are complete.
