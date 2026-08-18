#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
state=json.loads((ROOT/'research/state/current.json').read_text())
runner=(ROOT/'rtk/joint_profile_runner.py').read_text()
prep=(ROOT/'rtk/prepare_inference_core.py').read_text()
protocol=(ROOT/'rtk/FINAL_MATCHED_COMPARISON_PROTOCOL.md').read_text()
inputs=(ROOT/'rtk/upgrade_rtk_inputs.py').read_text()
lock=json.loads((ROOT/'rtk/reproducibility_lock.json').read_text())
identity=(ROOT/'rtk/validate_artifact_identity.py').read_text()
identity_norm=''.join(identity.split()).replace('"',"'")
signature=(ROOT/'rtk/build_signature_atlas_pair.py').read_text()
lcdm_stationarity=(ROOT/'rtk/autonomous_dense_lcdm_stationarity.py').read_text()
rtk_stationarity=(ROOT/'rtk/autonomous_dense_rtk_stationarity.py').read_text()
negative_ray=(ROOT/'rtk/autonomous_negative_eigenray_gate.py').read_text()
orchestrator=(ROOT/'rtk/autonomous_orchestrator.py').read_text()
multiscale=(ROOT/'rtk/enforce_stage4d3_multiscale_gate.py').read_text()
adaptive=(ROOT/'rtk/enforce_adaptive_quarter_gate.py').read_text()
ladder=(ROOT/'rtk/enforce_stage4d3_scale_ladder_gate.py').read_text()

checks=[]
def ok(name, cond, detail=''):
    if not cond:
        raise SystemExit(f'AUDIT_INVARIANT_FAIL {name}: {detail}')
    checks.append(name)

ok('production_gauge_newtonian', '"gauge = newtonian"' in runner,
   'production likelihood must not enter the unsupported Khronon synchronous dynamics branch')
ok('exact_float_cache_preparation', "tuple(float(p[k]) for k in ['lam','h','Ob','Om','As','ns','zre'])" in prep and 'round(float(p[k]),12)' in prep,
   'preparation script must explicitly replace legacy rounded cache keys with exact-float keys')
ok('success_only_likelihood_cache', "if r.get('ok')" in prep and 'all_failures_uncached' in prep,
   'failed CLASS/post-processing evaluations must not poison the exact likelihood cache')
ok('production_mapping_eff', state.get('production_mapping')=='eff')
ok('matched_dense_objective', state.get('objective',{}).get('name')=='matched-ultra-linstep2+dense-BOSS')
ok('lambda_is_real_input', 'class_read_double("lambda_D",pba->lambda_D)' in inputs)
ok('mapping_separation_protocol', 'eff` and `k01`' in protocol and 'treated as separate objective variants' in protocol)
ok('lcdm_steps_decoupled_from_rtk', "STATE['rtk']['base_steps']" not in lcdm_stationarity and 'DEFAULT_LCDM_STEPS' in lcdm_stationarity,
   'LCDM Hessian finite-difference scale must not silently inherit the RTK state block')
ok('rtk_hessian_records_eigenvectors', 'np.linalg.eigh(H)' in rtk_stationarity and "'eigenvectors_y':vee.T.tolist()" in rtk_stationarity and "'eigenvectors_y':vek.T.tolist()" in rtk_stationarity,
   'future RTK Hessian artifacts must retain eigenvectors for multiscale convergence/overlap diagnostics')
ok('orchestrator_same_iteration_freeze_uses_best_exact',
   'summary.get("best_exact_S", summary["S_center"])' in orchestrator and
   'eff.get("best_exact_S", eff["S_center"])' in orchestrator and
   orchestrator.count('accepted_score_semantics"] = "best_exact_stencil_within_recenter_tolerance"') >= 2,
   'generic orchestrator must freeze best exact local scores, not center scores, before same-iteration raw comparison')

ok('fs8_eff_is_dsigma8_dloga', 'fs=derivative3(' in runner and 'result[z0]=(fs,f01*s8)' in runner,
   'eff mapping must remain d sigma8 / d ln a; k01 is stored separately')
ok('k01_mapping_separate', 'f01=.5*derivative3(' in runner and "0 if which=='eff' else 1" in runner)
ok('pantheon_offset_profile', 'off=sum(Cid)/sum(Ci1)' in runner and "quad(L_SN,[x-off for x in d])" in runner,
   'Pantheon additive magnitude zero-point must be profiled with full covariance')
ok('boss_bao_rescaling', "*R_FID/rd" in runner and "*C_KM_S*rd/R_FID" in runner,
   'BOSS DM and H observables must use the same fiducial sound-horizon convention')

ok('signature_uses_legacy_As_ns', 'f"A_s = {p[\'As\']}"' in signature and 'f"n_s = {p[\'ns\']}"' in signature,
   'legacy nonlocal CLASS must receive A_s/n_s directly in standalone signature runs')
ok('signature_rejects_As_ad_ns_ad', 'A_s_ad =' not in signature and 'n_s_ad =' not in signature,
   'A_s_ad/n_s_ad previously produced incorrect absolute amplitudes in this legacy CLASS branch')
ok('signature_neutrino_baseline_matches_production', '"N_ur = 3.046"' in signature and '"N_ncdm = 0"' in signature,
   'signature diagnostic must not silently change the production neutrino baseline')
ok('signature_recfast_matches_production', '"recombination = RECFAST"' in signature)
ok('signature_gauge_newtonian', '"gauge = newtonian"' in signature)
ok('signature_exact_pk_redshift_gate', 'required exact P(k,z) output' in signature)
ok('signature_drag_epoch_gate', 'baryon drag stops at z' in signature)

ok('class_upstream_pinned_target', lock['external_git']['class_public']['commit']=='36cf283628c4a3330ec9fd3d84239bf775f77317')
ok('pantheon_pinned_target', lock['external_git']['pantheon']['commit']=='7eb29dc87ba223b4ec8457cd3cccba1216c36fb7')
ok('clipy_pinned', lock['likelihood']['clipy_like']=='0.15')
ok('artifact_identity_checks_objective', "summary.get('objective')!=expected_objective" in identity_norm)
ok('artifact_identity_checks_center', "exact_center_equal(summary.get('center'),expected_center)" in identity_norm)
ok('artifact_identity_checks_objective_fingerprint', "'objective_fingerprint'" in identity_norm and "canonical_hash(state['objective'])" in identity_norm,
   'RTK proof artifacts must match the canonical frozen-objective fingerprint')
ok('artifact_identity_checks_center_fingerprint', "'center_fingerprint'" in identity_norm and "'model':'RTK'" in identity_norm and "'mapping':state.get('production_mapping','eff')" in identity_norm,
   'RTK proof artifacts must match the canonical model/center/objective/mapping fingerprint')
ok('artifact_identity_checks_locked_class_sha', "'class_upstream_commit'" in identity_norm and "repro['external_git']['class_public']['commit']" in identity_norm)
ok('artifact_identity_checks_locked_pantheon_sha', "'pantheon_commit'" in identity_norm and "repro['external_git']['pantheon']['commit']" in identity_norm)
ok('artifact_identity_checks_locked_numpy', "'numpy_version'" in identity_norm and "repro['python_packages']['numpy']" in identity_norm)
ok('artifact_identity_includes_negative_eigenray', "('rtk','negative_eigenray_run')" in identity_norm and "'negative_eigenray_run'" in identity_norm)
ok('artifact_identity_includes_quarter_stencil', "('rtk','quarter_hessian_run')" in identity_norm and "'quarter_hessian_run'" in identity_norm)
ok('artifact_identity_includes_eighth_negative_eigenray',
   "('rtk','eighth_negative_eigenray_run')" in identity_norm and "'eighth_negative_eigenray_run'" in identity_norm,
   'terminal 1/8 negative-eigenray artifacts must receive the same locked proof-artifact validation')

ok('stage4d3_negative_eigenray_before_half',
   'process_negative_ray' in multiscale and 'rtk-autonomous-negative-eigenray.yml' in multiscale and
   multiscale.find('ray_status=process_negative_ray') < multiscale.find("half=rtk.get('half_hessian_run')"),
   'Stage4D3 must run exact negative-eigenray gate before half-stencil for non-PD base Hessians')
ok('adaptive_quarter_requires_ray_clear_and_half_pd',
   "ray_clear=(base_pd or rtk.get('negative_eigenray_certification')=='exact_negative_eigenrays_recenter_clear')" in adaptive and
   "if (not base_pd) and half_pd:" in adaptive and "expected_stencil_scale':0.25" in adaptive,
   'adaptive quarter proof must require exact-ray clearance and a PD half stencil after a non-PD coarse base')
ok('adaptive_proof_requires_half_and_quarter_pd',
   "bool(qe.get('positive_definite'))" in adaptive and 'N5_ADAPTIVE_HALF_AND_QUARTER_PASS' in adaptive,
   'adaptive interior-minimum certification must require a recenter-clear PD quarter stencil after PD half')
ok('negative_eigenray_worker_supports_eighth_scale',
   "'eighth':('eighth_hessian_result','eighth_hessian_run',0.125)" in negative_ray,
   'generic exact-ray worker must be able to falsify a non-PD terminal 1/8 Hessian at its own physical scale')
ok('scale_ladder_requires_eighth_ray_before_exhaustion',
   "rs=ensure_ray(state,'eighth',changes)" in ladder and
   ladder.find("rs=ensure_ray(state,'eighth',changes)") < ladder.find("N5_SCALE_LADDER_EXHAUSTED_CURVATURE_UNRESOLVED"),
   'a non-PD 1/8 Hessian may not be classified as exhausted until its same-scale exact ray is recenter-clear')
ok('scale_ladder_eighth_ray_is_scale_locked',
   "'eighth':('eighth_negative_eigenray_run','eighth_negative_eigenray_result','eighth_negative_eigenray_certification',EIGHTH_RAY_WF,EIGHTH_RAY_ART,0.125)" in ladder and
   "expected={'half':0.5,'quarter':0.25,'eighth':0.125}" in ladder,
   'terminal eigenray dispatch and artifact semantics must remain fixed to source scale 0.125')
ok('scale_ladder_recenter_clears_eighth_ray',
   "'eighth_negative_eigenray_result','eighth_negative_eigenray_run'" in ladder,
   'a downhill recenter must invalidate all old terminal-ray proof state')

tol=float(state['objective']['recenter_tolerance_S'])
for model in ('lcdm','rtk'):
    m=state.get(model,{})
    if m.get('certification')!='local_dense_accepted':continue
    result=m.get('hessian_result') or {}
    if model=='rtk':result=result.get('eff',{})
    imp=float(result.get('best_improvement',1e99));best=result.get('best_exact_S');accepted=m.get('accepted_score_eff')
    if imp<=tol and best is not None and accepted is not None:
        ok(f'{model}_freeze_uses_best_exact', abs(float(accepted)-float(best))<=1e-12,
           f'accepted={accepted} best_exact={best} improvement={imp}')

print('RTK_AUDIT_INVARIANTS_PASS', json.dumps(checks, sort_keys=True))
