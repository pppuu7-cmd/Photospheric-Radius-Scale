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

## Interpretation

This explains how both facts can be true simultaneously:

1. the historical A5 LCDM point was correctly certified as a local minimum under its local multiscale Hessian/replay protocol;
2. a later B9 reoptimization could discover a lower basin of the same baseline objective outside that local neighborhood.

The new cross-basin discovery therefore does not falsify the historical local Hessian theorem. It falsifies only the stronger interpretation that the historical local basin was necessarily the best known basin after the broader B9 search.

The new seed improves the historical LCDM score by `0.5651417435669828`, far above the `0.005` recenter threshold, so the separate cross-basin stationarity/fresh-tree chain is mandatory before A5 can be re-frozen.
