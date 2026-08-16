#!/usr/bin/env python3
"""Symbolically verify the large-lambda RTK dust-boundary expansion.

This is a model-internal analytic check of the equations implemented in
khronon_background.c and the coefficients entering khronon_perturbations.c.
It does not use observational data.
"""
import sympy as sp

eps,A,a,k,mu=sp.symbols('eps A a k mu', positive=True)
lam=eps**-2
D=1+2*A+lam*A**2
x0=A*(2+lam*A)/(1+lam*A+sp.sqrt(D))
x=x0/a**3
s=sp.sqrt(1+(x/eps)**2)
r=x/s
t=x/(s+1)
rho=x*(1+t)          # rho_K/(2 mu_K^2)
p=r*t                 # p_K/(2 mu_K^2)
w=sp.simplify(p/rho)
ca2=sp.simplify(r/(s*(s+x)))
Q=1+r
# k_star = a * mu_K * Q * s^(3/2)
kstar2=sp.simplify(a**2*mu**2*Q**2*s**3)
inv_kstar2=sp.simplify(1/kstar2)
cs2=sp.simplify(ca2/(1+k**2*inv_kstar2))

def coeffs(expr,n=4):
    ser=sp.series(expr,eps,0,n+1).removeO().expand()
    return [sp.factor(sp.simplify(ser.coeff(eps,i))) for i in range(n+1)]

print('x0 coefficients eps^0..3:', coeffs(x0,3))
print('rho/(2mu^2) coefficients eps^0..3:', coeffs(rho,3))
print('w coefficients eps^0..3:', coeffs(w,3))
print('ca2 coefficients eps^0..4:', coeffs(ca2,4))
print('1/kstar^2 coefficients eps^0..4:', coeffs(inv_kstar2,4))
print('cs2 coefficients eps^0..6:', coeffs(cs2,6))
print('r coefficients eps^0..3:', coeffs(r,3))
print('Q coefficients eps^0..3:', coeffs(Q,3))

# Exact leading coefficients expected from the implemented background equations.
assert sp.simplify(coeffs(x0,3)[0]-A)==0
assert sp.simplify(coeffs(x0,3)[1]+A)==0
assert sp.simplify(coeffs(x0,3)[2]-(A+1))==0
assert sp.simplify(coeffs(rho,3)[0]-A/a**3)==0
assert sp.simplify(coeffs(rho,3)[1])==0
assert sp.simplify(coeffs(rho,3)[2]-(a**-3-1))==0
assert sp.simplify(coeffs(w,3)[1])==0
assert sp.simplify(coeffs(w,3)[2]-a**3/A)==0
assert sp.simplify(coeffs(ca2,4)[1])==0
assert sp.simplify(coeffs(ca2,4)[2])==0
assert sp.simplify(coeffs(ca2,4)[3]-a**6/A**2)==0

# Scale-dependent sound speed: for fixed finite k, k_star grows as eps^(-3/2),
# so k^2/k_star^2=O(eps^3). Hence cs2 and ca2 agree through O(eps^5),
# and both start only at eps^3=lambda^(-3/2).
assert all(sp.simplify(coeffs(inv_kstar2,4)[i])==0 for i in range(3))
assert sp.simplify(coeffs(inv_kstar2,4)[3]-a**7/(A**3*mu**2))==0
assert all(sp.simplify(coeffs(cs2,6)[i])==0 for i in range(3))
assert sp.simplify(coeffs(cs2,6)[3]-a**6/A**2)==0
assert sp.simplify(coeffs(cs2,6)[3]-coeffs(ca2,6)[3])==0
assert sp.simplify(coeffs(cs2,6)[4]-coeffs(ca2,6)[4])==0
assert sp.simplify(coeffs(cs2,6)[5]-coeffs(ca2,6)[5])==0

print('ASYMPTOTIC_DUST_COORDINATE_PASS')
print('Background leading physical deviation: O(eps^2) = O(1/lambda_D)')
print('Linear perturbation coefficients: w=O(eps^2), ca2=cs2=O(eps^3), k^2/kstar^2=O(eps^3)')
print('Therefore the leading fixed-k physical perturbation departure is also u = 1/lambda_D')
