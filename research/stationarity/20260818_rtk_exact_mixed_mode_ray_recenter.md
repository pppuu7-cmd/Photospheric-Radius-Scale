# RTK exact mixed-mode ray recenter result

Date: 2026-08-18

## Provenance

Workflow run `32079620601` — success.

Artifact:
- `rtk-current-mixed-mode-ray`;
- ID `9305064814`;
- digest `sha256:fcbdf2d0a24a7b8a6c3272894a86d21d14bbb3daf5567d243233d49acecc2058`.

The profile used the frozen objective `matched-ultra-linstep2+dense-BOSS` and the exact negative eigenvector of base-Hessian run `32065998894` at center fingerprint

`78171ac0528a3436969a6d5c58f6db376c0643aee736d1b1b2c0c7633066fbef`.

Coordinate order is

`[loglam, h, Ob, Om, As, ns, zre]`.

The ray direction was approximately

`[8.651885e-05, 0.715640269, -0.376643177, -0.416254198, -0.033080705, 0.413552729, 0.024721757]`.

## Exact ray points

| t | S_eff |
|---:|---:|
| -2.00 | 1050.340663082952 |
| -1.50 | 1050.3368056012223 |
| -1.00 | 1050.3264088015906 |
| -0.50 | 1050.3082478230463 |
| -0.25 | 1050.3051895601707 |
| 0.00 | 1050.3022180985636 |
| +0.25 | 1050.2996411357158 |
| +0.50 | 1050.2980359092155 |
| +1.00 | 1050.2768798143277 |
| +1.50 | **1050.275007936606** |
| +2.00 | 1050.279086171286 |

Best exact improvement over the former center:

`Delta S = 1050.3022180985636 - 1050.275007936606 = 0.0272101619575551`.

This is more than five times the frozen recenter threshold `0.005`.

Therefore the former center is **not recenter-clear** once the mixed Hessian eigendirection is tested directly.

## New exact point

The exact best tested ray point, at `t=+1.5`, has

- `As = 2.0872356834621613e-09`
- `Ob = 0.046795335641066506`
- `Om = 0.2523064029808687`
- `h = 0.6910694838209896`
- `lambda_D = 219968.33239135708`
- `ns = 0.9646445048182237`
- `zre = 7.319677519287684`
- `S_eff = 1050.275007936606`
- `S_k01 = 1050.2752882692346`.

The corresponding provisional, **not frozen**, raw difference to the already accepted LCDM best-exact score is

`1050.275007936606 - 1049.966118347761 = +0.308889588845`.

This number is only a progress diagnostic. The RTK minimum has moved again and must pass the complete axis/Hessian/multiscale protocol before any raw matched difference is frozen.

## Curvature along the ray

Symmetric finite differences along the ray are not monotonic in scale:

- `|t|=0.25`: curvature `+0.00631198`;
- `|t|=0.5`: `+0.00739014`;
- `|t|=1`: `-0.00114758`;
- `|t|=1.5`: `+0.00327882`;
- `|t|=2`: `+0.00382826`.

The decisive information is not the sign of any one quadratic estimate but the exact downhill objective values. The profile is asymmetric and strongly non-quadratic over the tested range, which explains why coordinate-axis/corner samples could miss the improvement.

## Consequences

1. Current-center Stage4D3 certification is reset.
2. Half-stencil run `32079555818`, which was launched at the former center, becomes scientifically stale once the recenter is committed and must not be used to certify the new center.
3. The new exact point must first pass the standard 15-point axis gate.
4. Only after that may a new Hessian/multiscale sequence begin.

## Claim boundary

Established:

> The frozen objective has an exact RTK point 0.02721 lower than the previous accepted center along a mixed `h-Ob-Om-ns` direction, so the previous center is not locally frozen under the predeclared 0.005 recenter rule.

Not established:

> The new ray point is the final or global RTK minimum.
