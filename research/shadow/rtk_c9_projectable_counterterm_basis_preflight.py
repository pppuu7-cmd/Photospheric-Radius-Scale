#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
target_path = ROOT / 'research/theory_targets/RTK_C9_PROJECTABLE_COUNTERTERM_BASIS_PREFLIGHT_TARGET_v1.json'
parent_path = ROOT / 'research/theory_results/RTK_C9_PROJECTABLE_STRUCTURAL_PROTECTION_RESULT_v1.json'
out_path = ROOT / 'research/theory_results/RTK_C9_PROJECTABLE_COUNTERTERM_BASIS_PREFLIGHT_RESULT_v1.json'

target = json.loads(target_path.read_text())
parent = json.loads(parent_path.read_text())
assert target['status'] == 'FROZEN_BEFORE_COUNTERTERM_BASIS_PREFLIGHT'
assert parent['classification'] == 'RTK_C9_PROJECTABILITY_STRUCTURALLY_ELIMINATES_SIGMA12_OPERATOR_PAIR_PASS_SCOPED'
assert parent['exact_identities']['a_i_projectable'] == '0'

k, a, dphi = sp.symbols('k a dphi', positive=True, nonzero=True)
c2, c4 = sp.symbols('c2 c4')
# Exact finite-Fourier-mode representatives of the quadratic carrier directions.
O2 = sp.simplify(k**2 * dphi**2 / a**2)
O4 = sp.simplify(k**4 * dphi**2 / a**4)
combined = sp.expand(c2*O2 + c4*O4)

checks = {
    'parent_projectability_result_locked': True,
    'acceleration_operator_not_reintroduced': parent['exact_identities']['a_i_projectable'] == '0',
    'carrier_spatial_gradient_survives_projectability': O2 != 0,
    'O2_finite_k_nonzero': sp.simplify(O2) != 0,
    'O4_finite_k_nonzero': sp.simplify(O4) != 0,
    'O2_coefficient_survives': c2 in combined.free_symbols,
    'O4_coefficient_survives': c4 in combined.free_symbols,
    'independent_k_scalings': sp.simplify(O4/O2 - k**2/a**2) == 0,
    'no_loop_generation_claim': True,
    'no_observable_fitting': True,
    'threshold_unchanged': target.get('threshold_changed') is False,
}
passed = all(checks.values())
classification = ('RTK_C9_PROJECTABLE_SYMMETRY_ALLOWS_NONVANISHING_FINITE_K_COUNTERTERM_DIRECTIONS_PASS_SCOPED'
                  if passed else 'RTK_C9_PROJECTABLE_COUNTERTERM_BASIS_PREFLIGHT_FAIL_SCOPED')
result = {
    'schema': 'RTK_C9_PROJECTABLE_COUNTERTERM_BASIS_PREFLIGHT_RESULT_v1',
    'target': str(target_path.relative_to(ROOT)),
    'classification': classification,
    'status': 'PASS_SCOPED' if passed else 'FAIL_SCOPED',
    'finite_k_witness': {
        'O2': str(O2),
        'O4': str(O4),
        'combined': str(combined),
        'O4_over_O2': str(sp.simplify(O4/O2)),
    },
    'checks': checks,
    'scientific_consequence': ('Exact projectability structurally removes the old acceleration pair but does not by itself eliminate invariant finite-k carrier-gradient counterterm directions. Therefore projectability alone is not a full C9 radiative-naturalness theorem.' if passed else 'Frozen counterterm-basis criterion was not met.'),
    'scope_boundary': {
        'actual_loop_generation_proven': False,
        'beta_functions_computed': False,
        'full_C9_closed': False,
        'projectable_candidate_invalidated': False,
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
