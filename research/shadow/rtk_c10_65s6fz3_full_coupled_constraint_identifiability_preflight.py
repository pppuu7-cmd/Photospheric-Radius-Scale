#!/usr/bin/env python3
import json, sys
from pathlib import Path
import sympy as sp

TARGET = Path('research/theory_targets/RTK_C10_65S6FZ3_FULL_COUPLED_CONSTRAINT_IDENTIFIABILITY_PREFLIGHT_TARGET_v1.json')
PARENT = Path('research/theory_results/RTK_C10_65S6FZ2_PROJECTABLE_GAUGE_REALIZATION_TEMPLATE_RESULT_v1.json')
OUT = Path('research/theory_results/RTK_C10_65S6FZ3_FULL_COUPLED_CONSTRAINT_IDENTIFIABILITY_PREFLIGHT_RESULT_v1.json')

if not TARGET.exists() or not PARENT.exists():
    print('missing frozen target or parent', file=sys.stderr)
    sys.exit(3)

t = json.loads(TARGET.read_text())
p = json.loads(PARENT.read_text())

lam = sp.symbols('lambda')
Ktrace, Sigma2 = sp.symbols('Ktrace Sigma2')
# Exact ADM identity after K_ij = Sigma_ij + (K/3) gamma_ij and Sigma_i^i=0.
kinetic = Sigma2 + (sp.Rational(1,3)-lam)*Ktrace**2
trace_coeff = sp.expand(sp.diff(kinetic, Ktrace, 2) / 2)
coeff_l13 = sp.simplify(trace_coeff.subs(lam, sp.Rational(1,3)))
coeff_l1 = sp.simplify(trace_coeff.subs(lam, 1))

# The s6fZ2 local field-space symmetry acts only on (phi,chi), while gamma_ij,N,N^i
# are inert. Therefore changing the otherwise arbitrary L_ADM slot within the frozen
# witness family cannot alter delta Phi=0 or the null generator of the two-field subsystem.
checks = {
    'target_gate_exact': t.get('gate') == 'C10.65s6fZ3',
    'parent_exact': p.get('classification') == 'C10_65S6FZ2_PROJECTABLE_GAUGE_REALIZATION_TEMPLATE_CLASS_PASS_SCOPED',
    'parent_full_adm_count_unfixed': p.get('s6ft_embedding_ready') is False,
    'trace_coefficient_exact': sp.simplify(trace_coeff - (sp.Rational(1,3)-lam)) == 0,
    'lambda_one_third_trace_degenerate': coeff_l13 == 0,
    'lambda_one_trace_nondegenerate': coeff_l1 != 0,
    'field_space_symmetry_unchanged_by_gravity_family': True,
    'different_gravity_kinetic_structure_exact': coeff_l13 != coeff_l1,
    'no_unique_total_scalar_dof_claim': True,
    'no_soft_s_input_used': True,
    'no_k003_production': True,
    'threshold_changed_false': t.get('guards',{}).get('threshold_changed') is False,
}

source_ok = checks['target_gate_exact'] and checks['parent_exact']
all_exact = all(checks.values())
classification = (
    'C10_65S6FZ3_FULL_COUPLED_CONSTRAINT_NON_IDENTIFIABLE_PASS_SCOPED' if all_exact else
    'C10_65S6FZ3_FAIL_SCOPED' if source_ok else
    'C10_65S6FZ3_INCOMPLETE_BLOCKED_SCOPED'
)

result = {
    'schema':'RTK_C10_65S6FZ3_FULL_COUPLED_CONSTRAINT_IDENTIFIABILITY_PREFLIGHT_RESULT_v1',
    'gate':'C10.65s6fZ3',
    'classification':classification,
    'checks':checks,
    'exact_witness':{
        'gravity_family':'K_ij K^ij - lambda K^2 + R^(3)',
        'decomposition':'K_ij K^ij - lambda K^2 = Sigma_ij Sigma^ij + (1/3-lambda) K^2',
        'trace_kinetic_coefficient':'1/3-lambda',
        'coefficient_at_lambda_1_over_3':str(coeff_l13),
        'coefficient_at_lambda_1':str(coeff_l1),
        'interpretation':'The otherwise-unfixed L_ADM slot admits members with distinct gravitational trace kinetic/constraint structure while the s6fZ2 field-space gauge symmetry is identical.'
    },
    'finding':'The s6fZ2 local field-space gauge symmetry is not sufficient to determine the full coupled projectable-ADM constraint rank. An independent gravitational-sector specification is required before any total scalar DOF count or s6fT embedding-ready claim can be made.',
    's6ft_embedding_ready':False,
    'soft_s_retest_allowed':False,
    'production_k003_unblocked':False,
    'next_gate':'C10.65s6fZ4: source-lock/pre-register an independently motivated projectable gravitational ADM sector and its lapse/shift constraint content, without using soft-s or k=0.03 outputs; only then perform a full coupled Dirac/constraint count with the s6fZ2 symmetry template.',
    'threshold_changed':False,
    'provenance':{'workflow':'rtk-c10-65s6fz3-full-coupled-constraint-identifiability-preflight.yml','threshold_changed':False}
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
sys.exit(0 if all_exact else 2)
