# A5 historical LCDM stationarity-semantics audit — 2026-08-24

## Scope

This audit was triggered by the preregistered exact old-to-new LCDM line profile
`research/robustness/A5_LCDM_OLD_TO_NEW_BASIN_LINE_PROFILE_RESULT_v1.json`.
It corrects the interpretation of the historical A5 LCDM local certificate without changing any historical exact score.

Objective: `matched-ultra-linstep2+dense-BOSS`

Production mapping: `eff`

Objective fingerprint: `754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666`

Frozen recenter tolerance: `0.005`.

## Exact facts that remain valid

The historical matched fresh-tree replay remains exact:

- historical LCDM score: `1049.966118347761`;
- historical RTK score: `1050.249912429787`;
- historical raw paired delta: `+0.2837940820259064`.

These scores remain valid historical local-objective evaluations. Nothing in this audit turns them into a global comparison, significance, posterior probability or Bayes factor.

## Semantics mismatch found in canonical state

The historical LCDM Hessian/stationarity center recorded in `research/state/current.json` has

`Ob = 0.04865764689799632`.

The parameter point whose accepted exact score is

`S_eff = 1049.966118347761`

has

`Ob = 0.04858764689799632`.

The difference is exactly

`0.00007000000000000`,

which is one frozen base `Ob` stencil step.

The state itself records the score semantics as `best_exact_stencil_within_recenter_tolerance`. Therefore the positive-definite historical Hessian was not evaluated at the same parameter point as the accepted-score point.

## Independent line-profile evidence

The preregistered exact line profile from the historical accepted-score point toward the independently confirmed new LCDM basin replays both endpoints with zero error and finds descent immediately:

- `t=0.00`: `S_eff=1049.966118347761`;
- `t=0.01`: `S_eff=1049.9530692041817`, improvement `0.013049143579337397 > 0.005`;
- `t=0.02`: `S_eff=1049.946782723808`, improvement `0.01933562395311128`;
- `t=0.05`: `S_eff=1049.936618484686`, improvement `0.029499863074988752`;
- `t=1.00`: `S_eff=1049.400976604194`, improvement `0.5651417435669828`.

The result classification is

`A5_LCDM_LINE_PROFILE_HISTORICAL_LOCAL_INTERPRETATION_AUDIT_REQUIRED`.

## Corrected historical interpretation

The following wording is now required:

1. The historical LCDM score point is an independently reproducible exact point under the frozen objective.
2. The historical positive-definite Hessian certifies the nearby recorded Hessian center, not the accepted-score point itself.
3. The accepted-score point must **not** be described as an independently Hessian-certified local minimum.
4. The exact old-to-new line profile demonstrates an admissible descent direction from the accepted-score point larger than the frozen `0.005` tolerance.
5. This correction does not prove that the new LCDM point is a global minimum. Its independent base/half/fresh-tree certification chain remains mandatory.
6. The historical RTK A5 certification is not changed by this LCDM-specific audit.

## Current A5 consequence

The best-known LCDM reference remains the independently replayed new seed

`S_A5 = 1049.400976604194`.

The formal base gate at this point was recenter-clear but non-PD; exact frozen base eigenmode rays found maximum exact improvement `0.0`. Therefore the mandatory next gate remains the independent half-scale Hessian at the unchanged new LCDM center.

The preregistered replacement paired replay remains conditional on half-scale recenter-clear + positive-definite curvature. No canonical pair is replaced before that replay passes.

## Guard

Do not retroactively rewrite the historical score or erase its provenance. Correct only the stationarity/minimum interpretation. A local Hessian at one point cannot certify a neighboring accepted-score point, and no local result here establishes global optimality.
