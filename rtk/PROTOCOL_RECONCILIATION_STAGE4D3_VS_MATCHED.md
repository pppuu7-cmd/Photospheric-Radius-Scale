# Protocol reconciliation: matched raw fit vs Stage-4D3 interior minimum

Date: 2026-08-17

This note resolves a semantic mismatch between two already-frozen project documents without weakening either one.

## Two distinct claims

### A. Matched raw-fit candidate

`FINAL_MATCHED_COMPARISON_PROTOCOL.md` defines the matched numerical comparison layer. Its recenter rule is based on the exact tested improvement

`S_center - S_best_exact <= 0.005`.

Passing this rule means that the current center does not require another recenter at the tested stencil scale. It permits recording a **matched raw-fit candidate score** from the best exact tested point. It does not, by itself, prove that the center is a strict interior local minimum.

### B. Stage-4D3 numerical interior minimum

`RTK_STAGE4D3_PROOF_GATE.md` is intentionally stronger. Gate N5 additionally requires:

1. no exact stencil/Newton improvement greater than `0.005`;
2. a positive-definite 7D Hessian at the accepted stencil scale;
3. stability under at least one smaller stencil scale, normally `1/2`;
4. no repeatable downhill direction requiring another optimizer pass.

Therefore the label **interior minimum proven** is forbidden until the stronger N5 conditions are satisfied.

## State semantics from this point forward

The autonomous state machine must distinguish:

- `raw_candidate_certification`: numerical recenter/raw-fit status;
- `certification`: stronger local-minimum status;
- `interior_minimum_certification`: explicit Stage-4D3 N5 status.

A non-positive Hessian may still leave a useful matched raw-fit candidate if no exact tested point improves by more than the numerical tolerance, but that result must be labelled curvature-unresolved and must not be called a proven local minimum.

## Multiscale rule

After the current full 7D base-stencil RTK Hessian completes without a recenter-sized improvement, a full `1/2`-stencil Hessian is required before Stage-4D3 N5 can pass.

If the base stencil is non-positive-definite but the half stencil becomes positive-definite, the base scale is not retroactively declared valid. The appropriate next step is an additional smaller-scale convergence check (normally `1/4`) before choosing a new accepted numerical stencil scale.

If the half stencil finds an exact improvement `> 0.005`, recenter and repeat the axis/Hessian chain.

## Raw score semantics

For a center that remains unrecentered, the raw local candidate score is the lowest exact score actually evaluated across the accepted base and smaller-stencil validation sets, while the accepted **center parameters** remain unchanged unless the recenter threshold is crossed.

This prevents overloading a center score with minimum-score semantics.

## Claim guardrail

Until N5 passes, allowed wording is:

> matched dense raw-fit candidate; local curvature/stencil certification pending or unresolved.

Forbidden wording is:

> proven local interior minimum; detected finite-lambda minimum; statistically preferred model.

The stronger gate is conservative and does not invalidate previously computed exact scores; it only constrains their interpretation.
