# RTK Stage 4D3 checkpoint v3

This checkpoint records the exact state after the first and second As-zre localization cycles. It is deliberately conservative: exact navigation records are not promoted to stationary best fits or statistical preference claims.

## ✅ Closed / established

- Official Planck 2018 Commander + SimAll + Plik-lite runtime is live with clipy-like 0.15 and self-tests reproduced.
- Production generated inference core uses exact-float cache keys; legacy rounded-As cache is excluded by CI.
- Legacy A_s_ad/n_s_ad inputs are replaced by A_s/n_s in the production generated core.
- Scientific Stage4D3 PASS gate now requires gradient tolerance, PD Hessian, no exact poll improvement beyond tolerance, and no correlated Newton improvement beyond tolerance.
- Pantheon covariance / Cholesky / additive-offset algebra audit passed.
- BOSS covariance linear algebra passed; sparse redshift derivative grid has a real numerical systematic and must be densified before final inference.
- Broad correlated descent from the old 300k region into the orthogonal basin is CLASS-precision robust: tight-to-ultra differential change is ~9e-4.
- The previous As-zre step (S_eff 1050.362361331657 -> 1050.345833538801) is also precision robust: tight ΔS=-0.0084412, ultra ΔS=-0.00823618, tight-to-ultra change ~2.05e-4.
- Fine Ob/ns 25-point exact map found only ~0.00465 additional improvement, below the 0.005 navigation gate at that scale.
- Model-internal large-lambda expansion identifies u=1/lambda_D as the natural leading dust-boundary coordinate.

## Current default-precision exact navigation record

From the first 25-point exact As-zre fine map:

- S_eff = **1050.2553996957809**
- S_k01 at the same point = **1050.2691358734728**
- lambda_D = 293868.81143246836
- h = 0.6903899123316766
- Omega_b = 0.046851744145772894
- Omega_m / Omega_khronon parameter = 0.25313821169954864
- A_s = 2.078203080347647e-9
- n_s = 0.9644164163369503
- z_re = 7.07112905430964
- logL_Planck = -501.597317289065
- chi2_SN = 39.550891596423256
- chi2_BOSS_eff = 7.509873521227489
- chi2_BOSS_k01 = 7.523609698919582
- r_d = 146.965419

Improvement relative to the previous As-zre center:

- eff: **0.0904338430200**
- k01: **0.0903139926493**

Both mappings selected the same physical point. However, the selected point lies on the upper z_re boundary of that 5x5 map, so the direction is still open.

## ❌ Not established

- The current 1050.2553997 point is **not** a certified 7D stationary point.
- Its latest ~0.0904 default-precision gain has not yet completed its own tight/ultra differential precision audit.
- Absolute CLASS high-l numerical convergence is not yet closed; ell sampling dominates the absolute shift.
- Dense BOSS mapping is not yet the production objective.
- A finite-lambda minimum is not proven.
- A lambda interval is not valid yet.
- No significance, Bayes factor, global model preference, or RTK-over-LambdaCDM claim is valid yet.

## Active computation streams

### A — strict 7D geometry

Workflow: `rtk-stage4d3-as-zre-finebest-recenter-both.yml`
Commit: `012cbbbdb32844f5100a2c0031556845d49092ba`
Run: `31917438959`

Six exact stationarity jobs: eff/k01 x scales 1.0, 0.5, 0.25, centered on S_eff=1050.2553996957809.

### B — second exact As-zre localization

Workflow: `rtk-as-zre-fine-scan-v2.yml`
Commit: `c01c6b6e6f7bf17e51c930bda2f2d51c40193bb9`
Run: `31917460024`

25 exact points around the current record, with delta A_s=5e-13 and delta z_re=0.0175, extending the previous upper-z_re boundary.

### C — CLASS precision structure

Workflow: `rtk-class-ell-sampling-crossgrid.yml`
Commit: `cdc749fe39044ff8cb6381905d5e18e803adc18f`

Separates l_logstep and l_linstep in a 3x3 cross-grid at two fixed RTK points.

### D — latest-record differential precision

Workflow: `rtk-class-precision-finebest-pair.yml`
Commit: `98bc8273d210eb5fb3a42e03cb093164c7747ba6`
Run: `31917523898`

Compares the previous As-zre center against the new S_eff=1050.2553996957809 record at baseline/tight/ultra settings.

## Immediate acceptance logic

1. Any new exact improvement >0.005 -> recenter immediately and repeat strict multiscale stationarity.
2. A boundary hit in the 2D As-zre map -> extend the map; do not call convergence.
3. A default-precision gain is promoted to a numerically credible direction only if it preserves sign and material size at tight/ultra and the tight-to-ultra differential change is <=~0.005.
4. Final inference waits for both converged CLASS precision and dense BOSS redshift mapping.
5. Only after re-optimization under the converged objective should the high-lambda profile be rebuilt in u=1/lambda_D and tested for an interior minimum versus the u=0 boundary.
