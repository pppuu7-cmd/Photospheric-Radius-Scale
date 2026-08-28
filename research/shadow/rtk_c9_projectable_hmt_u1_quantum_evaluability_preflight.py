#!/usr/bin/env python3
import json
from pathlib import Path

TARGET = Path('research/theory_targets/RTK_C9_PROJECTABLE_HMT_U1_QUANTUM_EVALUABILITY_PREFLIGHT_TARGET_v1.json')
PARENT = Path('research/theory_results/RTK_C9_PROJECTABLE_HMT_U1_RG_TRANSFER_AUDIT_RESULT_v1.json')
RESULT = Path('research/theory_results/RTK_C9_PROJECTABLE_HMT_U1_QUANTUM_EVALUABILITY_PREFLIGHT_RESULT_v1.json')
CHECKPOINT = Path('research/checkpoints/RTK_C9_PROJECTABLE_HMT_U1_QUANTUM_EVALUABILITY_PREFLIGHT_2026-08-28.md')

t = json.loads(TARGET.read_text())
p = json.loads(PARENT.read_text())

checks = {
    'target_schema_exact': t.get('schema') == 'RTK_C9_PROJECTABLE_HMT_U1_QUANTUM_EVALUABILITY_PREFLIGHT_TARGET_v1',
    'parent_rg_transfer_classification_exact': p.get('classification') == 'RTK_C9_PROJECTABLE_HMT_U1_RG_TRANSFER_NOT_SOURCE_LOCKED_PARTIAL_PASS_SCOPED',
    'ordinary_projectable_parent_rg_control_retained': p.get('decision', {}).get('ordinary_projectable_parent_RG_control_survives') is True,
    'hmt_classical_constraint_structure_retained': p.get('source_locked_distinction', {}).get('HMT_local_U1_extension', {}).get('classical_constraint_structure_source_locked') is True,
    'explicit_hmt_quantum_gauge_fixing_not_source_locked': t['frozen_checks']['explicit_HMT_U1_quantum_gauge_fixing_source_locked'] is False,
    'explicit_hmt_ghost_brst_not_source_locked': t['frozen_checks']['explicit_HMT_U1_ghost_or_BRST_operator_source_locked'] is False,
    'unique_one_loop_determinant_not_defined': t['frozen_checks']['unique_HMT_U1_one_loop_Hessian_determinant_defined_from_current_inputs'] is False,
    'no_parent_beta_import': t['frozen_checks']['do_not_import_parent_beta_functions'] is True,
    'full_c9_not_claimed': t['frozen_checks']['do_not_claim_full_C9_closed'] is True,
    'soft_s_blocked': t['frozen_checks']['do_not_unblock_soft_s'] is True,
    'k003_blocked': t['frozen_checks']['do_not_unblock_k003_production'] is True,
    'threshold_unchanged': t['frozen_checks']['threshold_changed'] is False,
}

status = 'PASS_SCOPED' if all(checks.values()) else 'FAIL_SCOPED'
classification = t['pass_classification'] if status == 'PASS_SCOPED' else t['failure_classification']

result = {
    'schema': 'RTK_C9_PROJECTABLE_HMT_U1_QUANTUM_EVALUABILITY_PREFLIGHT_RESULT_v1',
    'status': status,
    'classification': classification,
    'checks': checks,
    'decision': {
        'ordinary_projectable_parent_RG_control_survives': True,
        'HMT_U1_classical_constraint_structure_source_locked': True,
        'HMT_U1_unique_gauge_fixed_one_loop_problem_source_locked': False,
        'full_C9_closed': False,
        'soft_s_retest_allowed': False,
        'production_k003_unblocked': False,
        'reason': 'The current source lock specifies the classical projectable HMT U(1) constrained field content, but not an HMT-specific quantum gauge-fixing plus ghost/BRST (or equivalent reduced-measure) prescription. Therefore a unique one-loop determinant is not yet defined and parent beta functions cannot be imported.'
    },
    'missing_quantum_inputs': [
        'explicit HMT-specific gauge-fixing functional for FDiff x local-U(1)',
        'corresponding FP/BRST ghost operator or equivalent reduced functional measure',
        'constraint treatment sufficient to define the one-loop determinant on a chosen background'
    ],
    'threshold_changed': False,
    'next_gate': 'C9 projectable HMT U1 quantum-specification source-lock: find or independently preregister one complete gauge-fixing/BRST/ghost prescription for a fixed projectable HMT gravitational action before constructing any HMT beta functions; keep the unresolved matter interface separate.'
}

RESULT.parent.mkdir(parents=True, exist_ok=True)
RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')

checkpoint = f'''# RTK C9 projectable HMT U(1) quantum-evaluability preflight — 2026-08-28\n\n## Classification\n\n`{classification}`\n\n## Frozen conclusion\n\nThe ordinary projectable gravity parent retains scoped quantitative RG control, and the classical HMT U(1) extension retains its source-locked A/nu constrained field content. However, the current RTK source lock does **not** contain an HMT-specific quantum gauge-fixing plus ghost/BRST (or equivalent reduced-measure) prescription. A unique one-loop functional determinant for the HMT gravitational sector is therefore not yet defined from the frozen inputs.\n\nThis is an **evaluability/source-lock blocker**, not evidence that projectable HMT U(1) gravity is nonrenormalizable. Parent beta functions are not transferred.\n\n## Still open / blocked\n\n- Full C9 radiative naturalness: OPEN.\n- HMT physical-matter-interface beta functions: BLOCKED by the independently unresolved matter interface.\n- soft-s retest: BLOCKED.\n- k=0.03 Mpc^-1 production: BLOCKED.\n\n## Next gate\n\nSource-lock or independently preregister one complete HMT-specific gauge-fixing/BRST/ghost prescription for a fixed projectable HMT gravitational action, sufficient to define the one-loop Hessian/determinant. Do not select it from desired RTK beta functions or soft-s behavior.\n'''
CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
CHECKPOINT.write_text(checkpoint)

if status != 'PASS_SCOPED':
    raise SystemExit('Frozen preflight failed: ' + ', '.join(k for k,v in checks.items() if not v))

print(json.dumps(result, indent=2, sort_keys=True))
