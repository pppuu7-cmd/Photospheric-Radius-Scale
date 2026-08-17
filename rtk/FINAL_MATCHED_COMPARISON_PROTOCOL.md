# Final matched RTK vs LCDM comparison protocol

Status: frozen before completion of the current dense RTK/LCDM Hessian runs.

## Objective

All final raw-fit comparisons must use the same matched-ultra + dense-BOSS likelihood objective and exact-float cache semantics. Old sparse-objective scores are historical only.

The `eff` and `k01` BOSS mappings are treated as separate objective variants. Their scores, gradients, minima, recenter decisions, and final comparisons must be reported separately. A better `k01` point does not by itself authorize moving the `eff` center, and vice versa.

## Required local certification before comparison

RTK:
- accepted dense center established by exact axis/recenter gate for the mapping being certified;
- full 7D local Hessian computed at that accepted center;
- Hessian eigenvalues recorded;
- exact Newton/trust proposal evaluated;
- best exact stencil point and improvement recorded;
- `eff` and `k01` kept separate throughout.

LCDM:
- full matched dense 6D local Hessian computed at its accepted center;
- Hessian eigenvalues recorded;
- exact Newton/trust proposal evaluated;
- best exact stencil point and improvement recorded.

## Mapping-specific recenter rule

For each mapping independently, let

`improvement = S_center(mapping) - S_best_exact(mapping)`.

- If improvement `> 0.005`, that mapping requires recenter/revalidation before its final Hessian certification.
- If improvement `<= 0.005`, no recenter is required by the predeclared project gate for that mapping.
- If `eff` and `k01` prefer different exact points, preserve both branches as separate mapping-specific results; do not construct a hybrid center by mixing them.

The primary production raw-fit comparison must always name which BOSS mapping it uses.

## Raw-fit quantity

Define, for the same mapping and same objective,

`Delta S = S_RTK,min - S_LCDM,min`.

Interpretation only at the raw-fit level:
- Delta S > 0: LCDM has lower raw objective;
- Delta S < 0: RTK has lower raw objective;
- |Delta S| <= 0.005: numerically indistinguishable at the predeclared local improvement tolerance used in this project.

The 0.005 band is a project numerical/local-gate convention, not a statistical confidence interval.

## Parameter-count caveat

RTK has the additional physical coordinate `lambda_D` relative to the matched 6D LCDM nuisance/cosmology parameter set. Therefore raw Delta-S is not by itself model selection. If information criteria are later reported, their formulas, effective sample count, and score convention must be frozen explicitly before calculating them.

## Prohibited claims before completion

Do not claim:
- observational preference;
- significance;
- Bayes factor/evidence;
- global minimum;
- exclusion of LCDM;
- quantum/UV completion;
from local Hessians or raw Delta-S alone.

## Reproducibility

Record workflow run IDs, source commits, objective settings, center parameters, exact scores, and artifact hashes/IDs for both models in the final checkpoint.
