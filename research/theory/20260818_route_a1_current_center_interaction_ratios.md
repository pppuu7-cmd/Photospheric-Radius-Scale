# Route A1 current-center long-wave interaction ratios

Date: 2026-08-18

## Provenance

Workflow run `32077282673` — success.

Artifact:
- `rtk-route-a1-background-ratios`;
- ID `9303879486`;
- digest `sha256:17cc45e0ff69adc11028108ce243977605143dad2eef20cbdf6ca1f559b608df`.

Pinned/current-center inputs:
- `gamma = 0.051663386535`;
- `lambda_D = 219966.90504044993`;
- `Omega_K0 = 0.25274346988872953`;
- `H0_CLASS = 2.3039064334293504e-4 1/Mpc`;
- exact closure `x0 = 0.8136230391761893`.

This diagnostic is conditional on the already-proved long-wave shift-symmetric `P(X)` subsector of Route A1. It does not determine the finite-k D4/D5 completion or the physical strong-coupling cutoff.

## Present epoch

At `a=1` (`z=0`):

- `w = 5.561055612226226e-6`;
- `c_a^2 = 1.4611272297306721e-8`;
- `K/H0^2 = 5.18938125851934e7`;
- `M_K/H0 = 5093.81058664304`;
- `c1/K = 3.421991980676246e7`;
- `c2/K = -0.49999999269436385`;
- `c_a^2 * c1/K = 0.49999656628860584`;
- sufficient homogeneous Legendre-map radius `|dot(pi)| < 4.870457546593385e-9`;
- `|dot(pi)|_safe / c_a^2 = 0.33333562248998333`.

This directly verifies the analytically derived dust-limit structure

`c_a^2 (c1/K) -> 1/2`,

`c2/K -> -1/2`,

`|dot(pi)|_safe / c_a^2 -> 1/3`.

## Evolution toward the dust limit

Selected rows:

| z | c_a^2 | c1/K | c2/K | c_a^2 c1/K | safe |dot(pi)|/c_a^2 |
|---:|---:|---:|---:|---:|---:|
| 0 | 1.461127e-8 | 3.421992e7 | -0.499999993 | 0.499996566 | 0.333335622 |
| 0.25 | 3.830286e-9 | 1.305383e8 | -0.499999998 | 0.499999100 | 0.333333933 |
| ~0.493 | 1.321724e-9 | 3.782934e8 | -0.4999999993 | 0.499999689 | 0.333333540 |
| 1 | 2.283034e-10 | 2.190067e9 | -0.4999999999 | 0.499999946 | 0.333333369 |
| 2 | 2.004310e-11 | 2.494624e10 | -0.49999999999 | 0.499999995 | 0.333333336 |
| 9 | 1.461142e-14 | 3.421980e13 | -0.5 | 0.49999999998 | 0.33333333335 |

Thus the large raw ratio `c1/K` is not a numerical instability. It is the expected compensation for the very small sound speed on the DBI dust-like branch.

## Canonical D3 coefficient-suppression proxies

Using the low-q canonical normalization adopted in Route A1, the bookkeeping scales at z=0 are

- `Lambda1_proxy = 2.7481426042441814e-5 eV`;
- `Lambda2_proxy = 0.2273493724357892 eV`;
- `Lambda1/H0 = 1.8652562445727608e28`;
- `Lambda2/H0 = 1.5430961842396246e32`.

These numbers only characterize the coefficients of the two reconstructed long-wave D3 operators. They are **not physical strong-coupling cutoffs**. The finite-k momentum-dependent normalization and presently underdetermined D4/D5 coefficients can set a lower physical interaction scale.

## Interpretation boundary

Established:

- the conditional D3 reconstruction is numerically evaluated on the actual current cosmological branch;
- the analytic DBI dust-limit identities are quantitatively reproduced;
- the homogeneous reduced-scalar velocity map has a finite explicit sufficient perturbative neighborhood at the current center.

Not established:

- a fluid-variable-to-`pi` mapping for observed cosmological perturbation amplitudes;
- physical scattering unitarity/strong-coupling cutoff;
- the values of `c3,c4` or D5 dispersive coefficients;
- full metric + RT + Khronon nonlinear constraint health.
