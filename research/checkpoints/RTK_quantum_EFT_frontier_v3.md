# RTK quantum / EFT consistency frontier v3

Date: 2026-08-18

This checkpoint supersedes v2 for the current theorem frontier. It preserves the previous quadratic-EFT and strong-coupling-identifiability results and adds the first validated nonlinear reduced-scalar EFT layer.

## Previously established theorem layer

✅ Background algebraic sign stability over broad scans.

✅ Exact symbolic identity `c_a^2 = dp/drho`.

✅ Positive quadratic gradient coefficient `G=rho+p` on the tested domain.

✅ Positive quadratic kinetic coefficient `K=(rho+p)/c_a^2` on the tested domain.

✅ Constructive local preferred-frame quadratic action reproduces the implemented finite-k dispersion exactly.

✅ Quadratic Fourier Hamiltonian is positive for `G>0`, `K>0`, `M^2>0`.

✅ No higher time derivatives in the quadratic representative.

✅ Pure two-derivative `P(X)` is insufficient for the implemented finite-k sector.

✅ Strong-coupling scale is not identifiable from the current linear CLASS equations; `M_K/k_*` is not derivable as the cutoff.

## New Route A1 nonlinear theorem layer

The project has now made an explicit **research EFT choice**, not a claim of unique fundamental derivation.

Route A1 assumptions are frozen in `rtk/PREFERRED_FRAME_EFT_ROUTE_A1.md`:

- preferred-frame locality;
- spatial translations and SO(3) rotations;
- parity;
- explicitly postulated constant shift `pi -> pi + const`;
- no Lorentz-invariance assumption away from the preferred frame;
- no time-reversal assumption;
- slowly time-dependent background coefficients;
- through the cubic truncation, no more than one time derivative acting on an individual field;
- three fields and total derivative order `D <= 4`.

Within this declared class the cubic basis is

`O1 = dot(pi)^3`,

`O2 = dot(pi)(grad pi)^2`,

`O3 = dot(pi)^2 Laplacian(pi)`,

`O4 = (grad pi)^2 Laplacian(pi)`.

Two nontrivial integration-by-parts redundancies are symbolically verified, leaving four independent representatives in the declared truncation.

The reduced scalar generalized momentum is

`P = K(1-Laplacian/M^2) dot(pi) + 3 c1 dot(pi)^2 + c2(grad pi)^2 + 2 c3 dot(pi)Laplacian(pi)`.

Its background velocity operator has Fourier eigenvalue

`K(1+q^2/M^2) > 0`.

Therefore, as long as cubic perturbations remain inside the EFT neighborhood in which this operator stays invertible, the **reduced Route A1 scalar sector retains one canonical pair through cubic order** and does not generate an Ostrogradsky mode from higher time derivatives.

## Reproducible evidence for Route A1

- Workflow run: `32072791555`, success.
- Job: `95519466034`.
- Research checkout: `d19612c4586441f4d5ab23bb1993886cabbf3edd`.
- SymPy: `1.14.0`.
- Artifact: `rtk-quantum-route-a1-cubic`.
- Artifact ID: `9302328178`.
- Artifact ZIP SHA256: `cccd7034ec94ab05fb2f880163dd015bac9b5e2b242e8b12f39e1daae6be17a9`.
- Classification emitted by CI: `ROUTE_A1_REDUCED_SCALAR_CUBIC_EFT_AUDIT_PASS`.
- Basis size: 4.
- IBP identities verified: 2.
- No second time derivative in the basis: true.
- Canonical coefficient mass dimensions: `[-2,-2,-3,-3]`.

## Major frontier changes

🚀 **CLOSED for the Route A research program: nonlinear EFT symmetry class selection.**

The project no longer has an unspecified nonlinear EFT class. Route A1 is explicitly chosen and versioned. This does not assert that nature/fundamental RTK must use A1.

🚀 **CLOSED for Route A1 through `D <= 4`: cubic operator-basis gate.**

The cubic basis is finite, complete under the stated assumptions/truncation, and symbolic-CI verified.

✅ **Advanced but not globally closed:** reduced-scalar cubic DOF health.

One scalar canonical pair is retained perturbatively in the reduced A1 theory while the velocity Hessian remains invertible.

## Still open — full theory

🔴 Unique fundamental/covariant DBI-Khronon completion.

🔴 Coupling the nonlinear Khronon completion consistently to metric/lapse/shift and the RT nonlocal auxiliary sector.

🔴 Full nonlinear constraint algebra and total physical DOF count of the complete coupled theory.

🔴 Determination of the physical coefficients `c1...c4`.

🔴 Actual finite-q strong-coupling scale.

🔴 Loop/radiative stability and counterterm closure.

🔴 UV completion.

## Claim language

Allowed:

> The RTK research program now has an explicitly frozen preferred-frame Route A1 nonlinear scalar EFT class. Within that class, the complete cubic operator basis through four derivatives is known, and the reduced scalar sector retains one perturbative time degree of freedom through cubic order while the velocity Hessian remains invertible.

Not allowed:

> The full metric + RT + Khronon theory is proven ghost-free to all orders.

or

> The strong-coupling cutoff is `M_K`/`k_*`.

## Next theorem target

The highest-value next theorem is now the **coupled constraint problem**: embed Route A1 (or a stronger Route B action) into the metric + RT sector, identify nondynamical variables and constraints, and count the total physical propagating degrees of freedom.
