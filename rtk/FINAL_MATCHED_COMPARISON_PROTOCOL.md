# Final matched RTK vs LCDM comparison protocol

Status: frozen before completion of the current dense RTK/LCDM Hessian runs.

## Objective

All final raw-fit comparisons must use the same matched-ultra + dense-BOSS likelihood objective and exact-float cache semantics. Old sparse-objective scores are historical only.

## Required local certification before comparison

RTK:
- accepted dense center established by exact axis/recenter gate;
- full 7D local Hessian computed at that accepted center;
- Hessian eigenvalues recorded;
- exact Newton/trust proposal evaluated;
- best exact stencil point and improvement recorded;
- `eff` and `k01` kept separate.

LCDM:
- full matched dense 6D local Hessian computed at its accepted center;
- Hessian eigenvalues recorded;
- exact Newton/trust proposal evaluated;
- best exact stencil point and improvement recorded.

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
