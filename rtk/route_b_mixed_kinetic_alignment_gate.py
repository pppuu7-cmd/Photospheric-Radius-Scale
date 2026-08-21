#!/usr/bin/env python3
"""C8 exact degeneracy gate for IR/mixed-derivative kinetic alignment.

Context
-------
Generic mixed-derivative preferred-foliation theories can activate an extra
scalar.  Our constructive escape instead requires a rank-one velocity Hessian
for all spatial momenta.

Let the two-field IR kinetic matrix and the p^2 mixed-kinetic correction be

    K0 = A v v^T,
    K1 = B w w^T,
    K(p^2) = K0 + p^2 K1,

with nonzero A,B and two real field-space vectors v,w.

Exact theorem
-------------
For two fields,

    det K(p^2) = A B p^2 (v1 w2-v2 w1)^2.

Therefore the full velocity Hessian remains rank one for every finite p^2 iff
v and w are collinear.  A generic misalignment immediately makes the Hessian
rank two at p^2>0 and propagates an additional scalar kinetic direction.

For the RTK fixed-state construction, both the ordinary kinetic term and the
mixed derivative term must therefore depend on the same combination

    S = X + a Y.

This is a necessary quadratic degeneracy condition, not a full nonlinear
Hamiltonian theorem.
"""

import json
import sympy as sp

A,B,s = sp.symbols('A B s', nonzero=True, finite=True, real=True)
v1,v2,w1,w2 = sp.symbols('v1 v2 w1 w2', finite=True, real=True)

v = sp.Matrix([v1,v2])
w = sp.Matrix([w1,w2])
K0 = A*(v*v.T)
K1 = B*(w*w.T)
K = sp.expand(K0+s*K1)

detK = sp.factor(K.det())
cross = sp.factor(v1*w2-v2*w1)
expected = sp.factor(A*B*s*cross**2)
assert sp.simplify(detK-expected) == 0

# Explicit aligned branch w=c v remains rank one for arbitrary p^2.
c = sp.symbols('c', nonzero=True, finite=True, real=True)
K_aligned = sp.simplify(K.subs({w1:c*v1,w2:c*v2}))
assert sp.factor(K_aligned.det()) == 0
# For a nonzero v and generic nonzero coefficient A+s B c^2 the matrix is
# proportional to vv^T, i.e. has at most one kinetic direction.
assert sp.simplify(K_aligned-(A+s*B*c**2)*(v*v.T)) == sp.zeros(2)

# Concrete RTK direction v=w=(1,a).
a = sp.symbols('a', finite=True, real=True)
v_rtk = sp.Matrix([1,a])
K_rtk = sp.factor(A+s*B)*(v_rtk*v_rtk.T)
assert K_rtk.rank() == 1
assert sp.factor(K_rtk.det()) == 0

# Explicit misaligned example shows immediate rank-two activation for s!=0.
K_mis = sp.diag(A,s*B)
assert sp.factor(K_mis.det()) == A*B*s

out = {
  'classification':'RTK_ROUTE_B_MIXED_KINETIC_ALIGNMENT_GATE_PASS',
  'setup':'K(p^2)=A vv^T + p^2 B ww^T',
  'determinant':'A B p^2 (v1 w2-v2 w1)^2',
  'necessary_condition':'For nonzero A,B and finite p^2>0, rank-one propagation requires w parallel to v.',
  'rtk_design_rule':'The IR kinetic and the mixed-spatial kinetic correction must act on the same degenerate field combination S=X+aY.',
  'failure_mode':'Any generic field-space misalignment makes the velocity Hessian rank two and opens an extra scalar kinetic direction at finite momentum.',
  'relation_to_literature':'This supplies the project-specific degeneracy condition that must be imposed before importing generic mixed-derivative preferred-foliation operators, which are known to risk additional scalar modes.',
  'non_claims':[
    'necessary quadratic velocity-Hessian condition only',
    'not a full nonlinear Dirac/Hamiltonian proof',
    'does not by itself prove stability of the surviving scalar',
    'does not address radiative stability of the alignment'
  ],
  'next_step':'Build the symmetry-based ADM/Khronon action so both zero-gradient and mixed-gradient kinetic terms depend on one identical background-silent combination, then test whether the alignment is enforced by a symmetry/constraint rather than tuning.'
}

print('RTK_ROUTE_B_MIXED_KINETIC_ALIGNMENT_GATE_PASS',json.dumps(out,sort_keys=True))
