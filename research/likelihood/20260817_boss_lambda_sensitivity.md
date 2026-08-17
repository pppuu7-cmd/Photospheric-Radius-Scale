# BOSS sensitivity to lambda_D at fixed current RTK shared parameters

Status: **validated BOSS-only sensitivity diagnostic; not a profile likelihood or optimization**.

## Provenance

- Workflow run: `32056154491`, success.
- Job: `95466670812`.
- RTK source checkout: `ebb329f184b5a4ca9c0090bc3b7d36359fed0345`.
- CLASS nonlocal upstream: `36cf283628c4a3330ec9fd3d84239bf775f77317`.
- Artifact ID: `9296744006`.
- Artifact ZIP SHA256: `356504f7a3268e2bad8bc3aa6bcaed1987eb7506d92c9da8d844901277ae818f`.

The six shared parameters `As,Ob,Om,h,ns,zre` were held fixed at the current RTK accepted center. Only `lambda_D` was changed. This deliberately does **not** reoptimize the matched objective.

Current accepted `lambda_D = 217644.75828347108`.

## Full BOSS eff chi-square

| factor vs current | lambda_D | chi2_BOSS_eff | delta from current |
|---:|---:|---:|---:|
| 0.125 | 27205.5948 | 7.6122105085 | +0.0000383051 |
| 0.25 | 54411.1896 | 7.6129831891 | +0.0008109857 |
| 0.5 | 108822.3791 | 7.6125958683 | +0.0004236648 |
| 1 | 217644.7583 | 7.6121722034 | 0 |
| 2 | 435289.5166 | 7.6119013630 | -0.0002708405 |
| 4 | 870579.0331 | 7.6117511208 | -0.0004210826 |
| 8 | 1741158.0663 | 7.6116724149 | -0.0004997885 |

Across a factor-64 range from 0.125x to 8x the entire BOSS chi-square varies by only about `0.00131`. From the current value to 8x larger lambda_D the improvement is only about `5.0e-4` in chi-square.

This is negligible compared with the present RTK-LCDM BOSS gap of about `+0.88456`.

## Observable sensitivity

The geometry predictions barely move. For example at z=0.61:

- D_M-rescaled changes from `2297.38619` at 0.125x to `2297.37502` at 8x;
- H-rescaled changes from `94.854163` to `94.854184`.

The compressed growth prediction changes slightly more but still weakly. At z=0.61:

- 0.125x: `f sigma8 = 0.4846031`;
- 1x: `0.4852402`;
- 8x: `0.4852624`.

The full 64-fold lambda change therefore alters this f sigma8 prediction by only about `6.6e-4` absolute.

## Scientific result

The BOSS pressure identified in the residual/PCA audits is essentially **orthogonal to lambda_D** in the present deep-dust regime. Changing lambda_D by more than an order of magnitude does not materially repair the geometry-growth consistency mode responsible for the current BOSS penalty.

This independently supports the interpretation that:

1. the current RTK point is already extremely close to the Khronon dust boundary;
2. lambda_D is weakly identified by the present linear late-time data in this region;
3. the percent-level growth/geometry signature is dominated by the RT/nonlocal gravitational sector and the correlated shared-parameter manifold, not by finite DBI pressure;
4. the tiny negative/flat Hessian curvature along log(lambda_D) has a plausible physical origin rather than being automatically dismissed as numerical noise.

## Boundary implication

The slight trend toward lower BOSS chi-square at larger lambda_D is far below the recenter tolerance and is not a meaningful BOSS-only preference by itself. However, if the **full matched objective** also remains flat toward larger lambda_D in the repeated Hessian/targeted profile, the correct statistical picture may be a dust-boundary or non-identifiable direction rather than a resolved finite interior lambda minimum.

Therefore this BOSS-only scan must not be used to select a new center or claim a lambda constraint. The repeated full-objective Hessian and Stage4D3 multiscale/low-mode gates remain authoritative.
