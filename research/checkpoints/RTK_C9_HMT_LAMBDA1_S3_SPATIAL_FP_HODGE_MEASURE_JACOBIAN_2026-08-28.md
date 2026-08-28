# RTK C9 HMT lambda=1 S3 spatial FP Hodge-measure Jacobian checkpoint

Classification: `RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_HODGE_JACOBIAN_ABSORBED_IN_ORTHONORMAL_VECTOR_BASIS_PASS_SCOPED`

Frozen target `a93e8261e03f9f7503e685a46c537ddcb687ca46`; scientific parent `c6c9e4062569fcbf94c8e1860f509cb39defd9a3`. For the L2 Hodge split `xi=xi_T+grad sigma`, a raw scalar-potential parametrization has the usual commuting-field Jacobian `[det_prime(-a^2 nabla^2)_0]^(1/2)`. However the already-certified transverse/longitudinal FP spectra were defined in L2-orthonormal vector harmonics, where the normalized longitudinal basis is `e_L=a grad Y/sqrt(l(l+2))` and this coordinate Jacobian is already absorbed.

For Grassmann ghost and antighost fields, raw scalar-potential variables instead produce the inverse pair Jacobian `[det_prime Delta0_hat]^(-1)`. The longitudinal quadratic form in those raw variables has eigenvalue `lambda_n m_n`, so its extra `det_prime Delta0_hat` cancels that inverse measure factor mode-by-mode. Therefore the existing orthonormal-vector FP spectral product must NOT be multiplied by an additional Hodge determinant; doing so would double count. The scalar l=0 constant is excluded because its gradient vanishes.

This is scoped measure bookkeeping only. The complete signed spatial FP quotient is not yet assembled with the residual SO(4) orbit normalization in one frozen expression. Full FP/FS determinants, TT Hessian, complete HMT gauge-fixed matrix, one-loop evaluability and C9 remain OPEN/BLOCKED. Thresholds unchanged; soft-s forbidden; k=0.03 production blocked; DSIR not mixed.
