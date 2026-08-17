# RTK BOSS RSD linear scale-dependence diagnostic

Date: 2026-08-18

Status: **linear-theory mapping caveat quantitatively bounded at the current RTK center; survey-window/nonlinear RSD treatment remains open.**

## Provenance

- Workflow run: `32074157652`, success.
- Job: `95523582062`.
- Research checkout: `f965e88771fad14e2984f9d55daf67b2b3394686`.
- CLASS upstream: `36cf283628c4a3330ec9fd3d84239bf775f77317`.
- Pantheon: `7eb29dc87ba223b4ec8457cd3cccba1216c36fb7`.
- Explicit RT auxiliary background IC patch applied.
- Artifact: `rtk-boss-rsd-scale-dependence`.
- Artifact ID: `9302798369`.
- Artifact ZIP SHA256: `733572348fe7dab80374e86cc65ed67a02eae86a4028c20ae77fdd5a241f711c`.
- Objective precision/redshift grid: current frozen `matched-ultra-linstep2+dense-BOSS` state.

The diagnostic is not a likelihood fit. It evaluates RTK at the current accepted center and LCDM at the accepted best-exact score parameters, using the same dense redshift derivative stencil as the production growth mapping.

## Quantity tested

For each BOSS target redshift `z = 0.38, 0.51, 0.61`, the run evaluates

`f(k,z) = 1/2 d ln P(k,z) / d ln a`

and

`f sigma8(k,z) = f(k,z) sigma8(z)`

across

`k = 0.02, 0.03, 0.05, 0.07, 0.10, 0.15, 0.20 h/Mpc`.

It also compares the `k=0.1 h/Mpc` result with the production integrated/effective definition

`f sigma8_eff = d sigma8 / d ln a`.

## Results

| z | RTK peak-to-peak fσ8(k) / mean | RTK k=0.1 vs eff | LCDM peak-to-peak | LCDM k=0.1 vs eff |
|---:|---:|---:|---:|---:|
| 0.38 | **0.012751%** | **0.015203%** | 0.000282% | 0.001222% |
| 0.51 | **0.006951%** | **0.008642%** | 0.000280% | 0.000892% |
| 0.61 | **0.004485%** | **0.005776%** | 0.000275% | 0.000711% |

Thus RTK does have more scale dependence than LCDM, as expected, but over the representative linear BOSS range tested it is only at the `~10^-4` fractional level, and becomes smaller with increasing redshift across the three DR12 bins.

## Scientific consequence

The existing difference between the production `eff` and `k01` compressed BOSS scores cannot plausibly be hiding an order-unity or percent-level scale-dependence effect across this linear k range. This directly supports the earlier observation that eff-vs-k01 changes the current BOSS chi-square by only about `2e-4`.

Therefore the current `~+0.9` RTK-vs-LCDM BOSS penalty is not primarily a consequence of choosing one of these two linear compressed-growth mappings. It is instead associated with the late-time correlated geometry-growth mismatch already isolated in the BOSS covariance/PCA audit.

## Claim boundary

This closes only the **linear-theory scale-dependence size question at the current centers and tested k range**.

It does not replace:

- survey-window convolution;
- nonlinear redshift-space distortion modeling;
- Alcock-Paczynski/template refitting in the full RTK cosmology;
- a reanalysis of the original galaxy catalog.

Those stronger survey-level tests remain open before claiming a definitive BOSS/RSD likelihood for arbitrary scale-dependent modified-gravity models.
