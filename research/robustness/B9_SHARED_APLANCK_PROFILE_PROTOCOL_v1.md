# B9 shared-A_planck profile robustness protocol v1

Status: **PREREGISTERED BEFORE THE FIRST SHARED-APLANK COSMOLOGICAL SCORE.**

This is a separately labelled robustness variant motivated by the completed four-product contract audit `research/robustness/B9_PLANCK_CALIBRATION_CONTRACT_RESULT_v1.json`. It does not mutate, replace or retroactively reinterpret the frozen conditional-default A5 or B9-v1 objectives.

## Interface facts fixed before this variant

The pinned Planck R3 products used by the project — Commander lowT, SimAll lowE, Plik-lite TTTEEE and the selected non-CMB-marginalized lensing likelihood — each declare exactly one extra parameter named `A_planck`. Their distributed default values are not identical: lowT/Plik-lite use `1.000442`, while lowE/lensing use `1.0`.

The official Cobaya Planck calibration definition at public source commit `b76b6fed2a6c8c5594c6f92d5058bef10079746a` assigns the shared calibration parameter the Gaussian prior

`A_planck ~ Normal(1, 0.0025)`.

## Variant objective

For each cosmological point `theta`, generate the same CLASS spectra and non-Planck observables as B9-v1. Evaluate all four pinned Planck likelihoods with one common numerical value `A` inserted into every product's `A_planck` slot.

Define

`S_cal(theta,A) = chi2_SN(theta) + chi2_BOSS_eff(theta) - 2[logL_lowT(theta,A)+logL_lowE(theta,A)+logL_PlikLite(theta,A)+logL_lensing(theta,A)] + ((A-1)/0.0025)^2`.

The additive normalization constant of the Gaussian prior is omitted because it is common to both models and all cosmological points in this profile objective.

Define the profiled robustness objective

`S_B9cal(theta) = min_A S_cal(theta,A)`.

Production mapping remains `eff`; `k01` may be reported only as a diagnostic evaluated at the production-selected cosmological point.

Objective label:

`matched-ultra-linstep2+dense-BOSS+PlanckR3-lensing+shared-Aplanck-profile-v1`.

## Numerical A_planck profiling

The interval `[0.95,1.05]` is a numerical search bracket, not an additional physical prior. The Gaussian penalty above is the only calibration prior contribution.

At every cosmological point:

1. minimize the one-dimensional deterministic function `S_cal(theta,A)` on `[0.95,1.05]` using bounded scalar minimization with absolute `xatol <= 1e-10` and at least 200 allowed iterations;
2. evaluate the returned `A*` exactly again together with `A* +/- 1e-5`, `A* +/- 5e-5` when inside the bracket, and both bracket endpoints;
3. select the best exact nuisance evaluation among those values and the optimizer point;
4. fail closed if the best exact nuisance point lies within `5e-4` of either numerical bracket endpoint; do not widen the bracket after inspecting further cosmological scores without a separately recorded protocol amendment;
5. cache nuisance evaluations only by the exact cosmological spectrum fingerprint plus full-precision float `A`.

No distributed per-product default is permitted once this variant is entered: the same physical `A` must be inserted into all four `A_planck` slots.

## Cosmological reoptimization

This variant must not start heavy cosmological optimization until B9-v1 has produced stationarity-certified accepted LCDM and RTK centers. If B9-v1 has an unresolved boundary/localization issue, resolve that issue first.

Starting centers are the accepted B9-v1 centers. Use the same deterministic B9-v1 normalized cosmological search geometry:

- shared half-widths: `h=0.004`, `Ob=0.0008`, `Om=0.008`, `As=5e-11`, `ns=0.004`, `zre=0.8`;
- RTK additionally uses `log(lambda_D)` half-width `2.0`;
- deterministic COBYQA plus exact recentered polls with the same B9-v1 trust-region and poll semantics;
- exact full-precision success-only cosmology cache/retry semantics.

At each cosmological evaluation, the reported objective is the nested shared-`A_planck` profile `S_B9cal(theta)` above.

Boundary interpretation follows `B9_BOUNDARY_INTERPRETATION_GUARD_v1.md`: no boundary endpoint is an interior stationarity candidate.

## Certification and closure of this variant

A raw optimizer endpoint is insufficient. Independently certify the final LCDM 6D and RTK 7D cosmological points on the profiled objective using the same recenter tolerance `0.005`, base/half multiscale logic and positive-definite local Hessian requirements appropriate to B9-v1.

Then perform a fresh locked-tree replay of both accepted points, reproducing:

- all four Planck likelihood contributions at the accepted shared `A_planck`;
- the calibration-prior penalty;
- the profiled total objective;
- SN and BOSS components;

within `2e-6` total-score tolerance.

Only after paired stationarity and replay may the variant freeze the raw local robustness delta

`Delta S_B9cal = S_RTK,B9cal - S_LCDM,B9cal`.

## Interpretation boundaries

This profile variant tests sensitivity to the standard shared Planck calibration nuisance treatment. It is still a deterministic local profile-likelihood robustness calculation, not a posterior marginalization, global optimization, significance, AIC/BIC comparison or Bayes factor. It must be reported separately from B9-v1 and from the massless A1-A5 comparison.
