# RT+DBI-Khronon — Stage 4B exact local basin recovery

## Status

Stage 4B maps the exact local likelihood basins around the focused Stage 3 points using the corrected primordial inputs `A_s`, `n_s`, the official Planck 2018 Commander low-T + SimAll low-E + Plik-lite TTTEEE likelihood, Pantheon covariance, and BOSS DR12 9x9 covariance.

This stage is **not** a global posterior, global optimizer or Bayesian-evidence calculation. It is an exact finite local stencil used to diagnose curvature, degeneracies and optimizer bias before the next minimization/sampling stage.

> **Correction note.** An earlier prose summary copied the wrong LCDM coordinates/components while quoting a low objective value from the Stage 4B run. The archived `basin_summary.json` and `basin_points.csv` are the source of truth. The corrected values below come directly from those artifacts.

## Exact design

The objective remains

S = -2 ln L_Planck + chi2_Pantheon + chi2_BOSS.

Both BOSS mappings are retained:

- `eff`: effective growth derived from sigma8(a),
- `k01`: f(k=0.1 h/Mpc) sigma8.

The RTK stencil used 7 normalized coordinates: log(lambda_D), h, Omega_b, Omega_K0, A_s, n_s and z_reio. The LCDM stencil used the analogous six coordinates excluding lambda_D. Symmetric axes and pairwise cross terms were evaluated with the exact CLASS likelihood.

A per-CLASS timeout was added to the inference harness so pathological parameter points cannot hang an inference workflow.

## Center regression

The Stage 3 points were reproduced to numerical tolerance. For RTK the recomputed center differed from the earlier saved objective by only about 0.0023, consistent with the independent rerun path. The LCDM Stage 3 center was reproduced at S_eff = 1059.12261372 and S_k0.1 = 1059.12427144.

## Best exact points actually present in the Stage 4B artifacts

| model | lambda_D | h | Omega_b | Omega_m-sector | A_s | n_s | z_reio | S_eff | S_k0.1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LCDM | - | 0.675000 | 0.04897310 | 0.26553984 | 2.0983169e-9 | 0.96368472 | 7.5583993 | **1051.26474145** | 1051.26534416 |
| RTK | 1322.81487 | 0.684000 | 0.04750000 | 0.26000000 | 2.0370000e-9 | 0.96300000 | 6.0000000 | **1059.99936843** | **1058.98527599** |

For LCDM the independently constructed `k01` Newton candidate is extremely close but not identical: S_k0.1 = 1051.26676765. The table reports the single exact point that is best for the `eff` objective and also has the lowest `k01` value among the stored evaluated points.

The RTK point is the +1 finite-difference step in log(lambda_D) relative to the previous lambda_D=1150 center. It improves the RTK objective but does not establish the RTK minimum.

The LCDM point is the clipped Newton/trust-region candidate built from the local Hessian. It improves the Stage 3 LCDM center by about 7.858 objective units for both mappings. Its normalized h displacement is exactly -2 in the Stage 4B trust coordinates, so it lies on the trust-region boundary and therefore is **not** evidence that the LCDM local minimum has been reached.

### Current Stage 4B finite-design comparison

Using effective-growth BOSS mapping:

Delta S_RTK-LCDM = 1059.99936843 - 1051.26474145 = **+8.73462698**.

Using the lowest stored k=0.1 objective values:

Delta S_RTK-LCDM = 1058.98527599 - 1051.26534416 = **+7.71993184**.

These values describe only the best exact points actually present in the Stage 4B design. They are **not** global Delta chi2 values, exclusion significances, posterior odds or Bayes factors.

## Component decomposition at the corrected best tested effective-growth points

LCDM:

- log L_Planck = -501.75583077
- chi2_SN = 40.07563743
- chi2_BOSS_eff = 7.67744248
- chi2_BOSS_k0.1 = 7.67804518
- r_d = 146.898851 Mpc

RTK:

- log L_Planck = -505.52209212
- chi2_SN = 39.29158003
- chi2_BOSS_eff = 9.66360417
- chi2_BOSS_k0.1 = 8.64951172
- r_d = 146.798022 Mpc

For the effective-growth comparison this gives approximately:

- Planck: RTK worse by +7.533 in the objective;
- Pantheon: RTK better by -0.784;
- BOSS: RTK worse by +1.986;
- net: +8.735.

Thus at these particular Stage 4B points the dominant current penalty comes from Planck, with a smaller BOSS contribution partially offset by Pantheon. This decomposition is local and will change when either model is further minimized.

## Local curvature and degeneracies

The finite-difference Hessians are positive definite at both Stage 3 centers, but strongly ill-conditioned.

RTK effective-growth normalized Hessian eigenvalues:

0.0845, 0.1253, 0.2188, 0.9802, 10.9213, 131.5855, 312.9803,

with absolute condition number about 3.7e3. For the k=0.1 mapping the condition number is about 6.5e3.

LCDM has condition number about 1.43e3 for both mappings. Strong local correlations remain present, so one-dimensional coordinate optimization is not reliable for matched-minimum comparison.

For RTK the lambda_D direction is especially soft in this local quadratic approximation. The corresponding quadratic width is much larger than the finite-difference log-lambda step, so it must not be interpreted as a credible interval.

## What the Newton proposals actually showed

The two models behaved differently and must not be conflated.

For RTK the Hessian-based Newton displacement was several normalized steps along soft directions. After trust clipping, the exact likelihood became worse by about 14.87 (`eff`) and 11.98 (`k01`). Therefore a large direct Newton jump is unreliable for RTK.

For LCDM the clipped Newton candidate instead improved the exact objective by about 7.858. However its h coordinate hit the -2 trust boundary. This means the quadratic direction was useful as a basin-recovery hint, but Stage 4B did not contain the LCDM minimum; the next local optimizer must expand around the recovered candidate.

## Consequence for the previous Stage 3 comparison

The earlier focused result Delta S approximately +1.29 (`eff`) and +0.04 (`k01`) is superseded as a matched-minimum diagnostic. It remains a valid comparison of those particular Stage 3 parameter points, but Stage 4B demonstrates that the LCDM control had a substantially lower nearby basin direction that the earlier coordinate search missed.

No claim that RTK is excluded follows from Stage 4B, because neither model has yet been shown to be at a stable matched local minimum, and the RSD mapping remains approximate for scale-dependent growth.

## Next step — Stage 4C

Run a bounded, derivative-free exact optimizer separately for RTK and LCDM, starting from the artifact-verified Stage 4B best points. Use multiple starts and an independent exact local poll. If the best point lies on a bound, expand that direction rather than calling the result converged.

Only after the two local minima are stable should a local MCMC/posterior run be initialized. A future broad-prior Bayesian-evidence run must keep independently declared broad priors; a data-tuned Stage 4C trust box must not be relabeled as a global evidence prior.
