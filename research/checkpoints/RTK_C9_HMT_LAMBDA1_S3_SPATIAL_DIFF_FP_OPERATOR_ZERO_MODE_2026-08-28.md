# RTK C9 HMT lambda=1 S3 spatial-diffeomorphism FP operator / zero-mode checkpoint

Classification: `RTK_C9_HMT_LAMBDA1_S3_SPATIAL_DIFF_FP_OPERATOR_ZERO_MODE_EXACT_PASS_SCOPED`

Frozen target commit: `0afc88e5602b4d689e977fa5a6606771c1242088`. Parent confirmed HEAD at freeze: `469fb4f1faba5facdd70be1cf4e70052c5644cda`.

The prospectively frozen spatial gauge is `F_i=nabla^j h_ij-(1/2)nabla_i h=0`. Its exact linearized spatial-diffeomorphism variation is

`delta F_i=(nabla^2 delta_i^j+R_i^j) xi_j`,

because the mixed gradient-divergence coefficient `1-2 beta` vanishes exactly at the frozen beta=1/2.

On round S3, transverse vector harmonics have FP eigenvalue `[3-l(l+2)]/a^2=-(l-1)(l+3)/a^2`. Thus the only transverse zero level is l=1, with multiplicity `2 l(l+2)=6`; it coincides with the six Killing generators of SO(4). For longitudinal generators `xi_i=nabla_i Y_l`, the eigenvalue is `[4-l(l+2)]/a^2=[5-(l+1)^2]/a^2`, which has no zero for any integer l>=1. The l=0 scalar gradient vanishes identically and is not a ghost zero mode.

The certified l=1 conformal witness is consistent: for `h_ij=f g_ij` and `xi_i=-(a^2/2)nabla_i f`, `L_xi g_ij=f g_ij` and both `F_i[f g]` and `M_i^j xi_j` equal `-(1/2)nabla_i f`. It is therefore fixed by the longitudinal spatial gauge and is not one of the residual Killing zero modes.

Strict scope: complete zero-mode measure quotient OPEN; zeta-regularized spatial FP determinant OPEN; full FP determinant OPEN; full FS determinant OPEN; physical TT Hessian OPEN; complete HMT gauge-fixed constraint matrix OPEN; HMT one-loop evaluability BLOCKED; full C9 OPEN. Projectable time gauge and HMT U(1) remain separate. Thresholds unchanged; soft-s forbidden; k=0.03 production blocked; DSIR not mixed.

Next gate: freeze the nonzero-mode spatial FP determinant normalization and zeta prescription, quotienting the six l=1 Killing generators explicitly, without combining FP with FS or TT Hessian factors.
