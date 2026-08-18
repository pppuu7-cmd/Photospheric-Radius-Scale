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

## Ordinary AIC arithmetic

Using `AIC = S + 2 k`:

- `AIC_LCDM = 1061.966118347761`
- `AIC_RTK = 1064.249912429787`
- `Delta AIC = AIC_RTK - AIC_LCDM = +2.2837940820259064`

Conditional Akaike relative likelihood:

`exp(-Delta AIC/2) = 0.31921288712815515`.

If, and only if, the candidate set is restricted to these two models, normalized ordinary-AIC weights are:

- `w_LCDM = 0.7580277677372741`
- `w_RTK = 0.24197223226272588`

## Interpretation boundary

✅ **A6a ordinary-AIC arithmetic diagnostic is closed.** On this local matched objective, the standard formula penalizes RTK by about `2.284` relative to ΛCDM because the raw score difference is small but RTK has one additional fitted physical coordinate `lambda_D`.

The arithmetic is exact for the frozen scores and declared parameter counts. The stronger asymptotic interpretation of ordinary AIC as a bias-corrected expected predictive/KL criterion assumes a regular identifiable likelihood family. RTK currently has a weakly identifiable, dust-like large-`lambda_D` direction, so those regularity assumptions have not been proved. Therefore these numbers remain a **conditional ordinary-AIC diagnostic**, not rigorous evidence or a probability that either model is true.

🔴 A stronger predictive-information claim requires a separately preregistered treatment that is valid for the actual identifiability structure.

🔴 BIC remains unauthorized until a defensible composite-likelihood effective sample count is preregistered.

🔴 Bayesian evidence remains unauthorized until normalized priors and parameterization/bounds — especially for the weakly identifiable `lambda_D` direction — are preregistered and the full evidence integral is actually computed.
