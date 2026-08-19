#!/usr/bin/env python3
"""Exact algebraic audit of the isolated c4=2 khronometric/DHOST branch.

Primary source: Ben Achour, Langlois & Noui, Phys.Rev.D 93 (2016) 124005,
arXiv:1602.08398, Eqs. (7.4), (7.10)-(7.13), together with the Class-II
metric-sector criterion around Eqs. (3.22)-(3.27).

This script does not claim that either family reproduces the RTK rational
mixed-kinetic dispersion. It only determines which exact c4=2 degeneracy
families survive and audits the metric-sector factor f-X*alpha1.
"""
import json
import sympy as sp

X=sp.symbols('X', positive=True, nonzero=True)
c2,c3=sp.symbols('c2 c3', real=True)
f=sp.Integer(1)
c4=sp.Integer(2)

def eq(a,b):
    return sp.simplify(a-b)==0

# Khronometric -> quadratic-DHOST dictionary after absorbing c1 (paper Eq. 7.4).
a1=-c3/X
a2=-c2/X
a3=2*c2/X**2
a4=(2*c3+c4)/X**2
a5=-(c2+c3+c4)/X**3

# Paper Eq. (7.11) on the isolated c4=2 D0 branch.
D1_special=8*(1+c3)*(3*c2+c3-2)/X**2
D2_special=sp.simplify(D1_special/X)
assert eq(sp.factor(D1_special),8*(c3+1)*(3*c2+c3-2)/X**2)

# The two exact degeneracy families from factorization.
family_A={c3:sp.Integer(-1)}
family_B={c3:sp.Integer(2)-3*c2}
assert sp.simplify(D1_special.subs(family_A))==0
assert sp.simplify(D2_special.subs(family_A))==0
assert sp.simplify(D1_special.subs(family_B))==0
assert sp.simplify(D2_special.subs(family_B))==0

# Reproduce Eqs. (7.12)-(7.13) directly from Eq. (7.4).
A=[sp.simplify(x.subs(family_A)) for x in (a1,a2,a3,a4,a5)]
B=[sp.simplify(x.subs(family_B)) for x in (a1,a2,a3,a4,a5)]
A_expected=[1/X,-c2/X,2*c2/X**2,0,-(c2+1)/X**3]
B_expected=[(3*c2-2)/X,-c2/X,2*c2/X**2,6*(1-c2)/X**2,2*(c2-2)/X**3]
assert all(eq(x,y) for x,y in zip(A,A_expected))
assert all(eq(x,y) for x,y in zip(B,B_expected))

# Class-II metric-block discriminator used in the same paper:
# IIa is derived assuming f-X*a1 != 0; IIb has f=X*a1 and is reported to
# have a degenerate metric sector. We audit this factor independently rather
# than trusting prose class labels in Sec. VII.
metric_factor_A=sp.simplify(f-X*A[0])
metric_factor_B=sp.factor(f-X*B[0])
assert metric_factor_A==0
assert eq(metric_factor_B,3*(1-c2))

# Therefore family A lies on the metric-degenerate factor identically.
# Family B lies off it for c2 != 1, and hits it only at c2=1.
# This algebra is internally useful because the prose after Eq. (7.13) labels
# that family IIb except c2=1, opposite to the defining factor above; we record
# the discrepancy instead of silently choosing one label.

out={
  'classification':'RTK_ROUTE_B_KHRONOMETRIC_C4EQ2_AUDIT_PASS',
  'primary_source':'Ben Achour, Langlois & Noui, arXiv:1602.08398, Eqs. 7.4 and 7.10-7.13; Class-II definitions Eqs. 3.22-3.27',
  'special_branch':{'c4':2,'D1':'8*(1+c3)*(3*c2+c3-2)/X^2','D2':'D1/X'},
  'exact_families':[
    {
      'name':'A','condition':'c3=-1',
      'alphas':['1/X','-c2/X','2*c2/X^2','0','-(c2+1)/X^3'],
      'f_minus_X_alpha1':'0',
      'metric_factor_status':'IDENTICALLY_DEGENERATE_BY_CLASS_II_DISCRIMINATOR'
    },
    {
      'name':'B','condition':'c3=2-3*c2',
      'alphas':['(3*c2-2)/X','-c2/X','2*c2/X^2','6*(1-c2)/X^2','2*(c2-2)/X^3'],
      'f_minus_X_alpha1':'3*(1-c2)',
      'metric_factor_status':'NONZERO_FOR_C2_NE_1; DEGENERATE_AT_C2_EQ_1'
    }
  ],
  'source_label_discrepancy':'The prose after Eq. (7.13) says the second family is IIb except c2=1, whereas the paper defining criterion f-X*alpha1 gives the opposite algebraic discriminator for this family. This audit records the discrepancy and does not resolve it by authority.',
  'rtk_completion_status':'OPEN: surviving algebraic family B for c2!=1 is only a nonlinear-completion candidate; its reduced scalar dispersion, tensor kinetic signs, constraints, strong-coupling scale, and matching to RTK normalization remain to be derived.',
  'scope_warning':'Exact constant-ci khronometric/DHOST algebra only. No claim of phenomenological viability, global ghost-freedom, strong-coupling safety, or unique RTK completion.'
}
print('RTK_ROUTE_B_KHRONOMETRIC_C4EQ2_AUDIT_PASS',json.dumps(out,sort_keys=True))
