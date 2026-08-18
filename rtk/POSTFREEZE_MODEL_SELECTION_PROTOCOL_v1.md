# Post-freeze model-selection protocol v1

**Frozen after A3–A5 closure and before calculating/reporting any information criterion.**

This protocol does not alter the matched likelihood objective or the final local scores. It separates what can be computed defensibly from the current composite likelihood from quantities that require additional assumptions.

## Inputs already frozen

- `S_RTK = 1050.249912429787`
- `S_LCDM = 1049.966118347761`
- `Delta S = +0.2837940820259064`
- same `matched-ultra-linstep2+dense-BOSS` objective
- independent clean-room paired replay passed with zero recorded score error.

## Parameter count

The matched ΛCDM fit has six fitted cosmological coordinates:

`As, Ob, Om(cdm), h, ns, zre`.

The matched RTK fit has the corresponding six coordinates with the nonbaryonic matter slot represented by the Khronon sector, plus one additional physical coordinate:

`lambda_D`.

Therefore

- `k_LCDM = 6`
- `k_RTK = 7`
- `Delta k = +1` for RTK.

Pantheon’s common absolute-magnitude/offset direction is profiled analytically in the same way for both models. Counting or not counting that common nuisance adds the same number to both `k` values and therefore does not change `Delta AIC`. Plik-lite has already marginalized its high-l foreground/calibration nuisance structure into the supplied likelihood; those are not independently fitted coordinates in this project objective.

## AIC subgate

For a common likelihood with `S = -2 log L + common constant`, use

`AIC = S + 2 k`.

Only the **difference** is interpreted:

`Delta AIC = AIC_RTK - AIC_LCDM = Delta S + 2 Delta k`.

Akaike relative likelihood `exp(-Delta AIC/2)` and normalized two-model Akaike weights may be reported only as AIC diagnostics conditional on the two-model candidate set. They are not posterior probabilities that a model is true and are not a sigma significance.

## BIC — not yet authorized

Do not compute BIC until an explicit, defensible effective sample count is frozen for the composite likelihood. A naive sum of CMB multipoles, supernovae and the nine BOSS compressed observables is not automatically an independent-sample count: the likelihood pieces are correlated/aggregated and Plik-lite is itself a compressed/marginalized likelihood object.

If a BIC result is desired, first create a separate protocol defining `N_eff`, justify it mathematically for every likelihood block, and show sensitivity to defensible alternative conventions.

## Bayes factor/evidence — not yet authorized

Do not infer a Bayes factor from the local Hessians or AIC. Bayesian evidence requires explicit normalized priors for every fitted coordinate and an evidence computation over the full allowed parameter volume.

The `lambda_D` direction is especially prior-sensitive because the current cosmological solution lies close to a dust-like / weakly identifiable large-lambda regime. A Bayes protocol must therefore freeze the parameterization (`lambda_D` versus `log lambda_D` or another physically justified coordinate), finite prior bounds, and priors for the six shared coordinates **before** running evidence integration.

## Wilks / sigma significance — not authorized

Do not translate `Delta S` or `Delta AIC` into a chi-square sigma. The two model families are not being treated here as a regular nested one-parameter extension satisfying Wilks conditions, and the weak/boundary-like `lambda_D` direction further invalidates a casual one-degree-of-freedom significance mapping.

## Closure semantics

- A6a (AIC diagnostic) may close after the arithmetic is independently reproduced from the frozen A5 scores and `Delta k=1`.
- BIC remains open until a separate `N_eff` protocol is justified.
- Bayes evidence remains open until a prior/evidence protocol is preregistered and executed.
- No model truth/probability/significance claim follows from AIC alone.
