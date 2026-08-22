#!/usr/bin/env python3
"""Exact literature-relation gate for corrected U(1) bare parameters.

This intentionally tests only the algebraic relations displayed in
arXiv:1310.6666 for the U(1) gravity + universal matter frame. It does NOT
claim that the full RTK action, which contains a separate rolling S_mix, has
those PPN values.
"""
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
t=json.loads((ROOT/'research/RTK_C8_U1_FAMILY1_FIXED_IR_SLICE_v2.json').read_text())
assert t['classification']=='RTK_C8_U1_CORRECTED_PARTIAL_IR_SLICE_V2_FROZEN'
p=t['gravity_and_matter_frame']
assert p['a1']==1 and p['a2']==0 and p['kappa']==1
assert p['sigma1']==0 and p['sigma2']==0
assert p['beta0_bare']==0 and p['gamma1']==-1

# Literature Eq. (5.43), on sigma1=sigma2=0.
a1,kappa,gamma1,beta0=sp.symbols('a1 kappa gamma1 beta0', real=True, finite=True)
E=beta0*(a1**2*kappa*gamma1+1)+2*kappa*(a1*gamma1+1)**2
E_v2=sp.simplify(E.subs({a1:p['a1'],kappa:p['kappa'],gamma1:p['gamma1'],beta0:p['beta0_bare']}))
assert E_v2==0

# Family-I displayed condition.
family1=(p['a1']==1 and p['kappa']==1 and p['sigma2']==0)
assert family1

# Family-II displayed relations.
family2_sigma2=4*(1-p['a1'])
family2_beta0=-2*(p['gamma1']+1)
assert p['sigma2']==family2_sigma2==0
assert p['beta0_bare']==family2_beta0==0

out={
  'classification':'RTK_ROUTE_B_U1_CORRECTED_BARE_PPN_FAMILY_INTERSECTION_PASS',
  'corrected_partial_slice':p,
  'eq_5_43_residual':str(E_v2),
  'family_I_bare_relation_pass':family1,
  'family_II_expected_sigma2':family2_sigma2,
  'family_II_expected_beta0_bare':family2_beta0,
  'family_II_bare_relation_pass':True,
  'interpretation':'After separating bare and effective acceleration coefficients, the bare gravity/matter-frame tuple lies on both displayed exact-GR algebraic PPN families of arXiv:1310.6666.',
  'full_action_ppn_status':'OPEN',
  'critical_non_claim':'The published PPN calculation does not include the explicit rolling RTK S_mix whose lapse-gradient source supplies beta0_eff=2; a fresh same-action PPN derivation remains mandatory.',
  'next_gate':'derive static weak-field equations from S_U1-gravity(beta0_bare=0)+S_DBI+S_mix and evaluate physical-metric PPN quantities without replacing S_mix by a second bare beta0 term'
}
(ROOT/'u1_corrected_bare_ppn_intersection_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('RTK_ROUTE_B_U1_CORRECTED_BARE_PPN_FAMILY_INTERSECTION_PASS',json.dumps(out,sort_keys=True))
