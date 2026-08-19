# Route-B theory frontier — 2026-08-19

This checkpoint collects the currently machine-checked narrow results relevant to constructing a local preferred-foliation completion of the RTK mixed-kinetic scalar dispersion. It is a frontier map, not a claim that the full theory is closed.

## 1. Operator discriminator

GitHub Actions run `32292598243`, artifact `9380038732`, digest `sha256:9d9e152f4bd54663fb7515874ddcde3a6235fdcfa51efcf750d2f8a58e223406`.

On the fixed-Minkowski clock perturbation `phi=t+pi`, the leading derivative fingerprints are:

- acceleration `a_i ~ partial_i pi_dot`, hence `a_i a^i -> q^2 omega^2 |pi|^2`;
- spatial derivative of extrinsic curvature gives a higher spatial fingerprint `q^6`;
- time-like derivative of acceleration gives `q^2 omega^4`.

**Narrow conclusion:** among these minimal candidates, acceleration-squared has the derivative fingerprint required by the target mixed kinetic factor.

## 2. Constant-coefficient khronometric c4=2 exact-target branch

GitHub Actions run `32292466634`, artifact `9379994876`, digest `sha256:56388efd4636b3a6faff889eb6d287fc5187df12b2525562a6274303e4786b0c`.

The exact no-`q^4` target condition gives `c2+c3=0`. On the special `c4=2` degeneracy branch, the audited metric kinetic discriminator reduces to

`D1 = -16 (c2-1)^2 / X^2`,

so the only simultaneous point is `c2=1, c3=-1`, where the relevant metric kinetic discriminants vanish.

**Narrow conclusion:** the tested constant-`c_i`, `c4=2` khronometric branch does not provide a nondegenerate exact RTK quadratic mapping. This does not exclude X-dependent, spatially covariant, DHOST-like, or nontrivially constrained auxiliary completions.

## 3. Simple algebraic auxiliary-vector completion

Worker: `rtk/route_b_auxiliary_acceleration_equivalence.py`.
GitHub Actions run `32300929835`, artifact `9382978932`, digest `sha256:6a00989cda157ef84fe4cc6146c8536e3d3920ce59dc36b24b5ebd6c9a090fae`.
Durable result: `research/theory/ROUTE_B_AUXILIARY_ACCELERATION_EQUIVALENCE_RESULT_v1.json`.

For

`L_aux = -M^2 B_i B^i/2 + B_i a^i`,

the algebraic equation is `B_i=a_i/M^2`, and exact elimination gives `+a_i a^i/(2M^2)`. In the clock decoupling fingerprint this yields the desired reduced dispersion

`omega^2 = c_s^2 q^2/(1+q^2/M^2)`.

**Narrow conclusion:** a derivative-free unconstrained algebraic `B_i` reproduces the desired operator but is only an exact Hubbard-Stratonovich rewrite of acceleration-squared. By itself it does not evade any degeneracy/constraint obstruction of the eliminated action.

## 4. Retarded RT localization variables

Worker: `rtk/route_b_retarded_aux_solution_space.py`.
GitHub Actions run `32301071093`, artifact `9383027131`, digest `sha256:a69d512c73742b8a9ab8e562e5f8ac55f31ebfbbe32bd3d9d0e7eb4e7d20fbfe`.
Durable result: `research/theory/RT_RETARDED_AUX_SOLUTION_SPACE_RESULT_v1.json`.
Implementation anchor: `rtk/audit_rt_retarded_auxiliary_ic.py`.

For a well-posed second-order auxiliary equation with nonzero fundamental-solution Wronskian at the initial hypersurface, fixing both the auxiliary value and normal derivative by the retarded prescription removes both formal homogeneous integration constants. A triangular retarded auxiliary chain inherits uniqueness inductively.

The existing implementation audit fixes background `U,U',V,V'` and perturbation `deltaU,deltaU',deltaV,deltaV',deltaZ,deltaZ'` initial data for RT/model=2.

**Narrow conclusion:** localized RT auxiliaries do not represent freely specifiable homogeneous dark-fluid initial modes inside the physical retarded solution space. This is not the full nonlinear Hamiltonian/ADM DOF theorem of metric+Khronon+RT.

## 5. Still viable completion classes

The current narrow results leave the following routes genuinely open:

- X-dependent coefficient functions whose degeneracy conditions differ from the constant-`c_i` branch;
- nontrivial auxiliary sectors with additional primary/secondary constraints, not merely algebraic rewriting;
- metric/extrinsic-curvature companion operators chosen as a degenerate spatially-covariant/DHOST-like combination;
- a spatially covariant preferred-foliation construction whose full constraint algebra yields the desired scalar branch without extra propagating ghosts.

## 6. Required next proof layers

C7 remains open until there is an explicit coupled metric+Khronon+RT constraint/DOF analysis on FLRW and a sufficiently generic background. A valid completion must then support machine-checkable no-ghost/no-gradient/hyperbolicity inequalities. C8 requires cubic interactions and canonical normalization to determine a strong-coupling/EFT cutoff; the quadratic dispersion alone cannot supply that number. C9 requires radiative/loop stability or an explicit symmetry/power-counting argument.

No result in this checkpoint is a global observational inference, model-selection statistic, UV completion, or proof of nonlinear causality.
