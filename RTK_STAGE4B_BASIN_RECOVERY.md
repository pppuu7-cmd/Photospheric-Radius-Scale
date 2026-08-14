# RT+DBI-Khronon — Stage 4B exact local basin recovery

## Status

Stage 4B maps the exact local likelihood basins around the focused Stage 3 points using the corrected primordial inputs `A_s`, `n_s`, the official Planck 2018 Commander low-T + SimAll low-E + Plik-lite TTTEEE likelihood, Pantheon covariance, and BOSS DR12 9x9 covariance.

This stage is **not** a global posterior, global optimizer or Bayesian-evidence calculation. It is an exact finite local stencil used to diagnose curvature, degeneracies and optimizer bias before the next minimization/sampling stage.

## Exact design

The objective remains

S = -2 ln L_Planck + chi2_Pantheon + chi2_BOSS.

Both BOSS mappings are retained:

- `eff`: effective growth derived from sigma8(a),
- `k01`: f(k=0.1 h/Mpc) sigma8.

The RTK stencil used 7 normalized coordinates: log(lambda_D), h, Omega_b, Omega_K0, A_s, n_s and z_reio. The LCDM stencil used the analogous six coordinates excluding lambda_D. Symmetric axes and pairwise cross terms were evaluated with the exact CLASS likelihood.

A per-CLASS timeout was added to the inference harness so pathological parameter points cannot hang an inference workflow.

## Center regression

The Stage 3 points were reproduced to numerical tolerance. For RTK the recomputed center differed from the earlier saved objective by only about 0.0023, consistent with the independent rerun path.

## New best exact points found in the Stage 4B stencil

| model | lambda_D | h | Omega_b | Omega_m-sector | A_s | n_s | z_reio | S_eff | S_k0.1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LCDM | - | 0.6765 | 0.0480 | 0.255 | 2.100e-9 | 0.9675 | 8.0 | 1051.26174152 | 1051.26277814 |
| RTK | 1322.81487 | 0.6840 | 0.0475 | 0.260 | 2.037e-9 | 0.9630 | 6.0 | 1059.99936843 | 1058.98527599 |

The RTK point is the +1 finite-difference step in log(lambda_D) relative to the previous lambda_D=1150 center. It improves the RTK objective but does not establish the RTK minimum.

The LCDM point is a correlated move with h=0.6765 and Omega_cdm=0.255. It improves the previously used Stage 3 LCDM reference by about 7.86 objective units. Therefore the Stage 3 near-tie was not a matched-minimum comparison.

### Current finite-stencil comparison

Using effective-growth BOSS mapping:

Delta S_RTK-LCDM = 1059.99936843 - 1051.26174152 = +8.73762691.

Using k=0.1 h/Mpc BOSS mapping:

Delta S_RTK-LCDM = 1058.98527599 - 1051.26277814 = +7.72249785.

These values describe only the best points actually tested in the Stage 4B local stencil. They are **not** global Delta chi2 values, exclusion significances, posterior odds or Bayes factors.

## Component decomposition at the best tested effective-growth points

LCDM:

- log L_Planck = -502.61973938
- chi2_SN = 39.76795709
- chi2_BOSS_eff = 6.25430568
- chi2_BOSS_k0.1 = 6.25534230
- r_d = 147.974364 Mpc

RTK:

- log L_Planck = -505.52209212
- chi2_SN = 39.29158003
- chi2_BOSS_eff = 9.66360417
- chi2_BOSS_k0.1 = 8.64951172
- r_d = 146.798022 Mpc

For the effective-growth comparison this gives approximately:

- Planck: RTK worse by +5.805 in the objective;
- Pantheon: RTK better by -0.476;
- BOSS: RTK worse by +3.409;
- net: +8.738.

Thus the updated local comparison differs qualitatively from the earlier Stage 3 decomposition: after the improved LCDM local point is found, Planck as well as BOSS contributes to the current RTK penalty.

## Local curvature and degeneracies

The finite-difference Hessians are positive definite at both Stage 3 centers, but strongly ill-conditioned.

RTK effective-growth normalized Hessian eigenvalues:

0.0845, 0.1253, 0.2188, 0.9802, 10.9213, 131.5855, 312.9803,

with absolute condition number about 3.7e3. For the k=0.1 mapping the condition number is about 6.5e3.

LCDM shows the same qualitative degeneracy structure, with condition number about 2.5e3.

Strong local correlations include approximately:

- h versus Omega_m-sector: about -0.99,
- h versus Omega_b: about -0.91,
- Omega_b versus Omega_m-sector: about +0.94,
- A_s versus z_reio: about +0.976.

For RTK the lambda_D direction is especially soft in this local quadratic approximation. The corresponding quadratic width is much larger than the finite-difference log-lambda step, so it must not be interpreted as a credible interval.

## Why the Newton proposal was rejected

Although the local Hessian is positive definite, the full Newton displacement is several normalized steps along the soft directions. After clipping it to the trust region and evaluating the exact likelihood, both RTK and LCDM candidate points became substantially worse.

Therefore the quadratic model is useful for identifying correlations and soft directions but is not reliable for a multi-step jump. A Hessian-based Newton optimizer should not be used directly here.

## Consequence for the previous Stage 3 comparison

The earlier focused result Delta S approximately +1.29 (`eff`) and +0.04 (`k01`) is superseded as a matched-minimum diagnostic. It remains a valid comparison of those particular Stage 3 parameter points, but Stage 4B demonstrates that the LCDM control had a substantially lower nearby point that the earlier coordinate search missed.

No claim that RTK is excluded follows from Stage 4B, because the RTK basin has also not yet been fully minimized and the RSD mapping remains approximate for scale-dependent growth.

## Next step — Stage 4C

Run a bounded, correlation-aware derivative-free exact optimizer separately for RTK and LCDM, starting from the new Stage 4B best points. Use multiple starts/order-independent checks and small trust boxes. The optimizer should stop only after independent local perturbations fail to improve S by more than a predeclared numerical tolerance.

Only after the two local minima are stable should a local MCMC/posterior run be initialized. A future broad-prior Bayesian-evidence run must keep independently declared broad priors; a data-tuned Stage 4C trust box must not be relabeled as a global evidence prior.
