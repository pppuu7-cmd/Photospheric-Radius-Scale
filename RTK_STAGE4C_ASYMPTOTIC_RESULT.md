# RT+DBI-Khronon — Stage 4C/4D0 asymptotic result

## Scope

This report summarizes the exact local-likelihood result after repeated Stage 4C boundary expansions in `lambda_D`, a conditional high-lambda scan, dedicated large-lambda RTK profiles, and independent Stage 4D0 stationarity/Hessian checks.

The objective is

S = -2 ln L_Planck + chi2_Pantheon + chi2_BOSS,

with two retained BOSS/RSD mappings:

- `eff`: effective growth from d sigma8 / d ln a;
- `k01`: f(k=0.1 h/Mpc) sigma8.

This is still a local exact comparison. It is not a global posterior, exclusion significance, or Bayesian evidence calculation.

## Stable LCDM local candidates

Corrected Stage 4C followed by a 73-point exact Stage 4D0 stencil gave boundary-free, positive-definite local candidates:

| mapping | S_LCDM | h | Omega_b | Omega_cdm | A_s | n_s | z_reio |
|---|---:|---:|---:|---:|---:|---:|---:|
| eff | 1050.17772999 | 0.67806754 | 0.04876337 | 0.26191682 | 2.1098745e-9 | 0.96487590 | 7.84743 |
| k01 | 1050.15993541 | 0.67801744 | 0.04876001 | 0.26196233 | 2.1097881e-9 | 0.96547536 | 7.84742 |

The Stage 4D0 exact stencil found no improving point and the local Hessians were positive definite. These are stable local candidates for the present objective, not proven global minima.

## Repeated finite-lambda RTK boundary hits

Starting from the Stage 4B RTK basin, exact bounded Powell searches improved the objective but repeatedly moved to the upper `lambda_D` boundary:

| stage | mapping | lambda_D | S |
|---|---|---:|---:|
| 4C | eff | 1877.16 | 1053.44877 |
| 4C | k01 | 1877.16 | 1053.07753 |
| 4C.1 | eff | 3253.60 | 1052.75505 |
| 4C.1 | k01 | 3253.60 | 1052.79995 |
| 4C.2 | k01 | 7569.74 | 1052.60360 |

Because the best point repeatedly sat on the log-lambda trust boundary, none of these values was treated as a finite-lambda minimum.

## Conditional exact high-lambda diagnostic

Holding the recovered non-lambda parameters fixed, an exact scan showed a monotonic and rapidly saturating trend:

| lambda_D | S_eff | S_k01 |
|---:|---:|---:|
| 1000 | 1055.52117 | 1054.13355 |
| 1877 | 1053.59130 | 1053.11662 |
| 3254 | 1052.95407 | 1052.79995 |
| 5000 | 1052.75455 | 1052.69289 |
| 8000 | 1052.65981 | 1052.63675 |
| 15000 | 1052.60349 | 1052.59903 |
| 30000 | 1052.57937 | 1052.58321 |
| 100000 | 1052.56707 | 1052.57609 |

This scan is diagnostic only because the other cosmological parameters were fixed, but it strongly motivated a dedicated asymptotic profile.

## Analytic large-lambda interpretation

For fixed positive A = Omega_K0/(6 gamma), the exact Khronon normalization obeys

x0 -> A

as lambda_D -> infinity. At any fixed finite scale factor,

r,t ~ lambda_D^(-1/2),
rho_K -> rho_K0 a^(-3),
P_K -> 0,
w_K -> 0,
c_a^2 ~ lambda_D^(-3/2) -> 0,
k_* ~ lambda_D^(3/4) -> infinity.

Thus the Khronon dark-matter sector approaches pressureless dust/CDM behavior. The full model does **not** become LambdaCDM because the RT nonlocal dark-energy sector remains.

If the profiled likelihood keeps improving toward this limit, the correct interpretation is a lower bound on lambda_D (or upper bound on a finite-deviation variable such as epsilon_D = lambda_D^(-1/2)), not a finite best-fit measurement of lambda_D.

## Dedicated asymptotic RTK local profiles

At fixed lambda_D = 1e8, reoptimizing the other six cosmological parameters gave boundary-free local candidates.

### Effective-growth mapping

- S_eff = **1051.91604846**
- h = 0.68898476
- Omega_b = 0.04702738
- Omega_K0 = 0.25490243
- A_s = 2.0571388e-9
- n_s = 0.96296258
- z_reio = 6.47677
- log L_Planck = -502.53673668
- chi2_SN = 39.46016445
- chi2_BOSS_eff = 7.38241065
- r_d = 146.882261 Mpc

### k=0.1 mapping

- S_k01 = **1051.78660426**
- h = 0.68900902
- Omega_b = 0.04702645
- Omega_K0 = 0.25483312
- A_s = 2.0584948e-9
- n_s = 0.96311662
- z_reio = 6.51740
- log L_Planck = -502.46029481
- chi2_SN = 39.46316948
- chi2_BOSS_k01 = 7.40284517
- r_d = 146.887432 Mpc

Independent Stage 4D0 exact 73-point stencils found no improving points in either mapping and both local Hessians were positive definite. Therefore these are stationarity-checked local candidates for the large-lambda basin.

## Current matched local differences

Relative to the independently stationarity-checked LCDM local candidates:

Delta S_eff(local, asymptotic RTK - LCDM) = **+1.73831847**,

Delta S_k01(local, asymptotic RTK - LCDM) = **+1.62666884**.

These are the most meaningful matched local numbers obtained so far, but they are **not** global Delta chi2 values and must not be converted into exclusion significance or model odds.

## What this changes

The earlier Stage 4B finite-design differences near +7.7 to +8.7 were not stable final comparisons because the RTK likelihood basin continued strongly along the large-lambda direction. After following that direction and reoptimizing the remaining cosmological parameters, the local gap is reduced to roughly +1.6 to +1.7.

The scientifically relevant next question is no longer “what finite lambda_D is preferred?” but instead:

**Does a full profile in lambda_D asymptote monotonically to the dust limit, and what lower bound on lambda_D (or upper bound on epsilon_D) follows from the exact profile likelihood?**

Only after that profile is mapped should a production posterior sampler be launched. The lambda prior/reparameterization must be declared explicitly because Bayesian evidence is prior-sensitive along a noncompact asymptotic direction.
