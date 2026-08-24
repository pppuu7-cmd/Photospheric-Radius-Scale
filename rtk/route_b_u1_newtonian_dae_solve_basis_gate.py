#!/usr/bin/env python3
"""C10 Newtonian DAE solve-basis determinant theorem.

Preregistered target:
  research/theory_targets/RTK_C10_U1_NEWTONIAN_DAE_SOLVE_BASIS_TARGET_v1.json

Scope: flat FLRW, k>0, lambda_HL>1, Eth_IR_full=2, two-derivative IR solve basis.
This theorem classifies the 3x3 Newtonian-source algebraic solve-basis crossing;
it is explicitly not a physical constraint-rank determinant theorem.
"""
import json
from pathlib import Path
import sympy as sp

x,m,C,rho,p,Ro,cao2,r,D,H = sp.symbols(
    'x m C rho p Ro cao2 r D H', positive=True, finite=True, real=True)
# x=k^2>0, m=a^2 M_c^2>0, r=lambda-1>0, D=3lambda-1>0.
KA=x+m
A1=KA+3*C*Ro
B1=-3*C*H**2*Ro*(1+3*cao2)
KB=-r*x+2*C*(rho+p)

# Frozen determinant bracket for Eth=2.
bracket=sp.expand(A1*(D*H**2-KB)+D*B1)
# Flat no-explicit-Lambda Friedmann: D H^2=(4/3) C rho.
bracket_flat=sp.factor(bracket.subs(H**2, sp.Rational(4,3)*C*rho/D))
A=sp.Rational(2,3)*C*(rho+3*p)
expected=sp.expand((x+m+3*C*Ro)*(r*x-A)-4*C**2*rho*Ro*(1+3*cao2))
assert sp.simplify(bracket_flat-expected)==0

poly=sp.Poly(expected,x)
a2=sp.factor(poly.coeff_monomial(x**2))
a1=sp.factor(poly.coeff_monomial(x))
a0=sp.factor(poly.coeff_monomial(1))
assert sp.simplify(a2-r)==0
expected_b=sp.expand(r*(m+3*C*Ro)-sp.Rational(2,3)*C*(rho+3*p))
assert sp.simplify(a1-expected_b)==0
expected_c=sp.expand(-sp.Rational(2,3)*C*(rho+3*p)*(m+3*C*Ro)-4*C**2*rho*Ro*(1+3*cao2))
assert sp.simplify(a0-expected_c)==0

# Under the frozen positive-domain assumptions: leading coefficient >0 and
# constant term <0. Therefore product of roots c/a <0: for a real quadratic,
# the two roots have opposite sign. Discriminant is automatically > b^2.
disc=sp.factor(a1**2-4*a2*a0)
assert sp.simplify(disc-(a1**2+4*r*(-a0)))==0
# We encode the sign proof structurally rather than asking SymPy to infer all
# inequalities from products of positive symbols.
minus_c=sp.factor(-a0)
assert minus_c == sp.factor(sp.Rational(2,3)*C*(rho+3*p)*(m+3*C*Ro)+4*C**2*rho*Ro*(1+3*cao2))
root_plus=sp.simplify((-a1+sp.sqrt(disc))/(2*r))
root_minus=sp.simplify((-a1-sp.sqrt(disc))/(2*r))

# Reconstruct the full determinant det=2 L Delta with L=-x.
L=-x
det=sp.factor(2*L*expected)
assert sp.simplify(det + 2*x*expected)==0

out={
  'classification':'C10_U1_NEWTONIAN_3X3_ALGEBRAIC_SOLVE_BASIS_HAS_ONE_POSITIVE_CROSSING_SCOPED',
  'status_scope':'YELLOW_SOLVE_BASIS_CROSSING_NOT_PHYSICAL_RANK_LOSS',
  'scope':'flat FLRW; k>0; lambda_HL>1; Eth_IR_full=2; explicit Lambda=0; two-derivative IR solve basis',
  'determinant':'det=2 L Delta(x), L=-x',
  'Delta':'r x^2 + b x + c',
  'b':str(a1),
  'c':str(a0),
  'minus_c_positive_form':str(minus_c),
  'discriminant':str(disc),
  'root_sign_theorem':'r>0 and c<0 imply product of the two real roots c/r<0; hence exactly one positive real root and one negative real root',
  'positive_root_symbolic':str(root_plus),
  'negative_root_symbolic':str(root_minus),
  'interpretation':'The positive root is a singularity of this chosen Newtonian 3x3 algebraic inversion. It is not promoted to physical rank loss because the original preferred-foliation/all-q constraint-rank determinant is a different object and remains separately certified.',
  'software_route':'Do not globally invert this 3x3 Newtonian matrix. Use a preferred-coordinate/DAE solve and construct Newtonian potentials as outputs, or derive a crossing-regular variable basis.',
  'non_claims':[
    'not a physical extra mode',
    'not a ghost or gradient instability theorem',
    'not a contradiction of the finite-k/all-q physical rank-safe completion',
    'not a higher-spatial transformed determinant',
    'not a CLASS failure or likelihood result'
  ],
  'target':'research/theory_targets/RTK_C10_U1_NEWTONIAN_DAE_SOLVE_BASIS_TARGET_v1.json'
}
Path('u1_newtonian_dae_solve_basis_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
