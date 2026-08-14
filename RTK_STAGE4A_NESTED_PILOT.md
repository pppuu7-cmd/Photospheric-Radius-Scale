# RT+DBI-Khronon — Stage 4A nested-sampling pilot

## Status

Stage 4A is a sampler/harness stress test only. It is **not** a converged posterior or Bayesian-evidence result.

Both the RTK and LCDM runs used the already validated official Planck 2018 Commander low-T + SimAll low-E + Plik-lite TTTEEE likelihood, Pantheon full covariance, and BOSS DR12 9x9 covariance. The primary BOSS mapping was the effective-growth `f sigma8`; the `k=0.1 h/Mpc` mapping was recorded for reweighting.

## Pilot priors and budget

Common uniform priors:

- h: [0.655, 0.705]
- Omega_b: [0.044, 0.052]
- Omega_m-sector parameter: [0.235, 0.285]
- A_s: [1.90e-9, 2.25e-9]
- n_s: [0.945, 0.985]
- z_reio: [4.5, 9.5]

RTK additionally used a log-uniform lambda_D prior [300, 30000].

Technical sampler settings: 24 live points, requested maxcall=260, dlogz target=5. Dynesty can exceed the nominal maxcall during final live-point handling, so the recorded call counts are larger.

## Result

| quantity | LCDM pilot | RTK pilot |
|---|---:|---:|
| exact CLASS/likelihood calls | about 295 | 313 |
| budget limited | yes | yes |
| effective posterior sample size | about 1.10 | about 1.00 |
| best sampled S_eff | 1098.8265 | 1087.4326 |
| previously validated focused local S_eff | 1059.1226 | 1060.4157 |
| pilot miss relative to known local score | +39.70 | +27.02 |

The RTK pilot best sampled point was approximately:

- lambda_D = 8390.15
- h = 0.68440
- Omega_b = 0.04653
- Omega_K0 = 0.25920
- A_s = 2.0146e-9
- n_s = 0.97090
- z_reio = 5.617
- S_eff = 1087.4326
- S_k0.1 = 1087.4014

The LCDM pilot best sampled point was approximately:

- h = 0.68402
- Omega_b = 0.04905
- Omega_cdm = 0.25507
- A_s = 2.0358e-9
- n_s = 0.97666
- z_reio = 5.935
- S_eff = 1098.8265

## Convergence diagnosis

Dynesty explicitly reported that the runs stopped because the maxcall/maxiter budget was reached before the requested delta(log Z) criterion was achieved. The resulting effective sample sizes are approximately one. Both samplers also failed to recover the already known focused local minima.

Therefore:

1. The Stage 4A posterior quantiles are not credible confidence/credible intervals.
2. The Stage 4A log-evidence values must not be used to quote a Bayes factor or model preference.
3. The difference between the best RTK and LCDM points found by these pilots is not a valid model comparison.
4. The useful result is operational: the exact-likelihood nested-sampling harness works, and the broad prior volume is too large for a ~300-call run.

## Next step: Stage 4B

Map the already validated likelihood basins with exact finite-difference evaluations around the focused RTK and LCDM minima. Build the local gradient, Hessian, eigen-directions and Gaussian proposal in normalized coordinates. Use the same exact likelihood and both RSD mappings. This is explicitly a **local basin recovery / proposal-construction stage**, not global Bayesian evidence.

Only after Stage 4B reproduces the known minima and gives a numerically stable positive local curvature should a longer posterior sampler be launched. A later broad-prior evidence run must retain a pre-declared broad prior and cannot inherit a narrow data-tuned prior while being called global evidence.
