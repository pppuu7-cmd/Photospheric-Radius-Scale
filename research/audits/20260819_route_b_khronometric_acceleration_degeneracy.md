# Route-B khronometric acceleration degeneracy audit — 2026-08-19

## Motivation

A promising covariant origin for the implemented RTK kinetic denominator is the acceleration of a preferred clock congruence. Let

`X = -g^{mu nu} partial_mu T partial_nu T > 0`,

`u_mu = -partial_mu T/sqrt(X)`,

`h_mu^nu = delta_mu^nu + u_mu u^nu`.

For a hypersurface-orthogonal clock field,

`a_mu = u^nu nabla_nu u_mu = -(1/(2X)) h_mu^nu nabla_nu X`,

hence

`h^{mu nu} nabla_mu X nabla_nu X = 4 X^2 a_mu a^mu`.

Around a local Minkowski clock background `T=t+pi`, one has at linear order

`a_i = -partial_i dot(pi)`,

so an `a_mu a^mu` operator produces precisely the quadratic structure `(grad dot(pi))^2` needed for the RTK denominator `1+q^2/M^2`.

This makes the acceleration operator an important Route-B candidate, but the full metric-scalar degree-of-freedom question must be checked before accepting it.

## Primary DHOST result

Ben Achour, Langlois and Noui, arXiv:1602.08398 / Phys. Rev. D 93, 124005 (2016), classify the constant-c_i khronometric action inside quadratic scalar-tensor theories. After absorbing `c1` into `c3,c4` and setting the Ricci coefficient `f=1`, their khronometric mapping gives

`alpha1 = -c3/X`, `alpha2 = -c2/X`,

and the first degeneracy condition becomes

`D0 = 4/X (c2+c3)(c4-2)`.

On the Class-I branch `c2+c3=0`, the remaining conditions reduce to

`D1 = X D2 = -8/X^2 (c2-1)^2 c4`.

The same paper explicitly notes that khronometric theories are **not generically degenerate**; only special families enter DHOST.

## Pure acceleration-squared proposal fails

For the simplest proposal `c2=c3=0`, with only a nonzero acceleration coefficient `c4`, `D0=0` but

`D1 = -8 c4/X^2`.

Therefore DHOST degeneracy requires `c4=0`. A pure nonzero `a_mu a^mu` addition to Einstein-Hilbert is not by itself a healthy quadratic-DHOST completion.

## Continuously tunable nonzero c4 branch

Suppose `c4` must remain a continuously tunable nonzero coefficient so that the cosmological kinetic scale can be matched rather than fixed to a special isolated value. For generic `c4 != 2`, `D0=0` forces

`c3=-c2`.

Then `D1=0` with `c4 != 0` forces

`c2=1`, `c3=-1`.

This is exactly the Class-Ib family identified in the primary classification. At this point

`alpha1=1/X`, `alpha2=-1/X`,

so

`f + X alpha2 = 0`.

That is the singular metric-kinetic branch, incompatible with the Route-B requirement that the ordinary tensor gravitational kinetic sector remain nondegenerate.

Interestingly, in a flat single-scalar Fourier reduction the `c2=1,c3=-1` spatial-Hessian combination cancels at quadratic order, so the remaining scalar structure looks almost exactly like the desired acceleration term. This explains why the reduced scalar route is attractive while the full metric theory is not acceptable.

## Special c4=2 branch

`c4=2` solves `D0` independently and gives Class-II degenerate khronometric families under further parameter restrictions. This branch is **not** excluded by the tunable-c4 argument, but it does not provide an arbitrary acceleration coefficient: `c4` is fixed relative to the Einstein-Hilbert normalization. It therefore requires a separate full cosmological/tensor matching analysis and cannot be silently used as the general RTK completion.

## Consequence for C7

The simple covariant idea

`S = integral sqrt(-g) [M_Pl^2 R/2 + P(X) + beta a_mu a^mu]`

with an otherwise unmodified metric sector is **not sufficient** as a healthy full Route-B completion for arbitrary nonzero `beta`.

A viable completion must instead provide additional companion operators/constraints, for example:

- a general X-dependent degenerate DHOST combination;
- a spatially covariant action with an explicitly verified constraint/degeneracy condition;
- a constrained auxiliary-field realization generating the effective kinetic denominator while retaining the intended DOF count.

Adding `P(X)` does not repair the higher-derivative degeneracy by itself: the cited DHOST classification states that terms depending on `P(phi,X)` and terms at most linear in second derivatives do not modify the quadratic degeneracy conditions.

## Machine audit

`rtk/route_b_khronometric_acceleration_degeneracy_audit.py`

checks the pure-c4 obstruction, the forced `c2=1,c3=-1` tunable branch, the vanishing `f+X alpha2` metric factor, the isolated `c4=2` exception, and the reduced Fourier-space Hessian cancellation.

## Claim boundary

✅ The simplest pure/tunable constant-coefficient khronometric acceleration completion is ruled out as a healthy ordinary-tensor Route-B completion.

🔴 General X-dependent DHOST/spatially covariant completions are not ruled out.

🔴 The special `c4=2` Class-II families are not ruled out by this theorem and require separate matching.

🔴 No full coupled RT+metric+Khronon nonlinear action/constraint theorem has yet been obtained, so C7 remains open.
