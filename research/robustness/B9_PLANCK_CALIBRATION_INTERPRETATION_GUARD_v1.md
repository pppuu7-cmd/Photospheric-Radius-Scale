# B9 Planck calibration interpretation guard v1

Status: **INTERPRETATION GUARD; DOES NOT MUTATE THE FROZEN B9-v1 OBJECTIVE OR ITS ACTIVE RUN.**

## Why this guard exists

The frozen B9-v1 implementation constructs each `clik` input vector by copying the distributed likelihood `default_par` vector and replacing only the requested CMB/lensing spectra. Therefore all remaining nuisance/calibration tail entries are conditional on their distributed defaults.

For the exact B9 lensing product

`baseline/plc_3.0/lensing/smicadx12_Dec5_ftl_mv2_ndclpp_p_teb_consext8.clik_lensing`,

the official Cobaya interface at public source commit `b76b6fed2a6c8c5594c6f92d5058bef10079746a` defines:

- `cobaya/likelihoods/planck_2018_lensing/clik.yaml`: `params: !defaults [../base_classes/planck_calib]`;
- `cobaya/likelihoods/base_classes/planck_calib.yaml`: `A_planck` Gaussian prior with mean `1` and sigma `0.0025`.

The Planck 2018 lensing analysis also distinguishes the ordinary likelihood, which depends on the primary CMB spectra, from a separately supplied CMB-marginalized lensing likelihood. B9-v1 intentionally froze the ordinary non-CMB-marginalized SMICA minimum-variance product before seeing the cosmological lensing scores.

## Consequence for B9-v1

B9-v1 remains a valid preregistered **conditional-default calibration robustness objective**:

`S_B9 = S_A5_base - 2 log L_lensing`,

with all distributed Planck nuisance tails, including `A_planck` where present, fixed at their default values. The active paired B9-v1 reoptimization must not be changed or restarted post hoc merely because this interpretation was clarified.

However, B9-v1 must not be described as a fully nuisance-profiled or nuisance-marginalized standard Planck combination. Its final statement must say that it is conditional on the frozen default nuisance/calibration convention inherited from A5.

## Separately scoped nuisance-aware robustness variant

A later calibration-nuisance robustness variant is scientifically earned, but its exact parameter sharing must be frozen only after the machine audit `.github/workflows/rtk-b9-planck-calibration-contract.yml` records the extra-parameter names/default tails for all four project Planck products: Commander lowT, SimAll lowE, Plik-lite TTTEEE and the selected non-marginalized lensing product.

The future variant must obey these rules:

1. use the same physical calibration parameter consistently across every likelihood product that declares that shared parameter;
2. apply the external Gaussian calibration prior only once, not once per likelihood component;
3. preserve the frozen B9 lensing product and all cosmological data/precision semantics;
4. receive a new objective name/fingerprint and a separately preregistered optimizer/profile procedure before the first nuisance-aware cosmological result;
5. never overwrite or reinterpret B9-v1 after seeing the nuisance-aware result.

## Non-claims

This guard does not alter any already-computed A5 or B9-v1 exact score. It does not imply that freeing `A_planck` will materially change the RTK-LCDM delta; that is an empirical question for the separately scoped variant. It also does not turn either branch into a global posterior/evidence/model-selection calculation.
