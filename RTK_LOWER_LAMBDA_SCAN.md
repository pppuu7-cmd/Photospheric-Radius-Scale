# RT+DBI-Khronon lower-lambda coarse scan

GitHub Actions run 56 completed successfully after extending the RTK CLASS grid to lambda_D = 4000, 5000, 6000, 7000 in addition to the previous 8000, 10000, 12500, 15000, 20000 points.

This remains a coarse diagnostic, not an official cosmological likelihood. Pantheon uses binned diagonal errors with a 0.02 mag floor, BOSS BAO/RSD use diagonal approximations, and the CMB term is a matched-LCDM TT-shape proxy rather than a Planck likelihood.

## Coarse likelihood results

| model | lambda_D | z_drag | r_d [Mpc] | chi2_SN | chi2_BAO | chi2_RSD_eff | CMB shape proxy | Delta chi2 (SN+BAO+RSD_eff) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| LCDM | - | 1059.859 | 147.4595 | 35.2037 | 3.7669 | 1.6670 | 0.000 | 0.0000 |
| RTK | 4000 | 1059.862 | 147.4503 | 32.6262 | 8.5315 | 1.2051 | 72.528 | **1.7252** |
| RTK | 5000 | 1059.861 | 147.4521 | 32.6253 | 8.5277 | 1.4665 | 72.854 | 1.9818 |
| RTK | 6000 | 1059.861 | 147.4534 | 32.6247 | 8.5251 | 1.6582 | 73.053 | 2.1703 |
| RTK | 7000 | 1059.861 | 147.4542 | 32.6243 | 8.5232 | 1.8026 | 73.203 | 2.3125 |
| RTK | 8000 | 1059.861 | 147.4549 | 32.6240 | 8.5219 | 1.9144 | 73.318 | 2.4225 |
| RTK | 10000 | 1059.860 | 147.4558 | 32.6235 | 8.5199 | 2.0738 | 73.484 | 2.5795 |
| RTK | 12500 | 1059.860 | 147.4566 | 32.6231 | 8.5184 | 2.2016 | 73.612 | 2.7054 |
| RTK | 15000 | 1059.860 | 147.4571 | 32.6229 | 8.5173 | 2.2853 | 73.709 | 2.7879 |
| RTK | 20000 | 1059.860 | 147.4577 | 32.6226 | 8.5160 | 2.3858 | 73.827 | 2.8868 |

The best tested RTK point by the real-data coarse score SN+BAO+RSD_eff is lambda_D=4000 with Delta chi2 = +1.725202 relative to the matched LCDM control. Since 4000 is the lower edge of the tested grid, this does not identify an interior best fit; the scan should be extended to lower lambda_D before interpreting a preferred scale.

## Growth diagnostics

| lambda_D | gamma | sigma8(z=0) | fs8_eff(z=0) | P_RTK/P_LCDM k=0.2 | k=0.5 | k=1.0 |
|---:|---:|---:|---:|---:|---:|---:|
| 4000 | 0.0510499195 | 0.8326983 | 0.3868633 | 0.9817035 | 0.9084011 | 0.8295724 |
| 5000 | 0.0510502956 | 0.8357275 | 0.3948159 | 0.9900997 | 0.9245260 | 0.8500495 |
| 6000 | 0.0510505479 | 0.8378685 | 0.4009395 | 0.9960044 | 0.9367660 | 0.8661732 |
| 7000 | 0.0510507286 | 0.8394586 | 0.4058102 | 1.0003577 | 0.9464231 | 0.8793194 |
| 8000 | 0.0510508622 | 0.8406831 | 0.4097794 | 1.0036810 | 0.9542598 | 0.8903122 |
| 10000 | 0.0510510502 | 0.8424374 | 0.4158551 | 1.0083779 | 0.9662360 | 0.9077898 |
| 12500 | 0.0510512037 | 0.8438635 | 0.4211989 | 1.0121162 | 0.9767976 | 0.9240566 |
| 15000 | 0.0510513026 | 0.8448155 | 0.4250121 | 1.0145545 | 0.9843851 | 0.9363854 |
| 20000 | 0.0510514313 | 0.8459887 | 0.4300422 | 1.0174724 | 0.9945133 | 0.9539792 |

The lower-lambda extension strengthens late scale-dependent suppression. At lambda_D=4000, sigma8 is lower than the matched LCDM value 0.8388853, and the z=0 power ratios are below unity already at k=0.2 h/Mpc and increasingly suppressed at k=0.5 and 1 h/Mpc.

## Interpretation

1. The coarse SN term prefers the RTK background relative to this fixed matched LCDM control, while BAO remains the dominant penalty.
2. Lower lambda_D improves the RSD_eff contribution enough that the total coarse SN+BAO+RSD score decreases monotonically from lambda_D=20000 to 4000.
3. The drag horizon remains extremely close to LCDM throughout the scan, so the BAO penalty is primarily a late-time geometry issue rather than a large early-time standard-ruler shift.
4. The CMB TT proxy also decreases toward lower lambda_D, but it is not an official Planck likelihood and must not be interpreted as a statistical exclusion or confidence interval.
5. No observational best-fit lambda_D has been established. The current result only says that the minimum of this fixed-parameter coarse grid lies below 4000.

Recommended next grid: lambda_D = 1000, 2000, 3000, 4000 (with intermediate refinement if the score turns over), followed by full covariance and official likelihood implementation before parameter inference claims.
