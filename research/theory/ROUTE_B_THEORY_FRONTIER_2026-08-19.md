# Route-B theory frontier — 2026-08-19

This checkpoint collects the currently machine-checked results relevant to constructing a local preferred-foliation completion of the RTK mixed-kinetic scalar dispersion. It is a frontier map, not a claim that the full theory is closed.

## 1. Operator discriminator

Run `32292598243`, artifact `9380038732`, digest `sha256:9d9e152f4bd54663fb7515874ddcde3a6235fdcfa51efcf750d2f8a58e223406`.

On fixed Minkowski with `phi=t+pi`, acceleration gives `a_i~partial_i pi_dot`, hence `a_i a^i -> q^2 omega^2 |pi|^2`. The tested spatial derivative of extrinsic curvature gives a higher `q^6` fingerprint, while the tested time-like derivative of acceleration gives `q^2 omega^4`.

**Narrow conclusion:** among the minimal tested operators, acceleration-squared has the derivative fingerprint required by the target mixed kinetic factor.

## 2. Narrow constant-coefficient no-go

Run `32292466634`, artifact `9379994876`, digest `sha256:56388efd4636b3a6faff889eb6d287fc5187df12b2525562a6274303e4786b0c`.

The exact no-`q^4` target condition gives `c2+c3=0`. On the constant-`c_i`, `c4=2` branch the audited metric kinetic discriminator becomes `D1=-16(c2-1)^2/X^2`; the only simultaneous point is `c2=1,c3=-1`, where the relevant metric kinetic discriminants vanish.

**Narrow conclusion:** this constant-coefficient khronometric subspace does not provide a nondegenerate exact RTK quadratic mapping. The result is not a no-go for the broader healthy nonprojectable/spatially-covariant class.

## 3. Simple algebraic auxiliary vector is only a rewrite

Run `32300929835`, artifact `9382978932`, digest `sha256:6a00989cda157ef84fe4cc6146c8536e3d3920ce59dc36b24b5ebd6c9a090fae`.
Durable result: `research/theory/ROUTE_B_AUXILIARY_ACCELERATION_EQUIVALENCE_RESULT_v1.json`.

For `L_aux=-M^2 B_i B^i/2+B_i a^i`, exact elimination gives `B_i=a_i/M^2` and `+a_i a^i/(2M^2)`.

**Narrow conclusion:** an unconstrained derivative-free `B_i` reproduces the operator but is only a Hubbard-Stratonovich rewrite; it does not by itself evade any degeneracy/constraint obstruction of the eliminated action.

## 4. Retarded RT localization variables do not add free homogeneous IC modes

Run `32301071093`, artifact `9383027131`, digest `sha256:a69d512c73742b8a9ab8e562e5f8ac55f31ebfbbe32bd3d9d0e7eb4e7d20fbfe`.
Durable result: `research/theory/RT_RETARDED_AUX_SOLUTION_SPACE_RESULT_v1.json`.

For a well-posed second-order auxiliary equation with nonzero fundamental-solution Wronskian, fixed retarded value and normal-derivative data remove both formal homogeneous constants. A triangular retarded chain inherits uniqueness inductively. Existing model=2 implementation audits fix `U,U',V,V'` and perturbation `deltaU,deltaU',deltaV,deltaV',deltaZ,deltaZ'` initial data.

**Narrow conclusion:** localized RT auxiliaries are not freely tunable dark-fluid initial modes inside the physical retarded solution space. This is still weaker than the full coupled nonlinear ADM/Hamiltonian DOF theorem.

## 5. Reduced mixed-kinetic scalar kinematics

Run `32302480967`, artifact `9383521326`, digest `sha256:b6c70616b972b5aec9b612dda9b65032ab7746a579a782f558cf03c5e74461d1`.
Durable result: `research/theory/ROUTE_B_MIXED_KINETIC_DISPERSION_KINEMATICS_RESULT_v1.json`.

For `(1+q^2/M^2)omega^2-c_s^2q^2=0`, exact machine-checked expressions are

- `omega=c_s q/sqrt(1+q^2/M^2)`;
- `v_phase=c_s/sqrt(1+q^2/M^2)`;
- `v_group=c_s/(1+q^2/M^2)^(3/2)`.

For positive `M^2,c_s^2`, the reduced branch is real and monotonic; at high momentum `omega->c_s M` and both phase/group velocities vanish.

**Narrow conclusion:** the reduced target pole is kinematically healthy under the stated sign conditions, but this is not the full characteristic/hyperbolicity theorem.

## 6. Quadratic data alone cannot determine strong coupling

Run `32304019916`, artifact `9384050448`, digest `sha256:030eb66fafa76dd179d227f1e1424f8ce8b74a589278a8616efc9978cef35833`.
Durable result: `research/theory/C8_QUADRATIC_STRONG_COUPLING_NONIDENTIFIABILITY_RESULT_v1.json`.

An infinite family with the same quadratic mixed-kinetic Hessian/dispersion but an independent cubic coefficient `g/Lambda^2` has identical `L2` and different cubic vertex `2g/Lambda^2`.

**C8 conclusion:** the quadratic scale `M`, `M_K` or `k_*` cannot be identified with a unique strong-coupling cutoff without an explicit nonlinear completion and canonicalized interaction vertices.

## 7. Constructive healthy nonprojectable Hořava pole embedding

Mature exact run `32305251435`, artifact `9384462213`, digest `sha256:2b54901ff525f7bd1bbace5e28e59c4bb97038548cb48dbe5b45413816659664`.
Durable result: `research/theory/ROUTE_B_BPS_EXACT_RATIONAL_EMBEDDING_RESULT_v1.json`.
Primary source equations: Blas-Pujolas-Sibiryakov healthy nonprojectable scalar `P/Q` sector, with independent higher-spatial scale `M_*`.

A continuous two-branch family is machine-checked:

- `alpha=2z/(1+z)`, `lambda=1+ell`, with positive `z,ell`;
- `g1=g2=g3=0`, `f3=-s<0`, `f1=f2^2/f3`;
- `f2/f3=(-2 +/- 2/sqrt(1+z))/alpha`.

It gives exactly

- `P=4-2alpha>0`;
- `Q(-p^2/M_*^2)=alpha+s p^2/M_*^2>0`;
- `omega^2=c_s^2 p^2/(1+p^2/M_disp^2)`;
- `c_s^2=ell/[z(2+3ell)]>0`;
- `M_disp^2=alpha M_*^2/s>0`.

**Constructive C7 conclusion:** the broader healthy nonprojectable Hořava scalar sector contains a continuous Minkowski-stable family with the exact RTK rational pole/dispersion. This explicitly shows that the earlier constant-`c_i` no-go is not a general completion no-go.

## 8. Same pole does not mean same off-shell propagator/observable response

Run `32304837982`, artifact `9384321313`, digest `sha256:418e71231c7a37a298928223fe3a3ad35b62137bd5b237b6fe42eef4603dacbb`.
Durable result: `research/theory/ROUTE_B_POLE_RESIDUE_DISTINCTION_RESULT_v1.json`.

For representative reduced kernels

`K_BPS=A omega^2-G q^2/(1+r q^2)`

and

`K_RTK=A(1+r q^2)omega^2-G q^2`,

machine algebra gives `K_RTK=(1+r q^2)K_BPS`: poles coincide, but fixed-source propagator residues differ by the momentum-dependent factor.

**Interpretation guard:** the BPS family is an exact pole/dispersion embedding, not yet an exact off-shell RTK action, source-coupling or gauge-invariant observable mapping. A field/source/transfer-function map is required before stronger equivalence language.

## 9. Exact all-scale rational tuning is not the standard z=3 UV completion

The exact rational family cancels the higher powers of `P(x)`, so its high-momentum scalar pole saturates rather than entering the generic healthy-Hořava `omega^2~p^6` regime.

**UV conclusion:** the exact rational BPS family should be interpreted as an intermediate/finite-range EFT pole embedding unless a second higher crossover restores `z=3` behavior before the low-energy strong-coupling cutoff.

## 10. Constructive two-crossover z=3 family

Run `32305611111`, artifact `9384581354`, digest `sha256:b66944c808a577c190b929f57b59f910d80b08a64402cfc5ed7e6a05cd4e79d7`.
Durable result: `research/theory/ROUTE_B_BPS_Z3_TWO_CROSSOVER_RESULT_v1.json`.
Post-artifact strong-coupling guard fix: worker commit `2c98b7ec95e599ee28c162d5587acba0a2bbbb79`.

A continuous nearby family gives exactly

`P(x)=(4-2alpha)[1-gamma x^3]`, `Q(x)=alpha(1-x)`,

with `gamma=4eta(1-eta)` and physical dispersion

`omega^2=c_s^2 p^2 [1+gamma(p^2/M_*^2)^3]/[1+p^2/M_*^2]`.

Hence

- the first RTK-like rational crossover is `M_disp=M_*`;
- the fractional numerator correction is `delta(p)=gamma(p/M_*)^6`;
- the actual `z=3` crossover is `p_UV=M_* gamma^(-1/6)`;
- for `p>>p_UV`, `omega^2~p^6`;
- physical `P,Q` remain positive and `lambda>1` keeps the BPS scalar kinetic sign positive.

**Constructive UV conclusion:** the healthy BPS class can approximate the exact RTK rational law arbitrarily accurately on any fixed finite momentum interval while restoring the `z=3` UV scaling at a parametrically higher, separately tunable scale.

## 11. C8 accuracy-versus-strong-coupling design window

Accuracy-window run `32306100498`, artifact `9384750676`, digest `sha256:5ff49cd1834e6f9e1eeee99edeeb378fd0171a258b1547d6f4172c07635d82c1`.
Cutoff-map run `32306271279`, artifact `9384806626`, digest `sha256:df0775eca5c896de235343ba755c7c68abcea4351437586edfc0d657ced0e73d`.
Combined durable result: `research/theory/C8_BPS_STRONG_COUPLING_DESIGN_RESULT_v1.json`.

The two-crossover family obeys the exact identity

`delta(p)=(p/p_UV)^6`.

Therefore an RTK-accuracy requirement `delta(p_max)<=epsilon` and a pre-strong-coupling UV crossover can coexist whenever a `p_UV` can be chosen inside

`max(M_*, p_max/epsilon^(1/6)) < p_UV < Lambda_p`.

At the crossover `omega_UV^2<2 c_s^2 M_*^2`, so `sqrt(2)c_s M_*<Lambda_omega` is a simple sufficient frequency guard.

Using the published BPS low-energy cubic cutoffs with `ell=lambda-1`, `M_alpha=M_P sqrt(alpha)` and `M_lambda=M_P sqrt(ell)`, the exact parameter map is:

If `ell<=alpha`:

- `Lambda_p=M_P ell^(3/4) alpha^(-1/4)`;
- `Lambda_omega=M_P ell^(5/4) alpha^(-3/4)`.

If `ell>=alpha`:

- `Lambda_p=M_P alpha^(3/4) ell^(-1/4)`;
- `Lambda_omega=M_P (alpha ell)^(1/4)`.

At `ell=alpha`, both equal `M_P sqrt(alpha)`.

**C8 design conclusion:** for this concrete completion route, strong-coupling avoidance has become a quantitative falsifiable window rather than an unspecified unknown. C8 is still not numerically closed until the RTK phenomenological `M_*,c_s,p_max,epsilon` are mapped and the tuned family's complete cubic/higher-spatial interactions are checked for any lower cutoff.

## 12. Current viable route and remaining proof layers

The most concrete surviving completion route is now the healthy nonprojectable Hořava/BPS class with a two-crossover scalar sector. Other X-dependent, DHOST-like or constrained spatially-covariant routes remain possible but are no longer the only constructive options.

C7 remains open on:

- off-shell field/source/observable mapping from the BPS scalar to the intended RTK Khronon sector;
- full nonlinear constraint/physical-DOF analysis for the tuned family, including whether the special coefficient surface changes generic constraint rank;
- FLRW and sufficiently generic-background scalar/tensor stability and hyperbolicity;
- coupling to matter and phenomenological Lorentz-violation constraints.

C8 remains open on:

- mapping the RTK phenomenological crossover to the BPS `M_*` and target `c_s`;
- specializing the full cubic/higher-spatial interaction vertices to the tuned family and canonicalizing them;
- demonstrating the explicit `p_UV<Lambda_p` and frequency window at the phenomenological target point.

C9 remains open on radiative stability, counterterm closure/naturalness and the hierarchy between the rational and `z=3` crossover operators.

No result in this checkpoint is a global observational inference, model-selection statistic, completed nonlinear RTK equivalence, numerical strong-coupling closure, radiative-stability proof or UV-completion proof.
