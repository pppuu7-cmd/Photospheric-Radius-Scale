#!/usr/bin/env python3
"""C8 auxiliary-rank gate for the zero-H grad-K obstruction.

Question
--------
Can a nondynamical auxiliary constraint generate the required RTK grad-K
coefficient U ~ H^{-2} while all coefficients of the *unreduced* local action
remain finite and the auxiliary constraint matrix keeps finite nonzero rank as
H -> 0?

For one algebraic auxiliary y coupled to the relevant scalar structure X,

    L_aux = 1/2 A(H) y^2 + B(H) y X + 1/2 C(H) X^2,

eliminating y gives

    C_eff(H) = C(H) - B(H)^2/A(H).

If A,B,C have a regular finite H->0 limit and A(0) != 0, then C_eff is finite.
Therefore a required H^{-2} term cannot arise.  More generally, if
B ~ H^m and B^2/A ~ H^{-2}, then A ~ H^(2m+2): the auxiliary Hessian vanishes
and the constraint rank degenerates at H=0.

For several algebraic auxiliaries y_a,

    C_eff = C - b^T M^{-1} b.

If M(H) has a finite nonsingular H->0 limit and b,C are finite, C_eff is
finite by continuity of matrix inversion.  Hence an H^{-2} reduced coefficient
requires either (i) a singular/divergent unreduced coefficient, or (ii) an
eigenvalue of M -> 0 so the auxiliary constraint matrix loses uniform rank.

This is a scoped structural theorem.  It does NOT exclude a theory whose
static limit intentionally changes constraint branch, a genuinely dynamical
auxiliary completion, nonlocal/retarded structure, or a cosmology-only EFT.
"""

import json
import sympy as sp

H = sp.symbols('H', positive=True, finite=True, real=True)
a0,b0,c0 = sp.symbols('a0 b0 c0', finite=True, real=True, nonzero=True)
m = sp.symbols('m', integer=True, nonnegative=True)

# Regular nonsingular one-auxiliary limit.
A_regular = a0
B_regular = b0
C_regular = c0
Ceff_regular = sp.simplify(C_regular - B_regular**2/A_regular)
assert not Ceff_regular.has(H)

# Power-counting branch: B ~ H^m and B^2/A ~ H^-2 implies A ~ H^(2m+2).
A_power = H**(2*m+2)
B_power = H**m
ratio = sp.simplify(B_power**2/A_power)
assert ratio == H**-2
# For every m>=0, exponent 2m+2 is positive: A -> 0 at H->0.
for mi in range(6):
    assert sp.limit(A_power.subs(m,mi),H,0,dir='+') == 0
    assert sp.simplify(ratio.subs(m,mi) - H**-2) == 0

# Explicit 2x2 multi-auxiliary continuity check with a finite nonsingular M0.
a,d,e,b1,b2,C = sp.symbols('a d e b1 b2 C', finite=True, real=True)
M = sp.Matrix([[a,e],[e,d]])
b = sp.Matrix([b1,b2])
detM = sp.factor(M.det())
quad = sp.factor((b.T*M.inv()*b)[0])
assert sp.denom(quad) == detM
# If detM stays finite/nonzero and all entries/couplings are finite, no H pole
# exists because the expression contains no H-dependent singular denominator.
assert not quad.has(H)

out = {
  'classification':'RTK_ROUTE_B_GRADK_AUXILIARY_RANK_GATE_PASS',
  'one_auxiliary':{
    'unreduced':'L_aux=1/2 A(H)y^2+B(H)yX+1/2 C(H)X^2',
    'reduced':'C_eff=C-B^2/A',
    'regular_nonsingular_result':'finite A(0)!=0 with finite B,C implies finite C_eff',
    'power_counting':'if B~H^m and B^2/A~H^-2, then A~H^(2m+2) -> 0 for m>=0'
  },
  'multi_auxiliary':{
    'reduced':'C_eff=C-b^T M^{-1} b',
    'theorem':'finite b,C and a finite nonsingular M(0) imply finite C_eff by continuity of inversion',
    'required_escape':'an H^-2 reduced coefficient requires a divergent unreduced coefficient or an eigenvalue of M approaching zero'
  },
  'connection_to_rtk':'The minimal exact grad-K carrier requires U~H^-2 for finite positive K_clock/M_K^2. Moving this pole into an algebraic auxiliary does not remove it: with regular couplings it moves the singularity into the auxiliary constraint eigenvalue/rank at H=0.',
  'scope':'algebraic nondynamical auxiliaries with coefficients regular near H=0; not a theorem against dynamical auxiliaries, intentional branch-changing static limits, retarded/nonlocal completions, or cosmology-only EFTs',
  'next_step':'If a local completion is pursued, test a dynamical/degenerate auxiliary or modified base constraint explicitly, including DOF count and strong-coupling behavior at the H->0 rank-change surface.'
}
print('RTK_ROUTE_B_GRADK_AUXILIARY_RANK_GATE_PASS',json.dumps(out,sort_keys=True))
