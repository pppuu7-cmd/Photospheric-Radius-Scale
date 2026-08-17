#!/usr/bin/env python3
"""No-go: the quadratic dispersive scale M does not fix nonlinear D5 coupling.

The A1 quadratic term (K/2M^2)(grad dot pi)^2 is derivative order D=4.
A shift-symmetric preferred-frame nonlinear completion can multiply this by a
function of dot pi (or another allowed background scalar), whose first
perturbative correction is dot pi (grad dot pi)^2 at cubic D=5.  The D5
coefficient is invisible to the complete quadratic target.
"""
import json
import sympy as sp

eps=sp.symbols('eps', real=True)
K,M,alpha,beta=sp.symbols('K M alpha beta', finite=True, nonzero=True)
v,gvd2=sp.symbols('v gvd2', real=True)
A=K/M**2

# pi=eps*psi. gvd2 denotes |grad dot psi|^2, hence the quadratic structure is
# eps^2*gvd2. Two nonlinear completions differing by alpha have identical L2.
Ldisp0=sp.Rational(1,2)*A*eps**2*gvd2
Ldisp_alpha=sp.Rational(1,2)*A*(1+alpha*eps*v)*eps**2*gvd2
Ldisp_beta=sp.Rational(1,2)*A*(1+beta*eps*v)*eps**2*gvd2

for L in (Ldisp_alpha,Ldisp_beta):
    assert sp.simplify(sp.diff(L,eps,2).subs(eps,0)/2 - sp.Rational(1,2)*A*gvd2) == 0

cubic_a=sp.simplify(sp.diff(Ldisp_alpha,eps,3).subs(eps,0)/6)
cubic_b=sp.simplify(sp.diff(Ldisp_beta,eps,3).subs(eps,0)/6)
assert sp.simplify(cubic_a-sp.Rational(1,2)*A*alpha*v*gvd2) == 0
assert sp.simplify(cubic_b-sp.Rational(1,2)*A*beta*v*gvd2) == 0
assert sp.simplify(cubic_a-cubic_b-sp.Rational(1,2)*A*(alpha-beta)*v*gvd2) == 0

# Derivative counting: dot(pi) carries 1 derivative; each grad dot(pi) carries
# 2. Therefore the cubic operator has total D=1+2+2=5 and is outside the
# already-closed D<=4 cubic basis, while still containing no second time
# derivative on an individual field.
derivative_order=1+2+2
assert derivative_order == 5

result={
 'classification':'RTK_ROUTE_A1_D5_DISPERSIVE_IDENTIFIABILITY_NOGO_PASS',
 'quadratic_operator':'(K/2M^2)*(grad dot(pi))^2',
 'quadratic_derivative_order':4,
 'first_example_nonlinear_operator':'dot(pi)*(grad dot(pi))^2',
 'example_cubic_derivative_order':5,
 'same_K_M_allows_different_D5_coefficients':True,
 'linear_M_determines_physical_cutoff':False,
 'D_le_4_cubic_basis_sufficient_near_q_sim_M':False,
 'required_next_layer':'enumerate/choose D5 dispersive nonlinear completion before physical strong-coupling claim',
}
print('RTK_ROUTE_A1_D5_DISPERSIVE_NOGO_PASS',json.dumps(result,sort_keys=True))
