# RT+DBI-Khronon — Stage 4D3 numerical proof gate

## Claim being tested

The strongest claim tested here is deliberately narrower than an observational discovery claim:

> Within the current Stage-4D exact CLASS + Planck-primary + Pantheon + BOSS likelihood harness, RT+DBI-Khronon possesses a numerically established local **interior** likelihood minimum at finite positive `lambda_D`, rather than only a boundary/asymptotic dust minimum or an optimizer artifact.

This document must **not** be used to claim that RTK is observationally proven, preferred over LCDM, globally best fitting, or statistically detected. Those stronger statements require a global posterior/evidence analysis, calibrated likelihood-ratio statistics, realistic neutrino sector, and a survey-window treatment of the scale-dependent RSD observable.

## Objective

`S = -2 ln L_Planck + chi2_Pantheon + chi2_BOSS`.

Two BOSS/RSD mappings are retained:

- `eff`: effective `d sigma8 / d ln a` diagnostic;
- `k01`: scale-specific `f(k=0.1 h/Mpc,z) sigma8(z)` diagnostic.

Neither is a final survey-window RSD likelihood for a scale-dependent-growth model.

## Predeclared PASS gates

A Stage-4D3 **NUMERICAL INTERIOR MINIMUM PASS** may be issued only if all of the following pass after the exact-float cache correction.

### N1 — exact-float likelihood evaluation

The generated inference core must not round physical parameters in its cache key. In particular the former

`round(float(p[k]),12)`

cache key is forbidden because it aliases small changes of `A_s ~ 2e-9`.

All proof-grade optimizer and stationarity runs must use exact Python floating-point parameter values as cache keys.

### N2 — independent finite-lambda optimization

At least one bounded derivative-free trust-region optimizer must converge to a finite-lambda basin without a parameter-box boundary hit. A second independent optimization path or cross-seed must reproduce the basin to the stated numerical tolerance.

### N3 — free lambda direction

A seven-dimensional local optimization over

`(log lambda_D, h, Omega_b, Omega_K0, A_s, n_s, z_reio)`

must return an interior `lambda_D`. Hitting either imposed log-lambda boundary fails this gate and requires a widened search.

### N4 — two-sided fixed-lambda profile

After equal-depth reoptimization of the other six parameters, fixed-lambda points on both sides of the candidate must have larger objective values. Neighbor points must be optimized with the same exact-float likelihood core and comparable numerical depth.

### N5 — local 7-D stationarity

At the final free-lambda candidate, an exact central finite-difference axis/cross stencil including the `log lambda_D` coordinate must satisfy all of:

1. no exact stencil/Newton point improves the center by more than `0.005` in S;
2. the seven-dimensional finite-difference Hessian is positive definite at the accepted stencil scale;
3. the result is stable under at least one smaller stencil scale (normally `1/2` of the base step);
4. the finite-difference gradient does not reveal a repeatable downhill direction requiring another optimizer pass.

If a smaller stencil finds a new downhill point, the center is reseeded and N5 repeats; the old center is not accepted.

### N6 — high-lambda competing basin

The large-lambda tail must be cross-seeded from its deepest known basin and optimized with the same exact-float core. A finite interior claim requires the final finite candidate to remain below the best high-lambda competitor at comparable optimization/stationarity depth.

### N7 — RSD-mapping robustness

The finite-basin location must remain qualitatively present under both `eff` and `k01`. The exact lambda minima need not coincide, because the two mappings are different diagnostics, but neither mapping may force the optimum solely to the high-lambda boundary within the tested range without explicit discussion.

### T1 — DBI physical-branch implementation stability

The model implementation must retain positive DBI branch margin and physical background/sound-speed quantities across the candidate region and a wider stress domain.

**Status: PASS.** Stage-4D3 stress test evaluated 263,424 states across `lambda_D=1e3...1e8`, `gamma=1e-4...1`, `Omega_K0=0.20...0.32`, `a=1e-10...1`, and `k=0...1e3`. It found zero violations. Maximum present-normalization residual was about `5.17e-16`; maximum error in the exact branch identity `dbi_margin * s^2 = 1` was about `2.22e-16`; the minimum stored DBI margin remained strictly positive.

This T1 result is a numerical implementation/branch-stability result. It is not a proof of quantum stability, UV completion, naturalness, nonlinear galaxy phenomenology, or full covariant perturbative health beyond the implemented effective fluid system.

### R1 — likelihood-harness consistency

Pantheon full covariance and analytically profiled additive magnitude offset, BOSS DR12 9x9 covariance ordering, model-specific drag horizon, and Planck-primary likelihood inputs must be internally consistent. Any newly found harness defect invalidates affected earlier proof-grade results and triggers reruns.

**Important correction already applied:** the inference cache previously rounded all physical parameters to 12 decimal places, which was too coarse for `A_s`. The proof-grade core now uses exact floating-point parameter tuples. Pre-correction sub-unit optimizer results are retained only as seeds/diagnostics.

## LCDM comparison gate

A numerical finite RTK minimum can be established independently of LCDM. However any quoted `Delta S = S_RTK - S_LCDM` after the cache correction must use a newly reoptimized LCDM control generated by the same exact-float likelihood core. The older Stage-4C LCDM minima are retained only as pre-correction references until rerun.

## Current status

`STAGE4D3_VERDICT = RUNNING / NOT YET ESTABLISHED`

Reason: T1 has passed and R1 has been tightened, but the exact-float seven-dimensional optimization, fine fixed-lambda profile, mapping cross-checks, high-lambda comparison, and final 7-D stationarity/Hessian checks are still being completed.

The verdict may be changed to PASS only by updating this file with exact workflow provenance and all gate outcomes. A visually U-shaped profile alone is insufficient.
