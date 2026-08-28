# RTK C9 HMT flat second-class kernel rank audit — checkpoint v1

- Classification: `RTK_C9_HMT_FLAT_SECOND_CLASS_KERNEL_RANK_CLASSIFIED_PASS_SCOPED`
- Frozen target commit: `e62ff6add973288f38ac8425d9aa0800be5db559`
- Background: flat periodic T^3, D=3, N=N(t), A=0, nu=0 gauge, zero curvature and zero background momenta.
- Exact local kernel at linearized order:
  `C12(x,y) = -2(1-lambda)/(kappa^2(3lambda-1)) * partial^4 delta(x-y)` (with the frozen canonical convention).
- Generic branch: for `lambda != 1, 1/3` and nonzero Fourier mode `k`, this local second-class block is nondegenerate at the frozen order.
- Critical branch `lambda=1`: the flat-linearized kernel vanishes. This is a rank/evaluability bifurcation of this scoped kernel, **not** a no-go for HMT.
- Critical branch `lambda=1/3`: the generic formula is not valid; separate constrained analysis is required.
- `k=0`: global/zero-mode sector remains open.
- Full Faddeev-Senjanovic determinant: **OPEN**.
- Full HMT one-loop evaluability: **OPEN/BLOCKED**.
- Full C9 radiative naturalness: **OPEN**.
- soft-s retest: **FORBIDDEN**.
- production `k=0.03 Mpc^-1`: **BLOCKED**.

## Next justified gate
If the retained RTK/HMT candidate includes `lambda=1`, freeze and execute a dedicated `lambda=1` constraint-bifurcation audit from the full source-locked constraint algebra (or a preregistered nonflat/background-momentum expansion). Do not regularize the rank change by choosing another lambda post hoc.
