#!/usr/bin/env python3
"""Symbolically verify the large-lambda RTK dust-boundary expansion.

This is a model-internal analytic check of the equations implemented in
khronon_background.c.  It does not use observational data.
"""
import sympy as sp

eps,A,a=sp.symbols('eps A a', positive=True)
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

def coeffs(expr,n=4):
    ser=sp.series(expr,eps,0,n+1).removeO().expand()
    return [sp.factor(sp.simplify(ser.coeff(eps,i))) for i in range(n+1)]

print('x0 coefficients eps^0..3:', coeffs(x0,3))
print('rho/(2mu^2) coefficients eps^0..3:', coeffs(rho,3))
print('w coefficients eps^0..3:', coeffs(w,3))
print('ca2 coefficients eps^0..3:', coeffs(ca2,3))
print('r coefficients eps^0..3:', coeffs(r,3))
print('Q coefficients eps^0..3:', coeffs(Q,3))

# Exact leading coefficients expected from the implemented equations.
assert sp.simplify(coeffs(x0,3)[0]-A)==0
assert sp.simplify(coeffs(x0,3)[1]+A)==0
assert sp.simplify(coeffs(x0,3)[2]-(A+1))==0
assert sp.simplify(coeffs(rho,3)[0]-A/a**3)==0
assert sp.simplify(coeffs(rho,3)[1])==0
assert sp.simplify(coeffs(rho,3)[2]-(a**-3-1))==0
assert sp.simplify(coeffs(w,3)[1])==0
assert sp.simplify(coeffs(w,3)[2]-a**3/A)==0
assert sp.simplify(coeffs(ca2,3)[1])==0
assert sp.simplify(coeffs(ca2,3)[2])==0
assert sp.simplify(coeffs(ca2,3)[3]-a**6/A**2)==0

print('ASYMPTOTIC_DUST_COORDINATE_PASS')
print('Leading physical deviation coordinate: u = eps^2 = 1/lambda_D')
