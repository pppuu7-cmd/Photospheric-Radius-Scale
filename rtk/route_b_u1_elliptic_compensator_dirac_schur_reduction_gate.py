#!/usr/bin/env python3
"""Exact Schur reduction of the enlarged U1+elliptic-compensator Dirac matrix.

Frozen parent action: research/RTK_U1_ELLIPTIC_MATTER_COMPENSATOR_CANONICAL_v1.json.

Order the old exceptional-U1 second-class candidates as
  O-basis = (pi_N, J_A^tot, H_perp^tot, phi_A^tot)
and the auxiliary constraints as
  E-basis = (p_Q, p_Lambda, C_Q, C_Lambda).

The full Poisson matrix is antisymmetric:

  M = [[O, X],[-X^T, E]].

The canonical-affinity gate proved that the isolated auxiliary block E is
invertible for ell=1+k_phys^2/M_c^2>0 and det(E)=ell^4. Therefore the exact
block determinant identity gives

  det M = det E * det( O + X E^{-1} X^T ).

So the full rank-8 question is exactly equivalent to invertibility of the
4x4 Schur-deformed old-U1 block S=O+X E^{-1}X^T. This gate proves that
reduction and records which cross-brackets must be derived from the frozen
action before any 3-DOF recertification.

It deliberately does NOT set X=0.
"""
import json
import sympy as sp

ell=sp.symbols('ell', positive=True, finite=True, real=True)

# Generic 4x4 antisymmetric old-U1 block O.
o12,o13,o14,o23,o24,o34=sp.symbols('o12 o13 o14 o23 o24 o34', finite=True, real=True)
O=sp.Matrix([
 [0,o12,o13,o14],
 [-o12,0,o23,o24],
 [-o13,-o23,0,o34],
 [-o14,-o24,-o34,0],
])

# Proven auxiliary four-second-class block.
E=sp.Matrix([
 [0,0,0,-ell],
 [0,0,-ell,0],
 [0,ell,0,0],
 [ell,0,0,0],
])
assert sp.simplify(E.det()-ell**4)==0
Einv=sp.simplify(E.inv())
assert sp.simplify(E*Einv-sp.eye(4))==sp.zeros(4)

# Keep every old/auxiliary cross bracket symbolic: no silent factorization.
x=sp.symbols('x11:15 x21:25 x31:35 x41:45', finite=True, real=True)
X=sp.Matrix(4,4,x)
M=O.row_join(X).col_join((-X.T).row_join(E))
S=sp.simplify(O+X*Einv*X.T)

# Symbolic determinant identity is expensive if fully expanded. Verify the
# exact block identity with a nontrivial symbolic low-rank X family and with
# several deterministic generic integer substitutions, while separately
# deriving the algebraic Schur formula from E^{-1}.
u,v=sp.symbols('u v', finite=True, real=True)
Xtest=sp.Matrix([[u,0,0,0],[0,v,0,0],[0,0,u+v,0],[0,0,0,u-v]])
Mtest=O.row_join(Xtest).col_join((-Xtest.T).row_join(E))
Stest=sp.simplify(O+Xtest*Einv*Xtest.T)
assert sp.simplify(Mtest.det()-E.det()*Stest.det())==0

# Generic numerical substitutions ensure no sign mistake in the assembled
# antisymmetric full matrix / Schur complement convention.
subs_base={ell:3,o12:2,o13:3,o14:5,o23:7,o24:11,o34:13}
for seed in (1,2,3):
    sub=dict(subs_base)
    for i,sym in enumerate(x): sub[sym]=seed+i%5-2
    lhs=sp.Matrix(M.subs(sub)).det()
    rhs=sp.Matrix(E.subs(sub)).det()*sp.Matrix(S.subs(sub)).det()
    assert sp.simplify(lhs-rhs)==0

# Old pure-U1 4x4 antisymmetric determinant is the square of its Pfaffian.
pf_old=sp.expand(o12*o34-o13*o24+o14*o23)
assert sp.simplify(O.det()-pf_old**2)==0

# Schur correction is antisymmetric, as required.
Delta=sp.simplify(X*Einv*X.T)
assert sp.simplify(Delta+Delta.T)==sp.zeros(4)
assert sp.simplify(S+S.T)==sp.zeros(4)

out={
 'classification':'RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_DIRAC_SCHUR_REDUCTION_PASS',
 'status_scope':'GREEN_EXACT_RANK_REDUCTION_FULL_CROSS_BRACKETS_PENDING',
 'frozen_parent':'research/RTK_U1_ELLIPTIC_MATTER_COMPENSATOR_CANONICAL_v1.json',
 'old_basis':['pi_N','J_A_total','H_perp_total','phi_A_total'],
 'aux_basis':['p_Q','p_Lambda','C_Q','C_Lambda'],
 'auxiliary_block':{
   'det_E':'ell^4',
   'ell':'1+k_phys^2/M_c^2 > 0',
   'invertible':'for all physical k and M_c>0'
 },
 'exact_reduction':{
   'full_matrix':'M=[[O,X],[-X^T,E]]',
   'schur_matrix':'S=O+X E^{-1} X^T',
   'det_identity':'det(M)=ell^4 det(S)',
   'rank8_iff':'det(S)!=0'
 },
 'old_u1_structure':{
   'pfaffian':'o12 o34 - o13 o24 + o14 o23',
   'det_O':'pfaffian^2'
 },
 'critical_warning':'Invertibility of the isolated Q,Lambda block does not prove full rank. Cross brackets X must be derived from the frozen action and inserted into S; setting X=0 would be an unjustified assumption.',
 'cross_brackets_to_derive':[
   '{pi_N, p_Q/p_Lambda/C_Q/C_Lambda}',
   '{J_A_total, p_Q/p_Lambda/C_Q/C_Lambda}',
   '{H_perp_total, p_Q/p_Lambda/C_Q/C_Lambda}',
   '{phi_A_total, p_Q/p_Lambda/C_Q/C_Lambda}'
 ],
 'next_gate':'derive exact zero/nonzero support of X from the frozen canonical action, first on the regular phi=0 rolling X_U>0 slice, then substitute the surviving entries into S and prove its Pfaffian is generically nonzero or classify the exact finite-k rank-loss locus.'
}
open('u1_elliptic_compensator_dirac_schur_reduction_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
