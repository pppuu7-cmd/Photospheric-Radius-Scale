# RT+DBI-Khronon — Stage 4D1 progress

## Status

Stage 4D1 is an exact fixed-`lambda_D` local profile grid. For each declared `lambda_D`, the other six cosmological parameters are reoptimized against the same CLASS + Planck + Pantheon + BOSS objective used in Stage 4C. These are local fixed-lambda profile candidates, not a global profile likelihood, posterior, confidence interval, or Bayesian evidence.

Active workflow run: `31856275702` (`RTK Stage 4D1 lambda profile`). It contains 14 jobs: seven `lambda_D` values for each of the `eff` and `k01` BOSS/RSD mappings.

## Important correction to the earlier asymptotic interpretation

The earlier dedicated large-lambda Stage 4C candidate at `lambda_D=1e8` had `S_eff=1051.91604846` and `S_k01=1051.78660426`. Stage 4D1 uses three deterministic optimizer starts at every fixed lambda and has found a substantially deeper `eff` basin. The old `S_eff=1051.91605` must therefore not be used as the asymptotic profile reference.

## Completed `eff` profile points

Reference stationarity-checked local LCDM candidate: `S_LCDM,eff=1050.17772999`.

| lambda_D | S_eff | Delta S vs local LCDM | boundary hit | Stage-4D1 poll improvement |
|---:|---:|---:|---|---:|
| 1e3 | 1054.57486 | +4.39713 | no | 0 |
| 3e3 | 1052.0558287744 | +1.87810 | no | 0 |
| 1e4 | 1051.7946846876 | +1.61695 | no | 0 |
| 3e4 | 1051.6092310268 | +1.43150 | no | 0.0018556 |
| 1e5 | **1051.5371767423** | **+1.35945** | no | **0** |
| 1e6 | 1051.5598569515 | +1.38213 | no | 0.0049113 |

The current best completed `eff` point is therefore finite, at `lambda_D=1e5`, not `1e6`. Since `S_eff(1e5)` is lower than both `S_eff(3e4)` and `S_eff(1e6)`, the completed grid now shows a shallow finite-lambda dip rather than a strictly monotonic approach to the dust limit. The new `1e8` Stage 4D1 point is still required to classify the high-lambda tail and determine whether this dip survives the full multi-start profile.

### Current best completed eff candidate: lambda_D = 100000

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
- independent Stage 4D1 poll improvement: `0`
- exact likelihood calls: `228`

Relative to the stationarity-checked local LCDM candidate,

`Delta S_eff(lambda_D=1e5) = +1.35944675`.

## Why multi-start coverage matters

At several completed Stage 4D1 points the positive correlated optimizer start found a much deeper objective than the center or negative start. This confirms a multi-basin likelihood surface and means the earlier single/local-basin asymptotic candidate was insufficient to establish the profile.

## Large-lambda analytic coordinate

At fixed `A=Omega_K0/(6 gamma)`, with `epsilon_D=lambda_D^(-1/2)`, the normalized density has a first-order cancellation:

`x(1+t) = A/a^3 - (a^3-1)/a^3 * epsilon_D^2 + O(epsilon_D^3)`.

Hence the leading density and equation-of-state departure from dust is naturally parameterized by `delta_D=1/lambda_D`, while `c_a^2` starts at `lambda_D^(-3/2)`. The Stage 4D1 aggregator records both `epsilon_D` and `delta_D` and includes only a diagnostic high-lambda fit `S=S_inf+C/lambda_D`; it is not used as a confidence construction.

## Independent validation now running

Two conditional fixed-lambda exact stationarity/Hessian checks are active:

1. `lambda_D=30000`, `eff`: the first attempt failed before physics evaluation because `scipy` was missing for `clipy` in NOJAX mode. The workflow dependency was corrected and the same center was re-launched as run `31857396800`.
2. `lambda_D=100000`, `eff`: a new exact 73-point symmetric stencil/Hessian check was launched directly at the current best completed Stage-4D1 point as run `31857719173`.

These tests check stationarity in the six reoptimized cosmological coordinates at fixed lambda. They do not test the derivative along the lambda direction; that is supplied by the assembled Stage-4D1 profile.

## Remaining Stage 4D1 work

The new `eff,1e8` point and the full `k01` sequence are still running/queued. After all 14 jobs finish, the automatic `RTK Stage 4D1 aggregate` workflow will require the complete set of summaries, assemble CSV/JSON/Markdown outputs, check boundary hits, and evaluate the high-lambda tail.

Because a preferred finite-deviation coordinate may lie near a physical/profile boundary, nominal Delta-S threshold crossings are shape diagnostics only until boundary-aware calibration or a declared-prior posterior analysis is performed.
