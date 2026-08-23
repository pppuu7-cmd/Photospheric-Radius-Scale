#!/usr/bin/env python3
"""Exact exterior finite-Mc Yukawa response for any nonnegative spherical source.

Given the certified static Helmholtz kernel and a spherical density rho(r') with
support 0<=r'<=R, the exterior field r>=R factorizes into the point-source
Yukawa field times one source moment.

With Msrc=4pi int r'^2 rho dr',
 F_rho(m)= [int r'^2 rho(r') sinh(m r')/(m r') dr'] /
           [int r'^2 rho(r') dr'].
Thus U=G Msrc F_rho(m) exp(-m r)/r.
For rho>=0, sinh(x)/x is increasing on x>=0, so
  1 <= F_rho(m) <= sinh(mR)/(mR).
Small-m expansion is controlled by ordinary mass moments:
 F_rho=1+m^2<r^2>/6+m^4<r^4>/120+O(m^6).
"""
import json
import sympy as sp
x=sp.symbols('x', nonnegative=True, finite=True)
# monotonicity of sinh(x)/x for x>0 via numerator x cosh x-sinh x.
f=sp.sinh(x)/x
# Avoid x=0 symbolic division; derivative numerator has positive derivative x sinh x.
num=x*sp.cosh(x)-sp.sinh(x)
assert sp.simplify(sp.diff(num,x)-x*sp.sinh(x))==0
assert sp.limit(num,x,0,dir='+')==0
# series weight.
series=sp.series(f,x,0,8)
assert series==1+x**2/sp.Integer(6)+x**4/sp.Integer(120)+x**6/sp.Integer(5040)+sp.Order(x**8)

# Uniform sphere check using normalized mass moments <r^(2n)>=3 R^(2n)/(2n+3).
m,R=sp.symbols('M_c R', positive=True, finite=True)
Fu=3*(m*R*sp.cosh(m*R)-sp.sinh(m*R))/(m*R)**3
# Direct normalized radial moment integral.
r=sp.symbols('r', positive=True, finite=True)
I=sp.integrate(r**2*sp.sinh(m*r)/(m*r),(r,0,R))
I0=R**3/sp.Integer(3)
assert sp.simplify(I/I0-Fu)==0
# Generic moment expansion placeholder algebra.
r2,r4=sp.symbols('mean_r2 mean_r4', nonnegative=True, finite=True)
Fsmall=1+m**2*r2/6+m**4*r4/120

out={
 'classification':'RTK_C9_PROJECTABLE_U1_FINITE_MC_ARBITRARY_SPHERICAL_YUKAWA_PASS',
 'status_scope':'GREEN_EXACT_LINEAR_STATIC_SPHERICAL_PROFILE_THEOREM_HIGHER_PN_AND_NONSpherical_PENDING',
 'domain':'linear static O2 projectable finite-Mc Helmholtz kernel; spherical rho(r)>=0 supported on [0,R]; exterior r>=R',
 'mass':'M_source=4 pi int_0^R dr r^2 rho(r)',
 'profile_form_factor':'F_rho(M_c) = [int_0^R dr r^2 rho(r) sinh(M_c r)/(M_c r)]/[int_0^R dr r^2 rho(r)]',
 'exterior_potential':'U(r)=G M_source F_rho(M_c) exp(-M_c r)/r',
 'exterior_force_ratio_to_point_Newton':'F_Y/F_N=F_rho(M_c)(1+M_c r)exp(-M_c r)',
 'profile_independent_bound':'1 <= F_rho(M_c) <= sinh(M_c R)/(M_c R)',
 'small_Mc':'F_rho=1+M_c^2 <r^2>_M/6+M_c^4 <r^4>_M/120+O(M_c^6 <r^6>_M)',
 'mass_moment_definition':'<r^n>_M=[int r^(n+2)rho(r)dr]/[int r^2 rho(r)dr]',
 'uniform_sphere_check':'<r^2>_M=3R^2/5 gives F=1+(M_cR)^2/10+... and reproduces 3[x cosh x-sinh x]/x^3 exactly',
 'interpretation':'Every weak-field spherical source can be handled by a single positive profile moment. The source-independent upper bound gives a conservative finite-size envelope before a density model is chosen.',
 'non_claims':['no nonlinear self-gravity or screening','no nonspherical multipoles','no O3 preferred-frame motion','no O4 convolution terms','does not choose an experimental source or M_c'],
 'next_gate':'combine the exact profile form factor with an explicit measurement geometry to derive an observable-weighted M_c bound; separately extend the convolution O4 kernel from uniform density to arbitrary spherical rho using the same radial transform.'
}
open('c9_projectable_u1_finite_mc_arbitrary_spherical_yukawa_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
