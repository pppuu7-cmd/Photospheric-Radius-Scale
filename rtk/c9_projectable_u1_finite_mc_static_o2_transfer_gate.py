#!/usr/bin/env python3
"""Finite-Mc static O(2) source-transfer theorem for the projectable U(1)+RTK candidate.

Primary projectable PPN equations: Lin, Mukohyama, Wang, Zhu, arXiv:1310.6666,
Sec. VI Eqs. (6.14),(6.15).  For the GR parent branch a1=1,a2=0,g1=-1:
  spatial dynamical O(2): gamma=1,
  A-constraint O(2):      gamma=kappa a1,  kappa=G/G_N.

After exact Q,Lambda elimination our ordinary-matter A-source is multiplied by
f(k)=a_eff=k^2/(M_c^2+k^2) relative to the original local a1=1 source.  At O(2)
the metric variation of the filtered A-source interaction is O(A2 H0)=O(4), so
it does not modify the O(2) spatial dynamical equation.  Thus the modified
A-constraint is gamma=kappa f(k), while gamma=1 remains fixed by the spatial
equation.  Hence G_N(k)=G f(k).

This is only a static linear theorem.  O(3)/O(4) finite-Mc source transfer must
be rederived before full alpha1,alpha2,beta claims.
"""
import json
import sympy as sp

q,M2,G,GN=sp.symbols('q M_c_squared G G_N', positive=True, finite=True)
a1,a2,g1,kappa=sp.symbols('a1 a2 g1 kappa', real=True, finite=True)
f=sp.factor(q/(M2+q))
# Published Eq.(6.14).
gamma_dyn=sp.factor(-(g1*a2+1)/(g1*a1))
parent={a1:1,a2:0,g1:-1}
assert sp.simplify(gamma_dyn.subs(parent)-1)==0
# Filtered Eq.(6.15): gamma = kappa*a1*f - a2/a1.
gamma_A=sp.factor(kappa*a1*f-a2/a1)
gamma_A_parent=sp.factor(gamma_A.subs(parent))
assert sp.simplify(gamma_A_parent-kappa*f)==0
# Solve gamma_dyn=gamma_A with kappa=G/GN.
GN_solution=sp.solve(sp.Eq(1,(G/GN)*f),GN)
assert GN_solution==[G*f]

# Exact relative Newton-transfer drift between two physical Fourier scales.
q1,q2=sp.symbols('q1 q2', positive=True, finite=True)
f1=q1/(M2+q1); f2=q2/(M2+q2)
ratio=sp.factor(f1/f2)
assert sp.simplify(ratio-q1*(M2+q2)/(q2*(M2+q1)))==0
# High-k deficit from local parent Newton value.
deficit=sp.factor(1-f)
assert deficit==M2/(M2+q)

out={
  'classification':'RTK_C9_PROJECTABLE_U1_FINITE_MC_STATIC_O2_TRANSFER_PASS',
  'status_scope':'GREEN_STATIC_O2_SCALE_DEPENDENT_NEWTON_GAMMA_ONE_FULL_FINITE_MC_PPN_PENDING',
  'primary_equations':'Lin-Mukohyama-Wang-Zhu arXiv:1310.6666 Sec.VI Eqs.(6.14),(6.15), with projectable GR branch a1=1,a2=0,g1=-1',
  'filter':'f(k)=a_eff=k^2/(M_c^2+k^2)',
  'O2_ordering':'The filtered interaction is linear in A and H0. Its A variation is O(2) and filters J_A, while its spatial-metric variation carries A2*H0 and starts at O(4); therefore Eq.(6.14) is unchanged at O(2).',
  'gamma_result':'gamma_PPN=1 from the unchanged O(2) spatial dynamical equation',
  'filtered_A_constraint':'1=kappa f(k), where kappa=G/G_N(k)',
  'newton_transfer':'G_N(k)=G k^2/(M_c^2+k^2)',
  'local_parent_deficit':'1-G_N(k)/G=M_c^2/(M_c^2+k^2)',
  'two_scale_ratio':'G_N(k1)/G_N(k2)=k1^2(M_c^2+k2^2)/[k2^2(M_c^2+k1^2)]',
  'tolerance_dictionary':'Requiring |1-G_N(k_local)/G|<=eps_local is exactly M_c^2 <= [eps_local/(1-eps_local)] k_local^2, identical to the local half of the dual-tolerance filter-window theorem.',
  'interpretation':'The projectable compensator does not shift gamma at static O(2); it makes the measured Newton normalization scale dependent. Local recovery is therefore controlled directly by the same 1-a_eff tolerance used in the symbolic M_c window.',
  'non_claims':[
    'does not certify beta_PPN at finite M_c because the filtered interaction contributes to metric equations at O(4)',
    'does not certify alpha1 or alpha2 at finite M_c because moving-source/prepotential and auxiliary responses must be rederived at O(3)',
    'does not identify a numerical experimental eps_local or choose M_c',
    'does not include finite-size source form factors or nonlinear screening'
  ],
  'next_gate':'derive the projectable O(3) momentum/prepotential system after auxiliary elimination and test alpha1,alpha2 as functions of f(k); then derive O(4) A/metric equations for beta_PPN and finite-size sources.'
}
open('c9_projectable_u1_finite_mc_static_o2_transfer_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
