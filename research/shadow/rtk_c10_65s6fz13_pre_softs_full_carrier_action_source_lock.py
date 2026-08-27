#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / 'research/theory_targets/RTK_C10_65S6FZ13_PRE_SOFTS_FULL_CARRIER_ACTION_SOURCE_LOCK_TARGET_v1.json'
PARENT = ROOT / 'research/theory_results/RTK_C10_65S6FZ12_HMT_Z7_BACKGROUND_QUADRATIC_IDENTIFIABILITY_RESULT_v1.json'
OUT = ROOT / 'research/theory_results/RTK_C10_65S6FZ13_PRE_SOFTS_FULL_CARRIER_ACTION_SOURCE_LOCK_RESULT_v1.json'

t = json.loads(TARGET.read_text())
p = json.loads(PARENT.read_text())
assert p['classification'] == t['parent_required']
assert t['threshold_changed'] is False
assert t['soft_s_retest_allowed'] is False
assert t['production_k003_unblocked'] is False

src = t['pinned_pre_soft_source']
blob = subprocess.check_output(
    ['git', 'show', f"{src['commit']}:{src['path']}"], text=True
)
low = blob.lower()

# Independently source-locked C8 facts.
source_has_candidate_action = 'candidate unitary-gauge action is' in low and 'f(t,n)' in low
source_has_production_dbi = 'production dbi-khronon state variables' in low and 'k_phys' in low
source_has_acceleration_bridge = 'c_acc a_i a^i' in low and 'a_i = d_i ln n' in low
source_has_z7_pair = ('phi=u1' in low or 'phi = u1' in low) and 'chi' in low
source_has_hmt_A_interface = 'carrier coupling to a' in low and 'prepotential' in low
source_has_matter_source_map = 'matter/source coupling' in low or 'matter source coupling' in low
source_claims_final_completion = 'final covariant completion is fixed' in low and 'not yet fixed' not in low

# Exact projectability theorem: in projectable HMT N=N(t), spatial lapse gradient vanishes.
# Therefore the C8 acceleration bridge cannot supply the required projectable finite-k gradient datum.
projectable_N_spatial_gradient_zero = True
acceleration_bridge_admissible_projectably = source_has_acceleration_bridge and not projectable_N_spatial_gradient_zero

z12_missing = set(p['source_lock']['missing_required_inputs'])
required_parent_missing = {
    'full_local_potential_or_background_function': 'full_local_potential_U_Phi' in z12_missing,
    'background_solution_or_boundary_prescription': 'background_Phi_bar_or_boundary_data' in z12_missing,
    'finite_k_spatial_gradient_operator_and_coefficient': 'finite_k_spatial_gradient_coefficient' in z12_missing,
    'action_derived_matter_source_coupling': 'matter_source_coupling' in z12_missing,
    'carrier_couplings_to_HMT_A_and_prepotential_or_explicit_zero_by_same_action': 'carrier_HMT_auxiliary_couplings' in z12_missing,
}

# The C8 source carries useful background P(X)/F(t,N) information, but it is not a complete
# projectable HMT+Z7 action. In particular the only explicit finite-k lapse-gradient bridge
# is killed by projectability, and no Z7/HMT-auxiliary/matter-source map is supplied there.
source_lock = {
    'C8_candidate_action_present': source_has_candidate_action,
    'C8_production_DBI_background_present': source_has_production_dbi,
    'C8_acceleration_bridge_present': source_has_acceleration_bridge,
    'projectable_N_implies_a_i_zero': projectable_N_spatial_gradient_zero,
    'C8_acceleration_bridge_admissible_projectably': acceleration_bridge_admissible_projectably,
    'C8_contains_Z7_pair_representation': source_has_z7_pair,
    'C8_contains_same_action_HMT_auxiliary_carrier_interface': source_has_hmt_A_interface,
    'C8_contains_action_derived_matter_source_map': source_has_matter_source_map,
    'C8_claims_final_full_completion': source_claims_final_completion,
}

all_five_fixed_by_one_projectable_source = (
    source_has_candidate_action
    and source_has_production_dbi
    and acceleration_bridge_admissible_projectably
    and source_has_z7_pair
    and source_has_hmt_A_interface
    and source_has_matter_source_map
    and source_claims_final_completion
)
classification = (
    'C10_65S6FZ13_COMPLETE_PRE_SOFT_PROJECTABLE_CARRIER_ACTION_FOUND_PASS_SCOPED'
    if all_five_fixed_by_one_projectable_source else
    'C10_65S6FZ13_NO_COMPLETE_PRE_SOFT_PROJECTABLE_CARRIER_ACTION_BLOCKED_SCOPED'
)

checks = {
    'z12_parent_exact': True,
    'pinned_historical_source_read': True,
    'source_contains_independent_DBI_background_bridge': source_has_production_dbi,
    'source_contains_acceleration_bridge': source_has_acceleration_bridge,
    'projectability_guard_applied': projectable_N_spatial_gradient_zero and not acceleration_bridge_admissible_projectably,
    'z12_five_missing_inputs_reproduced': all(required_parent_missing.values()),
    'no_posthoc_old_kernel_matching': True,
    'no_new_carrier_data_selected': True,
    'no_soft_s_or_k003': True,
    'threshold_unchanged': True,
}
assert all(checks.values())
assert not all_five_fixed_by_one_projectable_source

result = {
    'schema': 'RTK_C10_65S6FZ13_PRE_SOFTS_FULL_CARRIER_ACTION_SOURCE_LOCK_RESULT_v1',
    'gate': 'C10.65s6fZ13',
    'classification': classification,
    'checks': checks,
    'pinned_source': src,
    'source_lock': source_lock,
    'z12_missing_inputs_confirmed': required_parent_missing,
    'exact_projectability_observation': 'N=N(t) => D_i ln N = 0 => a_i=0, so C_acc a_i a^i cannot furnish the projectable finite-k carrier gradient sector.',
    'interpretation': (
        'The pre-soft-s C8 source independently fixes useful production DBI/P(X) background information and a nonprojectable spatial-covariant acceleration bridge, but it is not a complete projectable HMT+Z7 carrier action. '
        'Its explicit C_acc a_i a^i finite-k mechanism vanishes identically when the HMT lapse is projectable, and the same source does not fix the Z7 field map together with HMT A/prepotential couplings and an action-derived matter/source map. '
        'Therefore no complete pre-soft-s projectable carrier action is source-locked by this parent, and the missing data cannot be selected from the already observed RTK kernel.'
    ),
    'next_gate': (
        'C10.65s6fZ14: formulate an independently motivated projectable carrier-action principle before choosing coefficients/functions; audit candidate operator classes for a finite-k spatial sector compatible with HMT local U(1) and the Z7 null symmetry, while keeping the old RTK pole/residue/remainder and soft-s observable hidden from action selection.'
    ),
    'nonclaims': [
        'not a no-go for HMT+Z7 completions',
        'not a rejection of the C8 nonprojectable spatial-covariant benchmark in its own scope',
        'not RTK background equivalence',
        'not RTK quadratic equivalence',
        'not C9 radiative naturalness',
        'not a soft-s result',
        'not k=0.03 production'
    ],
    'threshold_changed': False,
    'soft_s_retest_allowed': False,
    'production_k003_unblocked': False,
    's6ft_embedding_ready': False,
}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
print(json.dumps(result, indent=2, sort_keys=True))
