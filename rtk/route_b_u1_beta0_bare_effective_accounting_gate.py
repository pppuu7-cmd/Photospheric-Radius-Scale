#!/usr/bin/env python3
"""C8 exact bare/effective beta0 accounting for the rolling U(1) RTK action.

Two already-established project identities must be combined rather than matched
separately to the same physical lapse-gradient coefficient:

1) U(1)-Hořava gravity convention
     L_V = ... - beta0 a_i a^i + ...,
     S_g = (M_Pl^2/2) int N sqrt(g) [L_K-L_V+...],
   so the BARE gravity coefficient of +a_i a^i is
     (M_Pl^2/2) beta0_bare.

2) Exact rolling RTK mixed operator
     C D_i(nabla_perp S) D^i(nabla_perp S)
   gives both the required mixed kinetic term and, on q=nabla_perp S_bar != 0,
   a lapse-gradient term with coefficient
     C q^2 = K_pi/(2 M_K^2) = M_Pl^2.

The production RTK direct/rolling target coefficient is M_Pl^2. Therefore the
FULL-ACTION coefficient is

  C_total = (M_Pl^2/2) beta0_bare + M_Pl^2,

and exact matching requires beta0_bare=0. Equivalently, packaging the total
coefficient into a single beta0_eff gives beta0_eff=2. Setting beta0_bare=2
in addition to S_mix double-counts the same target strength and yields
beta0_eff=4.
"""
import json
import sympy as sp

Mpl2,MK2,q,C=sp.symbols('Mpl2 MK2 q C', positive=True, finite=True, real=True)
# beta0_bare must be allowed to vanish; do not declare it strictly positive.
beta_bare=sp.symbols('beta_bare', finite=True, real=True)
Kpi=2*Mpl2*MK2
mix_required=sp.simplify(Kpi/(2*MK2))
assert mix_required==Mpl2

# Exact rolling matching fixes the invariant mixed/lapse-gradient product.
C_solution=sp.solve(sp.Eq(C*q**2,mix_required),C)[0]
mix_coeff=sp.simplify(C_solution*q**2)
assert mix_coeff==Mpl2

bare_gravity_coeff=sp.simplify(Mpl2*beta_bare/2)
total_coeff=sp.simplify(bare_gravity_coeff+mix_coeff)
target_coeff=Mpl2
beta_solution=sp.solve(sp.Eq(total_coeff,target_coeff),beta_bare)
assert beta_solution==[0]

beta_eff=sp.simplify(2*total_coeff/Mpl2)
assert beta_eff==beta_bare+2
assert beta_eff.subs(beta_bare,0)==2
assert total_coeff.subs(beta_bare,0)==Mpl2
assert beta_eff.subs(beta_bare,2)==4
assert total_coeff.subs(beta_bare,2)==2*Mpl2

out={
  'classification':'RTK_ROUTE_B_U1_BETA0_BARE_EFFECTIVE_ACCOUNTING_PASS',
  'production_identity':'K_pi=2 M_Pl^2 M_K^2',
  'rolling_mixed_match':'C q^2=K_pi/(2 M_K^2)=M_Pl^2',
  'bare_gravity_coefficient':'(M_Pl^2/2) beta0_bare',
  'full_action_lapse_gradient_coefficient':'(M_Pl^2/2) beta0_bare + M_Pl^2',
  'target_full_action_coefficient':'M_Pl^2',
  'required_beta0_bare':0,
  'equivalent_beta0_eff_total':2,
  'old_beta0_bare_2_consequence':{
    'full_action_coefficient':'2 M_Pl^2',
    'equivalent_beta0_eff_total':4,
    'classification':'DOUBLE_COUNT_OF_ROLLING_RTK_LAPSE_GRADIENT_STRENGTH'
  },
  'interpretation':'The earlier beta0_RTK=2 dictionary is valid only as an EFFECTIVE single-coefficient representation when S_mix is not separately added. In the explicit full action S_g+S_DBI+S_mix, beta0=2 cannot simultaneously be used as the bare gravity coefficient.',
  'ppn_warning':'Published U(1) PPN formulae use bare gravity-action beta0 and do not include the separate rolling RTK S_mix lapse-gradient source; therefore plugging beta0_bare=0 into those formulae is not a full-action RTK PPN proof.',
  'next_gate':'withdraw the v1 full-action interpretation, freeze a corrected v2 partial slice with beta0_bare=0 and beta0_eff_rolling=2, then redo same-action static/constraint bookkeeping with S_mix explicit.'
}
open('u1_beta0_bare_effective_accounting_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('RTK_ROUTE_B_U1_BETA0_BARE_EFFECTIVE_ACCOUNTING_PASS',json.dumps(out,sort_keys=True))
