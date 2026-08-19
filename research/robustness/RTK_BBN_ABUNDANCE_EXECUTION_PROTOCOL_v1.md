# RTK B6 paired AlterBBN abundance execution protocol v1

Status: **FROZEN BEFORE THE FIRST RTK H(T)-INJECTED ABUNDANCE NETWORK OUTPUT**.

Frozen at `2026-08-19T12:00:16Z` / `2026-08-19T15:00:16+03:00 Europe/Helsinki`.

This execution protocol implements the already-frozen `RTK_BBN_ABUNDANCE_PROTOCOL_v1.md`. It is a robustness branch and does not mutate the A1–A5 production likelihood.

## Immutable numerical inputs

The H(T) input is the completed B6 entropy-aware mapping from GitHub Actions run `32243547025`, artifact `9361734444` (`rtk-b6-entropy-aware-ht-mapping`). The abundance workflow must download that exact artifact and fail closed unless all of these digests match:

- `output/b6_bbn_ht_mapping/nominal_256.csv`: SHA256 `cdb0e72b3bb59c53d01719ad3eab827e14f2424de73f4dd9029f559877192c15`;
- `output/b6_bbn_ht_mapping/refined_512.csv`: SHA256 `a9116a22844927a4d085343de9c22215e407e62813b6a7f4b0eeb6f7cec187b9`;
- `output/b6_bbn_ht_mapping/summary.json`: SHA256 `5c5bfeea86c3c352418c51a6c217dee5b45df7a4d556815dc6a65e0f28d98416`.

The mapping classification must be `RTK_BBN_ENTROPY_AWARE_HT_MAPPING_PASS`, with 256/512 nested grids, `max_abs_R_minus_1 <= 2.3e-9`, and nominal/refined interpolation discrepancy `<=2e-12`.

The AlterBBN source is the already-pinned published v2.2 archive, DOI `10.17632/k7j3b9zyvf.1`, filename `alterbbn_v2.2.tar.xz`, SHA256 `2bcb7d2e3f4a74f59cd589e60f0923892bb90296a793f80016897405920c5fae`, size `2586656` bytes. Compiler/runtime semantics remain the previous source-lock/self-test semantics (`gcc-13`, the locked CFLAGS).

## Frozen baryon/radiation semantics

The first B6 abundance run uses the massless A1–A5 accepted RTK point, not the B4 0.06-eV branch:

- `Omega_b = 0.046800730927437424`;
- `h = 0.691103719964454`;
- therefore `omega_b = Omega_b h^2 = 0.022353168770582937`.

Before any abundance output, freeze the conversion convention

`eta_10 = 273.9 * omega_b`,

which gives `eta_10 = 6.122532926262666` and `eta = 6.122532926262666e-10`.

This is a preregistered interface convention, not fitted to the BBN result. Reference and RTK use exactly the same eta. AlterBBN v2.2 standard radiation semantics are retained (`Nnu=3.046`, `dNnu=0`, zero neutrino chemical potentials); no massive-neutrino B4 settings may leak into this run.

## H(T) injection contract

Make three byte-separated build trees from the same verified archive:

1. `reference`: identical H-ratio interpolation code but every table value is forced to `R_H=1`;
2. `rtk_nominal`: exact values from the 256-point table;
3. `rtk_refined`: exact values from the 512-point table.

All three receive the same eta edit, compiler flags, nuclear network/rates, and full-precision abundance output edit. Thus the only scientific difference in the paired comparison is `R_H(T)`.

The patch must target the single common Friedmann-H assignment in pinned `src/bbn.c` and multiply H immediately after it, before weak/nuclear rates and the abundance linearization. Patch application is fail-closed on source structure. Interpolation is log(T)-log(R), matching the H(T) mapping builder.

No scientific extrapolation is allowed. Because the accepted AlterBBN trace endpoint and the exact Kelvin-to-GeV constant differ at the initial T9=27 endpoint by only about 3.1e-7 fraction, an endpoint-only relative tolerance of `5e-7` is preregistered: values within it may be snapped to the nearest tabulated endpoint; anything farther outside aborts. This tolerance cannot be widened after seeing abundance output.

## Execution and numerical-resolution rule

Run central abundances for failsafe `1` and `7` for reference, RTK nominal, and RTK refined. Record at least Yp, D/H, He3/H, Li7/H, Li6/H, and Be7/H at full double-output precision.

For each failsafe and observable define paired shifts `delta = RTK - reference`. The primary value is the refined-table shift at failsafe=1. Numerical sensitivity is assessed *before interpretation* using both:

- table refinement: `|delta_refined,f1 - delta_nominal,f1|`;
- solver-mode sensitivity: `|delta_refined,f1 - delta_refined,f7|`.

Define `noise = max(these two)`. A nonzero shift is classified as numerically resolved only if `|delta_refined,f1| > 5*noise` and it is nonzero at full precision. Otherwise report `ABUNDANCE_SHIFT_BELOW_NUMERICAL_RESOLUTION` and quote a conservative bound `|delta_refined,f1| + 5*noise`; never replace an unresolved value by a physics claim of exact zero.

## Observational constraints frozen before output

The following observational references and central constraints are fixed before running the RTK network:

- primordial deuterium: Kislitsyn et al. (2024), arXiv:2401.12797, `(D/H)_p = (2.533 +/- 0.024)e-5`;
- primordial helium: Aver et al. (2026), arXiv:2601.22238, `Y_p = 0.2458 +/- 0.0013`.

Report individual standardized residuals for the reference and RTK-refined failsafe=1 values against those quoted observational uncertainties. This is a diagnostic observational comparison: the old AlterBBN-v2.2 nuclear-rate uncertainty is not silently absorbed into the observational sigma. Do not cherry-pick a different observational compilation after seeing the result.

## Acceptance semantics

The workflow may mark the numerical execution PASS only if source/artifact hashes, patch contract, both refinement grids, all six network runs, finite positive yields, and full-precision parsing pass. B6 scientific closure is a separate interpretation gate: it requires a stable paired abundance result or a defensible numerical upper bound, plus explicit observational comparison and provenance checkpoint.

No lithium-problem claim is allowed from this gate.
