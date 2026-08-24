# A5 LCDM cross-basin geometry diagnostic — 2026-08-24

Status: **DIAGNOSTIC / EXPLANATORY, NOT A STATIONARITY CERTIFICATE**

The independently replayed new LCDM seed of the unchanged A5 objective is

- `h=0.6803133881531521`
- `Ob=0.048406958808714234`
- `Om=0.25869220161756795`
- `As=2.099031119902081e-09`
- `ns=0.9662859140870312`
- `zre=7.684806125603674`.

The historical independently replayed A5 LCDM accepted-score point is

- `h=0.6782837587382693`
- `Ob=0.04858764689799632`
- `Om=0.2611722579449536`
- `As=2.1054040998203598e-09`
- `ns=0.9653185632254442`
- `zre=7.788312934950947`.

Using the frozen local LCDM stencil geometry

- `delta h=0.00035`
- `delta Ob=0.00007`
- `delta Om=0.0007`
- `delta As=4e-12`
- `delta ns=0.00035`
- `delta zre=0.07`,

the displacement from the historical point to the new seed, in normalized stencil coordinates, is

- `Delta h / delta h = +5.798941185379507`
- `Delta Ob / delta Ob = -2.581258418315528`
- `Delta Om / delta Om = -3.5429376105508954`
- `Delta As / delta As = -1.5932449795697474`
- `Delta ns / delta ns = +2.7638596045344497`
- `Delta zre / delta zre = -1.4786687049610439`.

The Euclidean norm in this normalized coordinate system is

`||Delta y||_2 = 8.075074700794058`.

Thus the new seed is not a small perturbation inside the historical one-step local Hessian neighborhood. The dominant coordinate displacement alone is almost six frozen `h` steps, with simultaneous multi-step motion in `Om`, `ns`, and `Ob`.

## Projection onto the historical local quadratic geometry

The live historical state stores a positive-definite six-dimensional LCDM Hessian in the same normalized parameter geometry. Its eigenvalues are

`[0.01076000540446865, 0.05095906682522973, 0.058585744253312616, 0.24761409818154007, 2.9769326338378908, 7.054039686019683]`.

That Hessian was centered one `Ob` base step above the final accepted-score point; the accepted score itself was the exact `axis_1_-1` point. It is therefore used here only as a nearby local quadratic diagnostic, not as an exact Hessian at the final accepted-score coordinates.

Projecting the normalized old-to-new displacement direction onto this eigensystem gives squared mode weights approximately

- softest mode: `0.804312264`;
- second-softest mode: `0.185425374`;
- third mode: `0.007287283`;
- fourth mode: `0.002266682`;
- fifth mode: `0.000549233`;
- stiffest mode: `0.000159164`.

Thus about `98.97%` of the direction norm lies in the two softest historical Hessian modes.

The corresponding local Rayleigh curvature is still positive:

`(Delta y)^T H (Delta y) / ||Delta y||^2 = 0.021849479777598664`.

For the full displacement the pure quadratic term would be

`0.5 * (Delta y)^T H (Delta y) = +0.7123676722734782`.

But the exact endpoint difference is instead

`S_new - S_old = -0.5651417435669828`.

Therefore the objective must depart strongly from the historical local quadratic approximation somewhere along the route to the new basin: the local curvature points uphill, while the distant endpoint is substantially downhill. This is precisely why the separately frozen exact old-to-new line-profile diagnostic is useful.

Target for that diagnostic:

`research/robustness/A5_LCDM_OLD_TO_NEW_BASIN_LINE_PROFILE_TARGET_v1.json`.

## Interpretation

This explains how both facts can be true simultaneously:

1. the historical A5 LCDM point was correctly certified as a local minimum under its local multiscale Hessian/replay protocol;
2. a later B9 reoptimization could discover a lower basin of the same baseline objective outside that local neighborhood.

The new cross-basin discovery therefore does not falsify the historical local Hessian theorem. It falsifies only the stronger interpretation that the historical local basin was necessarily the best known basin after the broader B9 search.

The new seed improves the historical LCDM score by `0.5651417435669828`, far above the `0.005` recenter threshold, so the separate cross-basin stationarity/fresh-tree chain is mandatory before A5 can be re-frozen.
