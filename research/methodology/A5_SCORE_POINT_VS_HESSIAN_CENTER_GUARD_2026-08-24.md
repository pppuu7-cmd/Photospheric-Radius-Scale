# A5 score-point versus Hessian-center guard — 2026-08-24

This addendum is mandatory for all future local-stationarity reporting.

## New guard

A Hessian/local-minimum certificate applies only to the exact parameter point at which the Hessian center score is replayed. If a workflow accepts a different exact stencil point because its improvement is within the frozen recenter tolerance, the accepted score may be retained for matched-score bookkeeping, but the Hessian certificate must **not** be transferred to that neighboring point.

Every future stationarity result that distinguishes `center`, `best_exact`, `accepted_score_params`, or equivalent fields must report all of the following explicitly:

1. exact Hessian-center parameters and center score;
2. exact accepted-score parameters and score;
3. normalized/physical displacement between them;
4. whether they are identical;
5. if not identical, separate semantics: `HESSIAN_CERTIFIED_CENTER` versus `BEST_EXACT_WITHIN_RECENTER_TOLERANCE`;
6. no wording such as `local minimum at accepted score point` unless the accepted score point itself has an admissible Hessian/stationarity certificate.

## Triggering A5 example

Historical LCDM:

- accepted-score `Ob=0.04858764689799632`;
- recorded Hessian-center `Ob=0.04865764689799632`;
- displacement: exactly one base `Ob` step, `0.00007`.

The preregistered old-to-new line profile later found exact descent from the accepted-score point exceeding the `0.005` recenter tolerance at `t=0.01`. This does not invalidate the exact historical score replay; it invalidates the stronger interpretation that the accepted-score point itself was Hessian-certified.

Canonical audit:
`research/robustness/A5_HISTORICAL_LCDM_STATIONARITY_SEMANTICS_AUDIT_2026-08-24.md`.

## Scope

This is a methodology correction, not a change to the frozen recenter tolerance and not a retroactive score modification. Existing historical scores remain preserved with provenance. Future automation should fail closed if it attempts to transfer Hessian certification between nonidentical centers.
