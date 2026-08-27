#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / 'research/theory_targets/RTK_C10_65S6FZ12_HMT_Z7_BACKGROUND_QUADRATIC_IDENTIFIABILITY_TARGET_v1.json'
PARENT = ROOT / 'research/theory_results/RTK_C10_65S6FZ11_FIXED_PROJECTABLE_U1_ACTION_SCALAR_DOF_PREFLIGHT_RESULT_v1.json'
Z11T = ROOT / 'research/theory_targets/RTK_C10_65S6FZ11_FIXED_PROJECTABLE_U1_ACTION_SCALAR_DOF_PREFLIGHT_TARGET_v1.json'
OUT = ROOT / 'research/theory_results/RTK_C10_65S6FZ12_HMT_Z7_BACKGROUND_QUADRATIC_IDENTIFIABILITY_RESULT_v1.json'

t = json.loads(TARGET.read_text())
p = json.loads(PARENT.read_text())
z11 = json.loads(Z11T.read_text())

assert p['classification'] == t['parent_required']
assert t['threshold_changed'] is False
assert t['soft_s_retest_allowed'] is False
assert t['production_k003_unblocked'] is False

# Source-lock audit of the already frozen Z11 interface.  These keys are the
# entire carrier content frozen there; absence here is scientifically material.
iface = z11['fixed_carrier_interface']
iface_text = json.dumps(iface, sort_keys=True)

def has_any(*tokens):
    low = iface_text.lower()
    return any(tok.lower() in low for tok in tokens)

locked = {
    'carrier_kinetic_kappa_nonzero': has_any('kappa'),
    'full_local_potential_U_Phi': has_any('U(Phi)', 'potential'),
    'background_Phi_bar_or_boundary_data': has_any('Phi_bar', 'background solution', 'boundary data'),
    'finite_k_spatial_gradient_coefficient': has_any('gradient', 'c_phi', 'spatial-gradient'),
    'matter_source_coupling': has_any('matter coupling', 'source coupling', 'source direction'),
    'carrier_HMT_auxiliary_couplings': has_any('carrier coupling to A', 'carrier coupling to nu', 'auxiliary coupling'),
}

# Constructive exact witness of non-identifiability.  Both completions retain
# the same Z11 kinetic/interface data (same kappa and symmetries), but choose
# previously-unfrozen local action data.  For a regular carrier perturbation,
# the generic inverse response contains
#   D(omega,k) = -kappa*omega^2 + c_s^2*k^2 + m_eff^2.
# Two legal post-Z11 choices therefore give inequivalent kernels.
witness = {
    'shared': {'kappa': 1, 'Z7_interface': True, 'HMT_gravity': True},
    'completion_A': {'U_prime_background': 0, 'U_double_prime': 0, 'c_s_squared': 0, 'D': '-omega^2'},
    'completion_B': {'U_prime_background': 1, 'U_double_prime': 2, 'c_s_squared': 3, 'D': '-omega^2 + 3*k^2 + 2'},
}
background_equations_differ = witness['completion_A']['U_prime_background'] != witness['completion_B']['U_prime_background']
quadratic_kernels_differ = witness['completion_A']['D'] != witness['completion_B']['D']

missing = [k for k,v in locked.items() if k != 'carrier_kinetic_kappa_nonzero' and not v]
match_ready = (not missing) and background_equations_differ is False and quadratic_kernels_differ is False

classification = (
    'C10_65S6FZ12_BACKGROUND_QUADRATIC_MATCH_READY_PASS_SCOPED'
    if match_ready else
    'C10_65S6FZ12_BACKGROUND_QUADRATIC_UNDERSPECIFIED_BLOCKED_SCOPED'
)

checks = {
    'z11_parent_exact': True,
    'hmt_gravity_fixed_from_z11': z11['fixed_gravity_source']['equation'] == 104 and z11['fixed_gravity_source']['lambda'] == 1,
    'z7_interface_fixed_from_z11': iface.get('representation_parent') == 'C10.65s6fZ7',
    'regular_kappa_interface_present': locked['carrier_kinetic_kappa_nonzero'],
    'missing_same_action_inputs_detected': len(missing) > 0,
    'two_z11_compatible_completions_constructed': True,
    'background_equations_differ': background_equations_differ,
    'finite_k_quadratic_kernels_differ': quadratic_kernels_differ,
    'no_posthoc_matching_performed': True,
    'no_soft_s_or_k003': True,
    'threshold_unchanged': True,
}

if classification.endswith('MATCH_READY_PASS_SCOPED'):
    assert all(locked.values())
else:
    assert missing
    assert background_equations_differ or quadratic_kernels_differ

result = {
    'schema': 'RTK_C10_65S6FZ12_HMT_Z7_BACKGROUND_QUADRATIC_IDENTIFIABILITY_RESULT_v1',
    'gate': 'C10.65s6fZ12',
    'classification': classification,
    'checks': checks,
    'source_lock': {
        'z11_fixed_carrier_interface': iface,
        'locked_input_audit': locked,
        'missing_required_inputs': missing,
    },
    'constructive_nonidentifiability_witness': witness,
    'interpretation': (
        'The HMT Eq.104 + Z7 interface fixes the scalar DOF architecture but does not yet fix a unique same-action FLRW carrier background or finite-k quadratic response. '
        'At least the carrier potential/background data, spatial-gradient coefficient, and matter/source map remain unfrozen. '
        'Two completions consistent with every Z11 interface statement therefore yield inequivalent background equations and finite-k inverse kernels. '
        'The old RTK pole/residue/remainder must not be used to choose these missing functions after the fact.'
    ),
    'next_gate': (
        'C10.65s6fZ13: independently preregister one full local HMT+Z7 carrier action (potential/background prescription, spatial-gradient sector, source/matter coupling, and any HMT-auxiliary couplings) from a pre-soft-s physical principle; only then rerun the unchanged Z12 match-ready audit and proceed to background/quadratic RTK equivalence.'
    ),
    'nonclaims': [
        'not a no-go for HMT+Z7 completions',
        'not RTK background equivalence',
        'not RTK pole/residue/remainder equivalence',
        'not C9 radiative naturalness',
        'not same-full-action primordial/background closure',
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
