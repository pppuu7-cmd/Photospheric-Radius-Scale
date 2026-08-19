# B9 Planck R3 standalone-lensing robustness protocol v1

Status: **FROZEN BEFORE THE FIRST RTK/LCDM COSMOLOGICAL STANDALONE-LENSING SCORE**.

This is a post-A5 robustness objective. It does not mutate, replace, or reinterpret the frozen massless A1-A5 comparison.

## Fixed likelihood product

The pinned Planck R3.00 baseline archive and `clipy-like==0.15` interface audit run `32243756716` established two loadable standalone lensing products. The first B9 objective uses, by rule fixed before any cosmological lensing score, the unique loadable **non-CMB-marginalized SMICA minimum-variance** product:

`baseline/plc_3.0/lensing/smicadx12_Dec5_ftl_mv2_ndclpp_p_teb_consext8.clik_lensing`

The CMB-marginalized product is not an interchangeable fallback inside B9-v1. A later comparison to it requires a separately labelled robustness variant.

## B9-v1 objective

Start from the exact frozen A1-A5 massless objective:

- low-l Planck temperature/polarization plus Plik-lite TTTEEE as already implemented;
- Pantheon with the same profiled additive offset;
- dense BOSS DR12 with production `eff` mapping (`k01` retained separately);
- the same dense redshift grid and ultra CLASS precision settings;
- exact-float success-only cache/retry semantics.

Add the standalone Planck R3 lensing-reconstruction likelihood above. Define

`S_B9 = S_A5_base - 2 log L_lensing`.

No AIC/BIC/Bayes/significance claim follows from this robustness objective.

## Cosmology and runtime semantics

- Use the **massless** A1-A5 neutrino baseline; do not mix B4's 0.06 eV branch into B9-v1.
- Use the same pinned CLASS, Pantheon, Planck archive, Python, NumPy, SciPy and clipy-like versions as the reproducibility lock.
- RTK keeps `model=2`, explicit retarded auxiliary initial conditions and production Newtonian gauge.
- The lensing adapter must provide exactly the spectra requested by the chosen `.clik_lensing` object with documented CLASS-to-clik units/order. No missing spectrum may be silently filled by zeros unless the likelihood's own `lmax` marks that spectrum unused.
- Before optimization, the adapter must pass an interface-contract audit recording requested `lmax`, input-vector length/order, finite likelihood value and exact chosen-product fingerprint.

## Execution sequence

1. **Adapter contract gate.** Evaluate the chosen likelihood at one frozen accepted LCDM point and one frozen accepted RTK point only after the adapter's spectrum ordering/units are machine-checked. These fixed-center values are diagnostics, not minima.
2. **Paired reoptimization.** Independently reoptimize RTK (7 parameters) and LCDM (6 shared cosmological parameters) on `S_B9`, starting from the respective frozen A5 accepted points. Lambda remains a genuine RTK coordinate.
3. **Stationarity certification.** Apply the same recenter threshold `0.005` and local multiscale logic appropriate to each model. A raw optimizer endpoint is insufficient.
4. **Independent replay.** Fresh locked-tree replay of both accepted B9 score points must reproduce the lensing and total scores within `2e-6`.
5. Freeze only the raw robustness delta `Delta S_B9 = S_RTK,B9 - S_LCDM,B9` with explicit statement that it belongs to B9-v1, not to A5.

## Closure

B9 may be marked closed only after adapter contract, paired reoptimization, stationarity certification, and independent replay all pass. A failure to instantiate or evaluate the fixed chosen product is fail-closed and cannot be repaired by switching to the CMB-marginalized product after seeing scores.
