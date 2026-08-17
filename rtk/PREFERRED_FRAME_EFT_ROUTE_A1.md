# RTK preferred-frame nonlinear EFT Route A1

Date: 2026-08-18

Status: **explicit research EFT postulate; not a derivation of the unique fundamental DBI/Khronon action.**

## Purpose

`NONLINEAR_EFT_COMPLETION_GATE.md` left the nonlinear symmetry class open because the linear CLASS implementation cannot determine it uniquely. This document makes an explicit choice for the next theorem layer: **Route A1**, a reduced preferred-frame scalar EFT completion. The choice is operational and falsifiable. It does not claim that the fundamental RTK theory must obey this symmetry set.

## A1. Frozen symmetry/field assumptions

Field content for the reduced nonlinear sector: one real scalar fluctuation `pi(t,x)` on the preferred cosmological foliation.

The Route A1 EFT assumes:

1. locality in preferred-frame spacetime coordinates;
2. spatial translations and SO(3) rotations;
3. spatial parity;
4. an **explicitly postulated** constant internal shift symmetry `pi -> pi + const`;
5. no assumption of Lorentz invariance away from the preferred frame;
6. no assumption of time-reversal symmetry;
7. EFT coefficients may depend slowly on cosmological background time; in a local strong-coupling patch they are treated adiabatically as constants;
8. through the cubic order studied here, no operator contains more than one time derivative acting on any individual `pi` field;
9. cubic derivative truncation: three powers of `pi` and at most four derivatives in total.

The constant shift is a **new explicit EFT postulate**, not something inferred from the linear equations. A future covariant/DBI Route B may supersede A1.

## A2. Required quadratic target

Every A1 completion must reproduce

`L2 = K/2 dot(pi)^2 + K/(2 M^2) (grad dot(pi))^2 - G/2 (grad pi)^2`,

with

- `G = rho + p > 0`,
- `K = (rho+p)/c_a^2 > 0`,
- `M = k_* > 0`.

Its mode kinetic operator is

`K_q = K (1 + q^2/M^2) > 0`,

and

`omega^2 = (G/K) q^2/(1+q^2/M^2)`.

## A3. Complete cubic basis through total derivative order D <= 4

Because of constant-shift symmetry, every `pi` must be differentiated at least once.

### D = 3

All three fields carry one derivative. Rotational invariance leaves exactly two scalar monomials:

`O1 = dot(pi)^3`,

`O2 = dot(pi) (grad pi)^2`.

There is no rotational scalar made from two time derivatives and one spatial gradient, and three identical spatial gradients cannot give a nonzero parity-even scalar.

### D = 4

The derivative partition is `(2,1,1)`. Second time derivatives are excluded by the A1 definition. Up to integration by parts, two additional operators remain:

`O3 = dot(pi)^2 Laplacian(pi)`,

`O4 = (grad pi)^2 Laplacian(pi)`.

Two common alternative representatives are redundant:

`dot(pi) grad(pi).grad(dot(pi)) = -1/2 dot(pi)^2 Laplacian(pi) + spatial boundary`,

`grad_i(pi) grad_j(pi) grad_i grad_j(pi) = -1/2 (grad pi)^2 Laplacian(pi) + spatial boundary`.

Therefore the Route A1 cubic action to this derivative order is

`L3 = c1(t) O1 + c2(t) O2 + c3(t) O3 + c4(t) O4`.

This is a **complete basis only under the explicitly frozen A1 assumptions and derivative truncation**. It is not a complete basis of every possible nonlinear Khronon theory.

## A4. Reduced-scalar degree-of-freedom statement

Using the integration-by-parts representatives above, the Lagrangian depends on `pi`, `dot(pi)`, spatial derivatives of `pi`, and `grad dot(pi)` from `L2`, but contains no `ddot(pi)`.

The generalized canonical momentum is

`P = dL/d dot(pi) - grad_i[dL/d(grad_i dot(pi))]`

which through cubic order gives

`P = K(1-Laplacian/M^2) dot(pi) + 3 c1 dot(pi)^2 + c2 (grad pi)^2 + 2 c3 dot(pi) Laplacian(pi)`.

The velocity Hessian/operator is

`delta P / delta dot(pi) = K(1-Laplacian/M^2) + 6 c1 dot(pi) + 2 c3 Laplacian(pi)`.

At the background `pi=0`, Fourier eigenvalues are exactly

`K(1+q^2/M^2) > 0`.

Hence, in the perturbative EFT neighborhood where the cubic correction does not drive this operator through zero, the velocity map remains invertible. The reduced A1 scalar sector therefore propagates **one scalar canonical pair through cubic order** and does not introduce an Ostrogradsky degree of freedom from higher time derivatives.

This is a reduced-scalar EFT theorem. It is **not** a Hamiltonian constraint proof for the full metric + lapse + shift + RT nonlocal sector.

## A5. Canonical normalization and interaction-scale placeholders

In the low-momentum regime `q << M`, define

`pi_c = sqrt(K) pi`.

In four spacetime dimensions the canonically normalized cubic basis can be parameterized as

`L3_c = a1/Lambda1^2 dot(pi_c)^3`

`     + a2/Lambda2^2 dot(pi_c)(grad pi_c)^2`

`     + a3/Lambda3^3 dot(pi_c)^2 Laplacian(pi_c)`

`     + a4/Lambda4^3 (grad pi_c)^2 Laplacian(pi_c)`.

The powers of `Lambda_i` follow from mass dimensions. Their numerical values are **not determined** by the linear CLASS equations. At `q ~ M`, canonical normalization is momentum dependent because the quadratic kinetic factor is `K(1+q^2/M^2)`; a physical strong-coupling analysis must use that full kinetic normalization and the actual nonlinear coefficients.

Therefore Route A1 does not convert `M`/`k_*` into a strong-coupling scale.

## A6. What this closes and what remains open

### Closed inside the Route A EFT program

- nonlinear research route selected: preferred-frame reduced scalar EFT;
- explicit symmetry class frozen;
- cubic derivative truncation frozen;
- complete cubic operator basis through `D <= 4` derived modulo spatial integration by parts;
- reduced scalar sector shown to retain one time degree of freedom perturbatively through cubic order, provided the velocity Hessian remains invertible.

### Still open

- whether Route A1 is the fundamental DBI/Khronon completion;
- coupling of the nonlinear scalar completion to metric/lapse/shift and the RT nonlocal auxiliary sector;
- full constraint algebra and total physical DOF count of the complete theory;
- numerical values of `c1...c4`;
- physical strong-coupling scale;
- radiative closure/naturalness;
- UV completion.

## Claim boundary

Allowed after symbolic audit:

> The RTK research program has an explicitly frozen preferred-frame Route A1 nonlinear scalar EFT class. Within that class, the cubic basis through four derivatives is finite and the reduced scalar sector retains one perturbative time degree of freedom through cubic order.

Not allowed:

> The full fundamental RTK gravity theory is now proven ghost-free.
