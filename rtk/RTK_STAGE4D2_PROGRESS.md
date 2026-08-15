# RT+DBI-Khronon — Stage 4D2 equal-depth profile progress

## Scope

This note supersedes any interpretation of the raw Stage-4D1 lambda curve as a final profile. The exact objective remains

`S = -2 ln L_Planck + chi2_Pantheon + chi2_BOSS`,

with `eff` and `k01` BOSS/RSD mappings. All values below are local numerical profile candidates, not global Delta-chi2 values, confidence intervals, significances, or Bayesian evidence.

Stationarity-checked local LCDM references are

- `S_LCDM,eff = 1050.17772999`,
- `S_LCDM,k01 = 1050.15993541`.

## Numerical repeatability

Four independent fresh CLASS+Planck evaluations of the same deep RTK point and four of the LCDM control gave zero recorded spread in the total objective and all stored components at printed double precision. The profile structures at Delta-S of order `0.01-0.1` are therefore optimizer/profile effects, not stochastic likelihood noise.

## Independent COBYQA cross-check

A bounded six-dimensional COBYQA trust-region optimizer was added as an independent alternative to the earlier Powell searches.

At `lambda_D=30000` it found

- `S_eff = 1051.05488757` in the first pass,
- `S_k01 = 1051.05800929` in the mapping-specific first pass.

A second COBYQA pass starting from the best exact As-z_reio cross-step substantially deepened the finite basin to

- `S_eff = 1050.77617898`,
- `S_k01 = 1050.78574780` at the same point,
- `h = 0.6906228451`,
- `Omega_b = 0.04682481963`,
- `Omega_K0 = 0.25284181742`,
- `A_s = 2.0671578968e-9`,
- `n_s = 0.9643135679`,
- `z_reio = 6.793035785`,
- `r_d = 146.977341 Mpc`.

There was no parameter-box boundary hit. The exact post-optimizer coordinate poll still improved the pre-poll candidate by about `0.00833`, so this is not yet declared stationary.

Relative to the stable local LCDM controls, this evaluated point is worse by approximately

- `Delta S_eff = +0.59845`,
- `Delta S_k01 = +0.62581`.

## Large-lambda competing basin

The high-lambda tail has a multi-basin optimizer structure. An eff-seeded COBYQA pass at `lambda_D=1e8` reached only

- `S_eff = 1051.14416617`.

However a k01-seeded COBYQA pass at the same `lambda_D=1e8` found a substantially deeper high-lambda point:

- `S_k01 = 1050.98494010`,
- `S_eff = 1050.97278123` at the same parameters,
- `h = 0.69048123736`,
- `Omega_b = 0.04684616533`,
- `Omega_K0 = 0.25300447188`,
- `A_s = 2.06455931045e-9`,
- `n_s = 0.96384877076`,
- `z_reio = 6.72012209766`.

This discovery invalidates any claim that the high-lambda tail was fully optimized by the earlier eff-only pass. A dedicated cross-seeded `eff @ 1e8` run has therefore been launched directly from this k01 high-tail point.

At the currently deepest evaluated points, the finite `lambda_D=30000` basin remains lower than the deepest evaluated `1e8` basin by about

- `0.19660` in the eff objective,
- `0.19919` in the k01 objective when comparing their respective listed values.

This difference is provisional until the cross-seeded high-lambda run and deep stationarity checks finish.

## Dense finite-lambda eff scan

A first-pass dense COBYQA scan started from the same finite-basin neighborhood. Completed eff values include

| lambda_D | S_eff |
|---:|---:|
| 15000 | 1050.85672654 |
| 20000 | 1050.84161756 |
| 25000 | 1050.83625236 |
| 30000 | 1050.77617898 (second-pass/deeper point) |
| 40000 | 1050.79690174 |
| 60000 | 1050.82966196 |
| 80000 | 1050.83211478 |

The curve is broadly U-shaped over this finite range, but the 30000 point has received an additional trust-region pass and is therefore not yet equal-depth with its neighbors. Second-pass COBYQA refinements have been launched at 20000, 25000, 40000 and 60000 before any interpolation or preferred-lambda estimate is attempted.

## Planck component audit

At the exact finite `lambda_D=30000` As-z_reio cross point (`S_eff=1051.02633814`) versus the improved eff-tail point at `1e8` (`S_eff=1051.25603999`), the objective difference is about `-0.22970` in favor of the finite point. The Planck pieces contribute approximately

- lowT: `+0.07382` (tail preferred),
- lowE: `-0.20474` (finite point preferred),
- high-l Plik-lite: `-0.17068` (finite point preferred),
- total Planck: `-0.30161`.

Pantheon contributes about `+0.01422` and BOSS-eff about `+0.05768`, partially offsetting the Planck improvement. Thus the finite-lambda structure is not produced solely by the approximate RSD mapping; both Planck lowE and high-l contribute relative to that particular high-lambda point.

Relative to the LCDM control, the same finite RTK point improves lowT and lowE but is worse in high-l Plik-lite; the net Planck primary objective remains worse by about `+0.623`, partly offset by a better Pantheon term and worsened by BOSS.

## Active validation

The following runs are active or queued:

1. exact 73-point stationarity/Hessian test at the deepest current `eff, lambda_D=30000` point;
2. cross-seeded `eff, lambda_D=1e8` COBYQA run initialized from the deep k01 tail point;
3. deep mapping-specific `k01, lambda_D=30000` run;
4. dense k01 finite-lambda grid;
5. second-pass eff refinements at `lambda_D=20000,25000,40000,60000`.

## Current interpretation

There is now reproducible evidence for a broad finite-lambda likelihood basin around a few times `10^4` in the current local Planck+Pantheon+BOSS objective, and it survives an independent optimizer family. However the high-lambda region also contains a deeper basin missed by earlier eff-only searches. Therefore neither a finite preferred `lambda_D` nor a dust-boundary preference is established yet.

The next valid decision point is an equal-depth, stationarity-checked comparison of the finite basin and the cross-seeded `lambda_D=1e8` basin. Only after that should the lambda profile be interpolated in `delta_D=1/lambda_D` or used to initialize a posterior sampler.
