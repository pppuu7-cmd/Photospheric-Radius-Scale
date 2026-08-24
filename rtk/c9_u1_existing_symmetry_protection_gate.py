#!/usr/bin/env python3
"""Scoped C9 gate: can the symmetries already declared by the fixed action protect sigma1=sigma2=0?

This is not a loop calculation. It combines the frozen action dictionary with
the published Hamiltonian theorem that the two exceptional operators are
allowed marginal invariants of the same nonprojectable U(1) symmetry.
"""
import json

T='research/theory_targets/RTK_C9_U1_EXISTING_SYMMETRY_PROTECTION_TARGET_v1.json'
t=json.load(open(T))
assert t['classification']=='RTK_C9_U1_EXISTING_SYMMETRY_PROTECTION_TARGET_V1_FROZEN'

ir=json.load(open('research/RTK_C8_U1_FIXED_IR_REPRESENTATIVE_v3.json'))
sc=json.load(open('research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json'))
g=ir['gravity_and_matter_frame']
assert g['sigma1']==0 and g['sigma2']==0
assert ir['uv_status']['radiative_protection_of_sigma1_sigma2_zero']=='open'
assert sc['dbi_px']['shift_symmetry'] is True

ext=t['external_theorem']
statements=' '.join(ext['statements'])
assert 'marginal' in statements
assert 'allowed by the same' in statements
assert 'quantum corrections' in statements

# The scalar's internal shift symmetry Sigma -> Sigma + const does not act on
# the pure-gravity U(1)-invariant operators a_i a^i sigma or D_i a^i sigma.
# Since the published most-general gravity action with the already-declared
# U(1) x Diff(M,F) symmetry contains them, none of the symmetries currently
# declared by the fixed action forbids them.

out={
  'classification':'RTK_C9_U1_EXISTING_SYMMETRY_PROTECTION_NEGATIVE_CLOSED',
  'status':'SCOPED_NEGATIVE_CLOSURE_EXISTING_SYMMETRY_DOES_NOT_PROTECT_EXCEPTIONAL_SURFACE',
  'target':T,
  'fixed_surface':{'sigma1':0,'sigma2':0},
  'external_source':'Mukohyama-Namba-Saitou-Watanabe arXiv:1504.07357v2',
  'operator_dictionary':{
    'eta1/sigma1':'a_i a^i sigma',
    'eta2/sigma2':'D_i a^i sigma'
  },
  'verified_logic':[
    'Fully nonlinear classical removal of the unwanted gravity scalar requires both exceptional couplings to vanish exactly in the cited Hamiltonian theorem.',
    'Both operators are marginal and are members of the most-general nonprojectable gravity action respecting the same local U(1) and foliation-preserving diffeomorphism symmetry.',
    'The additional RTK internal Sigma shift symmetry does not transform these pure-gravity operators and therefore cannot forbid them.',
    'Therefore the symmetry content already declared in the frozen action does not protect sigma1=sigma2=0.'
  ],
  'scientific_consequence':'C9 cannot be closed by appealing to the presently declared U(1) x Diff(M,F) plus Sigma-shift symmetries. A new protection mechanism or a quantitative counterterm/tuning analysis is mandatory.',
  'allowed_next_mechanisms':[
    'additional exact symmetry/Ward identity',
    'counterterm-stable structural degeneracy',
    'explicit RG fixed surface with both beta functions zero',
    'quantitative induced-coupling tolerance below a demonstrated physical EFT cutoff'
  ],
  'non_claims':t['non_claims'],
  'next_gate':t['next_gate_if_negative_closed']
}
open('c9_u1_existing_symmetry_protection_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
