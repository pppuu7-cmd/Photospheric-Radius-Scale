# B9 paired-reoptimization boundary interpretation guard v1

Status: **CONTROL-PLANE GUARD FROZEN BEFORE CONSUMING ANY COMPLETED B9 PAIRED-REOPTIMIZATION ARTIFACT**.

This guard does not change the frozen B9-v1 objective, likelihood product, start points, optimizer geometry, or current Actions run. It repairs only the downstream decision semantics for `research/robustness/B9_PAIRED_REOPTIMIZATION_TARGET_v1.json` and `rtk/b9_paired_reoptimization.py`.

## Reason

The current worker correctly records `status=REOPTIMIZATION_BOUNDARY_HIT` whenever the exact best point has a normalized coordinate with `|y|>0.97`, but its human-readable `next_gate` string is unconditional and mentions recenter/Hessian certification. A boundary point is not an interior-minimum candidate and must not enter an interior Hessian certification as if the box had enclosed the basin.

## Frozen decision rule

1. If `boundary_axes` is empty, the current exact best point may proceed to the already-preregistered B9 base/half stationarity-Hessian gate.
2. If any shared cosmological axis (`h`, `Ob`, `Om`, `As`, `ns`, `zre`) is in `boundary_axes`, do **not** certify stationarity at that point. Recenter the *same* preregistered physical half-width box on the exact boundary winner and rerun the same deterministic COBYQA + exact poll sequence. This is a translated search box, not a new objective or a widened prior.
3. If the only RTK boundary axis is `loglam`, do **not** import the massless-objective B10 tail conclusion into B9. Freeze a B9-specific fixed-lambda/tail profile under the lensing-added objective before any lambda-identifiability or interior-minimum claim.
4. If translated same-width searches repeatedly hit a shared-parameter boundary in the same direction, stop and preregister a wider-corridor search before running it; do not widen after inspecting additional score values.
5. No boundary result may be used for B9 closure, raw final `Delta S_B9`, significance, AIC/BIC, posterior preference, or Bayes-factor language.

## Scope

This is a decision/control-plane guard only. It neither invalidates nor modifies already-computed exact B9 likelihood evaluations; it governs what may be inferred from their location within the preregistered search box.
