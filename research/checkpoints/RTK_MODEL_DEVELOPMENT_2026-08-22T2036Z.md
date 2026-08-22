# RTK model-development checkpoint — 2026-08-22 20:36 UTC

Status: **active research checkpoint; individual frozen targets, CI artifacts and later results remain authoritative**.

## B9 Planck R3 lensing robustness

- RTK branch remains independently fresh-tree locally certified under the frozen B9-v1 objective.
- LCDM recenter-v5 run `32587768594` was positive definite but had exact improvement `0.04857762431061019 > 0.005`, forcing recenter-v6.
- LCDM recenter-v6 base run `32592618365` completed **SUCCESS**. Artifact `9481581498`, digest `sha256:890a1eb848ce3c9a819f176c5c5190c7470f753c2c7e74e1281540b8a4326730`.
- Exact v6 base result: `S_center=S_best=1058.2447104245823`, `best_improvement=0.0`, center replay error `0.0`, positive-definite eff Hessian with eigenvalues `[0.016466325422027518, 0.07770290821703023, 0.08800640116954664, 0.26844100581525293, 3.0931520001557304, 7.197826455326002]`.
- Preregistered independent half-scale target is frozen at `rtk-class-build:research/robustness/B9_LCDM_RECENTER_TARGET_v6_half.json`.
- Half-scale workflow launched by commit `63b8b424b0cbdc2cc74aa7cd198029c49371c304`; Actions run `32596694426` is the current B9 numerical gate.
- Decision rule: half-scale recenter-clear + positive definite -> freeze LCDM B9 local stationarity and proceed to final paired fresh-tree B9 replay; otherwise use the frozen recenter/ray tree.

## U(1) compensator architecture: what survived and what failed

### 1. Naive clock-kinetic compensator

Candidate `Delta L=-sigma F(X_U)` reconstructs the homogeneous source, but its `dot(phi)-dot(Sigma)` cross velocity structure invalidates inheritance of the old exceptional primary-degeneracy theorem. Subsequent primary-constraint-loss CI closed this candidate as unsuitable for direct promotion.

### 2. Coordinate compensator

Candidate `Delta L=-sigma F_Sigma(Sigma)` exploits monotonic `Sigma(a)` on the oriented rolling branch. It preserves the primary velocity degeneracy and passed the scoped quadratic kinetic-rank gate.

High-k principal-rank run `32596250590`: **SUCCESS**, artifact `9481623031`, digest `sha256:a011bab3ab65f63bd34e1fc3fa453b56bf211ef25421a81cd2a5ef9548e70a8d`.

Classification: `GREEN_SCOPED_HIGHK_PRINCIPAL_RANK_PRESERVED_FINITE_K_PENDING`. This does not exclude isolated finite-k determinant zeros.

However, the coordinate-only candidate has a stronger cosmological limitation. Linear source variation is

`delta J_A^tot = 2 delta rho_H - 2 F'_Sigma delta Sigma`

already in the density subsector. The independent tangent direction `delta Sigma=0`, `delta rho_H!=0` leaves a nonzero A source. Therefore a fixed function of the RTK clock coordinate alone cannot identically cancel arbitrary independent matter perturbations.

Perturbation-obstruction run `32596799364`: **SUCCESS**, artifact `9481769069`, digest `sha256:8ec05c14140ff66cae4ed9e6e3dcd0762531e5f79a856561e227c7dd4ae62f62`.

Classification: `BLACK_SCOPED_COORDINATE_ONLY_FULL_PERTURBATIVE_A_SOURCE_CANCELLATION`. The exact homogeneous FLRW rescue remains valid; the BLACK result is only for full perturbative cancellation by a coordinate-only function.

## New scale-separated auxiliary route

A new prefilter has been introduced at `rtk-class-build:rtk/route_b_u1_elliptic_matter_compensator_prefilter_gate.py`:

- neutral auxiliary fields `Q,Lambda` with no time kinetic terms;
- elliptic constraint `(1-D^2/M_c^2) Q = rho_H` in the canonical matter representation;
- A-source compensator proportional to `sigma Q` with the sign opposite to ordinary family-I matter.

In Fourier space the intended filter is

`Q/rho_H = 1/(1+k_phys^2/M_c^2)`.

Therefore `Q=rho_H` exactly at `k=0` but the compensator decouples as `k^-2` at high k. The isolated auxiliary constraint block has formal determinant `[1+k_phys^2/M_c^2]^4`, so it is a candidate for adding zero propagating auxiliary DOF.

For the preregistered 1% separation target, simultaneous `>=99%` cosmological compensation at `k_cos` and `<=1%` local compensation at `k_local` has a nonempty `M_c` interval if `k_local/k_cos >= 99`.

First run `32596875938` failed only because a generic-epsilon SymPy square-root simplification was asserted without the assumption `epsilon<1`; this is an implementation failure, not a scientific falsification. The gate was corrected to use exact rational `epsilon=1/100` without changing the candidate architecture and rerun.

## Immediate gates

1. Complete B9 LCDM v6 half-scale stationarity.
2. Re-run/certify the corrected elliptic auxiliary prefilter.
3. If the elliptic prefilter passes, freeze its precise canonical action before testing the full coupled Dirac matrix. The isolated auxiliary rank is not enough.
4. Derive the finite-k A-constraint transfer function and identify a physical `M_c` window that covers production cosmological modes while decoupling from local PPN sources.
5. Recompute PPN/equivalence-principle, radiative protection, cutoff and compact-object gates on the same frozen action. No result from an older action may be silently inherited where the source/constraint structure changed.
