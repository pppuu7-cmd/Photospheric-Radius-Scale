# RTK current-center base Hessian and mixed-mode diagnosis

Date: 2026-08-18

## Provenance

- workflow run: `32065998894` — success;
- artifact: `rtk-autonomous-dense-rtk-stationarity`;
- artifact ID: `9304537454`;
- artifact digest: `sha256:feff5d096411e270e1584a44fe24a3470e5d3178b6121bf18f89293d65c7bc22`;
- CLASS upstream: `36cf283628c4a3330ec9fd3d84239bf775f77317`;
- Pantheon: `7eb29dc87ba223b4ec8457cd3cccba1216c36fb7`;
- NumPy: `2.5.2`;
- objective: `matched-ultra-linstep2+dense-BOSS`;
- center fingerprint: `78171ac0528a3436969a6d5c58f6db376c0643aee736d1b1b2c0c7633066fbef`.

Accepted center tested:

- As = `2.0874341676903437e-09`
- Ob = `0.046834883174647964`
- Om = `0.25274346988872953`
- h = `0.6906937726797984`
- lambda_D = `219966.90504044993`
- ns = `0.9644273896355182`
- zre = `7.317081734823917`

## Exact-point stationarity result

For production `eff` mapping:

- `S_center = 1050.3022180985636`;
- `best_exact_S = 1050.3022180985636`;
- `best_improvement = 0.0`;
- `best_label = center`.

Thus the complete tested 101-point base stencil is recenter-clear at the frozen `0.005` tolerance.

The `k01` diagnostic is also center-best:

- `S_center = 1050.302499618449`;
- `best_exact_S = 1050.302499618449`;
- `best_improvement = 0.0`.

## Curvature result

The `eff` Hessian eigenvalues are

`[-0.0044758233976694844, 0.00014469889940377578, 0.0336156235369222, 0.07123211780980822, 0.2472028959256006, 3.0710463945625275, 7.327945929821453]`.

Therefore the base Hessian is **not positive definite**.

Crucially, the negative mode is no longer the almost-pure `log(lambda_D)` direction.  In coordinate order

`[loglam, h, Ob, Om, As, ns, zre]`

the normalized negative eigenvector (sign chosen with positive h component) is approximately

`[+8.65e-05, +0.71564, -0.37664, -0.41625, -0.03308, +0.41355, +0.02472]`.

The next-smallest eigenvector is instead almost pure `loglam` and has a small **positive** eigenvalue `+1.44699e-4`.

## Interpretation

This invalidates the earlier working hypothesis that all residual curvature ambiguity at the final RTK center is merely the near-flat `lambda_D` direction.  The current base Hessian contains a distinct mixed standard-cosmological negative-curvature combination dominated by `h`, `Ob`, `Om`, and `ns`.

At the same time, no one of the 101 exact tested stencil points is downhill.  Therefore the negative Hessian eigenvalue must be tested directly along its eigenvector and at a smaller stencil before being interpreted as a physical saddle.

Two independent follow-ups are now required and have been launched:

1. Stage4D3 half-stencil Hessian (`0.5` scale), run `32079555818`;
2. exact mixed-mode ray profile along the negative eigenvector.

## Claim boundary

Allowed now:

> The current RTK center is exact-point recenter-clear on the full base stencil, but its base local Hessian is non-PD because of a mixed cosmological negative mode.  Interior-minimum certification is therefore still unresolved.

Not allowed:

> RTK has a certified interior local minimum.

or

> The only remaining flat/negative direction is lambda_D.
