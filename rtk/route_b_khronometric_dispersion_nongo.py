#!/usr/bin/env python3
"""Symbolic Route-B non-mapping theorem for the RTK/Khronon linear dispersion.

Scope: quadratic scalar sector only.  The standard low-energy khronometric /
hypersurface-orthogonal Einstein-aether action has a momentum-independent
quadratic kinetic coefficient.  The usual healthy-Horava UV completion adds
higher *spatial-potential* derivatives, producing polynomial q^4,q^6,... terms
in the numerator of omega^2 while retaining two time derivatives.

The implemented RTK/Khronon target instead is

    omega^2 = c_a^2 q^2 / (1 + q^2/M^2),

which requires a q^2-dependent kinetic coefficient, e.g. a mixed-derivative
operator (grad dot(pi))^2, or an equivalent auxiliary-field reduction.  This
script proves that no nonzero finite polynomial potential with constant kinetic
coefficient can equal the RTK rational target for all q.

This excludes a *minimal/potential-only mapping*, not all possible
khronometric/Horava-inspired nonlinear completions.
"""
import sympy as sp

x=sp.symbols('x', nonnegative=True)  # x=q^2/M^2
c,A0,A2=sp.symbols('c A0 A2', nonzero=True)
b1,b2,b3=sp.symbols('b1 b2 b3')

# Generic standard potential-only scalar quadratic dispersion through z=3:
#   K=A0,  V/M^2 = b1*x+b2*x^2+b3*x^3
# Overall dimensions are irrelevant for the rational-function identity test.
P=b1*x+b2*x**2+b3*x**3
rtk=c*x/(1+x)
poly_identity=sp.Poly(sp.expand(P*(1+x)-A0*c*x),x)
sol=sp.solve(poly_identity.all_coeffs(),[b1,b2,b3],dict=True)
# With A0*c nonzero there must be no solution.  To make the contradiction
# transparent, also solve allowing c to vary: the only exact polynomial match
# forces c=0 and all spatial coefficients zero.
sol_with_c=sp.solve(poly_identity.all_coeffs(),[b1,b2,b3,c],dict=True)
assert sol==[]
assert sol_with_c==[{b1:0,b2:0,b3:0,c:0}]

# Conversely a mixed-derivative kinetic polynomial K=A0*(1+x), with only a
# q^2 gradient potential, reproduces the target exactly.
omega_mixed=(A0*c*x)/(A0*(1+x))
assert sp.simplify(omega_mixed-rtk)==0

# More generally, take K=A0+A2*x and V=b1*x. Matching c*x/(1+x)
# fixes A2=A0 and b1=A0*c up to the dimensionless normalization used here.
expr=sp.Poly(sp.expand(b1*x*(1+x)-c*x*(A0+A2*x)),x)
sol_mixed=sp.solve(expr.all_coeffs(),[A2,b1],dict=True)
assert sol_mixed==[{A2:A0,b1:A0*c}]

out={
  'classification':'RTK_ROUTE_B_STANDARD_KHRONOMETRIC_POTENTIAL_ONLY_NONMAPPING_PASS',
  'target':'omega^2 = c_a^2 q^2/(1+q^2/M^2)',
  'potential_only_ansatz':'K=A0 constant; V proportional to b1*x+b2*x^2+b3*x^3',
  'potential_only_exact_nonzero_solution':False,
  'solution_if_target_speed_allowed_zero':{'b1':0,'b2':0,'b3':0,'c':0},
  'minimal_mixed_kinetic_match':{'K':'A0*(1+x)','V':'A0*c*x'},
  'generic_mixed_match_conditions':{'A2':'A0','b1':'A0*c'},
  'scope_warning':'Quadratic dispersion non-mapping only. Does not exclude khronometric/Horava-inspired completions with mixed derivative kinetic terms, auxiliary fields, or other nonlinear structures, and is not a full DOF/ghost theorem.'
}
import json
print('RTK_ROUTE_B_KHRONOMETRIC_DISPERSION_NONGO_PASS',json.dumps(out,sort_keys=True))
