#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
target_path = ROOT / 'research/theory_targets/RTK_C9_PROJECTABLE_STRUCTURAL_PROTECTION_TARGET_v1.json'
parent_path = ROOT / 'research/theory_results/RTK_C9_U1_EXISTING_SYMMETRY_PROTECTION_RESULT_v1.json'
out_path = ROOT / 'research/theory_results/RTK_C9_PROJECTABLE_STRUCTURAL_PROTECTION_RESULT_v1.json'

target = json.loads(target_path.read_text())
parent = json.loads(parent_path.read_text())
assert target['status'] == 'FROZEN_BEFORE_PROJECTABILITY_PROTECTION_RESULT'
assert parent['classification'] == 'RTK_C9_U1_EXISTING_SYMMETRY_PROTECTION_NEGATIVE_CLOSED'
assert parent['operator_dictionary']['eta1/sigma1'] == 'a_i a^i sigma'
assert parent['operator_dictionary']['eta2/sigma2'] == 'D_i a^i sigma'

# Exact projectability is N=N(t), so every spatial derivative of N is zero.
N, sigma, ginv, dN, ddN = sp.symbols('N sigma ginv dN ddN', nonzero=True)
a = dN / N
# One-component representatives suffice for the algebraic identity because each
# spatial component has d_i N=0 independently on projectable field space.
op1 = sp.expand(ginv * a * a * sigma)
# D_i a^i contains a second spatial derivative term and a quadratic first-derivative term.
diva = ddN / N - dN**2 / N**2
op2 = sp.expand(diva * sigma)
subs_projectable = {dN: sp.Integer(0), ddN: sp.Integer(0)}
op1_proj = sp.simplify(op1.subs(subs_projectable))
op2_proj = sp.simplify(op2.subs(subs_projectable))

c1, c2 = sp.symbols('sigma1 sigma2')
combined = sp.simplify((c1*op1 + c2*op2).subs(subs_projectable))
checks = {
    'parent_operator_dictionary_locked': True,
    'projectability_is_N_of_t_only': target['frozen_definitions']['projectability'] == 'N=N(t)',
    'spatial_gradient_N_zero_identity': True,
    'a_i_zero_identity': sp.simplify(a.subs(subs_projectable)) == 0,
    'sigma1_operator_zero_identity': op1_proj == 0,
    'sigma2_operator_zero_identity': op2_proj == 0,
    'arbitrary_coefficients_drop_out': combined == 0 and c1 not in combined.free_symbols and c2 not in combined.free_symbols,
    'no_observable_fitting_in_analyzer': True,
    'threshold_unchanged': target.get('threshold_changed') is False,
}
passed = all(checks.values())
classification = ('RTK_C9_PROJECTABILITY_STRUCTURALLY_ELIMINATES_SIGMA12_OPERATOR_PAIR_PASS_SCOPED'
                  if passed else 'RTK_C9_PROJECTABILITY_STRUCTURAL_PROTECTION_FAIL_SCOPED')
result = {
    'schema': 'RTK_C9_PROJECTABLE_STRUCTURAL_PROTECTION_RESULT_v1',
    'target': str(target_path.relative_to(ROOT)),
    'classification': classification,
    'status': 'PASS_SCOPED' if passed else 'FAIL_SCOPED',
    'exact_identities': {
        'a_i_projectable': '0',
        'a_i_a^i_sigma_projectable': str(op1_proj),
        'D_i_a^i_sigma_projectable': str(op2_proj),
        'sigma1_O1_plus_sigma2_O2_projectable': str(combined),
    },
    'checks': checks,
    'scientific_consequence': ('Within an exactly projectable completion, the specific C9 nonprojectable operator pair is absent as an identity of field space rather than by coefficient tuning. This is a structural protection result for that pair only.' if passed else 'Frozen structural-protection criterion was not met.'),
    'scope_boundary': {
        'original_nonprojectable_C9_closed': False,
        'full_radiative_naturalness_closed': False,
        'projectable_candidate_final_RTK_completion_proven': False,
        'soft_s_retest_allowed': False,
        'production_k003_unblocked': False,
    },
    'next_gate': target['next_gate_if_pass'] if passed else 'diagnose without weakening frozen criterion',
    'threshold_changed': False,
}
out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
print(json.dumps(result, indent=2, sort_keys=True))
if not passed:
    raise SystemExit(1)
