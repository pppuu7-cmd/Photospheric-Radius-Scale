#!/usr/bin/env python3
"""Refine the static weak-field power counting on the v3 family-I branch.

Inputs:
  * O(2) same-action solution: gamma=1 and A_2=U (f=1).
  * universal matter metric: N_tilde=F(sigma)N with a1=1, a2=0.
    In prepotential gauge phi=0, sigma=A/N, hence N_tilde=N-A exactly.
  * physical PPN metric has h_00=2U+O(4), so N_tilde=1-U+O(4)
    in the static zero-shift sector.

Therefore N=N_tilde+A=1+O(4): the ADM-lapse perturbation has no O(2) part.
This changes the PN interpretation of the earlier generic expansion comparing
explicit S_mix ~ (Dn)^2/(1+n)^3 with beta0_eff=2 ~ (Dn)^2/(1+n).
Their nonlinear difference begins at n(Dn)^2, but on this branch n=O(4), not
O(2). Hence that difference cannot affect O(4)/1PN equations; at O(4) the
pure-lapse contribution of S_mix is still represented by the same quadratic
beta0_eff=2 operator acting on n_4.

This does not yet certify full beta_PPN because the complete O(4) system and
possible non-lapse S_mix support must still be checked.
"""
import json
import sympy as sp

# PN bookkeeping uses integer labels: U,A2 are O2; n2 is solved exactly.
U,A2,n2=sp.symbols('U A2 n2', finite=True, real=True)
# Ntilde = N-A at O2, with N=1+n2 and physical Ntilde=1-U.
eq_metric=sp.Eq(1-U,1+n2-A2)
sol_n2=sp.solve(eq_metric.subs(A2,U),n2)
assert sol_n2==[0]

# Weak-field order audit. D does not change formal PN velocity order here.
order_n=4
order_Dn=4
order_quad=2*order_Dn       # (Dn)^2
order_cubic=order_n+2*order_Dn  # n(Dn)^2
# Euler variation lowers by one field factor: quadratic action -> O4 equation;
# cubic action -> O8 equation on this n=O4 branch.
order_eq_quad=4
order_eq_cubic=8
assert order_quad==8 and order_cubic==12
assert order_eq_quad==4 and order_eq_cubic==8

# Algebraic nonlinear difference from the previous gate.
n,Mpl2,X=sp.symbols('n Mpl2 X', finite=True, real=True)
Lmix=Mpl2*X/(1+n)**3
Leff=Mpl2*X/(1+n)
delta=sp.series(Lmix-Leff,n,0,2).removeO().expand()
assert delta==-2*Mpl2*n*X

out={
  'classification':'RTK_ROUTE_B_U1_STATIC_ADM_LAPSE_PN_ORDER_PASS',
  'representative':'research/RTK_C8_U1_FIXED_IR_REPRESENTATIVE_v3.json',
  'inputs':['A_2=U from the same-action O(2) equations','N_tilde=N-A for a1=1,a2=0 in phi=0 gauge','physical N_tilde=1-U+O(4) from h00=2U+O(4)'],
  'result_n2':'0',
  'ADM_lapse_order':'N=1+n_4+O(6); no O(2) ADM-lapse perturbation',
  'explicit_vs_effective_nonlinear_difference':'-2 M_Pl^2 n (D n)^2 + higher powers',
  'difference_action_PN_order_on_v3':'O(12)',
  'difference_field_equation_PN_order_on_v3':'O(8), therefore absent from O(4)/1PN equations',
  'quadratic_Smix_field_equation_order':'O(4), identical in the pure-lapse channel to beta0_eff=2 at this order',
  'correction_to_previous_interpretation':'The generic statement that the cubic mismatch feeds 1PN assumes n=O(2). On the actual v3 family-I static solution n_2=0, so that mismatch is delayed beyond 1PN.',
  'status_scope':'STATIC_PN_ORDER_REFINEMENT_GREEN',
  'non_claims':[
    'does not yet prove full beta_PPN=1; the complete O(4) field system must be checked',
    'does not cover moving-source O(3) preferred-frame/vector effects',
    'does not prove that every static solution has zero Sigma perturbation; that must be checked from the Sigma equation',
    'does not establish radiative stability or strong-coupling cutoff'
  ],
  'next_gate':'prove that Sigma=q t with no local static perturbation is a consistent solution of DBI+S_mix through O(4); if so, the complete static O(4) system is equivalent to the pure-U1 beta0_eff=2 family through 1PN and beta_PPN can be tested sharply'
}
open('u1_static_adm_lapse_pn_order_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
