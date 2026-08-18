# Minimal-neutrino fixed-center sensitivity — robustness checkpoint

This is a **robustness-only** result.  It does not alter the frozen massless matched objective and is not a model-selection result.

## Provenance

- workflow run: `32083374097`
- artifact: `9306029433`, `rtk-neutrino-mass-robustness`
- artifact digest: `sha256:4e42969a70a4e0438a546d525e347deefebcb5eccdb3e8c175a7e5c77d467582`
- state iteration in artifact: `52`
- RTK axis run: `32081135646`
- objective: `matched-ultra-linstep2+dense-BOSS`
- massive-neutrino test: `N_ncdm=1`, `m_ncdm=0.06 eV`, `N_ur=2.0328`, `T_ncdm=0.71611`
- production massless baseline remains unchanged.

The RTK point used here predates the current Stage-4D3 candidate, so these numbers are a sensitivity diagnostic, not a current-center final robustness statement.

## Exact fixed-center scores

| Mode | RTK S_eff | LCDM S_eff | RTK-LCDM delta S |
|---|---:|---:|---:|
| massless control | 1050.275007936606 | 1049.9661183477613 | +0.3088895888447496 |
| mnu=0.06 additive | 1080.9625013084656 | 1081.763653074504 | -0.8011517660384015 |
| mnu=0.06, fixed total nonbaryonic density | 1060.2688230571703 | 1061.734966516065 | -1.4661434588947486 |

Changes from each model's massless fixed-center value:

- additive: RTK `+30.687493371859546`, LCDM `+31.797534726742697`;
- fixed-total-nonbaryonic: RTK `+9.99381512056425`, LCDM `+11.768848168303748`.

## Interpretation

The exact massless controls reproduce the expected archived scores.  However, a 0.06-eV massive-neutrino modification moves the fixed-center likelihood by O(10–30), far larger than the current RTK-vs-LCDM matched-score separation.  Therefore the sign flip of the *fixed-center* RTK-LCDM difference is not interpretable as preference: the original six shared cosmological parameters are no longer near their appropriate conditional optima.

### Scientific conclusion

✅ **Fixed-center sensitivity is established.** The neutrino baseline materially couples to the CMB/growth degeneracy manifold.

🔴 **Minimal-neutrino robustness is not closed by this run.** After the final massless Stage-4D3 + clean-room freeze, a separate, explicitly robustness-only paired optimization with the same `mnu=0.06 eV` baseline for RTK and LCDM is required if the project wants a strong claim that the near-equal massless fit is robust to the standard minimal-neutrino assumption.

No AIC/BIC/Bayes/significance or observational-preference statement follows from this fixed-center diagnostic.
