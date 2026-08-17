# RTK log-lambda low-mode diagnostic

This note compares the two consecutive matched-ultra+dense RTK 7D local Hessians before the latest recenter.

Coordinate ordering is fixed by `rtk/autonomous_dense_rtk_stationarity.py` as:

`[loglam, h, Ob, Om, As, ns, zre]`.

## First Hessian

Minimum eigenvalue:

`-2.347590562032417e-4`

Normalized minimum-mode eigenvector (sign convention chosen with positive loglam component):

`[0.999985999, -0.00389745, 0.00177195, 0.00228277, 0.000401024, -0.00204616, 0.000337410]`

Squared log-lambda weight:

`0.999971998` (about 99.9972%).

## Repeated/recentered Hessian, run 32047204215

Minimum eigenvalue:

`+3.721256411550938e-4`

Normalized minimum-mode eigenvector:

`[0.999999897, 0.000321165, -0.0000936894, -0.0000729608, 0.000161946, 0.0000873125, 0.000232634]`

Squared log-lambda weight:

`0.999999795` (about 99.99998%).

Absolute eigenvector overlap between the two low modes:

`|v_first · v_repeat| = 0.9999842766`.

## Interpretation

The almost-flat mode is a stable physical/numerical direction aligned overwhelmingly with `log(lambda_D)`, not an unstable mixture of the six standard cosmological directions. What is not yet stable is the tiny curvature *sign*: it moved from approximately `-2.35e-4` to `+3.72e-4` after recentering while the eigendirection stayed essentially unchanged.

This is consistent with the independent wide BOSS lambda scan and the dust-limit Khronon diagnostic: lambda_D is weakly identifiable in the current solution. Therefore a smaller-stencil repeat is scientifically required before claiming an interior local minimum. The Stage4D3 gate should require positive curvature on both base and half stencils; otherwise classify the direction as curvature/boundary unresolved rather than treating one Hessian sign as decisive.
