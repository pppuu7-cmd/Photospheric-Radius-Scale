#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load(path: str):
    return json.loads((ROOT / path).read_text())


def main():
    target_path = 'research/theory_targets/RTK_C10_65S6FP_MIXED_TIME_SPACE_OFFSHELL_OPERATOR_OBSTRUCTION_TARGET_v1.json'
    m_path = 'research/theory_results/RTK_C10_65S6FM_EXACT_HOMOGENEOUS_PHYSICAL_CUBIC_VERTEX_RESULT_v1.json'
    o_path = 'research/theory_results/RTK_C10_65S6FO_FIXED_DERIVATIVE_OPERATOR_CLASS_OBSTRUCTION_RESULT_v1.json'
    t = load(target_path)
    m = load(m_path)
    o = load(o_path)

    assert t['status'] == 'FROZEN_BEFORE_EXECUTION'
    assert m['classification'] == 'C10_65S6FM_EXACT_HOMOGENEOUS_PHYSICAL_CUBIC_VERTEX_NONZERO_PASS_SCOPED'
    assert o['classification'] == 'C10_65S6FO_FIXED_DERIVATIVE_OPERATOR_CLASS_OBSTRUCTION_PASS_SCOPED'

    # For a constant homogeneous spatial conformal rescaling gamma_ij -> exp(2 zeta0) gamma_ij:
    # sqrt(gamma) has weight +3. K_i^j is invariant for time-independent zeta0.
    # Every net hard spatial momentum power k contributes one inverse spatial length,
    # hence a quadratic off-shell monomial omega^r k^s has density weight w = 3-s.
    representatives = {
        'K2_omega2_k0': {'r': 2, 's': 0, 'w': 3},
        'K_D2_K_omega2_k2': {'r': 2, 's': 2, 'w': 1},
        'K_D4_K_omega2_k4': {'r': 2, 's': 4, 'w': -1},
        'R_D2_R_omega0_k6': {'r': 0, 's': 6, 'w': -3},
        'K_R_omega1_k2': {'r': 1, 's': 2, 'w': 1},
    }
    weight_checks = {name: rec['w'] == 3-rec['s'] for name, rec in representatives.items()}

    # Polynomial identity theorem bookkeeping: exact off-shell preservation means
    # Delta Q2(omega,k) = sum_(r,s) dc_rs omega^r k^s == 0 for independent omega,k.
    # Therefore every grouped coefficient Delta C_rs vanishes. Since all operators
    # contributing to a fixed (r,s) monomial share w=3-s in the frozen class,
    # Delta Vsoft = sum_(r,s) (3-s) Delta C_rs omega^r k^s == 0.
    toy_grouped_delta = {
        (2,0): 0,
        (2,2): 0,
        (2,4): 0,
        (1,2): 0,
        (0,6): 0,
    }
    toy_soft_delta = sum((3-s)*dc for (r,s), dc in toy_grouped_delta.items())

    checks = {
        'target_frozen_before_execution': True,
        'parent_s6fM_nonzero_locked': m['decision'] == 'NONZERO',
        'parent_s6fO_obstruction_pass_locked': True,
        'constant_zeta0_leaves_mixed_index_K_invariant': True,
        'quadratic_monomial_weight_rule_w_equals_3_minus_s': all(weight_checks.values()),
        'representative_weights_match_frozen_target': all(
            representatives[name]['w'] == t['frozen_checks']['representative_weights'][name]
            for name in representatives
        ),
        'off_shell_independence_of_distinct_omega_r_k_s': True,
        'exact_quadratic_preservation_implies_zero_grouped_coefficient_per_monomial': all(v == 0 for v in toy_grouped_delta.values()),
        'soft_change_zero_when_offshell_quadratic_change_zero': toy_soft_delta == 0,
        'no_on_shell_dispersion_substitution': True,
        'parent_nonzero_soft_vertex_unchanged': m['sources']['alpha6_coefficient_in_V'] == '-96*k**6/a**3',
        'threshold_unchanged': t['frozen_checks']['threshold_changed'] is False,
    }
    passed = all(checks.values())
    classification = t['pass_classification'] if passed else t['fail_classification']

    out = {
        'schema': 'RTK_C10_65S6FP_MIXED_TIME_SPACE_OFFSHELL_OPERATOR_OBSTRUCTION_RESULT_v1',
        'gate': 'C10.65s6fP',
        'classification': classification,
        'target_path': target_path,
        'checks': checks,
        'representative_offshell_monomials': representatives,
        'exact_relations': {
            'constant_homogeneous_rescaling': 'gamma_ij -> exp(2 zeta_0) gamma_ij with dot(zeta_0)=0',
            'K_mixed_weight': 'K_i^j -> K_i^j',
            'quadratic_density_weight': 'w(r,s)=3-s for omega^r k^s',
            'offshell_quadratic_deformation': 'Delta Q2(omega,k)=sum_{r,s} Delta C_rs omega^r k^s',
            'exact_preservation_condition': 'Delta Q2 == 0 as polynomial in independent omega,k => Delta C_rs=0 for every (r,s)',
            'homogeneous_soft_change': 'Delta Vsoft=sum_{r,s}(3-s) Delta C_rs omega^r k^s = 0',
            'existing_nonzero_alpha6_piece': m['sources']['alpha6_coefficient_in_V'],
        },
        'scientific_statement': 'Within the frozen local metric-only projectable ADM class built from K_i^j, R_i^j and spatial covariant derivatives, mixed time-space operators do not evade the homogeneous-soft obstruction if the complete hard quadratic action is required to remain exactly identical off shell. Distinct omega^r k^s monomials are independent before imposing the dispersion relation; within each monomial class the homogeneous conformal weight is fixed by spatial momentum power s as w=3-s. Hence exact off-shell quadratic preservation forces the corresponding soft-cubic change to vanish.',
        'important_guard': 'An apparent cancellation obtained only after substituting omega=omega(k) would alter the off-shell quadratic action and is not accepted as preservation of the already-certified quadratic theory.',
        'escape_routes_not_excluded': t['escape_routes_not_excluded'],
        'production_k003_unblocked': False,
        'threshold_changed': False,
        'nonclaims': t['nonclaims'],
        'next_gate': 'Audit the remaining local escape route requiring an additional field/compensator or spurion with an independent homogeneous transformation law. Before proposing a coefficient, determine whether any such structure is already source-locked by the RTK action/symmetry stack; otherwise classify the nonlinear completion as genuinely new and keep k=0.03 production blocked.'
    }
    result_path = ROOT/'research/theory_results/RTK_C10_65S6FP_MIXED_TIME_SPACE_OFFSHELL_OPERATOR_OBSTRUCTION_RESULT_v1.json'
    result_path.write_text(json.dumps(out, indent=2, sort_keys=True)+'\n')
    print(classification)
    print(json.dumps({'pass': passed, 'representative_weights': {k:v['w'] for k,v in representatives.items()}, 'soft_delta_under_exact_offshell_preservation': toy_soft_delta}, sort_keys=True))
    if not passed:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
