# RTK C9 HMT lambda=1 S3 reduced scalar FS-block checkpoint

Classification: `RTK_C9_HMT_LAMBDA1_S3_REDUCED_SCALAR_FS_BLOCK_NONDEGENERATE_PASS_SCOPED`

Frozen target commit: `a2b81b7808cf4928bef5ae9e000d6c2b18a94adc`.
Parent confirmed HEAD: `9ccb2322a0aa9320886b25309cd2468975297e75`.

On round S3 at lambda=1,

`C12=(R/3)(-R-2 nabla^2)`, `R=6/a^2`,

so for scalar harmonics

`mu_l a^4 = 4[l(l+2)-3] = 4(l-1)(l+3)` with `d_l=(l+1)^2`.

The only nonnegative-integer zero is ell=1, with degeneracy four. The parent gate already proved these four conformal zero modes are spatial-diffeomorphism gauge directions. After quotienting exactly that sector, the reduced scalar domain is ell=0 and ell>=2. Here `mu_0 a^4=-12` is negative but nonzero, while `mu_l>0` for every ell>=2. Therefore the reduced scalar C12 block has no zero eigenvalues.

For the antisymmetric 2x2 second-class mode matrix `[[0,mu_l],[-mu_l,0]]`, `det=mu_l^2>0` on every reduced mode. This proves scoped nondegeneracy only.

Strict scope: no zeta/heat-kernel regularization was frozen, so no finite scalar functional determinant is claimed. The complete HMT gauge-fixed constraint matrix, complete zero-mode quotient, full FS determinant, HMT one-loop evaluability and full C9 remain OPEN/BLOCKED. Parent beta functions were not imported; unresolved HMT matter coefficients were not chosen; thresholds unchanged; soft-s retest forbidden; k=0.03 production blocked; no DSIR content used.

Next gate: preregister a dimensionless spectral regularization/normalization prescription for this reduced scalar block and test whether its finite reduced determinant is well defined, while explicitly keeping the complete HMT determinant and C9 open.
