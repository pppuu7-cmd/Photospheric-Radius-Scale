# RTK Route-B mixed-derivative literature audit v1

## Question

Can the RTK quadratic clock kinetic fingerprint

`q^2 omega^2 |pi|^2`

be identified with the mixed-derivative Hořava operators already studied in the literature, without introducing a new propagating scalar or changing the target into a higher-spatial-potential theory?

## Primary sources

1. Colombo, Gumrukcuoglu, Sotiriou, *Hořava gravity with mixed derivative terms*, Phys. Rev. D 91, 044021 (2015), arXiv:1410.6360.
2. Coates, Colombo, Gumrukcuoglu, Sotiriou, *The uninvited guest in mixed derivative Hořava Gravity*, Phys. Rev. D 94, 084014 (2016), arXiv:1604.04215.
3. Klusoň, *Hamiltonian Analysis of Mixed Derivative Hořava-Lifshitz Gravity*, arXiv:1607.08361.

## What the literature establishes

The 2014/2015 construction studied terms schematically of the `D K D K` type and showed that they modify graviton kinetic propagators. In the later complete symmetry/power-counting audit, Coates et al. stress that the full two-spatial/two-temporal derivative basis contains additional terms involving

`A_i = (1/(2N)) (dot a_i - N^j D_j a_i - a_j D_i N^j)`

and mixed contractions with `D_i K` / `D_j K^{ij}`. Their perturbative analysis around Minkowski finds two tensor plus two scalar propagating degrees of freedom; the new scalar is unstable at low energy. The paper explicitly attributes the new scalar to the `A_i`-containing terms, distinguishing them from the older `D K D K` kinetic deformations. Klusoň's Hamiltonian analysis independently confirms an additional scalar degree of freedom for that mixed-derivative theory.

## RTK operator discriminator

The relevant RTK question is more specific than "are mixed derivatives allowed?". For a clock Stückelberg field `phi=t+pi` around fixed Minkowski, linearized foliation geometry gives the derivative fingerprints

- `a_i ~ partial_i pi_dot`, hence `a_i a^i -> q^2 omega^2 |pi|^2`;
- `K_ij ~ partial_i partial_j pi`, hence `D_l K_ij D^l K^ij -> q^6 |pi|^2`;
- `A_i ~ -(1/2) partial_i pi_ddot`, hence `A_i A^i -> (1/4) q^2 omega^4 |pi|^2`.

Therefore the old `D K D K` sector is not the direct fixed-metric clock operator that generates the RTK denominator, while the complete `A_i` sector overshoots the desired time-derivative order and is known to activate another scalar in the generic theory. The direct derivative match remains the acceleration-squared `a_i a^i` structure.

This explains the earlier Route-B result: the constant-`c_i` acceleration route failed because of full metric/DHOST degeneracy constraints, not because `a_i a^i` had the wrong quadratic derivative structure.

## Surviving theory space

The literature audit therefore does **not** provide a ready-made Hořava completion of RTK. It instead narrows the next search to constructions that preserve the `a_i a^i` / `q^2 omega^2` clock fingerprint while restoring a healthy constrained metric sector, for example:

- X-dependent degenerate DHOST companion operators;
- spatially-covariant combinations engineered to remain degenerate;
- constrained auxiliary-field formulations whose elimination reproduces the RTK quadratic operator without activating an extra scalar.

Any candidate must be checked explicitly for Hamiltonian constraint rank / propagating DOF, tensor kinetic signs, scalar hyperbolicity, nonlinear interactions and strong-coupling scale. Merely containing "mixed derivative" operators is not sufficient.

## Status

`ROUTE_B_MIXED_DERIVATIVE_LITERATURE_AUDIT_COMPLETE`.

This is a literature/operator-classification result, not a nonlinear RTK completion and not a strong-coupling proof.
