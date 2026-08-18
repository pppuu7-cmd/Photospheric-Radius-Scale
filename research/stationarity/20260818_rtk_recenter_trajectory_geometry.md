# RTK recenter trajectory geometry

Date: 2026-08-18

Status: diagnostic of the exact matched-dense stationarity trajectory; not a global-minimum proof.

## Score sequence

The accepted/recentered RTK trajectory on the frozen `matched-ultra-linstep2+dense-BOSS` objective has so far moved through:

| stage | exact S_eff | improvement to next accepted point |
|---|---:|---:|
| c0 | 1050.4261151803064 | 0.09340731445036 |
| c1 | 1050.3327078658560 | 0.03048976729247 |
| c2 | 1050.3022180985636 | 0.02721016195756 |
| c3 | 1050.2750079366060 | 0.02509550681907 |
| c4 current | 1050.2499124297870 | pending current Hessian |

Current c4 is the center of heavy Hessian run `32117012431`.

## Physical/stencil coordinates

Base steps are

- log(lambda_D): 0.05
- h: 0.00035
- Omega_b: 0.00007
- Omega_m: 0.0007
- A_s: 4e-12
- n_s: 0.00035
- z_reio: 0.07

The normalized recenter displacements are:

### c0 -> c1

Norm = `1.27667` stencil units.

`(loglam,h,Ob,Om,As,ns,zre) = (0.03861, 0.44529, 0.02932, -0.29376, 0.60869, 0.21018, 0.96347)`.

### c1 -> c2

Norm = `0.61555` stencil units.

`(0.21226, 0.15656, -0.04957, -0.08333, 0.31763, -0.01853, 0.44576)`.

### c2 -> c3: exact negative-eigenray recenter

Norm = exactly `1.5` stencil units to numerical precision, matching the exact ray grid point `|t|=1.5`.

Normalized direction (divide displacement by 1.5):

`(loglam,h,Ob,Om,As,ns,zre)`

`= (8.65e-05, +0.71564, -0.37664, -0.41625, -0.03308, +0.41355, +0.02472)`.

This is a key diagnostic result. The negative mode exposed after run `32065998894` is **not** the earlier almost-pure log(lambda_D) weak-curvature mode. Its lambda component is essentially zero. It is a strongly mixed standard-cosmological-parameter direction dominated by h, Omega_b, Omega_m and n_s.

Therefore the exact improvement from `1050.3022180985636` to `1050.275007936606` is evidence for a real mixed CMB-correlated downhill direction that independent coordinate-axis tests could not see.

### c3 -> c4: half-stencil recenter

Norm = `0.33813` base-stencil units.

`(loglam,h,Ob,Om,As,ns,zre) = (-0.04649, +0.09782, +0.07708, -0.02857, +0.13678, -0.24779, +0.12545)`.

The smaller displacement after the mixed-mode recenter is encouraging but is not itself convergence proof.

## Scientific interpretation

Two distinct curvature phenomena have appeared during RTK stationarity:

1. an early very weak mode almost purely aligned with log(lambda_D), physically consistent with the deep Khronon dust-limit / poor lambda_D identifiability;
2. a later, substantially more negative mixed mode with nearly zero lambda_D component, dominated by correlated standard cosmological parameters and invisible to the axis-only gate.

These must not be conflated. The second phenomenon is why exact negative-eigenray falsification is now a mandatory Stage4D3 step before accepting a non-PD coarse Hessian.

The trajectory also explains the component-level behavior: successive recentering has primarily improved the Planck/high-l CMB fit while leaving the BOSS geometry-growth penalty intact or slightly larger.

## Cycling/convergence watch

For each future recenter, record the normalized displacement and compare its direction with the c2->c3 mixed mode. Repeated large displacements with high absolute overlap would indicate an extended valley requiring a better local coordinate/optimizer treatment; shrinking displacements and recenter-clear adjacent stencils would support convergence.

No global-minimum statement follows from this trajectory alone.
