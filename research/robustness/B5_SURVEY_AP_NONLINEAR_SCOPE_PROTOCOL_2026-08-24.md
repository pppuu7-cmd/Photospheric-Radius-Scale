# B5 survey-window / AP / nonlinear RSD scope protocol — 2026-08-24

## Purpose

This note prevents the frozen B5 linear `fσ8(k,z)` test from being over-interpreted. A tiny linear scale dependence is necessary for the present compressed BOSS growth mapping to be plausible, but it is not sufficient to certify survey-level/full-shape adequacy.

## What the current production objective actually uses

The RTK production objective uses the published BOSS DR12 compressed measurements and their covariance at effective redshifts `z=0.38,0.51,0.61`. The prediction vector contains distance/expansion observables and one growth entry `fσ8` per redshift. It does not explicitly forward-model the galaxy multipoles, survey mask/window, nonlinear bias or fingers-of-God nuisance parameters.

## Why B5 must remain split

The BOSS DR12 power-spectrum RSD analysis fits monopole/quadrupole information over approximately `k=0.02...0.24 h/Mpc` (quadrupole starts at about `0.04 h/Mpc`) and jointly constrains `fσ8` with Alcock–Paczynski geometry. The published analysis emphasizes the multivariate covariance among `fσ8`, `H(z) r_s` and `D_A(z)/r_s`. Relevant references include Gil-Marín et al., MNRAS 460 (2016) 4188 and the final BOSS DR12 consensus literature.

Authoritative reference URLs:

- https://academic.oup.com/mnras/article/460/4/4188/2609021
- https://academic.oup.com/view-large/46473541
- https://academic.oup.com/mnras/article/469/2/1369/3586649

## Frozen decomposition

### B5-LIN — linear scale-dependence subgate

Question: over the actual BOSS Fourier range, how different is the scale-dependent RTK prediction `f(k,z) sigma8(z)` from the production effective value `d sigma8/d ln a`?

Already-frozen result path:

`research/robustness/B5_BOSS_LINEAR_SCALE_DEPENDENCE_RESULT_v1.json`

A PASS here may justify saying that *linear scale dependence alone* is negligible at the declared threshold. It cannot close B5-SURVEY.

### B5-SURVEY — survey/template adequacy subgate

Separate question: would an RTK forward model passed through the same survey window, AP deformation, nonlinear RSD/bias template and nuisance marginalization return compressed `{D_M,H,fσ8}` constraints consistent with using the published compressed Gaussian likelihood directly?

This requires one of the following before closure:

1. **Preferred direct route:** implement/reproduce a BOSS-style multipole likelihood or a sufficiently faithful public full-shape surrogate, inject the RTK linear spectra/growth, apply AP + survey window + nonlinear/bias/RSD nuisance treatment, and compare the resulting compressed prediction/likelihood shift against the present compressed objective; or
2. **Bound route:** derive a conservative, model-specific upper bound on the induced compressed-likelihood shift from all omitted survey/template effects and show it lies below a preregistered tolerance. The bound must cover AP coupling and nonlinear/template response, not only `fσ8(k)` variation.

## Quantities that must be preserved together

The B5-SURVEY comparison must treat at minimum the correlated block

`{D_M(z)/r_d, H(z) r_d, fσ8(z)}`

at the three effective redshifts. It must not vary growth while artificially holding AP geometry fixed if the underlying survey analysis couples them.

## Non-closure conditions

B5 remains OPEN if any of the following is true:

- only `fσ8(k)` scale dependence has been checked;
- a different `k_max`, redshift binning or AP convention is used without a controlled mapping;
- survey-window convolution is ignored without a quantitative bound;
- nonlinear/bias/RSD nuisance response is assumed to be LCDM-identical without an RTK-specific justification;
- a raw full-shape score is compared directly with the existing compressed-objective score.

## Next admissible implementation task

After `B5_BOSS_LINEAR_SCALE_DEPENDENCE_RESULT_v1.json` persists, inspect whether its maximum scale-dependent deviation is small enough to make a perturbative template-response bound meaningful. In parallel, inventory public BOSS DR12 window/multipole/model assets already present or reproducibly obtainable. Freeze a numerical B5-SURVEY target only after the exact observable vector, covariance/window inputs, nuisance treatment and comparison tolerance are specified.

## Guard

This protocol is robustness methodology only. It does not change the frozen A5 objective and cannot retroactively alter A5 scores. It prevents an under-scoped B5-LIN PASS from being promoted to a survey-level validation claim.
