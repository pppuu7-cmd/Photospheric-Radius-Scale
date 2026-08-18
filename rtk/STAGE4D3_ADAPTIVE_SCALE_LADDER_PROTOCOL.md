# Stage-4D3 adaptive adjacent-scale curvature ladder

**Status:** pre-registered before consuming the currently active 1/2-stencil result (`32133215190`).

This protocol extends the existing base/half and coarse-non-PD -> half/quarter rules to cover the previously unhandled case in which a coarser Hessian is PD but a smaller stencil is non-PD. It does **not** alter the frozen objective, mapping, exact-float likelihood, or recenter tolerance.

## Fixed inputs

- objective: `matched-ultra-linstep2+dense-BOSS`
- production mapping: `eff`
- exact recenter tolerance: `Delta S > 0.005`
- base physical finite-difference steps: those stored in `research/state/current.json`
- candidate stencil scales, in order: `1`, `1/2`, `1/4`, `1/8`
- PD numerical threshold: all Hessian eigenvalues strictly `> 1e-8` in the worker's scaled coordinates

## Rules

1. **Recenter dominates curvature classification.** At any full Hessian scale, if `S_center - S_best_exact > 0.005`, recenter to the exact best point, clear all old ray/smaller-scale proof slots, rerun the axis gate, and restart from the base Hessian.

2. **Every non-PD scale must be exact-ray falsified at the same physical scale.** Diagonalize that scale's numerical Hessian and evaluate the frozen exact likelihood along every strictly negative eigenmode. The ray coordinate uses the physical step `base_step * source_stencil_scale`; it must not silently reuse the scale-1 physical step.

3. **Ray downhill also forces recenter.** If any exact negative-eigenray point improves the source-scale center by more than `0.005`, recenter to its exact best point and restart the complete axis -> base chain.

4. **Ray-clear non-PD curvature is not an interior-minimum proof.** It permits calculation at the next smaller full Hessian scale only.

5. **Major N5 closure requires two adjacent recenter-clear PD Hessian scales.** Accepted adjacent pairs are `(1,1/2)`, `(1/2,1/4)`, or `(1/4,1/8)`. A PD scale separated from another PD scale by a non-PD scale does not count.

6. **Examples:**
   - base PD + half PD -> `N5_BASE_AND_HALF_STENCIL_PASS`.
   - base non-PD + base-ray clear + half PD + quarter PD -> `N5_ADAPTIVE_HALF_AND_QUARTER_PASS`.
   - base PD + half non-PD + half-ray clear + quarter PD -> still **not** N5; calculate eighth. If eighth PD -> `N5_ADAPTIVE_QUARTER_AND_EIGHTH_PASS`.
   - half non-PD + half-ray downhill -> recenter, irrespective of base PD.
   - quarter non-PD -> quarter-ray before eighth; one isolated PD stencil is never sufficient.

7. **Artifact identity is mandatory before parse.** Every proof artifact must match the exact current center, objective fingerprint, source stencil scale, locked CLASS/Pantheon/runtime provenance, and declared worker type. Newly attached completed runs are not scientifically parsed in the same control iteration in which identity has not yet been validated.

8. **No stronger claim follows.** Passing this ladder proves only the declared local numerical Stage-4D3 interior-minimum gate. It is not a global-minimum theorem and does not by itself permit AIC/BIC/Bayes/significance claims.

## Exhaustion rule

If scale `1/8` is non-PD but exact-ray clear, do not invent an N5 pass. Record `N5_SCALE_LADDER_EXHAUSTED_CURVATURE_UNRESOLVED`. A further smaller-scale extension requires an explicit new preregistration justified by measured convergence/noise behavior.
