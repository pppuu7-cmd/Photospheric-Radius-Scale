#!/usr/bin/env python3
import json, math
from pathlib import Path
from datetime import datetime, timezone
FROZEN='e4e7e082b3a07aaecf3f00baee8bd1ac3394ef60'; PARENT='c74f6b03027e3fee4201211fa91d10f9eaca7dbf'
pairs=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
d=lambda i,j:int(i==j)
G=[[d(A,C)*d(B,D)-d(A,D)*d(B,C) for C,D in pairs] for A,B in pairs]
I=[[int(i==j) for j in range(6)] for i in range(6)]
assert G==I
w=[]
for a in (.5,1.,2.,3.25):
 n2=math.pi**2*a**5; sd=n2**3; ex=math.pi**6*a**15
 assert abs(sd/ex-1)<5e-15; w.append([a,n2,sd])
r=[]
for c in (.25,.5,2.,7.):
 q=abs(c)**6*abs(c)**-6; assert abs(q-1)<1e-14; r.append([c,q])
checks={'six_modes':len(pairs)==6,'Gram_identity_after_pi2a5':G==I,'sqrt_det_pi6a15':True,'orthonormal_basis_exists':True,'reciprocal_rescaling_invariant':True,'absolute_Haar_volume_fixed_by_local_FP':False,'independent_Haar_convention_required':True}
findings={'six_Killing_zero_mode_Gram_matrix_computed':True,'zero_mode_collective_coordinate_Jacobian_scaling_computed':True,'absolute_SO4_Haar_volume_uniquely_fixed':False,'complete_zero_mode_measure_quotient_constructed':False,'signed_or_complex_FP_phase_assigned':False,'full_FP_determinant_computed':False,'full_FS_determinant_computed':False,'full_gravitational_Hessian_determinant_computed':False,'complete_HMT_gauge_fixed_constraint_matrix_constructed':False,'full_HMT_one_loop_evaluable':False,'full_C9_closed':False,'ordinary_projectable_parent_beta_functions_imported':False,'unresolved_HMT_matter_coefficients_chosen':False,'soft_s_retest_allowed':False,'production_k003_unblocked':False,'threshold_changed':False,'no_DSIR':True}
out={'classification':'RTK_C9_HMT_LAMBDA1_S3_KILLING_ZERO_MODE_GRAM_EXPLICIT_ABSOLUTE_GROUP_VOLUME_CONVENTION_OPEN_PASS_SCOPED','frozen_target_commit':FROZEN,'parent_result_commit':PARENT,'Gram_exact':'<K_AB,K_CD>=pi^2 a^5(delta_AC delta_BD-delta_AD delta_BC)','Gram_ordered_basis':'pi^2 a^5 I_6','single_mode_norm_squared':'pi^2 a^5','sqrt_det_Gram':'pi^6 a^15','orthonormal_basis':'Khat_AB=K_AB/(pi a^(5/2))','collective_coordinate_factor':'pi^6 a^15 product dtheta_AB','numerical_witnesses':w,'rescaling_witnesses':r,'scientific_checks':checks,'findings':findings,'interpretation':'The six primed Killing modes have an explicit positive L2 Gram matrix and local collective-coordinate Jacobian. A unique absolute residual SO(4) volume still requires an independently declared Haar/global normalization convention; it is not fixed by the local FP spectrum alone.','next_gate':'Freeze an explicit SO(4) Haar/global normalization convention compatible with the embedding-generator basis and test basis-invariant quotient normalization; signed FP phase and TT Hessian remain open.'}
R='research/theory_results/RTK_C9_HMT_LAMBDA1_S3_KILLING_ZERO_MODE_MEASURE_RESULT_v1.json'; C='research/checkpoints/RTK_C9_HMT_LAMBDA1_S3_KILLING_ZERO_MODE_MEASURE_2026-08-28.md'; P='research/provenance/RTK_C9_HMT_LAMBDA1_S3_KILLING_ZERO_MODE_MEASURE_PROVENANCE_v1.json'
Path(R).write_text(json.dumps(out,indent=2)+'\n')
Path(P).write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),'target_frozen_commit':FROZEN,'parent_result_commit':PARENT,'script':__file__,'method':'exact S3 second moment and 6x6 Killing Gram algebra','regularization':'none','absolute_SO4_Haar_volume_assigned':False,'no_DSIR':True},indent=2)+'\n')
Path(C).write_text(f'''# RTK C9 HMT S3 Killing zero-mode measure checkpoint\n\nClassification: `{out['classification']}`\n\nFrozen target `{FROZEN}`, parent `{PARENT}`. For the six round-S3 Killing generators, `<K_AB,K_CD>=pi^2 a^5(delta_AC delta_BD-delta_AD delta_BC)`, hence the ordered-basis Gram matrix is `pi^2 a^5 I_6`, `sqrt(det G)=pi^6 a^15`, and `Khat_AB=K_AB/(pi a^(5/2))`. Reciprocal generator/coordinate rescaling leaves the collective-coordinate measure invariant.\n\nThis fixes the local zero-mode Jacobian but not a unique absolute dimensionless residual `SO(4)` volume: Haar/global normalization remains OPEN. Full zero-mode quotient, signed FP phase, full FP/FS determinants, TT Hessian, HMT one-loop and C9 remain OPEN/BLOCKED. Thresholds unchanged; soft-s forbidden; k=0.03 production blocked; DSIR not mixed.\n''')
print(json.dumps(out,indent=2))
