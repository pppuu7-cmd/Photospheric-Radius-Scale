# RTK model-development addendum — 2026-08-22 20:48 UTC

This addendum updates `research/checkpoints/RTK_MODEL_DEVELOPMENT_2026-08-22T2036Z.md`.

## Elliptic matter-compensator prefilter corrected result

Corrected run `32596939267` completed **SUCCESS**. Artifact `9481806357`, digest `sha256:5057f93978e516a3ac597316056f612873366f91ecba52c75e49a3b80b5cf082`.

Scoped classification: `YELLOW_CONSTRUCTIVE_SCALE_SEPARATED_A_SOURCE_RESCUE_FULL_DIRAC_AND_OBSERVABLES_PENDING`.

The isolated auxiliary filter satisfies `Q/H0=1/(1+k_phys^2/M_c^2)`, has positive elliptic operator for `M_c>0`, and the isolated four-constraint auxiliary block has determinant `ell^4`. The 1%/1% scale-separation window is nonempty when `k_local/k_cos >= 99`. This remains a prefilter rather than a full coupled-DOF theorem.

## Canonical-affinity result

After replacing only SymPy structural equalities with algebraic simplification checks, run `32597148540` completed **SUCCESS**. Artifact `9481859928`, digest `sha256:f77902d2fb2027beb3008b5078a46d48eebdbd5ae249e555eeb5b5ec935f5796`.

The exact canonical form is

`H_aux = (A-Acal) Q + Lambda[(1-D^2/M_c^2)Q-H0]`,

combined with the already-certified family-I `a1=1,a2=0` matter Hamiltonian.

Certified in scope:

- `J_A^m=-H0`, `J_A^aux=+Q`;
- `p_nu^m=+H0`, `p_nu^aux=-Q`;
- `p_nu_total+J_A_total=0` exactly;
- `dJ_A_total/dN=0` exactly;
- Hamiltonian affinity in `A` and `dot(nu)` is preserved;
- auxiliary constraints solve `Q=H0/ell` and `Lambda=-(A-Acal)/ell`;
- isolated auxiliary four-constraint determinant is `ell^4`;
- source transfer is `J_A^matter+aux = H0(1/ell-1)`, giving exact cancellation at `k=0` and recovery of the original local family-I source as `k->infinity`.

## Frozen candidate

The canonical functional form is now frozen on `rtk-class-build` as

`research/RTK_U1_ELLIPTIC_MATTER_COMPENSATOR_CANONICAL_v1.json`

with status `FROZEN_BEFORE_FULL_COUPLED_DIRAC`. The scale `M_c>0` remains symbolic and intentionally unfitted.

## Full Dirac reduction

The enlarged constraint basis is

- old U1: `(pi_N, J_A_total, H_perp_total, phi_A_total)`;
- auxiliary: `(p_Q,p_Lambda,C_Q,C_Lambda)`.

For the full antisymmetric matrix `M=[[O,X],[-X^T,E]]`, the already-proved invertibility of the auxiliary block gives the exact reduction

`det M = det E * det(O + X E^{-1} X^T)`.

Therefore the full rank-8 question reduces to a 4x4 Schur-deformed U1 block. A dedicated CI gate has been launched. It explicitly keeps all cross brackets `X` rather than assuming block factorization.

## Numerical B9

B9 LCDM recenter-v6 half-scale run `32596694426` remains in the exact Hessian computation step. No decision is taken before its frozen half-scale summary is complete.
