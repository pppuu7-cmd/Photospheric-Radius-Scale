# RT + DBI-Khronon: five-point lambda_D growth scan

Run: GitHub Actions `RTK CLASS build`, run 31767294239 (2026-08-14).

Fixed baseline for this diagnostic scan:

- h = 0.67556
- Omega_b = 0.049
- Omega_K0 = 0.26
- Omega_cdm = 0 in RTK
- A_s = 2.1e-9
- n_s = 0.965
- lambda_D = 8000, 10000, 12500, 15000, 20000
- P(k,z) tabulated over z = 0 ... 3 and k up to 5 h/Mpc
- matched LCDM control has Omega_cdm = 0.26

This is a fixed-parameter diagnostic comparison, **not an observational likelihood constraint**.

## Background closure

| lambda_D | gamma | F(gamma) |
|---:|---:|---:|
| 8000  | 0.05105086218772 | -1.12e-9 |
| 10000 | 0.05105105024118 | -8.08e-9 |
| 12500 | 0.05105120365372 | +5.23e-9 |
| 15000 | 0.05105130262980 | -8.68e-9 |
| 20000 | 0.05105143129898 | +6.47e-9 |

The RT background closure gamma is almost insensitive to lambda_D across this interval.

## Linear P(k,z=0) / matched LCDM

| lambda_D | k=0.05 | k=0.10 | k=0.20 | k=0.50 | k=1.00 |
|---:|---:|---:|---:|---:|---:|
| 8000  | 1.022864 | 1.018182 | 1.003681 | 0.954260 | 0.890312 |
| 10000 | 1.023135 | 1.019675 | 1.008378 | 0.966236 | 0.907790 |
| 12500 | 1.023315 | 1.020776 | 1.012116 | 0.976798 | 0.924057 |
| 15000 | 1.023414 | 1.021449 | 1.014555 | 0.984385 | 0.936385 |
| 20000 | 1.023509 | 1.022203 | 1.017472 | 0.994513 | 0.953979 |

k is in h/Mpc. Increasing lambda_D shifts the late small-scale suppression to smaller physical scales (larger k): suppression at fixed k is weaker for larger lambda_D.

## Redshift evolution of the ratio

At z=1 the same ratios are already close to unity:

| lambda_D | P(.2)/LCDM | P(.5)/LCDM | P(1)/LCDM |
|---:|---:|---:|---:|
| 8000  | 1.012583 | 1.010588 | 1.004002 |
| 10000 | 1.012640 | 1.011208 | 1.006344 |
| 12500 | 1.012676 | 1.011650 | 1.008082 |
| 15000 | 1.012694 | 1.011915 | 1.009155 |
| 20000 | 1.012710 | 1.012207 | 1.010374 |

At z=2 the sampled k=0.05--1 h/Mpc ratios are all approximately 1.0059; at z=3 they are approximately 1.0031. Thus the scale-dependent suppression develops mainly at late times.

Approximate redshift where P_RTK/P_LCDM crosses unity, obtained by linear interpolation in the diagnostic redshift grid:

| lambda_D | k=0.5 crossing z | k=1 crossing z |
|---:|---:|---:|
| 8000  | 0.448 | 0.923 |
| 10000 | 0.396 | 0.836 |
| 12500 | 0.334 | 0.709 |
| 15000 | 0.271 | 0.546 |
| 20000 | 0.133 | 0.450 |

These crossings are derived diagnostics, not fitted observables.

## sigma8

Matched LCDM gives sigma8(z=0) = 0.8388853 for this fixed primordial normalization.

| lambda_D | sigma8(z=0) | ratio to LCDM |
|---:|---:|---:|
| 8000  | 0.8406831 | 1.00214 |
| 10000 | 0.8424374 | 1.00423 |
| 12500 | 0.8438635 | 1.00593 |
| 15000 | 0.8448155 | 1.00707 |
| 20000 | 0.8459887 | 1.00847 |

The slightly larger sigma8 is not inconsistent with the suppression at k >= 0.5 h/Mpc: the sigma8 window also receives weight from k around 0.1--0.2 h/Mpc, where this fixed-parameter RTK comparison has a small power enhancement.

Numerical sensitivity of sigma8 to truncating the integration at k=3 instead of 5 h/Mpc is below 3.6e-5 fractionally in the scan.

## Growth and f sigma8 diagnostics

Because RTK growth is scale dependent, there is no single survey-independent scalar f sigma8 without specifying the RSD observable/window. We therefore record two diagnostics:

1. `fs8_eff = d sigma8 / d ln a`, a sigma8-window-weighted effective growth diagnostic.
2. `fs8_k0p1 = f(k=0.1,z) sigma8(z)`, with f(k,z)=0.5 d ln P(k,z)/d ln a.

LCDM reference:

| z | sigma8 | fs8_eff | f(k=.1) sigma8 |
|---:|---:|---:|---:|
| 0.0 | 0.8388853 | 0.4378945 | 0.4373590 |
| 0.5 | 0.6464693 | 0.4882503 | 0.4885885 |
| 1.0 | 0.5107137 | 0.4457966 | 0.4458537 |
| 2.0 | 0.3514463 | 0.3363555 | -- |

RTK `fs8_eff`:

| lambda_D | z=0 | ratio/LCDM | z=.5 | ratio/LCDM | z=1 | ratio/LCDM |
|---:|---:|---:|---:|---:|---:|---:|
| 8000  | 0.4097794 | 0.93579 | 0.4932267 | 1.01019 | 0.4531044 | 1.01639 |
| 10000 | 0.4158551 | 0.94967 | 0.4947422 | 1.01330 | 0.4533376 | 1.01692 |
| 12500 | 0.4211989 | 0.96187 | 0.4958881 | 1.01564 | 0.4535050 | 1.01729 |
| 15000 | 0.4250121 | 0.97058 | 0.4966066 | 1.01711 | 0.4536055 | 1.01752 |
| 20000 | 0.4300422 | 0.98207 | 0.4974362 | 1.01881 | 0.4537167 | 1.01777 |

At z=0 the window-weighted growth is lower than the matched LCDM control, most strongly for the smallest lambda_D. Around z=0.5--1 the same diagnostic is about 1--2% above the fixed LCDM control. This time dependence is potentially useful for RSD tests, but it is not itself an RSD likelihood.

At z=0, the scale-specific diagnostic f(k=.1) sigma8 / LCDM is:

- lambda_D=8000: 0.97681
- 10000: 0.98571
- 12500: 0.99272
- 15000: 0.99723
- 20000: 1.00258

The difference between `fs8_eff` and `fs8_k0p1` is itself evidence of scale-dependent growth and is why a future RSD comparison must use each survey's actual scale/window dependence rather than a single universal f sigma8 number.

## What this scan establishes

Code/numerics:

- all five RTK models build and run to completion in the same patched RT-CLASS pipeline;
- positive log-gamma closure succeeds for all five points;
- multi-redshift P(k,z) is finite and analyzable;
- the old CLASS 2.4.5 z=0 spline-endpoint roundoff was isolated and patched with an endpoint guard;
- the full growth-analysis sanity gate passes.

Physics at fixed baseline parameters:

- gamma changes only at the ~1e-5 relative level over lambda_D=8000--20000;
- the characteristic late scale dependence is monotonic with lambda_D;
- at z >= 2 the sampled linear spectra are nearly scale-independent relative to the matched LCDM control;
- the strong small-scale suppression is predominantly a low-redshift effect;
- sigma8 alone hides much of the scale-dependent suppression, so P(k,z) and RSD/lensing are more discriminating.

## Not established yet

This scan does **not** show that any lambda_D value is observationally allowed or preferred. The baseline cosmological parameters were held fixed rather than refitted. The next stage is a likelihood-level comparison, starting with a controlled coarse fit of CMB/background/growth observables and then a joint CMB+BAO+SNe+RSD+lensing analysis.
