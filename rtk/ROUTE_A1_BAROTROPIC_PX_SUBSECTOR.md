# RTK Route A1: long-wavelength barotropic P(X) subsector

Date: 2026-08-18

Status: **conditional low-derivative reconstruction inside Route A1; not the complete finite-k Khronon action.**

## Motivation

The implemented Khronon background is barotropic and obeys `x=x0/a^3` together with the exact identity `c_a^2=dp/drho`. Route A1 already postulates a constant-shift scalar EFT. These facts allow a minimal two-derivative shift-symmetric `P(X)` **subsector** to be reconstructed in the long-wavelength limit.

This does not contradict the earlier result that pure `P(X)` is insufficient for the full finite-k dispersion. The role of this reconstruction is narrower: determine the part of the cubic EFT that is already fixed by background thermodynamics, and isolate which coefficients require genuinely higher-spatial-derivative completion data.

## 1. Barotropic reconstruction

Let `n` be the conserved number-density coordinate. Since the implementation has

`x = x0/a^3`,

we may choose `n` proportional to `x`; the constant of proportionality is a field-normalization convention.

For an isentropic shift-symmetric `P(X)` fluid,

`p=P`,

`rho=2 X P_X-P`,

and the chemical potential satisfies

`sqrt(2X) = (rho+p)/n`.

Choosing `n=x` fixes a convenient representative

`X(x) = 1/2 [(rho(x)+p(x))/x]^2`.

A constant rescaling of `X` corresponds to a field normalization and does not change the invariant combinations below.

For the exact implemented Khronon thermodynamics,

`rho = 2 mu_K^2 x (1+t)`,

`p = 2 mu_K^2 r t`,

with

`s=sqrt(1+lambda_D x^2)`, `r=x/s`, `t=x/(s+1)`.

The symbolic audit verifies

`d ln[(rho+p)/x] / d ln x = c_a^2`,

hence

`d ln X/d ln x = 2 c_a^2`.

## 2. Quadratic matching

Use the time-shift Goldstone convention locally,

`phi(t,x) = phi_bar(t+pi)`

with slowly varying background `dot(phi_bar)` treated as constant in the local patch. Then

`X = X0[(1+dot pi)^2-(grad pi)^2]`.

Expanding `P(X)` to quadratic order gives

`L2 = K/2 dot(pi)^2 - G/2 (grad pi)^2`,

where

`G = 2X P_X = rho+p`,

`K = 2X P_X + 4X^2 P_XX = (rho+p)/c_a^2`.

Thus the low-q part of the already established Route-A1 quadratic target is exactly the barotropic `P(X)` result. The extra `(grad dot pi)^2/M^2` term required by the implemented finite-k dispersion remains outside pure `P(X)`.

## 3. Cubic coefficients fixed by thermodynamics

Expanding `P(X)` to cubic order gives only the Route-A1 `D=3` operators

`O1 = dot(pi)^3`,

`O2 = dot(pi)(grad pi)^2`.

Their coefficients are

`c1_PX = 2 X^2 P_XX + (4/3) X^3 P_XXX`,

`c2_PX = -2 X^2 P_XX`.

Using the quadratic coefficients, these become the invariant thermodynamic relations

`c2_PX = -(K-G)/2`,

`c1_PX = [dK/d ln X - K]/3`.

Since `d ln X/d ln x = 2 c_a^2`, the first relation involving a derivative can also be evaluated directly from the implemented background functions:

`c1_PX = { [dK/d ln x]/(2 c_a^2) - K }/3`.

Therefore, **conditional on the minimal long-wavelength shift-symmetric P(X) reconstruction, the coefficients of `O1` and `O2` are fixed functions of the implemented background thermodynamics.**

## 4. What remains genuinely nonlinear/frequency dependent

Pure `P(X)` cannot generate the established quadratic operator

`K/(2M^2) (grad dot pi)^2`

or the corresponding finite-k denominator in the dispersion. Therefore it cannot determine the complete higher-spatial-derivative nonlinear completion.

In the Route-A1 basis this means:

- `c1` and `c2` have a thermodynamically fixed **minimal P(X) long-wave contribution**;
- `c3` and `c4` are not fixed by background thermodynamics;
- higher-spatial-derivative completion can in principle also renormalize/mix the finite-q realization of the cubic vertices, so the P(X) values must not be extrapolated blindly to `q~M`;
- the physical strong-coupling scale still cannot be obtained without the higher-derivative nonlinear coefficients.

## 5. Claim boundary

Allowed after symbolic audit:

> The implemented Khronon background admits a minimal shift-symmetric barotropic P(X) reconstruction in the long-wavelength limit. In that conditional subsector, the Route-A1 D=3 cubic coefficients are fixed by `G`, `K`, and the background derivative of `K`.

Not allowed:

> The full finite-k Khronon action has been reconstructed as P(X).

or

> All four Route-A1 cubic coefficients are now known.

or

> The strong-coupling scale is now known.
