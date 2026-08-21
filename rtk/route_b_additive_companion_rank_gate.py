#!/usr/bin/env python3
"""C8 rank gate: a healthy companion cannot simply be appended to the existing scalar.

The production clock/gravity sector already carries one positive scalar kinetic
direction.  A separate positive rank-one companion kinetic term generically
adds a second direction.

Let

    K_old  = A e e^T,   e=(1,0), A>0,
    K_comp = B v v^T,   v=(v1,v2), B>0.

Then

    det(K_old+K_comp)=A B v2^2.

Thus any genuinely independent companion component v2!=0 makes the full
kinetic matrix rank two.  A final one-scalar RTK completion cannot be obtained
by simply adding a healthy positive companion action on top of the unchanged
DBI/Khronon scalar sector.

The viable options are instead:
  (i) replace/promote the original clock kinetic so the IR and mixed kinetic
      terms depend on one common field combination from the start; or
  (ii) introduce an explicitly constraint-degenerate/indefinite structure and
       prove its Dirac constraints and positive reduced residue.
"""

import json
import sympy as sp

A,B,v1,v2 = sp.symbols('A B v1 v2', positive=True, finite=True, real=True)
# v2 is declared positive here to represent a genuinely independent companion.
e = sp.Matrix([1,0])
v = sp.Matrix([v1,v2])
Kold = A*(e*e.T)
Kcomp = B*(v*v.T)
Ktot = sp.simplify(Kold+Kcomp)
detK = sp.factor(Ktot.det())
assert sp.simplify(detK-A*B*v2**2) == 0
assert detK.is_positive
assert Ktot.rank() == 2

# If the added vector is collinear with the old direction (v2=0), no new field
# direction is kinetically activated; this is the trivial aligned case.
u = sp.symbols('u', nonzero=True, finite=True, real=True)
Kaligned = sp.simplify(Kold+B*sp.Matrix([u,0])*sp.Matrix([u,0]).T)
assert sp.factor(Kaligned.det()) == 0
assert Kaligned.rank() == 1

out = {
  'classification':'RTK_ROUTE_B_ADDITIVE_COMPANION_RANK_GATE_PASS',
  'determinant':'det(K_old+K_comp)=A B v2^2 for K_old=A e1e1^T and K_comp=B vv^T',
  'theorem':'A positive healthy companion with a genuinely new field component makes the total kinetic rank two when appended to an unchanged one-scalar DBI/Khronon kinetic sector.',
  'consequence':'The background-silent companion action is a building block, not an additive final completion. The original clock kinetic must be promoted into the same degenerate combination, or a separate constraint-degenerate mechanism must remove the extra direction.',
  'allowed_trivial_case':'v2=0 is rank one but does not kinetically activate an independent companion.',
  'non_claims':[
    'not a no-go for multi-field degenerate theories',
    'not a no-go for replacing the original clock action by a common-combination action',
    'not a statement about an indefinite kinetic matrix after constraints',
    'does not replace a full gravitational Hamiltonian analysis'
  ],
  'next_step':'Construct a covariant/spatially-covariant replacement of the DBI clock kinetic in which both the p^0 and p^2 kinetic pieces act on one common combination, while the same background rho,p,c_a^2 and matter sourcing are retained.'
}

print('RTK_ROUTE_B_ADDITIVE_COMPANION_RANK_GATE_PASS',json.dumps(out,sort_keys=True))
