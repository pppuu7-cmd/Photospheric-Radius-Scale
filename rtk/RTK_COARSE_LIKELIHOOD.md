# RT+DBI-Khronon: first coarse observational diagnostic

Status: **diagnostic only; not an official cosmological likelihood**.

Successful CI run: GitHub Actions run 48 (`31768430335`). The pipeline built the patched RT-CLASS code, ran the five-point grid `lambda_D = 8000, 10000, 12500, 15000, 20000`, ran the matched LCDM control, generated multi-redshift spectra/growth tables, and completed the coarse observational score.

## What is included

- Pantheon 40-bin SN Hubble diagram: diagonal binned errors plus a 0.02 mag floor; the absolute magnitude/H0 offset is analytically minimized.
- BOSS DR12 anisotropic BAO at z=0.38, 0.51, 0.61: diagonal approximation in this first pass.
- BOSS DR12 RSD at z=0.38, 0.51, 0.61: both an effective `d sigma8 / d ln a` mapping and a `k=0.1 h/Mpc` growth diagnostic are reported because RTK growth is scale dependent.
- CMB TT shape-consistency proxy relative to the matched LCDM run over ell=30..1200. **This is not a Planck likelihood and must not be interpreted as a Planck chi-square.**
- BAO uses the exact CLASS baryon-drag redshift and comoving sound horizon parsed from each model's thermodynamics output.

## Main results

| model | lambda_D | z_drag | r_d [Mpc] | chi2_SN | chi2_BAO | chi2_RSD_eff | Delta chi2 (SN+BAO+RSD_eff) | CMB TT proxy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| LCDM | - | 1059.859 | 147.4595 | 35.2037 | 3.7669 | 1.6670 | 0.0000 | 0.000 |
| RTK | 8000 | 1059.861 | 147.4549 | 32.6240 | 8.5219 | 1.9144 | **+2.4225** | 73.318 |
| RTK | 10000 | 1059.860 | 147.4558 | 32.6235 | 8.5199 | 2.0738 | +2.5795 | 73.484 |
| RTK | 12500 | 1059.860 | 147.4566 | 32.6231 | 8.5184 | 2.2016 | +2.7054 | 73.612 |
| RTK | 15000 | 1059.860 | 147.4571 | 32.6229 | 8.5173 | 2.2853 | +2.7879 | 73.709 |
| RTK | 20000 | 1059.860 | 147.4577 | 32.6226 | 8.5160 | 2.3858 | +2.8868 | 73.827 |

The least-penalized point in the current fixed grid is `lambda_D=8000`, with

`Delta chi2_coarse = +2.422516`

relative to the matched LCDM control for the simplified SN+BAO+RSD_eff score.

## Interpretation

The current grid is mildly worse than matched LCDM in the simplified combined real-data score, but the result is a trade-off: the SN term improves by about 2.58 in chi-square, while BAO worsens by about 4.75 and dominates the net penalty. The RSD penalty is smaller and grows with lambda_D across this grid.

The best point occurs at the lower boundary of the tested interval, so this scan does **not** define a preferred lambda_D interval. It motivates extending the grid below 8000 before making any parameter statement.

The near equality of `z_drag` and `r_d` across the grid confirms that the early standard ruler is almost unchanged in these runs; the BAO penalty is therefore mainly a late-time distance/expansion-history issue rather than a large shift of the drag horizon.

The CMB TT proxy is large compared with the matched control because percent-level spectral differences accumulate over many multipoles under the chosen diagnostic weighting. It is only a warning that CMB may be constraining. The next decisive step is an official CMB likelihood (or a validated Planck-lite equivalent), not treating the proxy number as statistical evidence.

## Required next validation

Before observational claims, replace the coarse ingredients by full covariance/official likelihood implementations: Pantheon/Pantheon+ covariance, BOSS/eBOSS or DESI BAO covariance as chosen, an RSD likelihood that handles scale-dependent growth consistently, and an official CMB likelihood. Only then should confidence intervals, model comparison statistics, or claims of competitiveness with LCDM be reported.
