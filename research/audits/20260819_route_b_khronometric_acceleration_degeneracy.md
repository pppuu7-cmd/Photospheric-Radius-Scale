# Route-B khronometric acceleration degeneracy audit — 2026-08-19

## Motivation

A promising origin for the implemented RTK kinetic denominator is the acceleration of a preferred clock congruence. Let

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

This makes the acceleration operator an important Route-B candidate, but the meaning of “healthy” depends on whether the fundamental theory is required to be a regular fully covariant DHOST scalar-tensor theory or is allowed to be a genuinely preferred-foliation spatially covariant theory, as Route A1 itself permits.

## Primary DHOST result

Ben Achour, Langlois and Noui, arXiv:1602.08398 / Phys. Rev. D 93, 124005 (2016), classify the constant-c_i khronometric action inside quadratic scalar-tensor theories. After absorbing `c1` into `c3,c4` and setting the Ricci coefficient `f=1`, their khronometric mapping gives

`alpha1 = -c3/X`, `alpha2 = -c2/X`,

and the first degeneracy condition becomes

`D0 = 4/X (c2+c3)(c4-2)`.

On the Class-I branch `c2+c3=0`, the remaining conditions reduce to

`D1 = X D2 = -8/X^2 (c2-1)^2 c4`.

The same paper explicitly notes that covariantized khronometric theories are **not generically degenerate** as ordinary quadratic DHOST theories; only special families enter the DHOST classes.

## Pure acceleration-squared proposal in ordinary DHOST language

For the simplest proposal `c2=c3=0`, with only a nonzero acceleration coefficient `c4`, `D0=0` but

`D1 = -8 c4/X^2`.

Therefore ordinary quadratic-DHOST degeneracy requires `c4=0`. A pure nonzero `a_mu a^mu` addition to Einstein-Hilbert is not by itself a regular quadratic-DHOST completion with an arbitrary clock scalar on unrestricted covariant backgrounds.

## Continuously tunable nonzero c4 branch inside constant-c_i DHOST

Suppose `c4` must remain a continuously tunable nonzero coefficient. For generic `c4 != 2`, `D0=0` forces

`c3=-c2`.

Then `D1=0` with `c4 != 0` forces

`c2=1`, `c3=-1`.

This is exactly the Class-Ib family identified in the primary classification. At this point

`alpha1=1/X`, `alpha2=-1/X`,

so

`f + X alpha2 = 0`.

That is the singular metric-kinetic Class-Ib branch. Thus it does not supply the desired regular ordinary-DHOST completion with a standard nondegenerate metric kinetic block.

Interestingly, in a flat single-scalar Fourier reduction the `c2=1,c3=-1` spatial-Hessian combination cancels at quadratic order, so the remaining scalar structure looks almost exactly like the desired acceleration term. This explains why the reduced scalar route is attractive while the regular fully covariant DHOST route is obstructed.

## Special c4=2 branch

`c4=2` solves `D0` independently and gives Class-II degenerate khronometric families under further parameter restrictions. The primary classification yields

`D1 = X D2 = 8/X^2 (1+c3)(3c2+c3-2)`,

so the two constant-coefficient families are `c3=-1` or `c3=2-3c2`. These are special Class-II branches, not a continuously tunable pure-acceleration completion; they require a separate tensor/cosmological matching analysis.

## Crucial preferred-foliation distinction

The DHOST result above must **not** be misread as proving that an `a_i a^i` term is inconsistent in a fundamental preferred-foliation theory.

Gao, arXiv:1409.6708, performs a Hamiltonian analysis directly in spatially covariant ADM variables. The allowed potential depends generally on `t,h_ij,N,R_ij` and arbitrary spatial derivatives; the healthy Hořava acceleration `a_i=partial_i ln N` is explicitly part of this spatial-potential language. When `N` enters nonlinearly but has no independent velocity `dot N`, the lapse primary/secondary constraints become second class and the broad class generically propagates three physical degrees of freedom: two tensor and one scalar.

The same paper gives the Stückelberg dictionary

`N -> 1/sqrt(2X)`,

`nabla_i N -> h_mu^nu nabla_nu N`,

showing directly how the preferred-foliation acceleration becomes a higher-derivative scalar operator after covariantization.

Therefore there are two distinct Route-B standards:

1. **regular fully covariant DHOST route:** pure/tunable constant-c_i acceleration is obstructed as described above;
2. **fundamental preferred-foliation spatially covariant route:** an `a_i a^i` potential is admissible in principle and must instead be judged by the ADM constraint count, quadratic stability, tensor sector, and cosmological matching.

This distinction is especially relevant because Route A1 explicitly permits a preferred frame and does not postulate Lorentz covariance as a fundamental symmetry.

## Consequence for C7

The simple expression

`S = integral sqrt(-g) [M_Pl^2 R/2 + P(X) + beta a_mu a^mu]`

is **not established as a regular generic DHOST completion** for arbitrary nonzero `beta`.

However, the corresponding unitary-gauge preferred-foliation action

`S = integral dt d^3x N sqrt(gamma) [L_EH + F(N) + C(N) a_i a^i]`

is **not ruled out by this DHOST audit**. It belongs to the spatially covariant route and must be analysed directly in its own Hamiltonian/ADM formulation. This is now the preferred constructive local metric+Khronon benchmark to test next.

Adding `P(X)` does not repair ordinary quadratic-DHOST degeneracy by itself, because the cited DHOST classification notes that `P(phi,X)` and terms at most linear in second derivatives do not change its quadratic degeneracy conditions. Conversely, in the preferred-foliation ADM route `F(N)=P(1/(2N^2))` is simply part of the nonlinear lapse potential and participates in the single scalar dynamics without introducing `dot N`.

## Machine audit

`rtk/route_b_khronometric_acceleration_degeneracy_audit.py`

checks the constant-c_i **ordinary-DHOST** pure-c4 obstruction, the forced `c2=1,c3=-1` tunable Class-Ib branch, the vanishing `f+X alpha2` factor, the isolated `c4=2` exception, and the reduced Fourier-space Hessian cancellation.

CI run `32197431357` passed. Artifact `9346332881`, digest `sha256:5b5ec1af374710cc17b948bbfc889e6a7bc5147c04d69dc66d4334712fa49135`.

## Claim boundary

✅ The simplest pure/tunable constant-coefficient acceleration route is ruled out **as a regular ordinary quadratic-DHOST completion with standard nondegenerate metric kinetic block**.

✅ The preferred-foliation ADM `a_i a^i` route remains admissible in principle and is now separated explicitly from the DHOST obstruction.

🔴 The preferred-foliation benchmark still needs exact quadratic matching and a project-specific ADM constraint/tensor audit.

🔴 General X-dependent DHOST completions and the special `c4=2` Class-II families remain open.

🔴 No full coupled causal-RT + metric + Khronon nonlinear theorem has yet been obtained, so C7 remains open.
