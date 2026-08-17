# Current RTK center is deep in the Khronon dust limit

Status: **derived from the validated current-center transition probe; model-internal diagnostic**.

Input provenance:
- transition run `32054604421`, artifact `9296007059`;
- current RTK center `lambda_D = 217644.75828347108`;
- extracted one-scale root `gamma = 0.05165838364253`;
- `x0 = 0.8138804588125383`.

The implemented stable background kernel uses

`x = x0/a^3`, `s = sqrt(1+lambda_D x^2)`, `r=x/s`, `t=x/(s+1)`,

`rho_K ∝ x(1+t)`,
`w_K = r t / [x(1+t)]`,
`c_a^2 = r/[s(s+x)]`,
`c_s^2(k,a)=c_a^2/[1+(k/k_star)^2]`.

## Current-center values

| z | w_K | c_a^2 |
|---:|---:|---:|
| 0.00 | 5.61847e-6 | 1.48362e-8 |
| 0.38 | 2.14136e-6 | 2.14808e-9 |
| 0.51 | 1.63493e-6 | 1.25160e-9 |
| 0.61 | 1.34899e-6 | 8.51865e-10 |
| 1.00 | 7.03929e-7 | 2.31818e-10 |

Thus the current Khronon background is extremely close to pressureless matter throughout the BOSS redshift range.

## Deviation from exact dust density scaling

Because `x ∝ a^-3`, exact dust would correspond to constant `(1+t)`. Relative to today's normalization,

`rho_K(a) / [rho_K(1) a^-3] = (1+t(a))/(1+t0)`.

The fractional excess over exact dust is:

| z | fractional deviation |
|---:|---:|
| 0.38 | +3.48e-6 |
| 0.51 | +3.99e-6 |
| 0.61 | +4.28e-6 |
| 1.00 | +4.92e-6 |
| 10 | +5.62e-6 |
| 1100 | +5.63e-6 |

So from today back to recombination the normalized background density departs from exact `a^-3` scaling by only about **5.6 parts per million** at this center.

## Perturbation implication on current linear survey scales

The transition probe gives `k_star(z=0)=1.686 h/Mpc`, increasing to `5.206 h/Mpc` at z=0.38 and `8.930 h/Mpc` at z=0.61. For BOSS-like k~0.1 h/Mpc, `k/k_star << 1`, so `c_s^2 ≈ c_a^2`; but `c_a^2` itself is already only 1e-8--1e-9. The Khronon therefore behaves very nearly as cold dust in both background and linear clustering over the compressed BOSS regime.

## Scientific consequence

The validated current-center signatures show percent-level changes in late-time geometry, linear power and growth. Those effects are orders of magnitude larger than the direct finite-pressure departure quantified above. Therefore the dominant origin of the present observable fingerprint cannot plausibly be the tiny finite-`lambda_D` background pressure alone; it must be dominated by the RT/nonlocal gravitational dynamics and correlated retuning of the shared cosmological parameters, with any finite-DBI correction subleading over the currently probed linear range.

This also provides a physical explanation for the nearly-flat `log(lambda_D)` Hessian direction found in the first RTK 7D stationarity calculation. At `lambda_D ~2.2e5` the model is already extremely close to its dust boundary, so large changes in lambda_D can have very small effects on the matched linear likelihood.

## Statistical boundary warning

If the repeated Hessian and explicit lambda diagnostics confirm continued flattening toward larger lambda_D, the correct interpretation may be a **dust-boundary/non-identifiable lambda direction**, not a well-resolved finite interior minimum. In that case ordinary interior-Wilks reasoning and naive counting of lambda_D as a normally identified extra parameter would require special care. No AIC/BIC/Bayes/significance conclusion is authorized from this observation alone.
