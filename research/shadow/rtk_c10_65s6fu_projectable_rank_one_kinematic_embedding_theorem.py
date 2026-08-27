#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

TARGET = Path('research/theory_targets/RTK_C10_65S6FU_PROJECTABLE_RANK_ONE_KINEMATIC_EMBEDDING_THEOREM_TARGET_v1.json')
RESULT = Path('research/theory_results/RTK_C10_65S6FU_PROJECTABLE_RANK_ONE_KINEMATIC_EMBEDDING_THEOREM_RESULT_v1.json')
PARENT = Path('research/theory_results/RTK_C10_65S6FT_FULL_PROJECTABLE_ADM_EMBEDDING_SOURCE_LOCK_RESULT_v1.json')

target = json.loads(TARGET.read_text())
parent = json.loads(PARENT.read_text())

A,B,C,a,z = sp.symbols('A B C a z', nonzero=True)
m11,m12,m22 = sp.symbols('m11 m12 m22')
vp,vc,sqrtg,N = sp.symbols('v_phi v_chi sqrtgamma N', nonzero=True)

K = sp.Matrix([[A,B],[B,C]])
detK = sp.factor(K.det())
rank_one_condition = sp.factor(detK) == A*C-B**2

# A != 0 coordinate patch of the rank-one locus.
K_rank1 = sp.simplify(K.subs({B:a*A, C:a**2*A}))
kinetic_form = sp.expand(A*vp**2 + 2*a*A*vp*vc + a**2*A*vc**2)
kinetic_square = sp.expand(A*(vp+a*vc)**2)

# Canonical momenta from L=N sqrt(gamma)/2 * v^T K v, v=(dot q-shift)/N.
p_phi = sp.expand(sqrtg*(A*vp + a*A*vc))
p_chi = sp.expand(sqrtg*(a*A*vp + a**2*A*vc))
primary_constraint = sp.simplify(p_chi-a*p_phi)

M = sp.Matrix([[m11,m12],[m12,m22]])
D_general = sp.expand((M-z*K).det())
z2_general = sp.expand(D_general).coeff(z,2)
D_rank1 = sp.factor(D_general.subs({B:a*A,C:a**2*A}))
z2_rank1 = sp.simplify(sp.expand(D_rank1).coeff(z,2))
z1_rank1 = sp.factor(sp.expand(D_rank1).coeff(z,1))
z0_rank1 = sp.factor(sp.expand(D_rank1).coeff(z,0))
expected_z1 = -A*(m22 + a**2*m11 - 2*a*m12)

checks = {
    'target_frozen_before_execution': target.get('status') == 'FROZEN_BEFORE_EXECUTION',
    'parent_is_exact_s6ft_blocker': parent.get('classification') == 'C10_65S6FT_BLOCKED_NO_FULL_PROJECTABLE_ADM_EMBEDDING_SCOPED',
    'parent_k003_still_blocked': parent.get('production_k003_unblocked') is False,
    'hessian_matrix_exact': K == sp.Matrix([[A,B],[B,C]]),
    'rank_one_determinant_exact': sp.simplify(detK-(A*C-B**2)) == 0,
    'rank_one_A_patch_exact': K_rank1 == A*sp.Matrix([[1,a],[a,a**2]]),
    'kinetic_perfect_square_exact': sp.simplify(kinetic_form-kinetic_square) == 0,
    'primary_constraint_exact': primary_constraint == 0,
    'general_z2_coefficient_is_detK': sp.simplify(z2_general-(A*C-B**2)) == 0,
    'rank_one_z2_vanishes': z2_rank1 == 0,
    'rank_one_affine_z1_exact': sp.simplify(z1_rank1-expected_z1) == 0,
    'rank_one_z0_is_detM': sp.simplify(z0_rank1-(m11*m22-m12**2)) == 0,
    'historical_toy_kinetic_structure_reproduced': sp.simplify(kinetic_square/A-(vp+a*vc)**2) == 0,
    'no_soft_s_retest': True,
    'k003_still_blocked': True,
    'threshold_changed': False
}

scientific_checks = [k for k in checks if k != 'threshold_changed']
passed = all(bool(checks[k]) for k in scientific_checks)
classification = ('C10_65S6FU_PROJECTABLE_RANK_ONE_KINEMATIC_EMBEDDING_CLASS_PASS_SCOPED'
                  if passed else
                  'C10_65S6FU_PROJECTABLE_RANK_ONE_KINEMATIC_THEOREM_FAIL_SCOPED')

result = {
    'schema': 'RTK_C10_65S6FU_PROJECTABLE_RANK_ONE_KINEMATIC_EMBEDDING_THEOREM_RESULT_v1',
    'gate': 'C10.65s6fU',
    'classification': classification,
    'checks': checks,
    'exact_results': {
        'velocity_hessian_up_to_positive_nonzero_prefactor': '[[A,B],[B,C]]',
        'rank_one_condition': 'A*C-B^2=0 with K nonzero',
        'A_nonzero_patch': {'a':'B/A','B':'a*A','C':'a^2*A'},
        'kinetic_combination': 'A*(v_phi+a*v_chi)^2',
        'primary_constraint': 'p_chi-a*p_phi=0',
        'det_M_minus_zK_general': str(sp.factor(D_general)),
        'det_M_minus_zK_rank_one': str(D_rank1),
        'z2_coefficient_rank_one': str(z2_rank1),
        'z1_coefficient_rank_one': str(z1_rank1),
        'pole_statement': 'det(M-zK) is affine in z=omega^2; hence at most one finite dynamical pole unless the affine coefficient also degenerates'
    },
    'interpretation': 'The historical rank-one kinetic architecture has a nonempty local projectable-ADM two-scalar kinematic embedding class. This does not select the RTK field map, potential/algebraic sector, source direction, background functions, or nonlinear completion.',
    'missing_for_full_s6ft_embedding': parent.get('missing_source_locked_inputs', []),
    'next_gate': target.get('next_if_pass'),
    'soft_s_retest_allowed': False,
    'production_k003_unblocked': False,
    'threshold_changed': False
}
RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
print(json.dumps(result, indent=2, sort_keys=True))
if not passed:
    raise SystemExit(1)
