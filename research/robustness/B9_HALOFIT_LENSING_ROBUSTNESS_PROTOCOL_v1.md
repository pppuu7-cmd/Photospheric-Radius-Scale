# B9 Halofit nonlinear-lensing robustness protocol v1

Status: **PREREGISTERED BEFORE THE FIRST B9-HALOFIT COSMOLOGICAL SCORE.**

This is a separately labelled numerical/physics robustness variant of B9-v1. It does not mutate, replace or reinterpret the frozen B9-v1 linear-lensing objective.

## Motivation fixed before this variant

The B9-v1 production `make_ini` enables `lensing = yes` but does not set a CLASS nonlinear method. Thus B9-v1 uses the pinned CLASS linear matter/lensing calculation. The official Cobaya CLASS interface warns when lensing C_l are requested without a nonlinear code.

The pinned RT-CLASS source commit `36cf283628c4a3330ec9fd3d84239bf775f77317` explicitly supports `non linear = halofit`. It does not expose `hmcode` in the audited input parser. Therefore this variant uses **Halofit**, not a modern unpinned nonlinear backend.

The same pinned CLASS `output_pk()` code calls `spectra_pk_at_z(..., linear, ...)` for the `pk.dat` files used by the project's BOSS growth reconstruction. Hence enabling Halofit can change nonlinear lensing/remapping while preserving the existing linear `pk.dat` semantics used by the BOSS part of the objective.

## Variant objective

Start from the exact frozen B9-v1 conditional-default calibration objective and change one CLASS setting only:

`non linear = halofit`.

All other data, Planck products, distributed nuisance defaults, Pantheon/BOSS handling, dense redshift grid, ultra precision overrides, neutrino sector, gauge, CLASS source pin and retry/cache semantics remain identical to B9-v1.

Objective label:

`matched-ultra-linstep2+dense-BOSS+PlanckR3-lensing+halofit-v1`.

The production mapping remains `eff`; `k01` remains diagnostic only.

## Execution dependency

Do not start heavy B9-Halofit reoptimization until B9-v1 has produced stationarity-certified accepted LCDM and RTK centers. If B9-v1 has an unresolved boundary/localization issue, resolve it first.

Starting cosmological centers are the accepted B9-v1 centers. Use the same deterministic B9-v1 normalized search geometry and exact full-precision cache semantics:

- shared half-widths: `h=0.004`, `Ob=0.0008`, `Om=0.008`, `As=5e-11`, `ns=0.004`, `zre=0.8`;
- RTK additionally uses `log(lambda_D)` half-width `2.0`;
- deterministic COBYQA plus exact recentered polls with the same trust-region and poll settings;
- same boundary interpretation guard `B9_BOUNDARY_INTERPRETATION_GUARD_v1.md`.

Before cosmological optimization, replay the B9-v1 accepted centers with Halofit and record separately the changes in:

- lowT, lowE and Plik-lite log-likelihoods;
- standalone lensing log-likelihood;
- BOSS `eff` and `k01` values, which must remain based on linear `pk.dat` output;
- total objective.

This fixed-center Halofit replay is diagnostic only, not a minimum.

## Certification

Raw optimizer endpoints are insufficient. Apply the same `0.005` recenter threshold, base/half multiscale stationarity logic, positive-definite local Hessian requirement and fresh locked-tree replay tolerance `2e-6` used for B9-v1.

Only after paired LCDM/RTK stationarity and replay may the variant freeze

`Delta S_B9_halofit = S_RTK,B9_halofit - S_LCDM,B9_halofit`.

## Interpretation boundaries

This variant isolates sensitivity to nonlinear Halofit corrections while retaining B9-v1's distributed-default Planck calibration convention. It is not the shared-`A_planck` variant; that is separately preregistered in `B9_SHARED_APLANCK_PROFILE_PROTOCOL_v1.md`.

It remains a deterministic local robustness calculation, not a posterior, global optimum, significance, AIC/BIC comparison or Bayes factor. A later combined `Halofit + shared A_planck` test, if earned, must be separately preregistered rather than inferred by adding the two individual score shifts.
