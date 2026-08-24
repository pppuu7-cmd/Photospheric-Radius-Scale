#!/usr/bin/env python3
"""Current-lineage replay of finite-k/all-q U(1) rank-domain theorems.

This gate does not choose parameters.  It replays exact symbolic workers and
records the strongest common statement that survives them: a constructive
flat-FLRW finite-k/all-q rank-safe domain exists, including a lambda_HL>1
near-GR branch, while production observable implementation and several broader
matter/background domains remain separate gates.
"""
import json, subprocess, sys
from pathlib import Path

TARGET=Path('research/theory_targets/RTK_ROUTE_B_U1_FINITE_K_RANK_DOMAIN_CONSOLIDATION_TARGET_v1.json')
t=json.loads(TARGET.read_text())
assert t['classification']=='RTK_ROUTE_B_U1_FINITE_K_RANK_DOMAIN_CONSOLIDATION_TARGET_V1_FROZEN'

jobs=[
 ('rtk/route_b_u1_flat_flrw_lowk_pure_gravity_rank_gate.py','u1_flat_flrw_lowk_pure_gravity_rank_result.json','RTK_ROUTE_B_U1_FLAT_FLRW_LOWK_PURE_GRAVITY_RANK_PASS'),
 ('rtk/route_b_u1_lowk_rank_perturbation_bound_gate.py','u1_lowk_rank_perturbation_bound_result.json','RTK_ROUTE_B_U1_LOWK_RANK_PERTURBATION_BOUND_PASS'),
 ('rtk/route_b_u1_rtk_lowk_e11_rank_immunity_gate.py','u1_rtk_lowk_e11_rank_immunity_result.json','RTK_ROUTE_B_U1_RTK_LOWK_E11_RANK_IMMUNITY_PASS'),
 ('rtk/route_b_u1_filtered_matter_rank_density_cancellation_gate.py','u1_filtered_matter_rank_density_cancellation_result.json','RTK_ROUTE_B_U1_FILTERED_MATTER_RANK_DENSITY_CANCELLATION_PASS'),
 ('rtk/route_b_u1_filtered_matter_perfect_fluid_rank_bound_gate.py','u1_filtered_matter_perfect_fluid_rank_bound_result.json','RTK_ROUTE_B_U1_FILTERED_MATTER_PERFECT_FLUID_RANK_BOUND_PASS'),
 ('rtk/route_b_u1_filtered_matter_rank_window_gate.py','u1_filtered_matter_rank_window_result.json','RTK_ROUTE_B_U1_FILTERED_MATTER_RANK_WINDOW_PASS'),
 ('rtk/route_b_u1_current_full_action_leading_rank_margin_gate.py','u1_current_full_action_leading_rank_margin_result.json','RTK_ROUTE_B_U1_CURRENT_FULL_ACTION_LEADING_RANK_MARGIN_PASS'),
 ('rtk/route_b_u1_flat_flrw_barotropic_lambda_gt1_no_root_gate.py','u1_flat_flrw_barotropic_lambda_gt1_no_root_result.json','RTK_ROUTE_B_U1_FLAT_FLRW_BAROTROPIC_LAMBDA_GT1_NO_ROOT_PASS'),
 ('rtk/route_b_u1_flat_flrw_lambda_gt1_near_gr_background_gate.py','u1_flat_flrw_lambda_gt1_near_gr_background_result.json','RTK_ROUTE_B_U1_FLAT_FLRW_LAMBDA_GT1_NEAR_GR_BACKGROUND_PASS'),
 ('rtk/route_b_u1_lambda_gt1_anisotropic_rank_margin_gate.py','u1_lambda_gt1_anisotropic_rank_margin_result.json','RTK_ROUTE_B_U1_LAMBDA_GT1_ANISOTROPIC_RANK_MARGIN_PASS'),
 ('rtk/u1_lambda_gt1_cosmology_anisotropy_window_gate.py','u1_lambda_gt1_cosmology_anisotropy_window_result.json','RTK_U1_LAMBDA_GT1_COSMOLOGY_ANISOTROPY_WINDOW_PASS'),
 ('rtk/route_b_u1_flat_tt_allq_stability_gate.py','u1_flat_tt_allq_stability_result.json','RTK_ROUTE_B_U1_FLAT_TT_ALLQ_STABILITY_PASS'),
]
replayed=[]
for script,result,expected in jobs:
    assert Path(script).is_file(),script
    cp=subprocess.run([sys.executable,script],text=True,capture_output=True)
    if cp.returncode:
        print(cp.stdout)
        print(cp.stderr,file=sys.stderr)
        raise SystemExit(f'worker failed: {script}')
    r=json.loads(Path(result).read_text())
    assert r['classification']==expected,(script,r.get('classification'),expected)
    replayed.append({'script':script,'result':result,'classification':expected})

r_low=json.loads(Path('u1_rtk_lowk_e11_rank_immunity_result.json').read_text())
r_den=json.loads(Path('u1_filtered_matter_rank_density_cancellation_result.json').read_text())
r_pf=json.loads(Path('u1_filtered_matter_perfect_fluid_rank_bound_result.json').read_text())
r_win=json.loads(Path('u1_filtered_matter_rank_window_result.json').read_text())
r_lead=json.loads(Path('u1_current_full_action_leading_rank_margin_result.json').read_text())
r_all=json.loads(Path('u1_flat_flrw_barotropic_lambda_gt1_no_root_result.json').read_text())
r_gr=json.loads(Path('u1_flat_flrw_lambda_gt1_near_gr_background_result.json').read_text())
r_an=json.loads(Path('u1_lambda_gt1_anisotropic_rank_margin_result.json').read_text())
r_joint=json.loads(Path('u1_lambda_gt1_cosmology_anisotropy_window_result.json').read_text())
r_tt=json.loads(Path('u1_flat_tt_allq_stability_result.json').read_text())

assert 'b2^2 |k|^4' in r_low['leading_determinant']
assert 'lambda-independent' in r_den['cancellations'][1]
assert 'rho/M_Pl^2' in r_pf['d3_eta0_1_specializations']['dust_w0']
assert '99 k_cos^2' in r_win['one_percent_cosmological_rescue']
assert 'isolated root' in r_lead['correction_to_old_bound']
assert 'det B(q)=F(q)^2+a(q)d(q)>0' in r_all['determinant_conclusion']
assert '2/(3 lambda-1)' in r_gr['ratio']
assert 'lambda>1' in r_an['domain']
assert 'sqrt(2/3)' in r_joint['joint_window_exists_if']
assert 'c_T^2=1' in r_tt['ir_speed']

out={
 'classification':'RTK_ROUTE_B_U1_FINITE_K_RANK_DOMAIN_CURRENT_LINEAGE_REPLAY_PASS',
 'status':'CONSTRUCTIVE_FLAT_FLRW_FINITE_K_AND_ALL_Q_RANK_SAFE_DOMAIN_REPLAYED_PRODUCTION_IMPLEMENTATION_OPEN',
 'target':str(TARGET),
 'replayed_workers':replayed,
 'low_k_summary':{
   'pure_gravity':'det B = b2^2 |k|^4 + O(|k|^6) on the regular expanding special-U1 branch',
   'neutral_RTK':'the only direct leading RTK E11 correction cannot change the leading |k|^4 determinant; it can change conditioning',
   'filtered_matter':'leading rank loss is controlled by an explicit M_c-dependent matrix/root rather than an unavoidable half-line failure',
   'current_action_root':'M_c^2=-x/b2 when positive is the isolated leading rank-loss root; away from it a nonzero leading margin exists',
   'perfect_fluid_scale':'a conservative lower bound is set by rho,p over M_Pl^2, not by the background canonical momentum or lambda_HL'
 },
 'all_q_constructive_domain':{
   'background':'d=3 flat homogeneous isotropic barotropic ordinary source with rho>=0 and 0<=w<=4/3',
   'lambda_HL':'strictly >1',
   'beta0_bare':0,
   'UV_lapse_signs':['beta24=beta2+beta4<=0','beta8<0 in the stated Zhu convention'],
   'source_bound':'M_c^2 >= (9 w^2/32) rho/(eta0 M_Pl^2); for w=1/3 this is rho/(32 eta0 M_Pl^2); dust satisfies the displayed trace condition automatically in that theorem',
   'rank':'det B(q)=F(q)^2+a(q)d(q)>0 for every q>0 in the sufficient domain',
   'near_GR':'H^2(lambda_HL)/H^2(1)=2/(3 lambda_HL-1), so the lambda_HL>1 domain has a nonempty arbitrarily-near-GR homogeneous interval',
   'anisotropy':'a finite perturbative anisotropic rank neighborhood exists for every lambda_HL>1 but its conservative margin shrinks as lambda_HL->1+',
   'tensor':'flat TT stability is independent of lambda_HL and lapse-UV beta24/beta8 in this channel; gamma5>0 and gamma3>-2 sqrt(gamma5) preserve positive all-q TT dispersion with IR c_T^2=1'
 },
 'parameter_freeze':'No numerical M_c, lambda_HL or UV Wilson coefficient is selected by this replay.',
 'critical_remaining_boundaries':{
   'production_CLASS':'OPEN: expose lambda_HL separately from lambda_D and implement the elliptic filtered A-source/constraint dynamics before any same-full-action likelihood claim',
   'history_wide_Mc':'OPEN: convert epochwise rho,p source bounds into a declared EFT-history domain, including radiation and massive-neutrino/aniso-stress treatment',
   'generic_background_rank':'OPEN beyond the stated FLRW/all-q and perturbative anisotropic neighborhoods',
   'local_rest_C8':'OPEN: the exact local-rest rank-collapse/strong-coupling problem is not cured by this matter-filter rank certificate',
   'C9':'OPEN: radiative protection of sigma1=sigma2=0 remains unresolved'
 },
 'interpretation':'The elliptic completion is no longer blocked by an unidentified finite-k rank failure on the controlled flat-FLRW barotropic branch: the repository contains a constructive all-q sufficient domain and a near-GR lambda_HL>1 intersection. The dominant next task is to implement that completion in the production cosmology code under a predeclared parameter/domain protocol; this replay does not transfer the old RTK likelihood score to the completed action.',
 'nonclaims':t['critical_nonclaims'],
 'next_gate':t['next_gate_if_pass']
}
Path('u1_finite_k_rank_domain_consolidation_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
