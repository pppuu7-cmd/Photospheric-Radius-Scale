# RTK C9 HMT lambda=1 constraint-bifurcation audit — checkpoint v1

- Classification: `RTK_C9_HMT_LAMBDA1_FLAT_CONSTRAINT_LINEARIZATION_DEGENERATE_PASS_SCOPED`
- Frozen target commit: `a1d97b870d01de6da3ce4c62588791aa05bc90f3`
- Exact lambda=1 HMT-limit constraint: `Phi2II = -2 R_ij pi^ij + 2/(D-1) R pi`; in D=3: `-2 R_ij pi^ij + R pi`.
- The `nabla^2 pi` coefficient vanishes exactly at lambda=1.
- Around the frozen flat zero-curvature, zero-momentum background, `Phi2II` starts at `O(delta g * delta pi)`, so its linear perturbation vanishes.
- Therefore the prior vanishing flat-linearized `C12` is a scoped linearization/rank degeneracy, not proof of a new exact first-class symmetry.
- The source-locked full Hamiltonian analysis classifies the pair as second-class and states that preservation fixes multipliers without generating an additional constraint in the full phase-space analysis.
- Full Faddeev-Senjanovic determinant: **OPEN**.
- Full HMT one-loop evaluability: **OPEN/BLOCKED**.
- Full C9 radiative naturalness: **OPEN**.
- soft-s retest: **FORBIDDEN**.
- production `k=0.03 Mpc^-1`: **BLOCKED**.

## Next justified gate
Freeze a minimally nonflat or nonzero-background-momentum lambda=1 witness background satisfying the relevant constraints, then compute the leading nonzero second-class bracket operator/rank there. Do not infer exact first-class closure from the singular flat linearization.
