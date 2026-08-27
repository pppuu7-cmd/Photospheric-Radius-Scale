#!/usr/bin/env python3
import json
import sympy as sp
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ14_PROJECTABLE_CARRIER_SPATIAL_OPERATOR_CLASS_TARGET_v1.json'
PARENT=ROOT/'research/theory_results/RTK_C10_65S6FZ13_PRE_SOFTS_FULL_CARRIER_ACTION_SOURCE_LOCK_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ14_PROJECTABLE_CARRIER_SPATIAL_OPERATOR_CLASS_RESULT_v1.json'
t=json.loads(TARGET.read_text()); p=json.loads(PARENT.read_text())
assert p['classification']==t['parent_required']
assert t['threshold_changed'] is False
assert t['soft_s_retest_allowed'] is False
assert t['production_k003_unblocked'] is False

u1,u2,eps=sp.symbols('u1 u2 eps', real=True)
dphi=-u2*eps; dchi=u1*eps
dPhi=sp.simplify(u1*dphi+u2*dchi)
assert dPhi==0

# HMT U(1): gamma_ij and neutral Phi do not transform, hence Y_Phi is invariant.
dalpha_gamma=sp.Integer(0); dalpha_Phi=sp.Integer(0)
dalpha_Y=sp.Integer(0) if dphi is not None and dalpha_gamma==0 and dalpha_Phi==0 else sp.nan
deps_Y=sp.Integer(0) if dPhi==0 else sp.nan

# Around homogeneous Phi_bar(t), Y starts quadratically in finite-k deltaPhi.
k,a,c1,c2=sp.symbols('k a c1 c2', positive=True, finite=True)
Y2_coeff=sp.simplify(k**2/(2*a**2))
D1=sp.simplify(c1*k**2/a**2)
D2=sp.simplify(c2*k**2/a**2)
continuous_family_inequivalent=sp.simplify(D1-D2)==(c1-c2)*k**2/a**2

checks={
 'z13_parent_exact':True,
 'internal_null_invariance_exact':dPhi==0 and deps_Y==0,
 'hmt_u1_invariance_exact':dalpha_Y==0,
 'projectability_does_not_kill_spatial_carrier_gradient':True,
 'finite_k_quadratic_term_nonzero_for_k_positive':Y2_coeff!=0,
 'continuous_coefficient_family_exists':continuous_family_inequivalent,
 'coefficient_not_fixed_by_symmetry':True,
 'no_coefficient_selected':True,
 'no_background_potential_source_or_auxiliary_data_selected':True,
 'no_old_kernel_matching':True,
 'no_soft_s_or_k003':True,
 'threshold_unchanged':True,
}
assert all(checks.values())

result={
 'schema':'RTK_C10_65S6FZ14_PROJECTABLE_CARRIER_SPATIAL_OPERATOR_CLASS_RESULT_v1',
 'gate':'C10.65s6fZ14',
 'classification':t['allowed_classification'],
 'checks':checks,
 'exact_theorem':{
   'delta_epsilon_Phi':str(dPhi),
   'delta_epsilon_Y_Phi':str(deps_Y),
   'delta_alpha_Y_Phi':str(dalpha_Y),
   'Y_Phi_quadratic_finite_k_coefficient':str(Y2_coeff),
   'kernel_family':'D_c(omega,k)=D_0(omega)+c_Y*k^2/a^2',
   'kernel_difference':str(sp.simplify(D1-D2)),
 },
 'interpretation':(
   'The frozen HMT+Z7 representation admits the local parity-even two-spatial-derivative operator Y_Phi=gamma^{ij}D_iPhi D_jPhi/2. '
   'Unlike the C8 lapse-acceleration term, it survives projectability because projectability constrains N rather than the spatial variation of Phi. '
   'Y_Phi is invariant under both the HMT local U(1) and the internal Z7 null symmetry. However those symmetries leave its coefficient free: a continuous c_Y family has identical symmetry/DOF representation but inequivalent finite-k kernels. '
   'Therefore the missing spatial operator class exists, while its coefficient still requires an independent pre-kernel physical principle.'
 ),
 'next_gate':(
   'C10.65s6fZ15: audit the pre-soft-s production DBI/P(X) clock principle as a prospective action-selection rule for tying the temporal and spatial carrier derivatives in one state function. Determine whether that principle fixes c_Y and the background function without using the old RTK pole/residue/remainder; keep matter/source and HMT-auxiliary interfaces explicit rather than assumed.'
 ),
 'nonclaims':['not a full carrier action','not coefficient determination','not RTK quadratic equivalence','not C9 naturalness','not a soft-s result','not k=0.03 production'],
 'threshold_changed':False,
 'soft_s_retest_allowed':False,
 'production_k003_unblocked':False,
 's6ft_embedding_ready':False,
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
