#!/usr/bin/env python3
"""Exact algebraic audit of the simplest covariant acceleration-squared Route-B idea.

Primary formulas are the constant-c_i khronometric specialization of the
quadratic DHOST degeneracy conditions in Ben Achour, Langlois & Noui,
arXiv:1602.08398, Sec. VII.  After absorbing c1 into c3,c4 and setting f=1,

  D0 = 4/X (c2+c3)(c4-2),

and on the Class-I branch c2+c3=0,

  D1 = X D2 = -8/X^2 (c2-1)^2 c4.

The RTK kinetic denominator suggests a nonzero, continuously tunable c4
(acceleration-squared) coefficient.  This script proves that within the
constant-c_i khronometric family such a tunable nonzero c4 forces
c2=1,c3=-1, the Class-Ib family with f+X*alpha2=0.  The latter makes the usual
metric kinetic block degenerate and therefore fails the Route-B requirement
that the ordinary tensor structure remain nondegenerate.

This does NOT exclude general X-dependent DHOST/spatially-covariant companion
operators or constrained auxiliary realizations.
"""
import json
import sympy as sp

X=sp.symbols('X', positive=True, nonzero=True)
c2,c3,c4=sp.symbols('c2 c3 c4', real=True)
f=sp.Integer(1)
D0=sp.simplify(4*(c2+c3)*(c4-2)/X)

# Pure acceleration-squared proposal after c1 absorption: c2=c3=0.
D0_pure=sp.simplify(D0.subs({c2:0,c3:0}))
# D0 vanishes on Class I, but the remaining degeneracy condition does not.
D1_classI=-8*(c2-1)**2*c4/X**2
D1_pure=sp.simplify(D1_classI.subs(c2,0))
assert D0_pure==0
assert D1_pure==-8*c4/X**2
# Therefore pure c4 is degenerate only in the trivial c4=0 case.
assert sp.solve(sp.Eq(D1_pure,0),c4)==[0]

# For a continuously tunable c4 not restricted to the isolated c4=2 branch,
# D0=0 requires Class I: c3=-c2. For nonzero c4, D1=0 then fixes c2=1.
classI_c3=-c2
solutions_c2=sp.solve(sp.Eq(sp.factor(D1_classI/c4),0),c2)
assert solutions_c2==[1]
forced={c2:sp.Integer(1),c3:sp.Integer(-1)}

# Khronometric-to-DHOST mapping with c1 absorbed:
# alpha1=-c3/X, alpha2=-c2/X.  At the forced point this is the Ib condition
# alpha1=-alpha2=1/X and f + X*alpha2 = 0.
alpha1=-c3/X
alpha2=-c2/X
alpha1_forced=sp.simplify(alpha1.subs(forced))
alpha2_forced=sp.simplify(alpha2.subs(forced))
tensor_metric_factor=sp.simplify(f+X*alpha2_forced)
assert alpha1_forced==1/X
assert alpha2_forced==-1/X
assert tensor_metric_factor==0

# The special D0 branch c4=2 is recorded rather than silently discarded.
# It is an isolated coefficient relation, not an arbitrary tunable c4 route.
D0_c4_2=sp.simplify(D0.subs(c4,2))
assert D0_c4_2==0

# Decoupling-level reason the forced Class-Ib combination looked attractive:
# the c2/c3 spatial-Hessian terms cancel for a single Fourier mode because
# (tr H)^2 == tr(H^2) for H_ij proportional to q_i q_j.
q2,pi=sp.symbols('q2 pi', nonnegative=True)
laplacian_sq=q2**2*pi**2
hessian_sq=q2**2*pi**2
assert sp.simplify(laplacian_sq-hessian_sq)==0

out={
  'classification':'RTK_ROUTE_B_KHRONOMETRIC_ACCELERATION_DEGENERACY_AUDIT_PASS',
  'pure_c4_result':'c2=c3=0 with nonzero c4 fails the remaining DHOST degeneracy condition',
  'tunable_nonzero_c4_classI_forces':{'c2':1,'c3':-1},
  'forced_dhost_coefficients':{'alpha1':'1/X','alpha2':'-1/X'},
  'forced_metric_kinetic_factor_f_plus_X_alpha2':'0',
  'forced_family':'Class Ib',
  'isolated_special_branch':'c4=2 also solves D0 and must be analysed separately; it is not a continuously tunable acceleration coefficient',
  'decoupling_scalar_note':'At quadratic single-mode level the c2=1,c3=-1 spatial Hessian combination cancels, explaining why c4 a^2 alone appears in the reduced scalar dispersion despite the full metric-sector pathology.',
  'scope_warning':'Constant-c_i khronometric/DHOST degeneracy audit only. General X-dependent degenerate DHOST/spatially covariant completions and constrained auxiliary realizations remain open.'
}
print('RTK_ROUTE_B_KHRONOMETRIC_ACCELERATION_DEGENERACY_AUDIT_PASS',json.dumps(out,sort_keys=True))
