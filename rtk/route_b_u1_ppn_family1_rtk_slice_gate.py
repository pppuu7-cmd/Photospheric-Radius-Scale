#!/usr/bin/env python3
"""C8 algebraic openness gate for the second explicit GR-PPN U(1) family.

Literature input (arXiv:1310.6666 / accompanying presentation):
all PPN parameters take their GR values in the explicit family

    a1 = kappa = 1,
    sigma2 = 0.

Unlike the other displayed exact-GR family, this condition does not itself fix
beta0.  The direct rolling RTK coefficient slice maps to beta0=2 in the action
convention zeta^2=M_Pl^2/2 and +zeta^2 beta0 a_i a^i.

This theorem proves only that the displayed family-I algebraic conditions do not
contradict beta0=2.  It is NOT a PPN certification of the full RTK completion:
remaining field equations, matter-frame parameters, stability/DOF, radiative
stability, Newton normalization and the exact static solution must still be
checked on the same parameter slice.
"""

import json
import sympy as sp

Mpl2,MK2,beta0,a1,kappa,sigma2 = sp.symbols(
    'Mpl2 MK2 beta0 a1 kappa sigma2', positive=True, finite=True, real=True
)

zeta2=Mpl2/2
Kprod=2*Mpl2*MK2
Cacc=sp.simplify(Kprod/(2*MK2))
beta_rtk=sp.solve(sp.Eq(zeta2*beta0,Cacc),beta0)
assert beta_rtk == [2]

# Exact-GR PPN family I conditions quoted in the literature.
family1={a1:sp.Integer(1),kappa:sp.Integer(1),sigma2:sp.Integer(0)}
assert sp.simplify((a1-1).subs(family1))==0
assert sp.simplify((kappa-1).subs(family1))==0
assert sp.simplify(sigma2.subs(family1))==0

# beta0 is not constrained by these three equalities, so beta0=2 is
# algebraically compatible with the displayed family-I conditions.
family1_rtk={**family1,beta0:sp.Integer(2)}
assert sp.simplify(beta0.subs(family1_rtk)-2)==0

out={
  'classification':'RTK_ROUTE_B_U1_PPN_FAMILY1_RTK_SLICE_ALGEBRAICALLY_OPEN',
  'literature_GR_PPN_family_I':{'a1':1,'kappa':1,'sigma2':0},
  'rtk_direct_beta0_slice':2,
  'algebraic_result':'The displayed family-I GR-PPN conditions do not fix beta0 and therefore do not algebraically exclude beta0=2.',
  'non_claims':[
    'not a proof that the full RTK beta0=2 slice has GR PPN parameters after all remaining theory/matter parameters are fixed',
    'not a static-field-equation solution',
    'not a nonlinear DOF or stability theorem',
    'not a radiative-stability or EFT-cutoff result'
  ],
  'next_gate':'Freeze a concrete family-I matter/gravity parameter tuple including beta0=2, derive/solve the IR static equations, and evaluate the published PPN expressions and constraint/DOF conditions on that same tuple.'
}
print('RTK_ROUTE_B_U1_PPN_FAMILY1_RTK_SLICE_ALGEBRAICALLY_OPEN',json.dumps(out,sort_keys=True))
