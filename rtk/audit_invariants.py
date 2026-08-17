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
signature=(ROOT/'rtk/build_signature_atlas_pair.py').read_text()
lcdm_stationarity=(ROOT/'rtk/autonomous_dense_lcdm_stationarity.py').read_text()
orchestrator=(ROOT/'rtk/autonomous_orchestrator.py').read_text()

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
ok('orchestrator_same_iteration_freeze_uses_best_exact',
   'summary.get("best_exact_S", summary["S_center"])' in orchestrator and
   'eff.get("best_exact_S", eff["S_center"])' in orchestrator and
   orchestrator.count('accepted_score_semantics"] = "best_exact_stencil_within_recenter_tolerance"') >= 2,
   'generic orchestrator must freeze best exact local scores, not center scores, before same-iteration raw comparison')

# Likelihood algebra invariants: preserve the audited definitions used by the
# matched objective. These are implementation guards, not statistical claims.
ok('fs8_eff_is_dsigma8_dloga', 'fs=derivative3(' in runner and 'result[z0]=(fs,f01*s8)' in runner,
   'eff mapping must remain d sigma8 / d ln a; k01 is stored separately')
ok('k01_mapping_separate', 'f01=.5*derivative3(' in runner and "0 if which=='eff' else 1" in runner)
ok('pantheon_offset_profile', 'off=sum(Cid)/sum(Ci1)' in runner and "quad(L_SN,[x-off for x in d])" in runner,
   'Pantheon additive magnitude zero-point must be profiled with full covariance')
ok('boss_bao_rescaling', "*R_FID/rd" in runner and "*C_KM_S*rd/R_FID" in runner,
   'BOSS DM and H observables must use the same fiducial sound-horizon convention')

# Standalone observable-signature pipeline must remain on the same legacy
# nonlocal CLASS input conventions and baseline as the production likelihood.
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

# Reproducibility/provenance lock and fail-closed artifact identity validation.
ok('class_upstream_pinned_target', lock['external_git']['class_public']['commit']=='36cf283628c4a3330ec9fd3d84239bf775f77317')
ok('pantheon_pinned_target', lock['external_git']['pantheon']['commit']=='7eb29dc87ba223b4ec8457cd3cccba1216c36fb7')
ok('clipy_pinned', lock['likelihood']['clipy_like']=='0.15')
ok('artifact_identity_checks_objective', "summary.get(\"objective\") != expected_objective" in identity)
ok('artifact_identity_checks_center', 'exact_center_equal(summary.get("center"), expected_center)' in identity)
ok('artifact_identity_checks_objective_fingerprint', 'objective_fingerprint' in identity and 'canonical_hash(state["objective"])' in identity,
   'RTK Hessian artifacts must match the canonical frozen-objective fingerprint')
ok('artifact_identity_checks_center_fingerprint', 'center_fingerprint' in identity and '"model": "RTK"' in identity and '"mapping": state.get("production_mapping", "eff")' in identity,
   'RTK Hessian artifacts must match the canonical model/center/objective/mapping fingerprint')
ok('artifact_identity_checks_locked_class_sha', 'class_upstream_commit' in identity and 'repro["external_git"]["class_public"]["commit"]' in identity,
   'RTK Hessian artifact must declare the locked CLASS upstream commit')
ok('artifact_identity_checks_locked_pantheon_sha', 'pantheon_commit' in identity and 'repro["external_git"]["pantheon"]["commit"]' in identity,
   'RTK Hessian artifact must declare the locked Pantheon commit')
ok('artifact_identity_checks_locked_numpy', 'numpy_version' in identity and 'repro["python_packages"]["numpy"]' in identity,
   'RTK Hessian artifact runtime NumPy must match the measured lock')

tol=float(state['objective']['recenter_tolerance_S'])
for model in ('lcdm','rtk'):
    m=state.get(model,{})
    if m.get('certification')!='local_dense_accepted':
        continue
    result=m.get('hessian_result') or {}
    if model=='rtk':
        result=result.get('eff',{})
    imp=float(result.get('best_improvement',1e99))
    best=result.get('best_exact_S')
    accepted=m.get('accepted_score_eff')
    if imp<=tol and best is not None and accepted is not None:
        ok(f'{model}_freeze_uses_best_exact', abs(float(accepted)-float(best))<=1e-12,
           f'accepted={accepted} best_exact={best} improvement={imp}')

print('RTK_AUDIT_INVARIANTS_PASS', json.dumps(checks, sort_keys=True))
