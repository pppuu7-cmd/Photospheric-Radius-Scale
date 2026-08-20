#!/usr/bin/env python3
"""Generalized alpha=0 no-go inside the full BPS scalar quadratic P/Q class.

Primary source: Blas, Pujolas, Sibiryakov, arXiv:1007.3503, Eqs. (5.1)-(5.8).

For the healthy nonprojectable Horava scalar after integrating nondynamical
fields,

  omega^2 = kappa * P(-p^2/M_*^2)/Q(-p^2/M_*^2) * p^2,

with finite nonzero kappa=(lambda-1)/[2(3lambda-1)] and
  Q(x)=g3*x^2+f3*x+alpha,
  P(0)=4-2 alpha.

This gate asks whether alpha=0 can reproduce an exact regular RTK target

  omega^2 = C p^2/(1+rho p^2),  C>0, rho>0,

without restricting f_i or g_i.  The result is a no-go for this quadratic
single-scalar P/Q class only.  It is not a no-go for RTK phenomenology, for a
singular joint limit in which kappa also vanishes, or for a broader nonlinear/
FLRW/higher-field completion.
"""
import json
import sympy as sp

x,u,rho,R = sp.symbols('x u rho R', positive=True, finite=True, real=True)
f1,f2,f3,g1,g2,g3 = sp.symbols('f1 f2 f3 g1 g2 g3', finite=True, real=True)
alpha = sp.Integer(0)

P = sp.expand((g2**2-g1*g3)*x**4
              -(g1*f3+g3*f1-2*g2*f2)*x**3
              +(f2**2-4*g2-f1*f3-2*g3-g1*alpha)*x**2
              -(2*f3+f1*alpha+4*f2)*x
              +(4-2*alpha))
Q = sp.expand(g3*x**2+f3*x+alpha)

Pphys = sp.expand(P.subs(x,-u))
Qphys = sp.expand(Q.subs(x,-u))
assert sp.simplify(Pphys.subs(u,0)-4) == 0
assert sp.simplify(Qphys.subs(u,0)) == 0

# Exact target matching of P/Q to R/(1+rho*u) requires
#   (1+rho*u) P(-u) - R Q(-u) == 0
# as a polynomial identity.  At alpha=0 its constant coefficient is 4,
# independently of every f_i, g_i, R and rho, so the identity is impossible.
identity = sp.expand((1+rho*u)*Pphys - R*Qphys)
constant = sp.Poly(identity,u).coeff_monomial(1)
assert constant == 4
assert sp.simplify(identity.subs(u,0)-4) == 0

# The common special cases also expose the IR pathology directly.
# If f3 != 0, Q(-u)~(-f3)u and P/Q~1/u, so omega^2 tends to a constant.
# If f3=0 and g3 !=0, Q(-u)~g3*u^2 and omega^2 behaves as 1/u.

out={
  'classification':'RTK_ROUTE_B_BPS_ALPHA0_GENERALIZED_NOGO_PASS',
  'scope':'full BPS scalar quadratic P/Q polynomial class at exact alpha=0 with finite nonzero scalar prefactor',
  'target':'omega^2=C p^2/(1+rho p^2), C>0, rho>0',
  'source_structure':{
    'P0_at_alpha0':'4',
    'Q0_at_alpha0':'0',
    'matching_identity':'(1+rho*u) P(-u) - R Q(-u) == 0',
    'constant_coefficient':'4'
  },
  'theorem':'At exact alpha=0, no choice of finite f1,f2,f3,g1,g2,g3 can make the regular BPS quadratic scalar P/Q ratio exactly proportional to 1/(1+rho p^2), because the required polynomial identity already fails at p=0.',
  'interpretation':'This strengthens the previous selected-family boundary to the whole standard BPS single-scalar quadratic P/Q class under its regular finite-prefactor assumptions.',
  'non_claims':[
    'not a no-go for RTK cosmological phenomenology',
    'not a no-go for a broader theory with additional constrained fields or a different observable/source map',
    'not a theorem about the full nonlinear higher-spatial-derivative black-hole solution',
    'does not cover a singular joint limit alpha->0 and lambda->1 in which the scalar prefactor/rank changes',
    'does not prove that UV operators cannot regularize the universal-horizon region'
  ],
  'next_step':'Audit the singular joint alpha->0, lambda->1 limit with canonical normalization and cutoff, and separately derive the full fixed-action FLRW scalar constraint/propagator map.'
}
print('RTK_ROUTE_B_BPS_ALPHA0_GENERALIZED_NOGO_PASS',json.dumps(out,sort_keys=True))
