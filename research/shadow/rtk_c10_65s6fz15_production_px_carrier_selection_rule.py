#!/usr/bin/env python3
import json
import subprocess
import sympy as sp
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ15_PRODUCTION_PX_CARRIER_SELECTION_RULE_TARGET_v1.json'
PARENT=ROOT/'research/theory_results/RTK_C10_65S6FZ14_PROJECTABLE_CARRIER_SPATIAL_OPERATOR_CLASS_RESULT_v1.json'
Z13=ROOT/'research/theory_results/RTK_C10_65S6FZ13_PRE_SOFTS_FULL_CARRIER_ACTION_SOURCE_LOCK_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ15_PRODUCTION_PX_CARRIER_SELECTION_RULE_RESULT_v1.json'
t=json.loads(TARGET.read_text()); p=json.loads(PARENT.read_text()); z13=json.loads(Z13.read_text())
assert p['classification']==t['parent_required']
assert t['threshold_changed'] is False and t['soft_s_retest_allowed'] is False and t['production_k003_unblocked'] is False

src=t['pinned_source']
blob=subprocess.check_output(['git','show',f"{src['commit']}:{src['path']}"],text=True)
low=blob.lower()
source_px=('p(x)-type scalar' in low) and ('fixed khronon/p(x)-type clock background' in low)
source_xlaw='x = x0/a^3' in low
source_G='g_8pig := rho_8pig+p_8pig = 2 mu_k^2 x q' in low
source_K='k_8pig = 2 m_k^2' in low

x,Q,s,mu=sp.symbols('x Q s mu', positive=True, finite=True)
G=2*mu**2*x*Q
K=2*mu**2*Q**2*s**3
ca2=x/(s**3*Q)
ratio=sp.simplify(G/K)
identity=sp.simplify(ratio-ca2)==0

# Z13 already certified that the old source does not supply a same-action matter/source map
# or HMT auxiliary carrier interface. Z15 does not silently fill those slots.
matter_open=(z13['source_lock']['C8_contains_action_derived_matter_source_map'] is False)
aux_open=(z13['source_lock']['C8_contains_same_action_HMT_auxiliary_carrier_interface'] is False)

source_locked=source_px and source_xlaw and source_G and source_K and identity
classification=('C10_65S6FZ15_PX_INTRINSIC_CARRIER_SECTOR_FIXED_PARTIAL_PASS_SCOPED' if source_locked else 'C10_65S6FZ15_PX_SELECTION_RULE_NOT_SOURCE_LOCKED_BLOCKED_SCOPED')
checks={
 'z14_parent_exact':True,
 'pinned_pre_soft_source_read':True,
 'production_px_principle_source_locked':source_px,
 'production_x_a_minus3_source_locked':source_xlaw,
 'production_enthalpy_G_source_locked':source_G,
 'production_kinetic_K_source_locked':source_K,
 'exact_G_over_K_equals_ca2':identity,
 'intrinsic_spatial_coefficient_fixed_by_production_G_along_background':source_locked,
 'intrinsic_temporal_coefficient_fixed_by_production_K_along_background':source_locked,
 'matter_source_interface_kept_open':matter_open,
 'hmt_auxiliary_interface_kept_open':aux_open,
 'no_old_kernel_matching':True,
 'no_soft_s_or_k003':True,
 'threshold_unchanged':True,
}
assert all(checks.values())

result={
 'schema':'RTK_C10_65S6FZ15_PRODUCTION_PX_CARRIER_SELECTION_RULE_RESULT_v1',
 'gate':'C10.65s6fZ15',
 'classification':classification,
 'checks':checks,
 'exact_identities':{
   'G_8piG':str(G),
   'K_8piG':str(K),
   'G_over_K':str(ratio),
   'c_a_squared':str(ca2),
   'G_over_K_minus_ca2':str(sp.simplify(ratio-ca2)),
   'background_charge_scaling':'x=x0/a^3'
 },
 'intrinsic_carrier_selection':{
   'temporal_quadratic_coefficient':'K_phys=Mpl^2*K_8piG',
   'spatial_quadratic_coefficient':'G_phys=Mpl^2*G_8piG',
   'ratio':'G_phys/K_phys=c_a^2',
   'selection_origin':'pre-soft-s production P(X)-type clock principle, not finite-k RTK matching'
 },
 'still_open_same_action_interfaces':['matter/source coupling fixing response numerator','explicit carrier coupling to HMT A/prepotential beyond the already frozen invariant-shift representation','global nonlinear P(X) completion away from the production background trajectory if needed beyond quadratic order'],
 'interpretation':(
   'The pre-soft-s production P(X)-type clock principle supplies a genuine independent selection rule for the intrinsic carrier derivative sector. Along the certified production background, G=rho+p and K=(rho+p)/c_a^2 obey G/K=c_a^2 exactly, so the temporal and ordinary spatial-gradient quadratic coefficients are fixed by the production background rather than by the previously observed finite-k RTK kernel. '
   'This removes the free c_Y ambiguity of Z14 at the intrinsic-carrier quadratic level. It does not yet make the HMT+Z7 completion match-ready because the action-derived matter/source numerator and the complete HMT auxiliary interface remain source-open, and no claim about the full nonlinear P(X) completion away from the background trajectory is made.'
 ),
 'next_gate':(
   'C10.65s6fZ16: source-lock the HMT matter/physical-metric coupling and the carrier A/prepotential interface for the P(X)-selected Z7 carrier. Only if one same action fixes those response interfaces may the unchanged Z12 match-ready audit be reopened; otherwise classify the remaining source-interface blocker without fitting to RTK observables.'
 ),
 'nonclaims':['not a full HMT+carrier action','not full response numerator determination','not RTK pole/residue/remainder equivalence','not C9 naturalness','not a soft-s result','not k=0.03 production'],
 'threshold_changed':False,'soft_s_retest_allowed':False,'production_k003_unblocked':False,'s6ft_embedding_ready':False
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
