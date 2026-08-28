# RTK C9 HMT lambda=1 S3 spatial FP nonzero-mode zeta-magnitude checkpoint

Classification: `RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_NONZERO_MODE_ZETA_MAGNITUDES_FINITE_PASS_SCOPED`

Frozen target commit: `4191e4dd12aff1c648af391755f3e169df33d378`. Parent confirmed HEAD at freeze: `5ec5fdd787571764daf723122300a34da6e09b38`.

For the parent-certified spatial FP operator `M=nabla^2+Ricci`, this gate regularizes only the positive spectral magnitudes of the two nonzero vector sectors. The transverse dimensionless spectrum is `A_T=a^2|M_T|`, with `n=l+1>=3`, eigenvalue `n^2-4` and degeneracy `2(n^2-1)` after priming out the six l=1 Killing generators. The longitudinal spectrum is `A_L=a^2|M_L|`, with the retained n=2 level `(lambda,d)=(1,4)` and n>=3 spectrum `(lambda,d)=(n^2-5,n^2)`.

Both spectral zetas are regular at zero. The audit obtains `zeta_T(0)=-5`, `zeta_L(0)=-1`, `zeta_T'(0)=-4.2175844210901928903126417441702651041697702742307` and `zeta_L'(0)=-0.78841578072819896521199609779193130990423885117523`. For the frozen normalizations, `Det_zeta(A_T)=67.869342368305180409328005773658622338151596454315` and `Det_zeta(A_L)=2.1999085267023697422585361883960668683089207686293`. The K=120 versus K=140 derivative differences are `5.7504491e-44` and `2.1442708e-32`; the direct-spectrum s=5 cross-check differences are `2.2317523e-31` and `1.0521444e-31`, all below the inherited `1e-30` tolerance.

Normalization dependence is explicit: `Det(c A_T)=c^(-5) Det(A_T)` and `Det(c A_L)=c^(-1) Det(A_L)`. These are determinant magnitudes only. No signed/complex FP phase is assigned, and no residual SO(4) gauge-group volume normalization is supplied.

Strict scope: complete zero-mode measure quotient OPEN; complete signed spatial FP determinant OPEN; full FP determinant OPEN; full FS determinant OPEN; physical TT Hessian OPEN; complete HMT gauge-fixed constraint matrix OPEN; HMT one-loop evaluability BLOCKED; full C9 OPEN. No scalar-gradient decomposition Jacobian is inserted. Thresholds unchanged; soft-s forbidden; k=0.03 production blocked; DSIR not mixed.

Next gate: prospectively freeze the six-Killing residual-isometry zero-mode measure quotient and gauge-group-volume normalization, without touching the signed FP phase or TT Hessian.
