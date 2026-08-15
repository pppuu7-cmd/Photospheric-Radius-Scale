# RT+DBI-Khronon — Stage 4D1 progress

## Status

Stage 4D1 is an exact fixed-`lambda_D` local profile grid.  For each declared `lambda_D`, the other six cosmological parameters are reoptimized against the same CLASS + Planck + Pantheon + BOSS objective used in Stage 4C.  These are local fixed-lambda profile candidates, not a global profile likelihood, posterior, confidence interval, or Bayesian evidence.

The active workflow run is `31856275702` (`RTK Stage 4D1 lambda profile`).  It contains 14 jobs: seven `lambda_D` values for each of the `eff` and `k01` BOSS/RSD mappings.

## Important correction to the earlier asymptotic interpretation

The earlier dedicated large-lambda Stage 4C candidate at `lambda_D=1e8` had

- `S_eff = 1051.91604846`,
- `S_k01 = 1051.78660426`.

Stage 4D1 uses three deterministic optimizer starts at every fixed lambda.  It has already found a deeper `eff` basin than that earlier candidate.  Therefore the old `S_eff=1051.91605` value must **not** be used as the asymptotic profile reference any longer.

## Completed `eff` profile points so far

### lambda_D = 30000

Artifact: `rtk-stage4d1-eff-30000`, artifact id `9239359284`.

- `S_eff = 1051.609231026803`
- `h = 0.6894847623963938`
- `Omega_b = 0.04698961834643647`
- `Omega_K0 = 0.2543493197461319`
- `A_s = 2.0604944100919008e-9`
- `n_s = 0.9635293974885859`
- `z_reio = 6.571580973046507`
- `log L_Planck = -502.36406841384417`
- `chi2_SN = 39.485470121680535`
- `chi2_BOSS_eff = 7.395624077434102`
- `r_d = 146.887902 Mpc`
- no parameter-box boundary hit
- independent Stage 4D1 poll improvement: `0.0018555744`
- exact likelihood calls: `216`

Relative to the stationarity-checked local LCDM `eff` candidate `S_LCDM=1050.17772999`, the current matched local difference at this fixed lambda is

`Delta S_eff(lambda_D=30000) = +1.43150104`.

### lambda_D = 1000000

Artifact: `rtk-stage4d1-eff-1000000`, artifact id `9239395711`.

- `S_eff = 1051.55985695145`
- `h = 0.6899025740387876`
- `Omega_b = 0.046942911064151334`
- `Omega_K0 = 0.2538531908192155`
- `A_s = 2.0594510160719244e-9`
- `n_s = 0.9634903411338158`
- `z_reio = 6.555298516852542`
- `log L_Planck = -502.35028124018424`
- `chi2_SN = 39.511026175431894`
- `chi2_BOSS_eff = 7.348268295649525`
- `r_d = 146.907267 Mpc`
- no parameter-box boundary hit
- independent Stage 4D1 poll improvement: `0.0049113067`
- exact likelihood calls: `218`

Relative to the same local LCDM candidate,

`Delta S_eff(lambda_D=1e6) = +1.38212696`.

The objective therefore decreases by about `0.0493741` between `lambda_D=30000` and `lambda_D=1e6` inside this deeper basin.  This currently favors continued movement toward larger lambda, but the `1e5` and new `1e8` Stage 4D1 points are still required before the tail shape can be classified.

## Why the deeper basin was missed before

At both completed Stage 4D1 points, the optimizer run from the positive correlated shift found a substantially lower objective than the center start and the negative shift.  This demonstrates that multi-start coverage is materially important in this likelihood surface.  The earlier large-lambda single/local-basin result was therefore insufficient to establish the asymptotic profile value.

## Large-lambda analytic coordinate

The exact fixed-`A=Omega_K0/(6 gamma)` expansion shows a first-order cancellation in the normalized physical density:

`x(1+t) = A/a^3 - (a^3-1)/a^3 * epsilon_D^2 + O(epsilon_D^3)`,

where `epsilon_D=lambda_D^(-1/2)`.  Consequently the leading density and equation-of-state departure from dust is naturally `delta_D=1/lambda_D`, while `c_a^2` starts at `lambda_D^(-3/2)`.  The Stage 4D1 aggregator therefore records both `epsilon_D` and `delta_D` and includes only a diagnostic high-lambda fit `S = S_inf + C/lambda_D`; it is not used as a confidence construction.

## Additional validation now running

A separate conditional fixed-lambda stationarity workflow has been launched for the surprising `lambda_D=30000`, `eff` point:

- workflow: `RTK Stage 4D0 fixed lambda 30000 eff`
- run id: `31857280997`
- design: exact 73-point symmetric stencil in the six reoptimized cosmological coordinates at fixed `lambda_D=30000`, followed by a Hessian/Newton diagnostic.

This test checks local stationarity conditional on fixed lambda.  It does not test the derivative along the lambda direction.

## Automation and aggregation

A post-run workflow `RTK Stage 4D1 aggregate` has been added on `main`.  After a successful Stage 4D1 completion it requires exactly all 14 profile summaries, assembles CSV/JSON/Markdown outputs, checks boundary hits, records numerical threshold crossings only as shape diagnostics, and evaluates the high-lambda `1/lambda_D` tail fit.

Because the preferred finite-deviation coordinate may terminate at a parameter-space boundary, nominal Delta-S threshold crossings must not be called confidence limits without boundary-aware calibration or a declared-prior posterior analysis.
