# Post-freeze AIC diagnostic

This calculation is authorized by `rtk/POSTFREEZE_MODEL_SELECTION_PROTOCOL_v1.md` and uses only the already-frozen A5 local matched scores. It is not a global-optimum theorem, Bayes factor, or sigma significance.

## Inputs

- `S_RTK = 1050.249912429787`
- `S_LCDM = 1049.966118347761`
- `Delta S = +0.2837940820259064`
- `k_RTK = 7`
- `k_LCDM = 6`
- `Delta k = 1`

The common analytically profiled Pantheon offset does not affect `Delta k`; if counted explicitly it adds equally to both models.

## AIC

Using `AIC = S + 2 k`:

- `AIC_LCDM = 1061.966118347761`
- `AIC_RTK = 1064.249912429787`
- `Delta AIC = AIC_RTK - AIC_LCDM = +2.2837940820259064`

Conditional Akaike relative likelihood:

`exp(-Delta AIC/2) = 0.31921288712815515`.

If, and only if, the candidate set is restricted to these two models, normalized Akaike weights are:

- `w_LCDM = 0.7580277677372741`
- `w_RTK = 0.24197223226272588`

## Interpretation boundary

✅ **A6a AIC diagnostic is closed.** On this local matched objective, AIC penalizes RTK by about `2.284` relative to ΛCDM because the raw score difference is small but RTK has one additional fitted physical coordinate `lambda_D`.

These numbers are model-ranking diagnostics under AIC assumptions, not posterior probabilities that either model is true and not a significance/exclusion claim.

🔴 BIC remains unauthorized until a defensible composite-likelihood effective sample count is preregistered.

🔴 Bayesian evidence remains unauthorized until normalized priors and parameterization/bounds — especially for the weakly identifiable `lambda_D` direction — are preregistered and the full evidence integral is actually computed.
