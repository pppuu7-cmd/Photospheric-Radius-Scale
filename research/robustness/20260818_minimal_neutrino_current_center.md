# Minimal-neutrino current-center sensitivity

**Robustness-only. Frozen massless production objective unchanged.**

## Provenance

- run `32144865816` — success
- artifact `9327720740`, digest `sha256:ca4968d67ef5c595438242834f9a160716de32369447d162117a5010fbeb998e`
- state iteration `75`
- RTK center exactly matches the currently active Stage-4D3 candidate:
  - As `2.0877827951474356e-09`
  - Ob `0.046800730927437424`
  - Om `0.2522864064078236`
  - h `0.691103719964454`
  - lambda_D `219457.5727136581`
  - ns `0.9645577770978523`
  - zre `7.328459220286924`
- massless controls reproduce RTK `1050.249912429787` and LCDM `1049.966118347761`.

## Exact fixed-center sensitivity

| mode | RTK delta from massless | LCDM delta from massless | fixed-center RTK-LCDM delta S |
|---|---:|---:|---:|
| massless | 0 | 0 | +0.2837940820259064 |
| mnu=0.06 eV additive | +30.666939297925865 | +31.79753472674338 | -0.846801346791608 |
| mnu=0.06 eV, fixed total nonbaryonic density | +10.00304335988244 | +11.768848168304203 | -1.4820107263958562 |

`k01` gives the same qualitative result (`-0.84577` and `-1.48118` respectively).

## Closure statement

✅ **B4a fixed-center minimal-neutrino sensitivity is closed.** The standard 0.06-eV neutrino modification has a material effect on the current CMB/growth degeneracy manifold and is not a negligible perturbation at fixed shared cosmological parameters.

🔴 **B4 overall remains open.** Because the absolute fixed-center displacement is O(10–30) in the objective, the sign of the fixed-center RTK-LCDM difference is not an observational-preference result. A strong robustness claim requires a separate paired reoptimization under one common `mnu=0.06 eV` robustness objective after the frozen massless Stage-4D3 + clean-room result is finalized.

No AIC/BIC/Bayes/significance claim follows from this diagnostic.
