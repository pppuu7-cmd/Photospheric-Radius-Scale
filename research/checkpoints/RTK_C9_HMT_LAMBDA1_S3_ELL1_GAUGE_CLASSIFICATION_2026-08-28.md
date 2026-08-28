# RTK C9 HMT lambda=1 S3 ell=1 gauge-classification checkpoint

Classification: `RTK_C9_HMT_LAMBDA1_S3_ELL1_ZERO_MODES_SPATIAL_DIFF_GAUGE_PASS_SCOPED`

Frozen target commit: `620982d5793c05f8da6095b5db21f9e399d9795a`.

For every scalar ell=1 harmonic f on round S3,

nabla_i nabla_j f = -(1/a^2) g_ij f.

Choosing xi_i=-(a^2/2)nabla_i f gives

2 nabla_(i xi_j) = f g_ij,

so the conformal metric perturbation that lies in the ell=1 kernel of C12 is exactly a spatial-diffeomorphism gauge direction. The scalar ell=1 space has dimension four. Thus the residual ell=1 kernel found in the parent constant-curvature witness is gauge in this frozen scalar/conformal sector, not evidence for physical second-class rank loss.

Strict scope: the complete HMT gauge-fixed constraint matrix and full zero-mode quotient have not been constructed. Full FS determinant OPEN; full HMT one-loop BLOCKED; full C9 OPEN; soft-s retest forbidden; k=0.03 production blocked; thresholds unchanged.

Next gate: construct the reduced scalar/conformal C12 determinant/spectrum with ell=1 gauge modes explicitly projected out, without claiming a full HMT determinant.
