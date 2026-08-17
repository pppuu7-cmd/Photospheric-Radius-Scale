# RTK adaptive multiscale curvature convergence protocol

Date: 2026-08-18
Status: **pre-registered before the 1/2-stencil result of run 32079555818 is known**.

## Purpose

The frozen matched-comparison recenter rule and the stronger Stage4D3 interior-minimum proof are distinct.  The current accepted RTK center is exact-point recenter-clear on the scale-1 101-point stencil, but the scale-1 finite-difference Hessian has a mixed negative eigenvalue.  A smaller stencil is already running.

This document specifies in advance how to interpret possible sign changes with stencil scale.  It is designed to prevent post-hoc selection of whichever stencil gives a preferred curvature sign.

## Coordinate convention

The stationarity worker uses normalized stencil coordinates `y`, with physical steps

`Delta theta_i(s) = s * Delta theta_i(base)`.

The reported `H_y(s)` is a second difference with unit steps in `y`; therefore, for a genuinely smooth local quadratic objective,

`H_y(s) ~ s^2 H_normalized_physical`

(up to the fixed diagonal rescaling by the declared base-step vector).

Consequently:

- **sign / inertia** of the Hessian may be compared directly across scales;
- magnitudes must be compared after dividing by `s^2`;
- gradients must be compared after dividing by `s`.

A raw eigenvalue at `s=1/2` is not expected to equal its `s=1` value; approximately one quarter is expected for a converged quadratic direction.

## Fixed scale hierarchy

The pre-registered hierarchy is

`1 -> 1/2 -> 1/4 -> 1/8 (only if still needed)`.

The project must never skip to a convenient scale after seeing a result.  It proceeds monotonically to smaller scales only when the preceding result does not settle the curvature question.

## Recenter gate at every scale

At every tested scale, the frozen rule is unchanged:

`S_center - S_best_exact > 0.005  => recenter`.

If this occurs at any scale, all curvature certification at the old center is void and the state machine restarts from an exact axis gate at the new center.

## Standard N5 pass

If two adjacent tested scales `s` and `s/2` are both:

1. recenter-clear (`best_improvement <= 0.005`), and
2. positive definite using the declared numerical PD threshold,

then the curvature sign has passed the original Stage4D3 two-scale requirement at that accepted stencil pair.

The ordinary case is `s=1` and `s/2=1/2`.

## Adaptive case after a coarse non-PD Hessian

If scale `1` is recenter-clear but non-PD while scale `1/2` is recenter-clear and PD, **do not certify an interior minimum yet**.  Instead:

1. run scale `1/4` at the identical center/objective;
2. require scale `1/4` to be recenter-clear and PD;
3. compare `H_y(1/2)/(1/2)^2` with `H_y(1/4)/(1/4)^2` as the adjacent convergent pair;
4. require no exact mixed-mode ray inherited from the coarse negative eigendirections to show improvement `>0.005` over the tested local radius.

Only then may scale `1` be classified as a **coarse finite-difference curvature artifact** and the accepted proof stencil be redefined to `1/2`, with `1/4` as its required smaller-stencil stability test.

This is not permission to ignore a negative coarse result merely because a smaller one is positive.  The two smaller adjacent scales and direct exact-ray falsification are mandatory.

## If scale 1/2 is also non-PD

A second non-PD result is not automatically proof of a physical saddle.  The next action is decided by the exact mixed-mode ray:

- if an exact ray point improves the objective by `>0.005`, recenter/restart;
- if the ray is recenter-clear but shows stable negative symmetric curvature as `|t| -> 0`, classify the center as curvature-unresolved / likely saddle and do not claim an interior minimum;
- if the ray is recenter-clear and the inferred curvature changes sign toward positive at smaller `|t|`, a `1/4` Hessian is justified as a convergence test.

## Convergence diagnostics

For adjacent scales `s` and `s/2`, record at minimum:

- inertia / number of negative eigenvalues;
- `lambda_min(H_y)/s^2`;
- sorted normalized eigenvalues `eig(H_y)/s^2`;
- overlap of corresponding low-curvature eigenvectors/subspaces;
- Frobenius relative change of the normalized Hessians;
- exact best improvement at each scale.

No single relative-difference cutoff is used as a hidden acceptance criterion unless separately pre-registered.  The theorem-level acceptance condition is sign stability (PD) on two adjacent scales plus no frozen-tolerance downhill point; the continuous diagnostics quantify convergence quality.

## Claim boundary

Allowed after an adaptive `1/2 -> 1/4` pass:

> The RTK center is an interior local minimum under the pre-registered adaptive multiscale numerical proof, with scale 1 identified as outside the converged finite-difference curvature regime and the adjacent 1/2 and 1/4 stencils providing the accepted PD stability pair.

Not allowed before that pair is obtained:

> A positive 1/2-stencil Hessian by itself overrides the negative scale-1 Hessian.
