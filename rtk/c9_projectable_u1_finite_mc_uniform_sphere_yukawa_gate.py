#!/usr/bin/env python3
"""Exact exterior Yukawa form factor for a uniform spherical source.

Input: the already derived projectable static O2 Helmholtz kernel
  U(x)=-G int d^3x' rho(x') exp(-M|x-x'|)/|x-x'|.
For a uniform sphere of radius R and total mass Msrc, derive the exterior
(r>=R) solution and force transfer relative to point-source Newton gravity.

No screening/nonlinearities are assumed.  This is a linear extended-source
correction only.
"""
import json
import sympy as sp

m,R,r,rp=sp.symbols('M_c R r r_prime', positive=True, finite=True)
x=sp.symbols('x', positive=True, finite=True)
# For r>rp, angular integral:
# int dOmega' exp(-m|r-r'|)/|r-r'| = 4 pi e^{-mr} sinh(m r')/(m r r').
# Radial source integral for constant rho.
I=sp.integrate(rp*sp.sinh(m*rp),(rp,0,R))
Iref=R*sp.cosh(m*R)/m-sp.sinh(m*R)/m**2
assert sp.simplify(I-Iref)==0

# Divide by Msrc=(4pi/3)rho R^3 to obtain dimensionless exterior form factor.
F=sp.factor(3*(m*R*sp.cosh(m*R)-sp.sinh(m*R))/(m*R)**3)
Fx=3*(x*sp.cosh(x)-sp.sinh(x))/x**3
assert sp.simplify(F-Fx.subs(x,m*R))==0
# Point-source/small-source limit.
seriesF=sp.series(Fx,x,0,8)
assert seriesF==1+x**2/sp.Integer(10)+x**4/sp.Integer(280)+x**6/sp.Integer(15120)+sp.Order(x**8)

# Exterior potential and radial force transfer relative to Newton GM/r^2.
y=sp.symbols('y', positive=True, finite=True) # y=m r
force_transfer=sp.factor(Fx*(1+y)*sp.exp(-y))
# At fixed source-size x, derivative w.r.t. exterior y is monotone negative.
dy=sp.factor(sp.diff((1+y)*sp.exp(-y),y))
assert dy==-y*sp.exp(-y)

# Form factor is >=1 for x>0 and grows ~ exp(x); exterior field remains finite
# because y>=x for r>=R, so the total product includes exp(-y).
# Surface transfer y=x has a regular small-x expansion.
surface=sp.factor(Fx*(1+x)*sp.exp(-x))
surface_series=sp.series(surface,x,0,5)
# Keep executable equality to the actual series returned by SymPy.
expected_surface=1-sp.Rational(2,5)*x**2+sp.Rational(1,3)*x**3-sp.Rational(6,35)*x**4+sp.Order(x**5)
assert sp.simplify((surface_series-expected_surface).removeO())==0

out={
  'classification':'RTK_C9_PROJECTABLE_U1_FINITE_MC_UNIFORM_SPHERE_YUKAWA_PASS',
  'status_scope':'GREEN_STATIC_O2_UNIFORM_SPHERE_EXTERIOR_KERNEL_GENERAL_PROFILE_AND_HIGHER_PN_PENDING',
  'domain':'linear static O2 projectable finite-Mc Helmholtz kernel, uniform sphere radius R, exterior r>=R',
  'angular_integral':'int dOmega exp[-M_c|r-r_prime|]/|r-r_prime| = 4 pi exp(-M_c r) sinh(M_c r_prime)/(M_c r r_prime) for r>r_prime',
  'form_factor':'F(x)=3[x cosh(x)-sinh(x)]/x^3, x=M_c R',
  'small_source':'F(x)=1+x^2/10+x^4/280+x^6/15120+O(x^8)',
  'exterior_potential':'U(r)=G M_source F(M_c R) exp(-M_c r)/r',
  'exterior_force_ratio':'F_Y/F_Newton = F(M_c R) (1+M_c r) exp(-M_c r)',
  'surface_small_x':'at r=R: F_Y/F_Newton = 1-(2/5)x^2+(1/3)x^3-(6/35)x^4+O(x^5)',
  'interpretation':'Finite source size partially compensates point-source Yukawa suppression through F(M_c R)>1. Therefore a local M_c constraint must use the source profile and measurement radius rather than only the point-source baseline.',
  'non_claims':[
    'does not include nonlinear self-gravity or screening',
    'does not include density-profile uncertainty or nonspherical bodies',
    'does not include finite-Mc O3/O4 PPN corrections',
    'does not select an experimental source or tolerance'
  ],
  'next_gate':'generalize the exterior amplitude to an arbitrary spherical density profile as a one-dimensional sinh-weighted moment and build source-specific form factors only after declaring a concrete local observable.'
}
open('c9_projectable_u1_finite_mc_uniform_sphere_yukawa_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
