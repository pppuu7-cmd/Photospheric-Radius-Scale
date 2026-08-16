# RTK Stage 4D3 — checkpoint v4

## Current exact navigation record

At the current production/default CLASS settings, the lowest directly evaluated RTK point found so far is the As–z_re v4 boundary point:

- **S_eff = 1050.135699621492**
- **S_k01 = 1050.149916197271**
- lambda_D = 293868.81143246836
- h = 0.6903899123316766
- Omega_b = 0.046851744145772894
- Omega_m = 0.25313821169954864
- A_s = 2.082203080347647e-9
- n_s = 0.9644164163369503
- z_re = 7.17612905430964

This point is an **exact likelihood navigation record**, not a certified best fit. The v4 2D map selected the upper A_s and z_re boundary, and strict 7D stationarity is still running.

## Exact descent sequence

Representative exact S_eff records:

- 1050.6106288 — early high-lambda basin
- 1050.5562518 — exact correlated Newton point
- 1050.4537918 — extended correlated ray
- 1050.4444187 — localized ray
- 1050.3623613 — orthogonal 7D stencil point
- 1050.3458335 — A_s/z_re correlated point
- 1050.2553997 — first fine A_s/z_re map
- 1050.2204635 — v2 boundary map
- 1050.1486477 — v3 map, first raw baseline crossing below harvested LCDM local candidates
- **1050.1356996 — v4 current navigation record**

The sequence is not a profile-likelihood curve; it records navigation improvements through different correlated directions.

## V3 repeatability and precision convergence

The v3 point is:

- S_eff = 1050.1486476532043
- S_k01 = 1050.162683960708
- A_s = 2.080703080347647e-9
- z_re = 7.14112905430964

A dedicated 5x repeatability audit reproduced the full fixed-point result bit-for-bit: spreads in S_eff, S_k01, Planck, both BOSS mappings and r_d were all zero.

The strict 1e-9 baseline regression precision rerun passed. For v2 -> v3:

| precision | Delta S_eff | Delta S_k01 |
|---|---:|---:|
| baseline | -0.0718158774705 | -0.0716359288970 |
| tight | -0.0710021317734 | -0.0708220624815 |
| ultra | -0.0709006160891 | -0.0707205249221 |

Tight -> ultra changes the differential improvement by only about 1.02e-4. Thus the v2 -> v3 correlated descent is numerically robust.

## Matched fixed-point RTK versus LCDM

Harvested exact-float LCDM local candidates are **not yet globally or strictly reoptimized at final precision**. The better harvested candidate for both mappings is the old `eff`-optimized point:

- LCDM S_eff = 1050.1661952170557
- LCDM S_k01 = 1050.1684126165533

Matched fixed-point comparisons using identical CLASS precision overrides for RTK v3 and both harvested LCDM candidates gave:

| precision | Delta S_eff = RTK - best fixed LCDM | Delta S_k01 = RTK - best fixed LCDM |
|---|---:|---:|
| baseline | **-0.0175475638514** | **-0.0057286558454** |
| tight | **-0.0041724831760** | +0.0080729475023 |
| ultra | **-0.0012775620387** | +0.0109591846801 |

Interpretation:

- At baseline, RTK v3 crosses below the harvested LCDM local candidates in both mappings.
- With matched tight/ultra numerical settings, the `eff` comparison remains essentially tied, with RTK lower by only ~0.0013 at ultra.
- Under `k01`, the sign reverses at tight/ultra and the fixed LCDM candidate is lower.
- **This is not a model-preference result.** Neither model has yet been reoptimized on the same final precision + dense-BOSS objective.

## CLASS precision status

Default absolute Planck scores are not precision converged. Earlier audits localized the dominant absolute shift to high-ell/ell sampling.

A focused ultra ell-sampling corner varied:

- l_logstep = 1.02, 1.01, 1.005
- l_linstep = 5, 3, 2

at otherwise-ultra settings. The differential RTK descent is robust across all nine settings with spread ~0.00123 < 0.005.

At l_linstep=2, the old300k and v2best scores were identical for all tested l_logstep values:

- old300k S_eff = 1050.9492611971352
- v2best S_eff = 1050.5547772149139
- Delta S_eff = -0.3944839822213

This strongly supports convergence of **relative** RTK descent. Absolute-score production settings still require a final locking check.

## BOSS and Pantheon

### Pantheon

Independent covariance/algebra audit: **PASS**.

- 40x40 covariance
- symmetric and SPD
- smallest eigenvalue ~4.16e-4
- correlation condition number ~5.29
- custom Cholesky agrees with NumPy

### BOSS

Covariance linear algebra is clean, but the production sparse redshift derivative/grid has a measurable numerical systematic:

- Delta chi2_eff sparse -> dense ~ +0.0341
- Delta chi2_k01 sparse -> dense ~ +0.0215

P_k,max is already effectively converged. Final inference must use a denser redshift-growth evaluation.

## Model-internal dust boundary

From the implemented RTK equations, the leading physical dust-boundary deformation scales as

u = 1 / lambda_D,

with u -> 0 at the dust boundary. Background density and w begin at O(1/lambda_D), while sound-speed terms begin at O(lambda_D^-3/2). Future final lambda profiling should therefore be organized in u, not only log(lambda_D).

## Active calculations

- Strict 7D multiscale stationarity around v4 record: run **31919232861**, 6 jobs, eff/k01 x scales 1.0/0.5/0.25.
- Neighbor strict 7D geometry around v3: run **31919131264**, 6 jobs.
- As–z_re v5 exact navigation scan: run **31919292115**, 25 exact calls.

## Scientific gates

✅ Official Planck likelihood self-tests reproduced.

✅ Exact-float production cache and modern A_s/n_s inputs gated.

✅ Pantheon covariance/algebra audit passed.

✅ Deep correlated RTK descent is repeatable and differential-precision robust.

✅ Raw fixed-point RTK/LCDM comparison has been performed with identical tight/ultra CLASS settings.

❌ Current RTK navigation record is not yet a strict 7D stationary point.

❌ Absolute CLASS precision is not fully locked for final production inference.

❌ Dense BOSS redshift mapping is not yet the production objective.

❌ Lambda_D finite interior minimum versus dust boundary is not established.

❌ LCDM and RTK have not yet both been reoptimized on the same converged objective.

❌ No valid final AIC/BIC/Bayes-factor/significance/model-preference claim yet.

## Immediate decision rule

Any newly exact-evaluated point improving the current relevant center by more than 0.005 is used immediately as the next strict multiscale center. Only after numerical settings and both models are reoptimized on the same objective may raw score differences be interpreted as model comparison.
