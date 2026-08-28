# RTK C9 HMT λ=1 round-S3 TT background admissibility / source-lock target

Status: FROZEN BEFORE EXECUTION
Branch: `rtk-class-build`
Parent scientific frontier: `1d4f3354ef43d38646da06fc2f98dd9656483e82`
Scope: RTK only. Do not mix with DSIR.

## Motivation

The spatial FP quotient is now assembled in its frozen convention. Before constructing a physical TT one-loop Hessian on the same round-S3 witness, verify that the witness is an admissible background of the source-locked HMT action and identify exactly which background data/couplings are required by the TT quadratic problem.

## Source lock

Primary HMT formulation: P. Hořava and C. M. Melby-Thompson, *General Covariance in Quantum Gravity at a Lifshitz Point*, Phys. Rev. D 82, 064027 (2010), arXiv:1007.2410, DOI 10.1103/PhysRevD.82.064027.

Source convention to be tested:

`S = (2/kappa^2) ∫ dt d^3x sqrt(g) { N[K_ij K^ij - K^2 - V + nu Theta^ij(2K_ij + nabla_i nabla_j nu)] - A(R - 2 Omega) }`

with `Theta^ij = R^ij - (1/2)g^ij R + Omega g^ij`, λ=1.

The source-lock is about the HMT action structure and A-constraint only. It does NOT freeze a numerical higher-spatial-derivative potential or its couplings.

## Frozen witness/background assumptions

- spatial dimension D=3;
- round `S^3` with radius `a>0`;
- `R_ij = 2 a^-2 g_ij`, `R = 6 a^-2`;
- λ=1;
- static witness: `K_ij=0`;
- Newton prepotential gauge `nu=0` for this scoped check;
- projectable lapse and shift conventions inherited from the preceding C9 HMT chain;
- TT metric perturbation satisfies `nabla^i h_ij=0`, `g^ij h_ij=0`.

## Exact assertions to test

1. Variation with respect to the HMT gauge field A imposes `R = 2 Omega`.
2. On round `S^3`, background admissibility therefore requires exactly `Omega = 3/a^2`.
3. For a TT perturbation on an Einstein background, the first scalar-curvature variation vanishes: `delta R = 0`.
4. The first volume variation also vanishes: `delta sqrt(g)=0`.
5. Therefore the A-constraint has no *linear* TT obstruction once the background A-equation is satisfied.
6. This is necessary but not sufficient for a physical TT Hessian: metric stationarity and the TT quadratic operator can depend on the background value `A0` and on the chosen potential `V[g]` / its couplings.
7. No numerical TT spectrum, TT determinant, one-loop evaluability, or C9 closure may be claimed unless those additional data are source-locked and the background metric equation is checked.

## Frozen pass/fail semantics

PASS_SCOPED only if assertions 1-6 are derived exactly and assertion 7 is enforced in persisted semantics.

FAIL if the round-S3 witness violates the A-equation under the frozen assumptions, if the TT first-variation statements fail, or if the implementation silently assigns unspecified HMT potential couplings/background A0.

A conditional relation `Omega=3/a^2` is a valid scoped result; it is not permission to retrofit a physical coupling without explicit provenance.

## Frozen non-claims

- `full_TT_hessian_derived = false`
- `tt_spectrum_computed = false`
- `tt_determinant_computed = false`
- `background_metric_stationarity_fully_checked = false`
- `full_FP_determinant_computed = false`
- `full_FS_determinant_computed = false`
- `complete_HMT_gauge_fixed_constraint_matrix_constructed = false`
- `full_HMT_one_loop_evaluable = false`
- `full_C9_closed = false`
- `soft_s_retest_allowed = false`
- `production_k003_unblocked = false`
- `threshold_changed = false`

## Required persisted artifacts

Save analyzer/script, result, checkpoint, provenance, and an Actions workflow/run. The result must distinguish a source/background admissibility prerequisite from a TT Hessian calculation.
