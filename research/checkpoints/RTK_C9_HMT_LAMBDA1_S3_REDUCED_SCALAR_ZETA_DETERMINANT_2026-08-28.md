# RTK C9 HMT lambda=1 S3 reduced scalar zeta determinant checkpoint

Classification: `RTK_C9_HMT_LAMBDA1_S3_REDUCED_SCALAR_ZETA_DETERMINANT_FINITE_NORMALIZATION_DEPENDENT_PASS_SCOPED`

Frozen target commit: `06ed86480e19a6b16d91307534bf1fe2d5b9d20c`. Parent confirmed HEAD: `ae2011561fee83c16c52d1f8d662f3d6e96e08d1`.

For the previously reduced scalar/conformal FS block define the positive dimensionless operator `A_hat=a^4|C12|`, with eigenvalues `lambda_l=|4(l-1)(l+3)|`, degeneracy `(l+1)^2`, and domain `l=0,l>=2` after removing the proven four-dimensional l=1 spatial-diffeomorphism gauge sector.

The spectral zeta `zeta_A(s)=sum d_l lambda_l^(-s)` has an explicit analytic continuation regular at s=0. The audit obtains exactly `zeta_A(0)=-4` and numerically `zeta_A'(0)=3.6779497092049564748725729911435744170228213935719`. Thus for the frozen normalization, `Det_zeta(A_hat)=exp[-zeta_A'(0)]=0.025274742319419109765101881172232968834960758539121`.

This finite number is NOT normalization invariant: `Det_zeta(c A_hat)=c^(-4) Det_zeta(A_hat)`. The gate therefore closes only the regularizability of this already-reduced scalar FS factor for a declared normalization. No signed C12 phase is assigned; the FS square-root uses `|mu_l|`.

Strict status: complete HMT gauge-fixed constraint matrix OPEN; complete zero-mode quotient OPEN; full FS determinant OPEN; HMT one-loop evaluability BLOCKED; full C9 OPEN. No parent beta functions imported, no unresolved HMT matter coefficients chosen, thresholds unchanged, soft-s forbidden, k=0.03 production blocked, no DSIR.

Next gate: construct a frozen block inventory for the remaining HMT gauge/constraint sectors on the same background before combining determinant factors.
