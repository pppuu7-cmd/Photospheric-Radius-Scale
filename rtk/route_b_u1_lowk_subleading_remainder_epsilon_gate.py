#!/usr/bin/env python3
"""Finite punctured-low-k interval from a bounded subleading remainder.

Let q=|k|^2 and suppose the already-reduced physical 2x2 cross block has

    B(q)=q L + q^2 R(q),      0<=q<=q0,

with L invertible and ||R(q)||_2<=C.  Then

    B(q)/q = L + q R(q).

By the standard smallest-singular-value perturbation inequality,

    sigma_min(L+qR) >= sigma_min(L)-q C.

Hence B(q) has full 2x2 rank for every

    0<q<min(q0, sigma_min(L)/C)

when C>0.  Equivalently,

    0<|k|<sqrt(min(q0,sigma_min(L)/C)).

For the RTK+antisymmetric-filtered leading matrix

    L=[[A,-B],[B,0]],  B=b+x/M_c^2,

the exact determinant is B^2 and

    sigma_min(L)^2 = (A^2+2B^2-|A|sqrt(A^2+4B^2))/2.

This theorem is purely a remainder-control bridge. It does not provide C.
"""
import json
import sympy as sp

A,B=sp.symbols('A B', real=True, finite=True)
L=sp.Matrix([[A,-B],[B,0]])
assert sp.simplify(L.det()-B**2)==0
G=sp.expand(L.T*L)
tr=sp.expand(sp.trace(G)); detG=sp.expand(G.det())
assert sp.simplify(tr-(A**2+2*B**2))==0
assert sp.simplify(detG-B**4)==0

# Symbolic squared singular roots of the Gram matrix.
lam=sp.symbols('lambda', real=True)
poly=sp.expand((G-lam*sp.eye(2)).det())
expected=sp.expand(lam**2-tr*lam+B**4)
assert sp.simplify(poly-expected)==0
# The smaller root written using |A|; verify separately for A>=0 representative.
Ap,Bp=sp.symbols('Apos Bpos', positive=True, finite=True)
smin2=(Ap**2+2*Bp**2-Ap*sp.sqrt(Ap**2+4*Bp**2))/2
smin2_rat=2*Bp**4/(Ap**2+2*Bp**2+Ap*sp.sqrt(Ap**2+4*Bp**2))
assert sp.simplify(smin2-smin2_rat)==0

q0,C,sigma=sp.symbols('q0 C sigma_min', positive=True, finite=True)
# The theorem's sufficient inequality is q*C<sigma.  We record the exact
# candidate radius in q and k; no numerical values are inserted.
qcrit=sp.simplify(sigma/C)
kcrit=sp.sqrt(qcrit)
assert sp.simplify(kcrit**2-qcrit)==0

out={
  'classification':'RTK_ROUTE_B_U1_LOWK_SUBLEADING_REMAINDER_EPSILON_PASS',
  'status_scope':'GREEN_GENERAL_FINITE_PUNCTURED_INTERVAL_BRIDGE_ACTION_REMAINDER_BOUND_PENDING',
  'assumption':'B(q)=q L+q^2 R(q), ||R(q)||_2<=C on 0<=q<=q0, L invertible, q=|k|^2',
  'perturbation_bound':'sigma_min(L+qR)>=sigma_min(L)-q C',
  'rank_interval_q':'0<q<min(q0,sigma_min(L)/C) for C>0',
  'rank_interval_k':'0<|k|<sqrt(min(q0,sigma_min(L)/C))',
  'rtk_filtered_leading_matrix':'L=[[A,-B],[B,0]], B=b+x/M_c^2',
  'leading_determinant':'det L=B^2',
  'sigma_min_squared':'(A^2+2B^2-|A| sqrt(A^2+4B^2))/2',
  'positive_rationalized_sigma_min_squared':'2B^4/(A^2+2B^2+|A| sqrt(A^2+4B^2))',
  'interpretation':'Once the leading off-diagonal coefficient B is nonzero, any explicit uniform action-level bound C on the O(k^4) remainder immediately yields a finite punctured low-k interval without a dense numerical root search arbitrarily close to k=0.',
  'non_claims':['does not derive C','does not choose M_c','does not extend the interval beyond q0','does not certify intermediate/high-k rank or phenomenology'],
  'next_gate':'derive a conservative C from the next terms of a_eff, the resolvent variation, the pure-gravity O(q^2) operators, and neutral-RTK O(q^2) support on a controlled FLRW background.'
}
with open('u1_lowk_subleading_remainder_epsilon_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
