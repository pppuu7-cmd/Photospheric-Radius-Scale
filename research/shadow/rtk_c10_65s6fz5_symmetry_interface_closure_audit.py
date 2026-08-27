#!/usr/bin/env python3
import json, sys
from pathlib import Path
T=Path('research/theory_targets/RTK_C10_65S6FZ5_SYMMETRY_INTERFACE_CLOSURE_AUDIT_TARGET_v1.json')
Z2T=Path('research/theory_targets/RTK_C10_65S6FZ2_PROJECTABLE_GAUGE_REALIZATION_TEMPLATE_TARGET_v1.json')
Z4=Path('research/theory_results/RTK_C10_65S6FZ4_PROJECTABLE_GRAVITY_SOURCE_LOCK_AUDIT_RESULT_v1.json')
C9=Path('research/checkpoints/RTK_PROJECTABLE_U1_C9_ARCHITECTURE_CHECKPOINT_2026-08-23T2007Z.md')
OUT=Path('research/theory_results/RTK_C10_65S6FZ5_SYMMETRY_INTERFACE_CLOSURE_AUDIT_RESULT_v1.json')
for p in (T,Z2T,Z4,C9):
    if not p.exists(): print('missing',p,file=sys.stderr); sys.exit(3)
t=json.loads(T.read_text()); z2=json.loads(Z2T.read_text()); z4=json.loads(Z4.read_text()); c9=C9.read_text()
ft=z2['frozen_template']; ft_text=json.dumps(ft,sort_keys=True)
# Source-lock audit only: absence below is intentionally classified, not repaired by an invented assignment.
checks={
 'target_exact':t.get('gate')=='C10.65s6fZ5',
 'parent_exact':z4.get('classification')=='C10_65S6FZ4_PROJECTABLE_GRAVITY_PARTIAL_PARENT_PASS_SCOPED',
 'shared_projectability_explicit':'N=N(t)' in ft.get('projectable_adm','') and 'For `N=N(t)`' in c9,
 'z2_field_space_symmetry_explicit':'epsilon(x,t)*n' in ft.get('gauge_transformation',''),
 'z2_adm_inert_under_field_space_symmetry':'gamma_ij and N^i are inert' in ft.get('projectable_adm',''),
 'z2_uses_Dperp_Phi':'D_perp Phi' in ft.get('action_class',''),
 'z4_requires_new_same_action_interface':z4.get('s6ft_embedding_ready') is False,
 'no_soft_s':t['guards']['no_soft_s_retest'] is True,
 'no_k003':t['guards']['no_k003_production'] is True,
 'threshold_unchanged':t['guards']['threshold_changed'] is False,
}
# The new fields phi,chi were introduced by s6fZ2. Its frozen template contains no U(1)
# representation/charge assignment and no invariant-shift/prepotential/gauge-field mapping.
missing={
 'phi_chi_gravity_gauge_representation_not_source_locked': not any(tok in ft_text for tok in ['U(1)','U1','charge','prepotential','nu','gauge field A']),
 'Dperp_shared_shift_definition_not_source_locked': 'D_perp Phi' in ft.get('action_class','') and not any(tok in ft_text for tok in ['invariant shift','tilde N','prepotential','nu']),
 'cross_symmetry_commutator_not_source_locked': True,
 'same_action_scalar_lapse_shift_interface_not_source_locked': z4.get('s6ft_embedding_ready') is False,
}
base_ok=all(checks.values())
under=base_ok and all(missing.values())
cls='C10_65S6FZ5_SYMMETRY_INTERFACE_UNDERDETERMINED_PASS_SCOPED' if under else 'C10_65S6FZ5_FAIL_SCOPED'
r={
 'schema':'RTK_C10_65S6FZ5_SYMMETRY_INTERFACE_CLOSURE_AUDIT_RESULT_v1','gate':'C10.65s6fZ5','classification':cls,
 'checks':checks,'missing_interface_data':missing,
 'finding':'The two parent sectors share projectability, and the s6fZ2 null redundancy is explicit, but the newly introduced fields phi,chi have no source-locked representation under the gravitational parent gauge symmetry and D_perp Phi is not tied to the same invariant lapse/shift variables. Therefore the cross-symmetry algebra and same-action lapse/shift source cannot yet be derived rather than chosen.',
 'what_is_not_claimed':'This is not a conflict between the symmetries and not a no-go. It is an identifiability/interface blocker: neutrality, charge assignments or an invariant-shift coupling must not be invented after the soft-s result.',
 's6ft_embedding_ready':False,'soft_s_retest_allowed':False,'production_k003_unblocked':False,
 'next_gate':'C10.65s6fZ6: source-lock audit for a pre-soft-s representation of the new scalar carrier under the projectable gravitational gauge symmetry. If none exists, freeze a symmetry-first representation theorem/class before writing any combined action.',
 'threshold_changed':False,
 'provenance':{'workflow':'rtk-c10-65s6fz5-symmetry-interface-closure-audit.yml','frozen_target_commit':'953d37a2c7a28b9530e738368282eeea8382b2ff','threshold_changed':False}
}
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); print(json.dumps(r,indent=2,sort_keys=True)); sys.exit(0 if under else 2)
