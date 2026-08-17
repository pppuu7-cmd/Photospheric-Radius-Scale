#!/usr/bin/env python3
"""Constructive no-go for inferring Route-A1 c3,c4 from background/linear data.

Within the frozen A1 basis, O3 and O4 start at cubic order and contain spatial
Laplacians. Therefore homogeneous background thermodynamics and the complete
quadratic action cannot identify their coefficients. This is an identifiability
theorem, not a statement that c3,c4 are physically arbitrary in a future
fundamental nonlinear completion.
"""
import json
import sympy as sp

# Bookkeeping amplitude: pi = eps * psi.  Treat local derivative structures of
# psi as independent symbols because only perturbative amplitude order matters.
eps=sp.symbols('eps', real=True)
K,G,M,c1,c2,c3,c4=sp.symbols('K G M c1 c2 c3 c4', finite=True)
v,gd2,gvd2,lap=sp.symbols('v gd2 gvd2 lap', real=True)

# v=dot psi, gd2=(grad psi)^2, gvd2=(grad dot psi)^2, lap=Delta psi.
L2=sp.Rational(1,2)*K*(eps*v)**2 + sp.Rational(1,2)*K/M**2*(eps**2*gvd2) - sp.Rational(1,2)*G*(eps**2*gd2)
O1=eps**3*v**3
O2=eps**3*v*gd2
O3=eps**3*v**2*lap
O4=eps**3*gd2*lap
L=L2+c1*O1+c2*O2+c3*O3+c4*O4

# Background and quadratic response are independent of all cubic coefficients.
background=sp.simplify(L.subs(eps,0))
linear=sp.simplify(sp.diff(L,eps).subs(eps,0))
quadratic=sp.simplify(sp.diff(L,eps,2).subs(eps,0)/2)
assert background == 0
assert linear == 0
assert sp.diff(quadratic,c3) == 0
assert sp.diff(quadratic,c4) == 0
assert sp.diff(quadratic,c1) == 0
assert sp.diff(quadratic,c2) == 0

# The third variation distinguishes the coefficients.
cubic=sp.simplify(sp.diff(L,eps,3).subs(eps,0)/6)
assert sp.diff(cubic,c3) == v**2*lap
assert sp.diff(cubic,c4) == gd2*lap

# Homogeneous backgrounds have no spatial gradient/laplacian, so D4 vertices
# vanish even away from the perturbative bookkeeping point.
homogeneous_D4=sp.simplify((c3*v**2*lap+c4*gd2*lap).subs({lap:0,gd2:0}))
assert homogeneous_D4 == 0

# Constructive degeneracy: shift c3,c4 by arbitrary alpha,beta.  The two
# theories have identical <=quadratic expansion but different cubic action.
alpha,beta=sp.symbols('alpha beta', nonzero=True, finite=True)
L_alt=sp.expand(L+alpha*O3+beta*O4)
for n in (0,1,2):
    assert sp.simplify(sp.diff(L_alt-L,eps,n).subs(eps,0)) == 0
cubic_delta=sp.simplify(sp.diff(L_alt-L,eps,3).subs(eps,0)/6)
assert sp.simplify(cubic_delta-(alpha*v**2*lap+beta*gd2*lap)) == 0

result={
 'classification':'RTK_ROUTE_A1_D4_LINEAR_IDENTIFIABILITY_NOGO_PASS',
 'background_fixes_c3_c4':False,
 'quadratic_linear_target_fixes_c3_c4':False,
 'reason':'O3 and O4 vanish on homogeneous background and first enter at cubic amplitude order',
 'constructive_degeneracy':'c3->c3+alpha and c4->c4+beta leaves the full expansion through O(pi^2) unchanged',
 'additional_nonlinear_postulate_required':True,
 'full_nonlinear_completion_closed':False,
}
print('RTK_ROUTE_A1_D4_IDENTIFIABILITY_PASS',json.dumps(result,sort_keys=True))
